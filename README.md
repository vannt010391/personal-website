# Website Cá Nhân

Website cá nhân được xây dựng bằng Django để quản lý blog, công việc và kiến thức.

## Tính Năng

### 1. Blog
- Viết và quản lý bài viết cá nhân với hỗ trợ Markdown
- Phân loại bài viết theo danh mục
- Trạng thái bài viết (Draft/Published)
- Hỗ trợ excerpt và content đầy đủ
- Web interface để xem và đọc bài viết
- Syntax highlighting cho code blocks

### 2. Quản Lý Công Việc (Tasks)
- Dashboard tổng quan công việc hàng ngày
- Quản lý danh sách công việc hàng ngày
- Phân loại: Công việc, Học tập, Cá nhân
- Mức độ ưu tiên: Low, Medium, High
- Trạng thái: Pending, In Progress, Completed, Cancelled
- Theo dõi thời gian học tập (Study Sessions)
- Hiển thị công việc quá hạn và đang thực hiện

### 3. Quản Lý Kiến Thức (Knowledge)
- Lưu trữ ghi chú và nghiên cứu với Markdown
- Phân loại theo chủ đề (Topics) với cấu trúc phân cấp
- Các loại entry: Note, Research, Article, Reference
- Quản lý tài nguyên học tập (sách, video, khóa học, website, paper)
- Đánh dấu yêu thích và đánh giá
- Tags và filtering
- Theo dõi trạng thái đọc (To Read, Reading, Completed)

### 4. RESTful API
- API endpoints cho tất cả models
- Token authentication và Session authentication
- Filtering, searching và pagination
- Markdown được render sang HTML tự động
- Swagger/OpenAPI documentation

## Cài Đặt và Chạy

### 1. Kích hoạt Virtual Environment

Trên Windows:
```bash
venv\Scripts\activate
```

Trên Mac/Linux:
```bash
source venv/bin/activate
```

### 2. Cài đặt dependencies (nếu cần)
```bash
pip install -r requirements.txt
```

### 3. Tạo Database (đã hoàn thành)
```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Tạo Superuser
```bash
python manage.py createsuperuser
```

Làm theo hướng dẫn để tạo tài khoản admin.

### 5. Chạy Server
```bash
python manage.py runserver
```

Website sẽ chạy tại: http://127.0.0.1:8000/

## Cách Sử Dụng

### Web Interface

#### Trang chủ
- URL: http://127.0.0.1:8000/
- Giới thiệu tổng quan về website

#### Đăng nhập
- URL: http://127.0.0.1:8000/login/
- Đăng nhập để truy cập các tính năng cá nhân

#### Admin Panel
- URL: http://127.0.0.1:8000/admin/
- Quản lý tất cả dữ liệu
- Thêm/sửa/xóa bài viết, công việc, kiến thức

#### Blog
- Danh sách: http://127.0.0.1:8000/blog/
- Chi tiết bài viết: http://127.0.0.1:8000/blog/<slug>/
- Lọc theo danh mục: http://127.0.0.1:8000/blog/category/<slug>/

#### Tasks
- Dashboard: http://127.0.0.1:8000/tasks/
- Danh sách công việc: http://127.0.0.1:8000/tasks/list/
- Phiên học tập: http://127.0.0.1:8000/tasks/study-sessions/

#### Knowledge
- Danh sách kiến thức: http://127.0.0.1:8000/knowledge/
- Chi tiết entry: http://127.0.0.1:8000/knowledge/entry/<slug>/
- Tài nguyên: http://127.0.0.1:8000/knowledge/resources/

### API Endpoints

Base URL: http://127.0.0.1:8000/api/

#### Authentication
```bash
# Lấy token (sử dụng cho các API requests)
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -d "username=your_username&password=your_password"

# Response: {"token": "your_token_here"}
```

#### Blog API
- Categories: `/api/categories/`
- Posts: `/api/posts/`
- Filter posts: `/api/posts/?status=published&category=1`
- Search: `/api/posts/?search=keyword`

#### Tasks API (Yêu cầu đăng nhập)
- Tasks: `/api/tasks/`
- Study Sessions: `/api/study-sessions/`
- Filter: `/api/tasks/?status=pending&priority=high`

#### Knowledge API (Yêu cầu đăng nhập)
- Topics: `/api/topics/`
- Knowledge Entries: `/api/knowledge-entries/`
- Resources: `/api/resources/`
- Filter: `/api/knowledge-entries/?entry_type=note&is_favorite=true`

#### Sử dụng API với Token
```bash
# Ví dụ: Lấy danh sách tasks
curl -H "Authorization: Token your_token_here" \
  http://127.0.0.1:8000/api/tasks/

# Tạo task mới
curl -X POST \
  -H "Authorization: Token your_token_here" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Học Django",
    "description": "Hoàn thành tutorial",
    "task_type": "study",
    "priority": "high",
    "status": "pending",
    "due_date": "2026-02-10"
  }' \
  http://127.0.0.1:8000/api/tasks/
```

## Cấu Trúc Dự Án

```
personal-website/
├── blog/               # App quản lý blog
├── tasks/              # App quản lý công việc
├── knowledge/          # App quản lý kiến thức
├── mywebsite/          # Thư mục cấu hình chính
├── templates/          # Templates HTML
├── static/             # Static files (CSS, JS, Images)
├── media/              # User uploaded files
├── venv/               # Virtual environment
├── manage.py           # Django management script
└── requirements.txt    # Dependencies
```

## Models

### Blog App
- **Category**: Danh mục bài viết
- **Post**: Bài viết với title, content, status, published_at

### Tasks App
- **Task**: Công việc với priority, status, due_date
- **StudySession**: Phiên học tập với subject, duration, notes

### Knowledge App
- **Topic**: Chủ đề kiến thức (hỗ trợ phân cấp)
- **KnowledgeEntry**: Ghi chú/nghiên cứu với content, tags
- **Resource**: Tài nguyên học tập (sách, video, khóa học)

## Công Nghệ Sử Dụng

- **Python** 3.11.5
- **Django** 5.2.10
- **Django REST Framework** 3.16.1 - API REST
- **Markdown** 3.10.1 - Xử lý markdown
- **Django Markdownx** 4.0.9 - Markdown editor trong admin
- **Django Filter** 25.2 - Filtering trong API
- **Pillow** 12.1.0 - Xử lý hình ảnh
- **SQLite3** - Database (có thể thay đổi sang PostgreSQL/MySQL)
- HTML/CSS - Frontend

## Phát Triển Tiếp

Một số tính năng có thể thêm vào:
- Full-text search với Elasticsearch hoặc PostgreSQL
- Export/Import data (JSON, CSV)
- File attachments cho entries
- Comments cho blog posts
- Tags autocomplete
- Dashboard với charts và statistics
- Email notifications
- Mobile responsive design cải thiện
- Dark mode
- API rate limiting
- Caching với Redis

## License

Dự án cá nhân - Tự do sử dụng và chỉnh sửa
