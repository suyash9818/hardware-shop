from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
        ("catalog", "0001_initial"),
        ("pricing", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProcurementOrder",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantity", models.PositiveIntegerField()),
                ("unit_cost_usd", models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ("status", models.CharField(choices=[("PLANNED", "Planned"), ("ORDERED", "Ordered"), ("RECEIVED", "Received"), ("CANCELLED", "Cancelled")], default="PLANNED", max_length=20)),
                ("expected_delivery", models.DateField(blank=True, null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("order", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="procurements", to="orders.order")),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="catalog.product")),
                ("supplier", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to="pricing.supplier")),
            ],
        ),
    ]
