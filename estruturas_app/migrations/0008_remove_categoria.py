# Generated manually  
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('estruturas_app', '0007_add_url_documentos'),
    ]

    operations = [
        migrations.RunSQL(
            "DROP INDEX IF EXISTS estruturas__categor_02fd1e_idx;",
            reverse_sql="CREATE INDEX estruturas__categor_02fd1e_idx ON estruturas_app_product (categoria);"
        ),
        migrations.RemoveField(
            model_name='product',
            name='categoria',
        ),
    ]
