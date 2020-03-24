# Generated by Django 3.0.4 on 2020-03-24 22:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Atendimento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True, verbose_name='Data')),
                ('confirmed', models.BooleanField(default=False, verbose_name='Confirmado')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('departure_date', models.DateField(blank=True, default=None, null=True, verbose_name='Ida')),
                ('return_date', models.DateField(blank=True, default=None, null=True, verbose_name='Volta')),
                ('country', models.CharField(blank=True, choices=[('CHN', 'China'), ('BRA', 'Brasil'), ('ESP', 'Espanha'), ('USA', 'Estados Unidos'), ('ITA', 'Itália')], default='', max_length=3, verbose_name='País')),
                ('atendimento', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='monitoring.Atendimento')),
            ],
        ),
        migrations.CreateModel(
            name='Symptom',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('symptom', models.CharField(choices=[('TR', 'Cansaço'), ('DI', 'Diarreia'), ('SB', 'Dificuldade respiratória'), ('ST', 'Dor de garganta'), ('AP', 'Dores no corpo'), ('FV', 'Febre'), ('DC', 'Tosse'), ('RN', 'Nariz escorrendo'), ('DI', 'Náusea'), ('OT', 'Outro')], default='', max_length=2, verbose_name='Tipo de sintoma')),
                ('intensity', models.CharField(choices=[('L', 'Leve'), ('M', 'Moderada'), ('H', 'Grave')], default='', max_length=1, verbose_name='Intensidade')),
                ('onset', models.DateField(blank=True, null=True, verbose_name='Data do surgimento')),
                ('atendimento', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='monitoring.Atendimento')),
            ],
        ),
        migrations.CreateModel(
            name='Comorbidity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(blank=True, choices=[('H', 'Doença cardíacas'), ('T', 'Hipertensão'), ('D', 'Diabetes'), ('E', 'Demência'), ('C', 'Bronquite crônica'), ('N', 'Câncer'), ('L', 'Doença crônica no fígado'), ('R', 'Doença renal crônica'), ('A', 'Asma'), ('P', 'Doença pulmonar crônica'), ('R', 'Doenças reumáticas'), ('O', 'Outra')], max_length=1, verbose_name='Tipo')),
                ('atendimento', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='monitoring.Atendimento')),
            ],
        ),
    ]
