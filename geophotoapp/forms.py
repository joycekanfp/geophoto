from django import forms
from django.core.exceptions import ValidationError

class SearchForm(forms.Form):
    latitude=forms.FloatField(label='Latitude')
    longitude=forms.FloatField(label='Longitude')
    
    def clean_latitude(self):
        data = self.cleaned_data['latitude']
        if data > 90 or data < -90:
            raise ValidationError("Latitude range should be between -90 and 90")

        return data

    def clean_longitude(self):
        data = self.cleaned_data['longitude']

        if data > 180 or data < -180:
            raise ValidationError("Longitude range should be between -180 and 180")

        return data


class PresetForm(forms.Form):
    name=forms.CharField(label='Name')
    latitude=forms.FloatField(label='Latitude')
    longitude=forms.FloatField(label='Longitude')
    
    def clean_latitude(self):
        data = self.cleaned_data['latitude']
        if data > 90 or data < -90:
            raise ValidationError("Latitude range should be between -90 and 90")

        return data

    def clean_longitude(self):
        data = self.cleaned_data['longitude']

        if data > 180 or data < -180:
            raise ValidationError("Longitude range should be between -180 and 180")

        return data