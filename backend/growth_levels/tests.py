from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import MiNetGrowthLevel


class MiNetGrowthLevelAPITests(APITestCase):

    def setUp(self):
        # Create initial test records
        self.level_1 = MiNetGrowthLevel.objects.create(
            level="Level A",
            lower_range=Decimal('0.00'),
            upper_range=Decimal('10000.00'),
            percentage=Decimal('5.00'),
            status='Active',
            created_user='SETUP_ADMIN',
            comments='Base tier'
        )
        self.level_2 = MiNetGrowthLevel.objects.create(
            level="Level B",
            lower_range=Decimal('10000.01'),
            upper_range=Decimal('50000.00'),
            percentage=Decimal('10.00'),
            status='Active',
            created_user='SETUP_ADMIN'
        )
        self.list_url = reverse('mi-net-growth-levels-list')

    def test_list_records(self):
        """GET /api/mi-net-growth-levels/ should list all records."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 2)
        results = response.data['results']
        self.assertEqual(results[0]['net_id'], self.level_1.net_id)

    def test_retrieve_single_record(self):
        """GET /api/mi-net-growth-levels/<id>/ should retrieve single record."""
        detail_url = reverse('mi-net-growth-levels-detail', kwargs={'pk': self.level_1.pk})
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['level'], "Level A")
        self.assertEqual(response.data['net_id'], self.level_1.net_id)

    def test_create_record_and_auto_net_id(self):
        """POST /api/mi-net-growth-levels/ should auto-generate NET_ID."""
        payload = {
            'level': 'Level C',
            'lower_range': '50000.01',
            'upper_range': '100000.00',
            'percentage': '15.00',
            'status': 'Active',
            'comments': 'Third tier'
        }
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['net_id'].startswith('NET'))
        self.assertEqual(response.data['net_id'], 'NET003')

    def test_create_with_file_upload(self):
        """POST /api/mi-net-growth-levels/ with multipart/form-data attachment."""
        file = SimpleUploadedFile("spec.pdf", b"Dummy PDF content", content_type="application/pdf")
        payload = {
            'level': 'Level D',
            'lower_range': '100000.01',
            'upper_range': '200000.00',
            'percentage': '20.00',
            'status': 'Active',
            'attachment': file
        }
        response = self.client.post(self.list_url, payload, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(response.data['attachment'])
        self.assertEqual(response.data['attachment_name'], 'spec.pdf')

    def test_update_record(self):
        """PUT /api/mi-net-growth-levels/<id>/ updates the record."""
        detail_url = reverse('mi-net-growth-levels-detail', kwargs={'pk': self.level_1.pk})
        payload = {
            'level': 'Level A Updated',
            'lower_range': '0.00',
            'upper_range': '10000.00',
            'percentage': '6.50',
            'status': 'Active'
        }
        response = self.client.put(detail_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['level'], 'Level A Updated')
        self.assertEqual(response.data['percentage'], '6.50')

    def test_delete_record(self):
        """DELETE /api/mi-net-growth-levels/<id>/ removes record."""
        detail_url = reverse('mi-net-growth-levels-detail', kwargs={'pk': self.level_2.pk})
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(MiNetGrowthLevel.objects.filter(pk=self.level_2.pk).exists())

    def test_validation_range_overlap(self):
        """Ensure overlapping LOWER_RANGE and UPPER_RANGE is rejected with 400 Bad Request."""
        payload = {
            'level': 'Overlapping Level',
            'lower_range': '5000.00',
            'upper_range': '15000.00', # Overlaps Level A (0-10000) and Level B (10000.01-50000)
            'percentage': '8.00',
            'status': 'Active'
        }
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)
        self.assertTrue(any('overlaps' in err.lower() for err in response.data['non_field_errors']))

    def test_validation_percentage_limits(self):
        """Ensure percentage > 100 or < 0 is rejected."""
        payload = {
            'level': 'Invalid Percentage',
            'lower_range': '60000.00',
            'upper_range': '70000.00',
            'percentage': '105.00', # Exceeds 100%
            'status': 'Active'
        }
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('percentage', response.data)

    def test_validation_upper_must_be_greater_than_lower(self):
        """Ensure upper_range <= lower_range is rejected."""
        payload = {
            'level': 'Inverted Ranges',
            'lower_range': '80000.00',
            'upper_range': '70000.00',
            'percentage': '5.00',
            'status': 'Active'
        }
        response = self.client.post(self.list_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('upper_range', response.data)

    def test_search_and_filter(self):
        """Test ?search= and ?status= query params."""
        # Search by level
        response = self.client.get(f"{self.list_url}?search=Level A")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

        # Filter by status
        response = self.client.get(f"{self.list_url}?status=Inactive")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_role_based_access_control(self):
        """Test RM (Read-Only) and DGM (No Delete) restrictions."""
        # RM trying to create should get 403 Forbidden
        response = self.client.post(
            self.list_url,
            {'level': 'RM Blocked', 'lower_range': '200000', 'upper_range': '300000', 'percentage': '5'},
            format='json',
            HTTP_X_USER_ROLE='RM'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # DGM trying to delete should get 403 Forbidden
        detail_url = reverse('mi-net-growth-levels-detail', kwargs={'pk': self.level_1.pk})
        response = self.client.delete(detail_url, HTTP_X_USER_ROLE='DGM')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
