# API Guide - Personal Website

Hướng dẫn sử dụng RESTful API của Personal Website.

## Base URL

```
http://127.0.0.1:8000/api/
```

## Authentication

API hỗ trợ 2 loại authentication:

### 1. Token Authentication

Lấy token:
```bash
POST /api/auth/token/
Content-Type: application/json

{
  "username": "your_username",
  "password": "your_password"
}
```

Response:
```json
{
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

Sử dụng token trong các requests:
```bash
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

### 2. Session Authentication

Đăng nhập qua web interface tại `/login/`, sau đó có thể sử dụng API với session cookie.

## Endpoints

### Blog API

#### Categories

**List Categories**
```bash
GET /api/categories/
```

Response:
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Technology",
      "slug": "technology",
      "description": "Tech articles",
      "created_at": "2026-02-01T10:00:00Z"
    }
  ]
}
```

**Create Category**
```bash
POST /api/categories/
Authorization: Token your_token_here
Content-Type: application/json

{
  "name": "Python",
  "slug": "python",
  "description": "Python programming"
}
```

#### Posts

**List Posts**
```bash
GET /api/posts/
```

Query parameters:
- `status`: draft, published
- `category`: category ID
- `search`: search in title, content, excerpt
- `ordering`: created_at, -created_at, updated_at, -updated_at

Example:
```bash
GET /api/posts/?status=published&category=1&search=django
```

Response:
```json
{
  "count": 10,
  "next": "http://127.0.0.1:8000/api/posts/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Getting Started with Django",
      "slug": "getting-started-django",
      "author": 1,
      "author_name": "admin",
      "category": 1,
      "category_name": "Python",
      "content": "# Introduction\n\nDjango is...",
      "content_html": "<h1>Introduction</h1><p>Django is...</p>",
      "excerpt": "Learn Django basics",
      "status": "published",
      "created_at": "2026-02-01T10:00:00Z",
      "updated_at": "2026-02-01T12:00:00Z",
      "published_at": "2026-02-01T12:00:00Z"
    }
  ]
}
```

**Get Single Post**
```bash
GET /api/posts/{id}/
```

**Create Post** (Authentication required)
```bash
POST /api/posts/
Authorization: Token your_token_here
Content-Type: application/json

{
  "title": "New Post",
  "slug": "new-post",
  "category": 1,
  "content": "# Heading\n\nContent here...",
  "excerpt": "Short description",
  "status": "draft"
}
```

**Update Post** (Authentication required)
```bash
PUT /api/posts/{id}/
Authorization: Token your_token_here
Content-Type: application/json

{
  "title": "Updated Title",
  "status": "published",
  "published_at": "2026-02-01T12:00:00Z"
}
```

**Delete Post** (Authentication required)
```bash
DELETE /api/posts/{id}/
Authorization: Token your_token_here
```

### Tasks API (Authentication Required)

#### Tasks

**List Tasks**
```bash
GET /api/tasks/
Authorization: Token your_token_here
```

Query parameters:
- `status`: pending, in_progress, completed, cancelled
- `priority`: low, medium, high
- `task_type`: work, study, personal
- `due_date`: YYYY-MM-DD
- `search`: search in title, description

Response:
```json
{
  "count": 5,
  "results": [
    {
      "id": 1,
      "user": 1,
      "user_name": "admin",
      "title": "Complete Django tutorial",
      "description": "Finish all chapters",
      "task_type": "study",
      "priority": "high",
      "status": "in_progress",
      "due_date": "2026-02-10",
      "completed_at": null,
      "created_at": "2026-02-01T10:00:00Z",
      "updated_at": "2026-02-01T10:00:00Z"
    }
  ]
}
```

**Create Task**
```bash
POST /api/tasks/
Authorization: Token your_token_here
Content-Type: application/json

{
  "title": "Learn API development",
  "description": "Study Django REST Framework",
  "task_type": "study",
  "priority": "medium",
  "status": "pending",
  "due_date": "2026-02-15"
}
```

**Update Task**
```bash
PATCH /api/tasks/{id}/
Authorization: Token your_token_here
Content-Type: application/json

{
  "status": "completed",
  "completed_at": "2026-02-01T15:00:00Z"
}
```

#### Study Sessions

**List Study Sessions**
```bash
GET /api/study-sessions/
Authorization: Token your_token_here
```

**Create Study Session**
```bash
POST /api/study-sessions/
Authorization: Token your_token_here
Content-Type: application/json

{
  "subject": "Django REST Framework",
  "description": "Learned about serializers",
  "duration_minutes": 90,
  "date": "2026-02-01",
  "notes": "Serializers are very powerful"
}
```

### Knowledge API (Authentication Required)

#### Topics

**List Topics**
```bash
GET /api/topics/
Authorization: Token your_token_here
```

Response:
```json
{
  "results": [
    {
      "id": 1,
      "name": "Web Development",
      "slug": "web-development",
      "description": "Web dev resources",
      "parent": null,
      "parent_name": null,
      "subtopics_count": 3,
      "created_at": "2026-02-01T10:00:00Z"
    }
  ]
}
```

#### Knowledge Entries

**List Entries**
```bash
GET /api/knowledge-entries/
Authorization: Token your_token_here
```

Query parameters:
- `entry_type`: note, research, article, reference
- `topic`: topic ID
- `is_favorite`: true, false
- `search`: search in title, content, tags, summary

**Create Entry**
```bash
POST /api/knowledge-entries/
Authorization: Token your_token_here
Content-Type: application/json

{
  "title": "Python Decorators",
  "slug": "python-decorators",
  "topic": 1,
  "entry_type": "note",
  "content": "# Decorators\n\nDecorators are...",
  "summary": "Quick guide to Python decorators",
  "source_url": "https://docs.python.org/3/glossary.html#term-decorator",
  "tags": "python, decorators, advanced",
  "is_favorite": false
}
```

#### Resources

**List Resources**
```bash
GET /api/resources/
Authorization: Token your_token_here
```

Query parameters:
- `resource_type`: book, video, course, website, paper
- `status`: to_read, reading, completed
- `rating`: 1-5
- `topic`: topic ID

**Create Resource**
```bash
POST /api/resources/
Authorization: Token your_token_here
Content-Type: application/json

{
  "title": "Two Scoops of Django",
  "resource_type": "book",
  "topic": 1,
  "url": "https://www.feldroy.com/books/two-scoops-of-django-3-x",
  "author": "Daniel Roy Greenfeld",
  "status": "reading",
  "notes": "Great book on Django best practices",
  "rating": 5
}
```

## Pagination

API sử dụng pagination mặc định 10 items/page.

Query parameters:
- `page`: page number
- `page_size`: số lượng items (max 100)

Example:
```bash
GET /api/posts/?page=2&page_size=20
```

## Filtering & Searching

### Filtering
Sử dụng query parameters với tên field:
```bash
GET /api/tasks/?status=pending&priority=high
```

### Searching
Sử dụng `search` parameter:
```bash
GET /api/posts/?search=django
GET /api/knowledge-entries/?search=python
```

### Ordering
Sử dụng `ordering` parameter:
```bash
GET /api/posts/?ordering=-created_at
GET /api/tasks/?ordering=due_date,-priority
```

Thêm `-` trước field name để sắp xếp giảm dần.

## Error Handling

API trả về HTTP status codes:
- `200 OK`: Success
- `201 Created`: Resource created
- `204 No Content`: Resource deleted
- `400 Bad Request`: Invalid data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Permission denied
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

Error response format:
```json
{
  "detail": "Error message here"
}
```

hoặc cho validation errors:
```json
{
  "field_name": ["Error message for this field"]
}
```

## Rate Limiting

Hiện tại API chưa có rate limiting. Trong production nên thêm rate limiting để bảo vệ server.

## CORS

Nếu cần truy cập API từ domain khác, cần cấu hình CORS trong settings.py bằng package `django-cors-headers`.
