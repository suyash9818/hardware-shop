from django import forms

from .models import RMA


class RMAForm(forms.ModelForm):
    class Meta:
        model = RMA
        fields = ["order", "product", "serial_unit", "customer_email", "reason"]
        widgets = {"reason": forms.Textarea(attrs={"rows": 4})}
