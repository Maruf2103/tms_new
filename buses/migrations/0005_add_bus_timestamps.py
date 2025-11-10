from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('buses', '0004_merge_20251110_2336'),
    ]

    operations = [
        migrations.AddField(
            model_name='bus',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='bus',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
