from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('knowledge', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='knowledgeentry',
            name='parent',
            field=models.ForeignKey(
                blank=True,
                help_text='Parent page for hierarchical structure',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='children',
                to='knowledge.knowledgeentry',
            ),
        ),
        migrations.AddField(
            model_name='knowledgeentry',
            name='order',
            field=models.IntegerField(default=0, help_text='Ordering within a topic or parent page'),
        ),
    ]
