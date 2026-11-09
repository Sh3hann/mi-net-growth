# Task 03 — Postman API Testing Guide

This guide provides complete instructions for testing the **MI Net Growth Levels Management System** REST APIs with Postman, cURL, or any HTTP client.

---

## 1. Quick Setup & Import

1. Open Postman.
2. Click **Import** (top left).
3. Select `postman/MI_Net_Growth_Levels.postman_collection.json`.
4. The collection is pre-configured with the environment variable:
   - `base_url`: `http://localhost:8000/api`
   - `sample_id`: `1`

---

## 2. API Endpoints Overview

| Method | Endpoint | Description | Role Required |
|---|---|---|---|
| **GET** | `/api/mi-net-growth-levels/` | List all records (paginated) | CFO, DGM, RM |
| **GET** | `/api/mi-net-growth-levels/?status=Active` | Filter records by status | CFO, DGM, RM |
| **GET** | `/api/mi-net-growth-levels/?search=Silver` | Search by Level, NET_ID, Comments | CFO, DGM, RM |
| **GET** | `/api/mi-net-growth-levels/statistics/` | Dashboard metrics & summary | CFO, DGM, RM |
| **GET** | `/api/mi-net-growth-levels/<id>/` | Retrieve single record | CFO, DGM, RM |
| **POST** | `/api/mi-net-growth-levels/` | Create new record (Auto NET_ID) | CFO, DGM |
| **PUT** | `/api/mi-net-growth-levels/<id>/` | Update existing record | CFO, DGM |
| **PATCH**| `/api/mi-net-growth-levels/<id>/` | Partial update | CFO, DGM |
| **DELETE**| `/api/mi-net-growth-levels/<id>/` | Delete record | CFO only |
| **GET** | `/api/mi-net-growth-levels/<id>/download_attachment/` | Download attached document | CFO, DGM, RM |

---

## 3. Detailed Request & Response Examples

### 3.1 List All Records
- **Method:** `GET`
- **URL:** `http://localhost:8000/api/mi-net-growth-levels/`
- **cURL Command:**
```bash
curl -X GET "http://localhost:8000/api/mi-net-growth-levels/"
```
- **Sample 200 OK Response:**
```json
{
  "count": 6,
  "total_pages": 1,
  "current_page": 1,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "net_id": "NET001",
      "level": "Tier 1 - Bronze Foundation",
      "lower_range": "0.00",
      "upper_range": "50000.00",
      "percentage": "2.50",
      "created_date": "2026-11-09T03:54:58.204561Z",
      "created_user": "CFO_ADMIN",
      "updated_date": "2026-11-09T03:54:58.204561Z",
      "updated_user": null,
      "status": "Active",
      "attachment": "http://localhost:8000/media/growth_attachments/2026/11/bronze_policy_guideline.txt",
      "attachment_name": "bronze_policy_guideline.txt",
      "attachment_url": "http://localhost:8000/media/growth_attachments/2026/11/bronze_policy_guideline.txt",
      "comments": "Initial base incentive bracket for entry-level sales targets.",
      "formatted_lower_range": "0.00",
      "formatted_upper_range": "50,000.00"
    }
  ]
}
```

---

### 3.2 Create New Record (JSON)
- **Method:** `POST`
- **URL:** `http://localhost:8000/api/mi-net-growth-levels/`
- **Headers:**
  - `Content-Type: application/json`
  - `X-User-Role: CFO`
- **Payload:**
```json
{
  "level": "Tier 6 - Zenith Club",
  "lower_range": "1500000.01",
  "upper_range": "3000000.00",
  "percentage": "22.50",
  "status": "Active",
  "comments": "Elite institutional partner tier."
}
```
- **Sample 201 Created Response:**
```json
{
  "id": 7,
  "net_id": "NET007",
  "level": "Tier 6 - Zenith Club",
  "lower_range": "1500000.01",
  "upper_range": "3000000.00",
  "percentage": "22.50",
  "created_date": "2026-11-09T04:00:12.123456Z",
  "created_user": "CFO",
  "updated_date": "2026-11-09T04:00:12.123456Z",
  "updated_user": null,
  "status": "Active",
  "attachment": null,
  "attachment_name": null,
  "attachment_url": null,
  "comments": "Elite institutional partner tier.",
  "formatted_lower_range": "1,500,000.01",
  "formatted_upper_range": "3,000,000.00"
}
```

---

### 3.3 Create New Record with File Upload (Multipart Form-Data)
- **Method:** `POST`
- **URL:** `http://localhost:8000/api/mi-net-growth-levels/`
- **Headers:** `X-User-Role: CFO`
- **Form Data Fields:**
  - `level`: `Tier 7 - Crown Heritage`
  - `lower_range`: `3000000.01`
  - `upper_range`: `5000000.00`
  - `percentage`: `25.00`
  - `status`: `Active`
  - `comments`: `Top institutional bracket with charter file attached.`
  - `attachment`: `[File]`
- **cURL Command:**
```bash
curl -X POST "http://localhost:8000/api/mi-net-growth-levels/" \
  -H "X-User-Role: CFO" \
  -F "level=Tier 7 - Crown Heritage" \
  -F "lower_range=3000000.01" \
  -F "upper_range=5000000.00" \
  -F "percentage=25.00" \
  -F "status=Active" \
  -F "attachment=@/path/to/charter.pdf"
```

---

### 3.4 Update Record (PUT / PATCH)
- **Method:** `PUT` / `PATCH`
- **URL:** `http://localhost:8000/api/mi-net-growth-levels/1/`
- **Headers:**
  - `Content-Type: application/json`
  - `X-User-Role: CFO`
- **Payload (PUT):**
```json
{
  "level": "Tier 1 - Bronze Foundation (Revised)",
  "lower_range": "0.00",
  "upper_range": "50000.00",
  "percentage": "3.00",
  "status": "Active",
  "comments": "Updated base percentage to 3%."
}
```

---

### 3.5 Delete Record
- **Method:** `DELETE`
- **URL:** `http://localhost:8000/api/mi-net-growth-levels/1/`
- **Headers:** `X-User-Role: CFO`
- **Sample 200 OK Response:**
```json
{
  "message": "Growth level 'NET001 - Tier 1 - Bronze Foundation' successfully deleted."
}
```

---

## 4. Validation Failure Scenarios

### 4.1 Range Overlap Validation (HTTP 400)
Attempting to create a range that overlaps with an existing Active record:
```json
{
  "level": "Conflicting Level",
  "lower_range": "25000.00",
  "upper_range": "75000.00",
  "percentage": "5.00",
  "status": "Active"
}
```
**Response (400 Bad Request):**
```json
{
  "non_field_errors": [
    "Range [25,000.00 - 75,000.00] overlaps with existing active level(s): 'Tier 1 - Bronze Foundation' (NET001: 0.00 - 50,000.00), 'Tier 2 - Silver Standard' (NET002: 50,000.01 - 150,000.00)."
  ]
}
```

### 4.2 Percentage Limit Validation (HTTP 400)
```json
{
  "level": "Invalid Level",
  "lower_range": "5000000.01",
  "upper_range": "6000000.00",
  "percentage": "115.00",
  "status": "Active"
}
```
**Response (400 Bad Request):**
```json
{
  "percentage": [
    "PERCENTAGE must be between 0.00% and 100.00%."
  ]
}
```

### 4.3 Upper Range <= Lower Range (HTTP 400)
```json
{
  "level": "Inverted Level",
  "lower_range": "500000.00",
  "upper_range": "400000.00",
  "percentage": "10.00",
  "status": "Active"
}
```
**Response (400 Bad Request):**
```json
{
  "upper_range": [
    "UPPER_RANGE (400000.00) must be strictly greater than LOWER_RANGE (500000.00)."
  ]
}
```

---

## 5. Role-Based Access Control (RBAC) Testing

Pass the header `X-User-Role` in requests:
- **`CFO`**: Full CRUD permissions (Add, Edit, Delete, View).
- **`DGM`**: Can Add and Edit, but Delete is denied (HTTP 403 Forbidden).
- **`RM`**: Read-only access. Any POST/PUT/PATCH/DELETE returns HTTP 403 Forbidden:
```json
{
  "detail": "Permission Denied: Relationship Managers (RM) have Read-Only access."
}
```
