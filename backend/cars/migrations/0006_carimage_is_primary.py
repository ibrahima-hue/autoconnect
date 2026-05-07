from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0005_add_premium_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='carimage',
            name='is_primary',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterModelOptions(
            name='carimage',
            options={'ordering': ['-is_primary', 'order', 'created_at']},
        ),
    ]
