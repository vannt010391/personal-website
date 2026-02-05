from knowledge.models import KnowledgeEntry
from django.contrib.auth.models import User

u = User.objects.first()
if not u:
    print("No users found")
    exit()

entries = KnowledgeEntry.objects.filter(user=u)
print(f'Total entries: {entries.count()}')
print(f'Entries with parent: {entries.exclude(parent__isnull=True).count()}')

children = entries.exclude(parent__isnull=True)
if children.exists():
    print("\nEntries with parents:")
    for e in children[:10]:
        print(f'  - {e.title} (parent: {e.parent.title if e.parent else "None"})')
else:
    print("\nNo child entries found")

print("\nRoot entries:")
root_entries = entries.filter(parent__isnull=True)
for e in root_entries[:5]:
    child_count = e.children.count()
    print(f'  - {e.title} ({child_count} children)')
