# Generated by Django 4.1 on 2022-10-30 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('condominio', '0005_alter_morador_options_visitante_cracha_veiculo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitante',
            name='cracha_veiculo',
            field=models.BooleanField(default=False, verbose_name='Devolução crachá veículo?'),
        ),
    ]
