import os
import django
from decimal import Decimal
from django.core.files.base import ContentFile

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'growth_backend.settings')
django.setup()

from growth_levels.models import MiNetGrowthLevel

def seed():
    print("Clearing existing data...")
    MiNetGrowthLevel.objects.all().delete()

    sample_levels = [
        {
            'level': 'Tier 1 - Bronze Foundation',
            'lower_range': Decimal('0.00'),
            'upper_range': Decimal('50000.00'),
            'percentage': Decimal('2.50'),
            'status': 'Active',
            'created_user': 'CFO_ADMIN',
            'comments': 'Initial base incentive bracket for entry-level sales targets.',
            'sample_file_name': 'bronze_policy_guideline.txt',
            'sample_file_content': 'Policy guidelines for Tier 1 Bronze Growth Level (Range: $0 - $50,000).'
        },
        {
            'level': 'Tier 2 - Silver Standard',
            'lower_range': Decimal('50000.01'),
            'upper_range': Decimal('150000.00'),
            'percentage': Decimal('5.00'),
            'status': 'Active',
            'created_user': 'CFO_ADMIN',
            'comments': 'Standard tier for consistent quarterly performers.',
            'sample_file_name': 'silver_benefits_matrix.txt',
            'sample_file_content': 'Incentive breakdown and payout terms for Tier 2 Silver Standard.'
        },
        {
            'level': 'Tier 3 - Gold Accelerator',
            'lower_range': Decimal('150000.01'),
            'upper_range': Decimal('350000.00'),
            'percentage': Decimal('8.75'),
            'status': 'Active',
            'created_user': 'DGM_FINANCE',
            'comments': 'Accelerated tier for enterprise accounts expansion.',
            'sample_file_name': 'gold_accelerator_spec.txt',
            'sample_file_content': 'Gold Accelerator Tier documentation approved by Executive Board.'
        },
        {
            'level': 'Tier 4 - Platinum Vanguard',
            'lower_range': Decimal('350000.01'),
            'upper_range': Decimal('750000.00'),
            'percentage': Decimal('12.50'),
            'status': 'Active',
            'created_user': 'CFO_ADMIN',
            'comments': 'Premium tier for high-volume deal closers and key account drivers.',
            'sample_file_name': 'platinum_vanguard_approval.txt',
            'sample_file_content': 'Platinum Tier compliance and risk evaluation documentation.'
        },
        {
            'level': 'Tier 5 - Diamond Elite',
            'lower_range': Decimal('750000.01'),
            'upper_range': Decimal('1500000.00'),
            'percentage': Decimal('18.00'),
            'status': 'Active',
            'created_user': 'CFO_ADMIN',
            'comments': 'Top-level enterprise incentive bracket with executive review.',
            'sample_file_name': 'diamond_elite_charter.txt',
            'sample_file_content': 'Diamond Elite VIP growth level charter and compensation agreement.'
        },
        {
            'level': 'Legacy Promotional Tier',
            'lower_range': Decimal('10000.00'),
            'upper_range': Decimal('40000.00'),
            'percentage': Decimal('3.00'),
            'status': 'Inactive',
            'created_user': 'RM_OFFICER',
            'comments': 'Archived promotional incentive tier from previous fiscal year.',
            'sample_file_name': None,
            'sample_file_content': None
        }
    ]

    for item in sample_levels:
        record = MiNetGrowthLevel(
            level=item['level'],
            lower_range=item['lower_range'],
            upper_range=item['upper_range'],
            percentage=item['percentage'],
            status=item['status'],
            created_user=item['created_user'],
            comments=item['comments'],
        )
        if item.get('sample_file_name'):
            record.attachment.save(
                item['sample_file_name'],
                ContentFile(item['sample_file_content'].encode('utf-8')),
                save=False
            )
        record.save()
        print(f"Created: {record.net_id} - {record.level} [{record.lower_range} - {record.upper_range}] ({record.status})")

    print("\nDatabase seeded successfully!")

if __name__ == '__main__':
    seed()
