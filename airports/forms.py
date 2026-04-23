from django import forms
from .models import AirportNode

class AddNodeForm(forms.ModelForm):
    name= forms.CharField()
    parent= forms.ModelChoiceField(queryset=AirportNode.objects.all(), required=False)
    side= forms.ChoiceField(choices=[('left', 'Left'), ('right', 'Right'), ('none', 'None')], required=False)
    distance= forms.IntegerField(min_value=0, required=False)

    class Meta:
        model = AirportNode
        fields = ['name', 'parent', 'side', 'distance']

class SingleNodeForm(forms.Form):
    name= forms.CharField()

class TwoNodeForm(forms.Form):
   source= forms.ModelChoiceField(queryset=AirportNode.objects.all())
   destination= forms.ModelChoiceField(queryset=AirportNode.objects.all())