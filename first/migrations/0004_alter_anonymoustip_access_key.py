# Generated by Django 5.2.3 on 2025-06-30 17:00

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first', '0003_anonymoustip_access_key'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anonymoustip',
            name='access_key',
            field=models.UUIDField(blank=True, default=uuid.uuid4, editable=False, null=True),
        ),
    ]
