# Generated by Django 4.1 on 2022-10-30 02:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('condominio', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apartamento',
            name='obs',
            field=models.TextField(blank=True, null=True, verbose_name='Observações'),
        ),
        migrations.AlterField(
            model_name='morador',
            name='obs',
            field=models.TextField(blank=True, null=True, verbose_name='Observações'),
        ),
        migrations.AlterField(
            model_name='predio',
            name='obs',
            field=models.TextField(blank=True, null=True, verbose_name='Observações'),
        ),
        migrations.AlterField(
            model_name='predio',
            name='sub_sindico',
            field=models.ForeignKey(blank=True, limit_choices_to={'status': True}, null=True, on_delete=django.db.models.deletion.PROTECT, to='condominio.condomino'),
        ),
        migrations.AlterField(
            model_name='veiculo',
            name='obs',
            field=models.TextField(blank=True, null=True, verbose_name='Observações'),
        ),
        migrations.AlterField(
            model_name='visitante',
            name='obs',
            field=models.TextField(blank=True, null=True, verbose_name='Observações'),
        ),
    ]
