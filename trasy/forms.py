from django import forms
from .models import PointList
#klasy które definiują form's, nasz form bedzie mial podane atrybuty

class FormPoint(forms.Form):
    x_value = forms.IntegerField(label="X-cord")
    y_value = forms.IntegerField(label="Y-cord")
    check = forms.BooleanField(required=False)

class FormList(forms.ModelForm):
    class Meta:
        model = PointList
        fields = ['name', 'backgroundImage']