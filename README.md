# MI Net Growth Levels Management System

Enterprise Full-Stack Application built with **PostgreSQL**, **Django & Django REST Framework (DRF)**, and **React.js**.

---

## 📋 System Architecture & Overview

This system manages sales/incentive **MI Net Growth Levels** with complete CRUD operations, automated sequence ID generation (`NET001`, `NET002`, ...), document attachment handling, real-time range overlap validation, and Role-Based Access Control (**CFO**, **DGM**, **RM**).

```
mi_net_growth_system/
├── backend/
│   ├── growth_backend/        # Django Project configuration (settings, urls, wsgi)
│   ├── growth_levels/         # Django App (Model, ViewSet, Serializer, Tests)
│   ├── media/                 # Storage for uploaded files and attachments
│   ├── docker-compose.yml     # PostgreSQL 15 Container configuration
│   ├── seed_data.py           # Database seeder with sample enterprise tiers
│   ├── requirements.txt       # Python dependencies
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── components/        # Navbar, StatsCards, Table, Modal, Toast, Visualizer
│   │   ├── services/          # api.js (Axios CRUD & Multipart handler)
│   │   ├── App.jsx            # Main React application
│   │   └── index.css          # Tailwind CSS styles & animations
│   ├── package.json
│   └── vite.config.js
└── postman/
    ├── MI_Net_Growth_Levels.postman_collection.json # Ready-to-import Postman collection
    └── POSTMAN_GUIDE.md                            # Comprehensive API documentation
```

---

## 🗄️ Task 01 — Database Table Specification

- **Table Name:** `SIA_MI_NET_GROWTH_LEVELS` (Created via Django ORM)
- **Columns & Data Types:**

| Column Name | Django Model Field | Description |
|---|---|---|
| `ID` | `AutoField` | Primary Key |
| `NET_ID` | `CharField(max_length=20, unique=True)` | Auto-generated sequential ID (`NET001`, `NET002`, ...) |
| `LEVEL` | `CharField(max_length=100)` | Level Name (e.g. Bronze Foundation, Gold Accelerator) |
| `LOWER_RANGE` | `DecimalField(max_digits=14, decimal_places=2)` | Lower Range Value (>= 0.00) |
| `UPPER_RANGE` | `DecimalField(max_digits=14, decimal_places=2)` | Upper Range Value (> LOWER_RANGE) |
| `PERCENTAGE` | `DecimalField(max_digits=6, decimal_places=2)` | Incentive Percentage (0.00% to 100.00%) |
| `CREATED_DATE` | `DateTimeField(auto_now_add=True)` | Automatic timestamp on creation |
| `CREATED_USER` | `CharField(max_length=100)` | Creator audit record |
| `UPDATED_DATE` | `DateTimeField(auto_now=True)` | Automatic timestamp on update |
| `UPDATED_USER` | `CharField(max_length=100, null=True)` | Updater audit record |
| `STATUS` | `CharField(max_length=20, choices=['Active', 'Inactive'])` | Level status |
| `ATTACHMENT` | `FileField(upload_to='growth_attachments/%Y/%m/')` | Document attachment (PDF/DOCX/TXT/Images) |
| `COMMENTS` | `CharField(max_length=500, null=True)` | Optional audit notes |

---

## 🚀 Quick Start Guide

### 1. Backend Setup (Django + PostgreSQL)

```bash
cd backend

# 1. (Optional) Start PostgreSQL using Docker:
docker-compose up -d

# 2. Install Python dependencies:
pip install -r requirements.txt

# 3. Run database migrations to create SIA_MI_NET_GROWTH_LEVELS:
python manage.py makemigrations growth_levels
python manage.py migrate

# 4. Seed sample enterprise levels:
python seed_data.py

# 5. Run test suite (11 unit tests covering CRUD, Overlap, RBAC):
python manage.py test

# 6. Start Django development server:
python manage.py runserver 8000
```

> **Note on Database:** By default, Django seamlessly connects to PostgreSQL when `USE_POSTGRES=True` or `DB_ENGINE=django.db.backends.postgresql` is configured in environment variables or `.env`. If PostgreSQL is not active, it gracefully runs on SQLite for instant plug-and-play development.

---

### 2. Frontend Setup (React.js + Tailwind CSS)

```bash
cd ../frontend

# 1. Install Node.js dependencies:
npm install

# 2. Start Vite development server:
npm run dev
```

Visit **`http://localhost:5173`** in your browser.

---

## 🔌 API Endpoints (Task 02)

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/mi-net-growth-levels/` | List all records (supports `?search=`, `?status=`, pagination) |
| `GET` | `/api/mi-net-growth-levels/<id>/` | Retrieve single record |
| `POST` | `/api/mi-net-growth-levels/` | Create new record (Auto NET_ID generation, file upload support) |
| `PUT` | `/api/mi-net-growth-levels/<id>/` | Full update of existing record |
| `PATCH` | `/api/mi-net-growth-levels/<id>/` | Partial update of existing record |
| `DELETE` | `/api/mi-net-growth-levels/<id>/` | Delete record (CFO role only) |
| `GET` | `/api/mi-net-growth-levels/statistics/` | Dashboard KPI metrics |
| `GET` | `/api/mi-net-growth-levels/<id>/download_attachment/` | Stream/download attachment |

---

## 🛡️ Business Logic & Validations (Task 05)

1. **NET_ID Auto-Generation:**
   - On creation, the backend inspects existing records and computes the next sequential code (`NET001`, `NET002`, `NET003`...).
2. **Range Overlap Prevention:**
   - The model and serializer automatically check that no two `Active` growth levels overlap:
     `lower_range <= other.upper_range AND upper_range >= other.lower_range`.
   - The React frontend also runs real-time overlap validation before submitting.
3. **Range Value Consistency:**
   - `LOWER_RANGE >= 0.00`
   - `UPPER_RANGE > LOWER_RANGE`
4. **Percentage Boundaries:**
   - `0.00 <= PERCENTAGE <= 100.00`
5. **Role-Based Access Control (RBAC):**
   - **`CFO` (Chief Financial Officer):** Full CRUD permissions + Deletion rights.
   - **`DGM` (Deputy General Manager):** Create & Edit records. Deletion is blocked (HTTP 403).
   - **`RM` (Relationship Manager):** Read-only viewer. Create, Edit, and Delete are blocked (HTTP 403).

---

## 📮 Postman API Testing (Task 03)

1. Open Postman.
2. Import `postman/MI_Net_Growth_Levels.postman_collection.json`.
3. All endpoints, validation test cases, and RBAC tests are pre-configured.
4. Refer to `postman/POSTMAN_GUIDE.md` for full documentation and sample payloads.
