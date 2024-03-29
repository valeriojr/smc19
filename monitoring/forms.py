from datetime import datetime

import bitfield
from bitfield.forms import BitFieldCheckboxSelectMultiple
from django import forms
from django.forms import inlineformset_factory
from django.utils import timezone
from django.utils.timezone import now

from monitoring import choices
from smc19 import settings
from . import models


class MonitoringForm(forms.ModelForm):
    class Meta:
        model = models.Monitoring
        fields = '__all__'
        labels = {
            'profile': 'Paciente'
        }


class SymptomCreateForm(forms.ModelForm):
    class Meta:
        model = models.Symptom
        exclude = ['intensity']
        widgets = {
            'symptom': forms.HiddenInput(),
            'label': forms.HiddenInput(),
            'onset': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'}),
            'intensity': forms.HiddenInput()
        }

    label = forms.CharField(widget=forms.HiddenInput(), required=False, empty_value='')


SymptomInlineFormset = inlineformset_factory(models.Monitoring, model=models.Symptom, form=SymptomCreateForm,
                                             extra=len(choices.symptoms), can_delete=False)


class TripForm(forms.ModelForm):
    class Meta:
        model = models.Trip
        fields = '__all__'
        widgets = {
            'profile': forms.HiddenInput(),
            'departure_date': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
            'return_date': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
            'country': forms.RadioSelect()
        }

    def clean(self):
        cleaned_data = super(TripForm, self).clean()

        departure_date = cleaned_data['departure_date']
        return_date = cleaned_data['return_date']

        if departure_date is not None and return_date is not None and departure_date > return_date:
            self.add_error('departure_date', 'A data da ida não pode ser depois da volta')

        return cleaned_data


TripInlineFormset = inlineformset_factory(models.Profile, models.Trip, form=TripForm, extra=1)


class ProfileCreationForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        exclude = ['account']
        widgets = {
            'birth_date': forms.DateInput(format='%d/%m/%Y', attrs={'type': 'date'}),
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = models.Address
        fields = '__all__'
        widgets = {
            'postal_code': forms.TextInput(attrs={'class': 'postal-code-field'}),
            'complement': forms.Textarea(attrs={'rows': 2}),
            'profile': forms.HiddenInput()
        }
        labels = {
            'people': 'Número de pessoas residindo nesse endereço'
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = '__all__'
        widgets = {
            'birth_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})
        }
