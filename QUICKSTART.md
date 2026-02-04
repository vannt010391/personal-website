# Hướng Dẫn Sử Dụng Nhanh

## Khởi động dự án

### 1. Kích hoạt môi trường ảo

```bash
# Windows
myenv\Scripts\activate

# Mac/Linux
source myenv/bin/activate
```

### 2. Chạy server

```bash
python manage.py runserver
```

Truy cập: **http://127.0.0.1:8000/**

---

## Đăng nhập Admin

Truy cập: **http://127.0.0.1:8000/admin/**

Sử dụng tài khoản superuser đã tạo.

---

## Các Tính Năng Chính

### 📝 Blog

**URL:** http://127.0.0.1:8000/blog/

- Xem danh sách bài viết đã xuất bản
- Lọc theo danh mục
- Đọc bài viết chi tiết với Markdown rendering
- **Yêu cầu đăng nhập để:**
  - Tạo bài viết mới
  - Chỉnh sửa/Xóa bài viết
  - Quản lý danh mục

**Tạo bài viết:**
1. Đăng nhập
2. Vào Blog > Tạo bài viết mới
3. Nhập tiêu đề (slug tự động tạo)
4. Viết nội dung với Markdown
5. Chọn danh mục và trạng thái
6. Lưu

**Markdown hỗ trợ:**
- Headings: `# H1`, `## H2`, `### H3`
- Bold: `**text**`
- Italic: `*text*`
- Code: `` `code` ``
- Code blocks: ` ```python ... ``` `
- Links: `[text](url)`
- Images: `![alt](url)`

---

### ✅ Quản Lý Công Việc

**Dashboard:** http://127.0.0.1:8000/tasks/

Hiển thị:
- Công việc hôm nay
- Công việc quá hạn
- Công việc đang thực hiện
- Phiên học gần đây

**Kanban Board:** http://127.0.0.1:8000/tasks/kanban/

Xem công việc theo các cột:
- Chưa làm (Pending)
- Đang làm (In Progress)
- Hoàn thành (Completed)

**Tạo công việc:**
1. Vào Tasks > Thêm công việc mới
2. Nhập tên công việc
3. Chọn loại: Work/Study/Personal
4. Đặt mức độ ưu tiên: Low/Medium/High
5. Chọn trạng thái
6. Đặt deadline
7. Lưu

**Theo dõi học tập:**
- Tạo phiên học tập với môn học, thời lượng
- Ghi chú những gì đã học
- Xem lịch sử học tập

---

### 📚 Quản Lý Kiến Thức

**URL:** http://127.0.0.1:8000/knowledge/

**Tạo ghi chú:**
1. Vào Knowledge > Thêm ghi chú mới
2. Nhập tiêu đề
3. Chọn loại: Note/Research/Article/Reference
4. Chọn chủ đề
5. Viết nội dung (Markdown)
6. Thêm tags (phân cách bằng dấu phẩy)
7. Đánh dấu yêu thích nếu cần
8. Lưu

**Quản lý chủ đề:**
- Tạo chủ đề mới
- Hỗ trợ chủ đề con (hierarchical)
- Ví dụ: Programming > Python > Django

**Tài nguyên học tập:**
- Lưu trữ sách, video, khóa học
- Theo dõi trạng thái: To Read/Reading/Completed
- Đánh giá (1-5 sao)
- Ghi chú về tài nguyên

---

## API REST

**Base URL:** http://127.0.0.1:8000/api/

### Lấy Token Authentication

```bash
curl -X POST http://127.0.0.1:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"your_password"}'
```

Response:
```json
{"token":"9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"}
```

### Endpoints chính

**Blog:**
- `GET /api/posts/` - Danh sách bài viết
- `GET /api/posts/{id}/` - Chi tiết bài viết
- `POST /api/posts/` - Tạo bài viết (cần token)
- `GET /api/categories/` - Danh sách danh mục

**Tasks:**
- `GET /api/tasks/` - Danh sách công việc (cần token)
- `POST /api/tasks/` - Tạo công việc (cần token)
- `GET /api/study-sessions/` - Phiên học tập (cần token)

**Knowledge:**
- `GET /api/topics/` - Danh sách chủ đề (cần token)
- `GET /api/knowledge-entries/` - Ghi chú (cần token)
- `GET /api/resources/` - Tài nguyên (cần token)

### Sử dụng API với Token

```bash
# Ví dụ: Lấy danh sách tasks
curl -H "Authorization: Token YOUR_TOKEN_HERE" \
  http://127.0.0.1:8000/api/tasks/

# Tạo task mới
curl -X POST \
  -H "Authorization: Token YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Học Django REST Framework",
    "task_type": "study",
    "priority": "high",
    "status": "pending",
    "due_date": "2026-02-10"
  }' \
  http://127.0.0.1:8000/api/tasks/
```

### Filtering & Search

```bash
# Lọc posts theo status
GET /api/posts/?status=published

# Lọc posts theo category
GET /api/posts/?category=1

# Search trong posts
GET /api/posts/?search=django

# Sắp xếp
GET /api/posts/?ordering=-created_at

# Lọc tasks
GET /api/tasks/?status=pending&priority=high

# Lọc knowledge entries
GET /api/knowledge-entries/?entry_type=note&is_favorite=true
```

---

## Tips & Tricks

### Auto-generate Slug
Khi tạo/sửa bài viết, category, entry - slug sẽ tự động tạo từ tiêu đề nhờ JavaScript.

### Markdown Preview
- Admin panel có MarkdownX editor với live preview
- Web forms hỗ trợ Markdown syntax

### Quản lý nhanh
Từ trang chủ (khi đã đăng nhập):
- Tạo bài viết
- Thêm công việc  
- Thêm ghi chú

### Pagination
Tất cả danh sách đều có phân trang (10-20 items/trang)

---

## Troubleshooting

### Server không chạy được
```bash
# Kiểm tra port 8000 có bị chiếm không
netstat -ano | findstr :8000

# Kill process nếu cần (thay PID)
taskkill /F /PID <PID>

# Chạy lại
python manage.py runserver
```

### Lỗi đăng nhập
- Kiểm tra username/password
- Tạo lại superuser: `python manage.py createsuperuser`

### Static files không load
```bash
python manage.py collectstatic
```

### Database issues
```bash
# Xóa database và tạo lại
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## Development

### Tạo migrations mới
```bash
python manage.py makemigrations
python manage.py migrate
```

### Tạo superuser mới
```bash
python manage.py createsuperuser
```

### Shell Django
```bash
python manage.py shell
```

### Chạy tests
```bash
python manage.py test
```

---

## Production Checklist

Trước khi deploy:

1. Tắt DEBUG trong settings.py
2. Thay SECRET_KEY
3. Cấu hình ALLOWED_HOSTS
4. Sử dụng PostgreSQL/MySQL thay vì SQLite
5. Cấu hình static/media files với nginx
6. Sử dụng gunicorn/uwsgi
7. Setup HTTPS
8. Cấu hình CORS nếu cần
9. Setup logging
10. Backup database định kỳ

---

Chúc bạn sử dụng hiệu quả! 🚀
