from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from knowledge.models import Topic, KnowledgeEntry, Resource


SAMPLE_ENTRIES = [
    {
        "title": "Hệ thống ghi chú kiểu GitBook",
        "entry_type": "note",
        "summary": "Cách tổ chức ghi chú với sidebar, mục lục và phân cấp nội dung.",
        "tags": "gitbook,notes,organization",
        "is_favorite": True,
        "content": """# Tổng quan\n\nGitBook phù hợp cho tài liệu dài nhờ cấu trúc rõ ràng và dễ điều hướng.\n\n## Vì sao hiệu quả\n- Có **sidebar** theo chủ đề\n- Có **mục lục** tự động\n- Nội dung đọc dễ hơn\n\n## Mẫu nội dung\n\n```python\ndef build_sidebar(topics):\n    return [t.name for t in topics]\n```\n\n> Mẹo: dùng heading hợp lý để tạo mục lục đẹp.\n\n### Checklist\n- [x] Chủ đề rõ ràng\n- [x] Tóm tắt đầu bài\n- [ ] Ví dụ thực tế\n""",
    },
    {
        "title": "Markdown chuẩn cho ghi chú",
        "entry_type": "reference",
        "summary": "Chuẩn hóa cách viết markdown để nội dung đồng nhất.",
        "tags": "markdown,formatting,reference",
        "content": """# Quy ước Markdown\n\n## Heading\n- H1: tiêu đề\n- H2: mục lớn\n- H3: mục nhỏ\n\n## List\n1. Danh sách có thứ tự\n2. Dùng cho quy trình\n\n## Code\n\n```bash\npython manage.py runserver\n```\n\n## Bảng\n\n| Mục | Ý nghĩa |\n|---|---|\n| H1 | Title |\n| H2 | Section |\n""",
    },
    {
        "title": "Ghi chú học tập hiệu quả",
        "entry_type": "article",
        "summary": "Nguyên tắc ghi chú giúp nhớ lâu và dễ tra cứu.",
        "tags": "learning,notes,method",
        "content": """# Nguyên tắc\n\n## 1. Tóm tắt trước\nViết 2–3 dòng tóm tắt ở đầu để dễ scan.\n\n## 2. Từ khóa chính\nDùng tag và heading để phân loại.\n\n## 3. Ví dụ nhỏ\nMỗi ý nên có 1 ví dụ thực tế.\n""",
    },
]

SAMPLE_RESOURCES = [
    {
        "title": "Atomic Habits",
        "resource_type": "book",
        "author": "James Clear",
        "status": "reading",
        "rating": 5,
        "notes": "Tập trung vào thói quen nhỏ tích lũy." 
    },
    {
        "title": "Deep Work",
        "resource_type": "book",
        "author": "Cal Newport",
        "status": "to_read",
        "rating": 4,
        "notes": "Giảm phân tán, tăng tập trung." 
    },
    {
        "title": "Learning How to Learn",
        "resource_type": "course",
        "author": "Coursera",
        "status": "completed",
        "rating": 5,
        "notes": "Pomodoro, spaced repetition." 
    },
]


class Command(BaseCommand):
    help = "Seed sample knowledge data for a user"

    def add_arguments(self, parser):
        parser.add_argument(
            "--username",
            type=str,
            help="Username to attach sample data to (default: first superuser or first user)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing topics/entries/resources for that user before seeding",
        )

    def handle(self, *args, **options):
        username = options.get("username")
        clear = options.get("clear")
        User = get_user_model()

        user = None
        if username:
            user = User.objects.filter(username=username).first()
        if not user:
            user = User.objects.filter(is_superuser=True).first() or User.objects.first()

        if not user:
            self.stdout.write(self.style.ERROR("No users found. Create a user first."))
            return

        if clear:
            KnowledgeEntry.objects.filter(user=user).delete()
            Resource.objects.filter(user=user).delete()

        topics = [
            {"name": "Ghi chú", "description": "Ghi chú học tập và ý tưởng"},
            {"name": "Nghiên cứu", "description": "Tóm tắt tài liệu và nghiên cứu"},
            {"name": "Phương pháp", "description": "Cách học và quy trình"},
        ]

        topic_objs = {}
        for t in topics:
            slug = slugify(t["name"], allow_unicode=True)
            topic, _ = Topic.objects.get_or_create(
                slug=slug,
                defaults={"name": t["name"], "description": t["description"]},
            )
            topic_objs[t["name"]] = topic

        entry_topics = ["Ghi chú", "Nghiên cứu", "Phương pháp"]
        for index, (entry, topic_name) in enumerate(zip(SAMPLE_ENTRIES, entry_topics), start=1):
            slug = slugify(entry["title"], allow_unicode=True)
            KnowledgeEntry.objects.get_or_create(
                slug=slug,
                defaults={
                    "user": user,
                    "title": entry["title"],
                    "topic": topic_objs.get(topic_name),
                    "order": index,
                    "entry_type": entry["entry_type"],
                    "content": entry["content"],
                    "summary": entry["summary"],
                    "tags": entry["tags"],
                    "is_favorite": entry.get("is_favorite", False),
                },
            )

        for res in SAMPLE_RESOURCES:
            Resource.objects.get_or_create(
                user=user,
                title=res["title"],
                defaults={
                    "resource_type": res["resource_type"],
                    "topic": topic_objs.get("Ghi chú"),
                    "author": res.get("author", ""),
                    "status": res.get("status", "to_read"),
                    "rating": res.get("rating"),
                    "notes": res.get("notes", ""),
                },
            )

        self.stdout.write(self.style.SUCCESS(f"Seeded sample knowledge data for user: {user.username}"))
