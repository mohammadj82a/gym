from django import forms
from jdatetime import datetime as jdatetime
from django.utils import timezone
from .models import gymodel


class GymodelForm(forms.ModelForm):
    class Meta:
        model = gymodel
        fields = ['name', 'age', 'height', 'weight', 'phone', 'start_date', 'end_date','renewal']
        widgets = {
            'renewal': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class GymodelSearchForm(forms.ModelForm):
    class Meta:
        model = gymodel
        fields = ['name', 'phone']
        



