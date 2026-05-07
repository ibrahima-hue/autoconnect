from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0006_carimage_is_primary'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='cancellation_reason',
            field=models.TextField(blank=True),
        ),
    ]
