from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('buses', '0003_initial_data'),
    ]

    operations = [
        migrations.AddField(
            model_name='bus',
            name='driver_contact',
            field=models.CharField(blank=True, default='', max_length=15),
        ),
    ]