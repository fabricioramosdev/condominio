# Generated by Django 4.1 on 2022-10-30 03:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('condominio', '0006_alter_visitante_cracha_veiculo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='visitante',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
        migrations.CreateModel(
            name='BoletimOcorrencia',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('obs', models.TextField(blank=True, null=True, verbose_name='Observações')),
                ('criado', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
                ('fk_apartamento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='condominio.apartamento')),
                ('fk_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Boletim Ocorrência',
                'verbose_name_plural': 'Boletim Ocorrências',
                'db_table': 'boletim_ocorrencias',
                'ordering': ['fk_apartamento', 'criado'],
            },
        ),
    ]
