from bitfield import BitField
from django.core.validators import MinValueValidator
from django.db import models
from django.urls import reverse

import validators
from . import choices


# Create your models here.

class Profile(models.Model):
    full_name = models.CharField(verbose_name='Nome completo', max_length=100, blank=True, default='')
    mother_name = models.CharField(verbose_name='Nome da mãe', max_length=100, blank=True, default='')
    birth_date = models.DateField(verbose_name='Data de nascimento', blank=True, default='',
                                  validators=[validators.prevent_future_date])
    cns = models.CharField(verbose_name='Cartão do SUS', max_length=15, blank=True, default='000000000000000')
    id_document = models.CharField(verbose_name='RG', max_length=15, blank=True, default='000000000')
    cpf = models.CharField(verbose_name='CPF', max_length=11, blank=True, default='00000000000',
                           validators=[validators.validate_cpf])
    phone_number = models.CharField(verbose_name='Número de telefone', max_length=11, blank=True, default='')
    gender = models.CharField(verbose_name='Sexo biológico', max_length=1, choices=choices.genders, blank=True,
                              default='')
    age = models.PositiveIntegerField(verbose_name='Idade', blank=True)
    weight = models.FloatField(verbose_name='Peso', blank=True, default=0,
                               validators=[MinValueValidator(0)])
    height = models.FloatField(verbose_name='Altura', blank=True, default=0, validators=[MinValueValidator(0)])

    smoker = models.BooleanField(verbose_name='Fumante', blank=True, default=False)
    vaccinated = models.BooleanField(verbose_name='Tomou vacina da gripe em 2020', blank=True, default=False)
    oxygen = models.BooleanField(verbose_name='Precisou de oxigênio recentemente', blank=True, default=False)

    comorbidities = BitField(verbose_name='Comorbidades', flags=choices.comorbidities, default=0)

    def __str__(self):
        return self.full_name


class Address(models.Model):
    profile = models.ForeignKey(Profile, models.CASCADE)
    type = models.CharField(verbose_name='Tipo', max_length=2, choices=choices.address_types, blank=True, default='')
    postal_code = models.CharField(verbose_name='CEP', max_length=8, blank=True, default='')
    neighbourhood = models.CharField(verbose_name='Bairro', max_length=100, blank=True, default='')
    street_name = models.CharField(verbose_name='Logradouro', max_length=100, blank=True, default='')
    number = models.PositiveIntegerField(verbose_name='Número', blank=True, null=True, default=0)
    complement = models.CharField(verbose_name='Complemento', max_length=100, blank=True, default='')
    city = models.CharField(verbose_name='Cidade', max_length=100, blank=True, default='')
    people = models.PositiveIntegerField(verbose_name='Quantidade de pessoas', blank=True, null=True, default=1)

    def __str__(self):
        return '%s, %s - %s, %s, %s' % (
        self.street_name, str(self.number or 'S/N'), self.neighbourhood, self.city, self.postal_code)


class Monitoring(models.Model):
    profile = models.ForeignKey(Profile, models.CASCADE)
    tested = models.BooleanField(verbose_name='Já foi testado', blank=True, default=False)
    date = models.DateField(verbose_name='Data', auto_now_add=True)
    suspect = models.BooleanField(verbose_name='Suspeito de COVID-19', default=False)
    virus_exposure = BitField(verbose_name='Exposição COVID-19', flags=choices.exposure, blank=True, default=0)
    result = models.CharField(verbose_name='Resultado do exame', max_length=2, choices=choices.results, default='SR')
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('monitoring:monitoring-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '%s (%s)' % (self.profile, self.date.strftime('%d/%m/%Y'))


class Symptom(models.Model):
    monitoring = models.ForeignKey(Monitoring, models.CASCADE, default=1)
    symptom = models.CharField(verbose_name='Tipo de sintoma', max_length=2, choices=choices.symptoms, default='')
    intensity = models.CharField(verbose_name='Intensidade', max_length=1, choices=choices.intensities, blank=True,
                                 default='L')
    onset = models.DateField(verbose_name='Data do surgimento', blank=True, null=True,
                             validators=[validators.prevent_future_date])

    def __str__(self):
        return '%s %s desde %s' % (self.get_symptom_display(), self.get_intensity_display(),
                                   self.onset.strftime('%d/%m/%Y'))


class Trip(models.Model):
    profile = models.ForeignKey(Profile, models.CASCADE, default=1)
    departure_date = models.DateField(verbose_name='Ida', null=True, blank=True, default=None,
                                      validators=[validators.prevent_future_date])
    return_date = models.DateField(verbose_name='Volta', null=True, blank=True, default=None,
                                   validators=[validators.prevent_future_date])
    country = models.CharField(verbose_name='País', max_length=3, choices=choices.countries, default='')

    def __str__(self):
        return '%s - %s a %s' % (self.get_country_display(), self.departure_date.strftime('%d/%m/%Y'),
                                 self.return_date.strftime('%d/%m/%Y'))
