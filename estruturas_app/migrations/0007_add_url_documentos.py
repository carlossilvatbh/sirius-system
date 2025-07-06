# Generated manually
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('estruturas_app', '0006_service_serviceactivity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='estrutura',
            name='url_documentos',
            field=models.URLField(blank=True, help_text='URL for structure documents and templates'),
        ),
    ]
