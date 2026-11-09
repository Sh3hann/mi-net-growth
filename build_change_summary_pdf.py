import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            canvas.Canvas.showPage(self)
        canvas.Canvas.save(self)

    def draw_page_decorations(self, page_count):
        # Top running header is completely removed as requested
        # Only simple, clean bottom footer is preserved
        self.saveState()
        self.setFont("Helvetica", 7.5)
        self.setFillColor(colors.HexColor("#64748b"))
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 36, 18, page_text)
        doc_info = "SIA (Sales Incentive Automation) · https://github.com/Sh3hann/mi-net-growth"
        self.drawString(36, 18, doc_info)
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(36, 26, letter[0] - 36, 26)
        self.restoreState()

def build_pdf(filename="MI_Net_Growth_Levels_Change_Summary.pdf"):
    pdf_path = os.path.abspath(filename)
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=32,
        bottomMargin=34,
    )

    styles = getSampleStyleSheet()

    # Typography styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=colors.HexColor('#0f172a'),
        spaceAfter=3,
    )

    meta_style = ParagraphStyle(
        'DocMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#334155'),
        spaceAfter=5,
    )

    desc_style = ParagraphStyle(
        'DocDesc',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor('#1e293b'),
        spaceAfter=7,
    )

    section_header_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor('#0f172a'),
        spaceBefore=7,
        spaceAfter=3,
    )

    th_style = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white,
    )

    td_style = ParagraphStyle(
        'TD',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7,
        leading=8.5,
        textColor=colors.HexColor('#0f172a'),
    )

    td_mono = ParagraphStyle(
        'TDMono',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.5,
        leading=8,
        textColor=colors.HexColor('#0f172a'),
    )

    td_bold = ParagraphStyle(
        'TDBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7,
        leading=8.5,
        textColor=colors.HexColor('#0f172a'),
    )

    header_navy = colors.HexColor('#1e293b')
    border_color = colors.HexColor('#cbd5e1')
    alt_bg = colors.HexColor('#f8fafc')

    def make_table(data, col_widths):
        t = Table(data, colWidths=col_widths, repeatRows=1)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), header_navy),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
            ('LEFTPADDING', (0, 0), (-1, -1), 3.5),
            ('RIGHTPADDING', (0, 0), (-1, -1), 3.5),
            ('GRID', (0, 0), (-1, -1), 0.5, border_color),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, alt_bg]),
        ]))
        return t

    def create_detail_block(title, rows, col_widths=[22, 130, 388]):
        elements = [Paragraph(title, section_header_style)]
        data = [[Paragraph("No", th_style), Paragraph("Change", th_style), Paragraph("Details", th_style)]]
        for r in rows:
            data.append([
                Paragraph(str(r[0]), td_style),
                Paragraph(r[1], td_bold),
                Paragraph(r[2], td_style),
            ])
        elements.append(make_table(data, col_widths))
        return elements

    elements = []

    # ================= PAGE 1 =================
    elements.append(Paragraph("MI Net Growth Levels Management - Change Summary", title_style))
    elements.append(Paragraph("<b>Developer:</b> Sh3hann &nbsp;|&nbsp; <b>Branch:</b> main / feature/mi-net-growth-levels &nbsp;|&nbsp; <b>Date:</b> November 2026", meta_style))
    elements.append(Paragraph("<b>Repository:</b> https://github.com/Sh3hann/mi-net-growth.git", meta_style))
    elements.append(Paragraph("Implemented a full-stack system to manage MI Net Growth Levels for the SIA (Sales Incentive Automation) system using PostgreSQL, Django REST Framework, and React.js with full CRUD functionality, sequential NET_ID auto-generation, range contiguity/overlap prevention, file attachment uploads, and Role-Based Access Control (CFO, DGM, RM).", desc_style))

    # Master Table (15 rows matching reference)
    col_master = [18, 90, 135, 105, 192]
    master_rows = [
        ("1", "models.py", "backend/growth_levels/models.py", "Database Table & ORM", "Created SIA_MI_NET_GROWTH_LEVELS table with sequential NET_ID auto-generator, range validation, and overlap checks."),
        ("2", "views.py", "backend/growth_levels/views.py", "REST API & Business Logic", "Built MiNetGrowthLevelViewSet supporting CRUD, statistics, file download, and RBAC enforcement (CFO/DGM/RM)."),
        ("3", "urls.py", "backend/growth_levels/urls.py", "Backend Routing", "Mapped /api/mi-net-growth-levels/ routes using DRF DefaultRouter for all endpoints."),
        ("4", "serializers.py", "backend/growth_levels/serializers.py", "API Serialization", "Created MiNetGrowthLevelSerializer with decimal validation, overlap checks, attachment URL builders, and audit user headers."),
        ("5", "pagination.py", "backend/growth_levels/pagination.py", "Data Pagination", "StandardResultsSetPagination supporting customizable page size and unpaginated query parameters."),
        ("6", "settings.py", "backend/growth_backend/settings.py", "Backend Settings", "Configured PostgreSQL with SQLite fallback, CORS headers, Media root and URL for file storage."),
        ("7", "tests.py", "backend/growth_levels/tests.py", "Automated Testing", "Added 11 unit tests covering CRUD, range overlap rejection (400), percentage limits (400), and RBAC permissions (403)."),
        ("8", "seed_data.py", "backend/seed_data.py", "Data Seeding", "Populated initial enterprise growth tiers (NET001 to NET006) with realistic ranges, percentages, and sample attachments."),
        ("9", "docker-compose.yml", "backend/docker-compose.yml", "PostgreSQL Setup", "Containerized PostgreSQL 15 alpine database service listening on port 5432."),
        ("10", "api.js", "frontend/src/services/api.js", "API Client Service", "Axios client with multipart/form-data support, dynamic role headers, error message parser, and blob download."),
        ("11", "Navbar.jsx", "frontend/src/components/Navbar.jsx", "Top Navigation", "Enterprise navigation with title, simulator modal trigger, and live RBAC role switcher (CFO, DGM, RM)."),
        ("12", "StatsCards.jsx", "frontend/src/components/StatsCards.jsx", "Dashboard KPIs", "Metric cards displaying Total Levels, Active Levels, Inactive Levels, Average Incentive %, and Max Range Ceiling."),
        ("13", "RangeVisualizer.jsx", "frontend/src/components/RangeVisualizer.jsx", "Spectrum Analyzer", "Visual range coverage bar confirming continuous non-overlapping active tiers from $0 to maximum ceiling."),
        ("14", "FilterBar.jsx", "frontend/src/components/FilterBar.jsx", "Toolbar & Actions", "Search by level or NET_ID, status filter tabs (All, Active, Inactive), CSV export button, and Add Level button."),
        ("15", "GrowthLevelTable.jsx", "frontend/src/components/GrowthLevelTable.jsx", "Data Table", "Table showing NET_ID, ranges, incentive %, active status pill, file download links, and role-based action buttons."),
    ]
    master_table_data = [[
        Paragraph("No", th_style),
        Paragraph("File", th_style),
        Paragraph("Path", th_style),
        Paragraph("Used In", th_style),
        Paragraph("What Changed", th_style),
    ]]
    for r in master_rows:
        master_table_data.append([
            Paragraph(r[0], td_style),
            Paragraph(r[1], td_bold),
            Paragraph(r[2], td_mono),
            Paragraph(r[3], td_style),
            Paragraph(r[4], td_style),
        ])
    elements.append(make_table(master_table_data, col_master))

    # models.py on Page 1
    elements.extend(create_detail_block("models.py", [
        (1, "Table Name", "Created SIA_MI_NET_GROWTH_LEVELS table mapped through Django ORM db_table setting."),
        (2, "NET_ID Field", "CharField unique=True (max_length=20) with automated sequence generator (NET001, NET002...)."),
        (3, "Range Fields", "LOWER_RANGE and UPPER_RANGE DecimalField(14,2) with non-negative and upper > lower constraints."),
        (4, "Overlap Validation", "Model clean() verifies that no two Active records overlap in the lower_range to upper_range interval."),
    ]))

    # views.py (growth_levels) on Page 1
    elements.extend(create_detail_block("views.py (growth_levels)", [
        (1, "CRUD Endpoints", "MiNetGrowthLevelViewSet provides POST (create), GET (list), GET /<id>/ (retrieve), PUT/PATCH (update), DELETE (destroy)."),
        (2, "Search & Filter", "Implemented ?search= (Level, NET_ID, Comments) and ?status=Active|Inactive query filtering."),
        (3, "Statistics API", "Added /api/mi-net-growth-levels/statistics/ action calculating total, active, inactive, avg %, and max ceiling."),
        (4, "RBAC Permissions", "check_role_permissions() blocks RM from all writes (403) and blocks DGM from delete actions (403)."),
    ]))

    # ================= PAGE 2 =================
    elements.append(PageBreak())

    # views.py continued
    elements.extend(create_detail_block("views.py (growth_levels) - Continued", [
        (5, "Download Attachment", "/api/mi-net-growth-levels/<id>/download_attachment/ streams binary file with Content-Disposition header."),
        (6, "Multipart Support", "parser_classes = [MultiPartParser, FormParser, JSONParser] allows file uploads and JSON interchangeably."),
        (7, "Ordering Logic", "Supported ?ordering= query parameter to dynamically sort by lower_range, percentage, or created_date."),
        (8, "Unpaginated Export", "Supported ?paginate=false to return all records for reporting, visualizations, and client calculations."),
    ]))

    # urls.py
    elements.extend(create_detail_block("urls.py", [
        (1, "DefaultRouter Route", "router.register(r'mi-net-growth-levels', MiNetGrowthLevelViewSet) creates full REST URL tree."),
        (2, "API Integration", "Mounted in growth_backend/urls.py under path('api/', include('growth_levels.urls'))."),
        (3, "Media File Handler", "Added static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) to serve uploads in dev."),
    ]))

    # serializers.py
    elements.extend(create_detail_block("serializers.py", [
        (1, "Key Normalization", "to_internal_value() maps incoming uppercase keys (LEVEL, LOWER_RANGE) to lowercase model fields."),
        (2, "Range Overlap Check", "Validates range bounds against database active records and returns clear 400 Bad Request if conflicts exist."),
        (3, "Percentage Boundaries", "Enforces 0.00% <= percentage <= 100.00% returning field error if boundary is violated."),
        (4, "Audit Header Tagging", "create() and update() auto-populate created_user and updated_user from request X-User-Role / X-User-Name."),
        (5, "Attachment Metadata", "SerializerMethodFields dynamically expose attachment_name and absolute attachment_url."),
    ]))

    # pagination.py
    elements.extend(create_detail_block("pagination.py", [
        (1, "Standard Pagination", "StandardResultsSetPagination with page_size=10, page_size_query_param='page_size', max_page_size=100."),
        (2, "Metadata Response", "Returns count, total_pages, current_page, next, and previous links alongside data results."),
    ]))

    # docker-compose.yml
    elements.extend(create_detail_block("docker-compose.yml", [
        (1, "PostgreSQL 15 Container", "Configured postgres:15-alpine image with POSTGRES_DB=mi_net_growth_db on port 5432."),
        (2, "Volume Persistence", "Mapped postgres_data volume to /var/lib/postgresql/data for local data durability."),
    ]))

    # api.js (Frontend Service)
    elements.extend(create_detail_block("api.js (Frontend Service)", [
        (1, "Axios Client", "Created centralized Axios instance with baseURL (http://localhost:8000/api) and timeout."),
        (2, "RBAC Interceptors", "Attaches current active role (X-User-Role) and user name from localStorage to every outbound request."),
        (3, "Multipart Form Support", "growthLevelsApi.create() and update() automatically inspect data and apply multipart/form-data."),
        (4, "Blob Download Helper", "downloadAttachment() requests responseType: 'blob' and generates temporary DOM anchor to download."),
        (5, "DRF Error Formatter", "formatApiError() unpacks DRF error dictionaries into human-readable toast notification strings."),
    ]))

    # ================= PAGE 3 =================
    elements.append(PageBreak())

    # Frontend Components
    elements.extend(create_detail_block("Frontend Components (React.js)", [
        (1, "Navbar.jsx", "Displays system title, simulator modal shortcut, and live role switcher (CFO, DGM, RM)."),
        (2, "StatsCards.jsx", "5 clean metrics cards showing Total Levels, Active Levels, Inactive Levels, Avg Incentive %, Max Range."),
        (3, "RangeVisualizer.jsx", "Visual tier coverage bar displaying continuous non-overlapping distribution from $0 to ceiling."),
        (4, "FilterBar.jsx", "Search by level or NET_ID, status filter tabs (All, Active, Inactive), CSV export, and Add Level button."),
        (5, "GrowthLevelTable.jsx", "Table displaying NET_ID, Level, Ranges, Incentive %, Active status pill, Attachment download, and actions."),
        (6, "LevelFormModal.jsx", "Modal with client-side range checks, real-time overlap collision alert, and file upload input."),
        (7, "DeleteConfirmModal.jsx", "Confirmation dialog showing tier details before deletion, restricted to CFO."),
        (8, "TierDetailDrawer.jsx", "Slide-over drawer displaying full tier specs, payout scenarios, audit trail, and document downloader."),
        (9, "Toast.jsx", "Toast notification container providing real-time feedback for create, update, delete, and validation errors."),
    ]))

    # SimulatorModal.jsx
    elements.extend(create_detail_block("SimulatorModal.jsx", [
        (1, "Deal Volume Input", "Allows entering gross net growth amount with quick presets ($25k, $100k, $250k, $500k, $1M)."),
        (2, "Bracket Matching", "Evaluates active tiers to find matching qualification tier and applicable incentive percentage."),
        (3, "Formula Breakdown", "Displays exact formula calculation and distance needed to unlock the next higher tier bracket."),
    ]))

    # .env
    elements.extend(create_detail_block(".env (Backend & Frontend)", [
        (1, "USE_POSTGRES", "USE_POSTGRES=False (defaults to SQLite for instant local dev) or True to connect to PostgreSQL."),
        (2, "DB Connection Keys", "DB_NAME=mi_net_growth_db, DB_USER=postgres, DB_PASSWORD=postgres, DB_HOST=localhost, DB_PORT=5432."),
        (3, "VITE_API_URL", "VITE_API_URL=http://localhost:8000/api for Vite React client."),
    ]))

    # User Flow
    flow_col_widths = [22, 130, 388]
    elements.append(Paragraph("User Flow", section_header_style))
    flow_data = [
        [Paragraph("No", th_style), Paragraph("Flow", th_style), Paragraph("Steps", th_style)],
        [
            Paragraph("1", td_style),
            Paragraph("View & Search Tiers", td_bold),
            Paragraph("User navigates to dashboard, views KPI metrics and active range spectrum, searches by level name or NET_ID, and filters by status (All, Active, Inactive).", td_style),
        ],
        [
            Paragraph("2", td_style),
            Paragraph("Add New Tier (CFO/DGM)", td_bold),
            Paragraph("User clicks 'Add Level', fills level title, lower & upper ranges, percentage, comments, and optional file. Client and backend validate range contiguity and overlap before committing.", td_style),
        ],
        [
            Paragraph("3", td_style),
            Paragraph("Edit Tier (CFO/DGM)", td_bold),
            Paragraph("User clicks Edit icon on a row, form pre-populates with existing data. User modifies range or replaces attachment. Table and KPI stats auto-refresh upon save.", td_style),
        ],
        [
            Paragraph("4", td_style),
            Paragraph("Delete Tier (CFO Only)", td_bold),
            Paragraph("CFO clicks Delete icon, confirmation dialog displays record summary. Deletion permanently removes tier. DGM and RM users have Delete button disabled (HTTP 403 on API).", td_style),
        ],
        [
            Paragraph("5", td_style),
            Paragraph("Simulate Deal Payout", td_bold),
            Paragraph("User clicks 'Simulator' in header, inputs gross deal volume (e.g. $250,000), engine highlights matching tier, applicable percentage (8.75%), and calculates payout ($21,875.00).", td_style),
        ],
    ]
    elements.append(make_table(flow_data, flow_col_widths))

    # Testing Checklist on Page 3
    test_col_widths = [22, 180, 338]
    elements.append(Paragraph("Testing Checklist", section_header_style))
    test_data_p3 = [
        [Paragraph("No", th_style), Paragraph("Test Case", th_style), Paragraph("Expected Result", th_style)],
        [
            Paragraph("1", td_style),
            Paragraph("Database Table Creation", td_bold),
            Paragraph("Table SIA_MI_NET_GROWTH_LEVELS created in PostgreSQL via makemigrations and migrate.", td_style),
        ],
        [
            Paragraph("2", td_style),
            Paragraph("Auto NET_ID Generation", td_bold),
            Paragraph("Sequential ID (NET001, NET002, ...) auto-generated on record creation without manual input.", td_style),
        ],
        [
            Paragraph("3", td_style),
            Paragraph("List Records API (GET)", td_bold),
            Paragraph("Returns HTTP 200 OK with paginated list, count, total_pages, and results array.", td_style),
        ],
    ]
    elements.append(make_table(test_data_p3, test_col_widths))

    # ================= PAGE 4 =================
    elements.append(PageBreak())

    # Testing Checklist continued
    elements.append(Paragraph("Testing Checklist - Continued", section_header_style))
    test_data_p4 = [
        [Paragraph("No", th_style), Paragraph("Test Case", th_style), Paragraph("Expected Result", th_style)],
        [
            Paragraph("4", td_style),
            Paragraph("Single Record Retrieval (GET)", td_bold),
            Paragraph("Returns HTTP 200 OK with single record details matching requested PK ID.", td_style),
        ],
        [
            Paragraph("5", td_style),
            Paragraph("Multipart File Upload (POST)", td_bold),
            Paragraph("Returns HTTP 201 Created; uploaded file stored in media directory and attachment URL returned.", td_style),
        ],
        [
            Paragraph("6", td_style),
            Paragraph("Range Overlap Validation", td_bold),
            Paragraph("Attempting to create or update an overlapping active range returns HTTP 400 Bad Request with conflicting tier names.", td_style),
        ],
        [
            Paragraph("7", td_style),
            Paragraph("Percentage Limit Validation", td_bold),
            Paragraph("Percentage < 0 or > 100 returns HTTP 400 Bad Request.", td_style),
        ],
        [
            Paragraph("8", td_style),
            Paragraph("Upper > Lower Range Validation", td_bold),
            Paragraph("Upper range <= lower range or negative lower range returns HTTP 400 Bad Request.", td_style),
        ],
        [
            Paragraph("9", td_style),
            Paragraph("RM Read-Only Access (RBAC)", td_bold),
            Paragraph("RM role sending POST, PUT, PATCH, or DELETE receives HTTP 403 Forbidden.", td_style),
        ],
        [
            Paragraph("10", td_style),
            Paragraph("DGM Delete Prevention (RBAC)", td_bold),
            Paragraph("DGM role sending DELETE receives HTTP 403 Forbidden. Can execute POST, PUT, and PATCH.", td_style),
        ],
        [
            Paragraph("11", td_style),
            Paragraph("CFO Full Permissions (RBAC)", td_bold),
            Paragraph("CFO role can create, view, update, and delete growth levels.", td_style),
        ],
        [
            Paragraph("12", td_style),
            Paragraph("Attachment File Download", td_bold),
            Paragraph("GET download_attachment streams file with Content-Disposition header and correct filename.", td_style),
        ],
        [
            Paragraph("13", td_style),
            Paragraph("Frontend Table & Auto-Refresh", td_bold),
            Paragraph("Table renders active pills, formatted currency, and auto-refreshes immediately after mutations.", td_style),
        ],
        [
            Paragraph("14", td_style),
            Paragraph("Automated Backend Test Suite", td_bold),
            Paragraph("All 11 unit tests in tests.py pass successfully (Ran 11 tests in 0.101s, OK).", td_style),
        ],
    ]
    elements.append(make_table(test_data_p4, test_col_widths))
    elements.append(Spacer(1, 10))

    # Git Status Section
    elements.append(Paragraph("Git Status & Repository State", section_header_style))
    git_box_style = ParagraphStyle(
        'GitBox',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=6.8,
        leading=9.2,
        textColor=colors.HexColor('#0f172a'),
    )
    git_text = """
<b>Remote Origin:</b> https://github.com/Sh3hann/mi-net-growth.git<br/>
<b>Branches Synced:</b> main, feature/mi-net-growth-levels (Up to date with origin)<br/>
<b>Author:</b> Sh3hann &lt;akilshehan760@gmail.com&gt;<br/>
<b>Commit Log:</b><br/>
• 8831c9e (origin/main, main) chore: sync with GitHub origin main and retain full system documentation<br/>
• 7d37abe docs(pdf): generate change summary and git status PDF documentation<br/>
• 4e7d294 feat(mi-net-growth): complete full-stack implementation with Django ORM, REST API, React frontend, and Postman suite<br/>
<br/>
<b>Tracked Files in Repository:</b><br/>
• backend/growth_levels/models.py ..................... [SIA_MI_NET_GROWTH_LEVELS table model]<br/>
• backend/growth_levels/views.py ...................... [MiNetGrowthLevelViewSet CRUD & RBAC]<br/>
• backend/growth_levels/serializers.py ................ [DRF serializer with overlap validation]<br/>
• backend/growth_levels/urls.py ....................... [API routes registration]<br/>
• backend/growth_levels/pagination.py ................. [Standard pagination handler]<br/>
• backend/growth_levels/tests.py ...................... [11 unit tests passing]<br/>
• backend/growth_backend/settings.py .................. [PostgreSQL / SQLite config & CORS]<br/>
• backend/seed_data.py ................................ [Database seeder for sample tiers]<br/>
• backend/docker-compose.yml .......................... [PostgreSQL 15 service]<br/>
• frontend/src/services/api.js ........................ [Axios CRUD service & multipart handler]<br/>
• frontend/src/components/Navbar.jsx .................. [Header & RBAC role switcher]<br/>
• frontend/src/components/StatsCards.jsx .............. [Executive KPI cards]<br/>
• frontend/src/components/RangeVisualizer.jsx ......... [Contiguity spectrum analyzer]<br/>
• frontend/src/components/FilterBar.jsx ............... [Search & status filter toolbar]<br/>
• frontend/src/components/GrowthLevelTable.jsx ........ [Data table with action triggers]<br/>
• frontend/src/components/LevelFormModal.jsx .......... [Add/Edit modal with overlap check]<br/>
• frontend/src/components/DeleteConfirmModal.jsx ...... [Deletion confirmation dialog]<br/>
• frontend/src/components/SimulatorModal.jsx .......... [Net revenue payout simulator]<br/>
• frontend/src/components/TierDetailDrawer.jsx ........ [Tier specs & dossier slide-over]<br/>
• frontend/src/components/Toast.jsx ................... [Toast notification system]<br/>
• postman/MI_Net_Growth_Levels.postman_collection.json  [Postman collection v2.1.0]<br/>
• postman/POSTMAN_GUIDE.md ............................ [Complete API testing guide]<br/>
• run_all.ps1 ......................................... [One-click startup PowerShell script]
    """
    git_table = Table([[Paragraph(git_text, git_box_style)]], colWidths=[540])
    git_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
    ]))
    elements.append(git_table)

    # Build the document
    doc.build(elements, canvasmaker=NumberedCanvas)
    print(f"PDF generated successfully at: {pdf_path}")
    return pdf_path

if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else "MI_Net_Growth_Levels_Change_Summary.pdf"
    build_pdf(target)
