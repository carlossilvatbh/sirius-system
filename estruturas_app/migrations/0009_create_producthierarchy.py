# Generated manually
from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('estruturas_app', '0008_remove_categoria'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductHierarchy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ownership_percentage', models.DecimalField(blank=True, decimal_places=2, help_text='Percentage of ownership (optional)', max_digits=5, null=True, validators=[django.core.validators.MinValueValidator(0.01), django.core.validators.MaxValueValidator(100.0)])),
                ('hierarchy_level', models.PositiveIntegerField(default=1, help_text='Level in hierarchy (1 = top level, 2 = second level, etc.)')),
                ('notes', models.TextField(blank=True, help_text='Additional notes about this hierarchy relationship')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('parent_structure', models.ForeignKey(blank=True, help_text='Parent structure (if this structure is owned by another)', null=True, on_delete=models.deletion.CASCADE, related_name='child_structures', to='estruturas_app.estrutura')),
                ('product', models.ForeignKey(help_text='Product to which this hierarchy belongs', on_delete=models.deletion.CASCADE, to='estruturas_app.product')),
                ('structure', models.ForeignKey(help_text='Legal Structure in this hierarchy', on_delete=models.deletion.CASCADE, to='estruturas_app.estrutura')),
            ],
            options={
                'verbose_name': 'Product Hierarchy',
                'verbose_name_plural': 'Product Hierarchies',
                'indexes': [
                    models.Index(fields=['product', 'hierarchy_level'], name='estruturas__product_1d16d5_idx'),
                    models.Index(fields=['structure'], name='estruturas__structu_235bfc_idx'),
                    models.Index(fields=['parent_structure'], name='estruturas__parent__d76478_idx'),
                ],
            },
        ),
        migrations.AlterUniqueTogether(
            name='producthierarchy',
            unique_together={('product', 'structure')},
        ),
    ]
