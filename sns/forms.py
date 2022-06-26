from django import forms

from .models import Park

class ParkForm(forms.ModelForm):

    class Meta:
        model   = Park
        fields  = ["category","name","tag","lat","lon"]

class CategorySearchForm(forms.ModelForm):
    class Meta:
        model   = Park
        fields  = ["category"]

class TagSearchForm(forms.ModelForm):

    class Meta:
        model   = Park
        fields  = ["tag"]


