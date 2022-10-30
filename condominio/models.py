import uuid

from django.db.models import CharField
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


class Condomino(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    nome = models.CharField(_('Nome'), max_length=255, null=False, blank=False)

    cpf = models.CharField(_('CPF'), max_length=15, null=True, blank=True, unique=True,
                           help_text='Registro caracteres especiais.')
    rg = models.CharField(_('RG'), max_length=15, null=True, blank=True,
                          help_text='Registro caracteres especiais.')
    orgao_emissor = models.CharField(_('Orgão emissor'), max_length=15, null=True, blank=True,
                                     help_text='Registro caracteres especiais.')
    sexo = models.CharField(_('Sexo'), max_length=5, choices=(('M', 'Masculino'), ('F', 'Feminino')),
                            null=False, blank=False)
    profissao: CharField = models.CharField(_('Profissão'), max_length=255, null=True, blank=True)

    tel_residencia = models.CharField(_('Tel. Residência'), max_length=15, null=True, blank=True)
    tel_celular = models.CharField(_('Tel. Celular'), max_length=15, null=True, blank=True, help_text='xx-xxxx-xxxx')
    email = models.CharField(_('E-mail'), max_length=255, null=True, blank=True)

    proprietario = models.BooleanField(_('Proprietário'), default=False, null=False, blank=False)
    morador = models.BooleanField(_('Morador'), default=False, null=False, blank=False)
    dependente = models.BooleanField(_('Dependente'), default=False, null=False, blank=False)

    obs = models.TextField(_('Observações'), blank=True, null=True)

    criado = models.DateTimeField(_('Criado em'), auto_now_add=True)
    status = models.BooleanField(_('Status'), default=True, null=False, blank=False)

    class Meta:
        db_table = 'condomino'
        verbose_name = 'Condômino'
        verbose_name_plural = 'Condôminos'
        ordering = ['nome', ]

    def __str__(self):
        return f'{self.nome}'


class Predio(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    num = models.IntegerField(_('N° Prédio'), unique=True, blank=False, null=False, )
    sub_sindico = models.ForeignKey(Condomino, on_delete=models.PROTECT,
                                    limit_choices_to={'status': True}, blank=True, null=True)
    obs = models.TextField(_('Observações'), blank=True, null=True)
    criado = models.DateTimeField(_('Criado em'), auto_now_add=True)
    status = models.BooleanField(_('Status'), default=True, null=False, blank=False)

    class Meta:
        db_table = 'predios'
        verbose_name = 'Prédio'
        verbose_name_plural = 'Prédios'
        ordering = ['num', ]

    def __str__(self):
        return f'Bloco {"%02d"%self.num}'


class Apartamento(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    num = models.IntegerField(_('N° Apartamento'), blank=False, null=False)
    fk_predio = models.ForeignKey(Predio, on_delete=models.PROTECT,
                                  limit_choices_to={'status': True})
    fk_condomino_proprietario = models.ForeignKey(Condomino, on_delete=models.PROTECT, blank=True, null=True,
                                                  limit_choices_to={'proprietario': True})
    obs = models.TextField(_('Observações'), blank=True, null=True)
    criado = models.DateTimeField(_('Criado em'), auto_now_add=True)
    status = models.BooleanField(_('Status'), default=True, null=False, blank=False)

    class Meta:
        db_table = 'apartamentos'
        verbose_name = 'Aparamento'
        verbose_name_plural = 'Apartamentos'
        ordering = ['fk_predio', 'num']
        unique_together = (('num', 'fk_predio'),)

    def __str__(self):
        return f'{self.fk_predio}-{self.num}'

    def get_full_name(self):
        full_name = '%s, %s - %s' % (self.num, self.fk_predio, self.proprietario)
        return full_name.strip()


class Morador(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    fk_apartamento = models.ForeignKey(Apartamento, on_delete=models.PROTECT, blank=True, null=True,
                                       limit_choices_to={'status': True})
    fk_condomino_morador = models.ForeignKey(Condomino, on_delete=models.PROTECT, blank=True, null=True,
                                             limit_choices_to={'morador': True}, related_name='apartamento_morador')
    data_entrada = models.DateField(_('Data entrada'), default=timezone.now, blank=False, null=False)
    data_saida = models.DateField(_('Data saída'), blank=True, null=True)

    responsavel = models.BooleanField(_('Responsável'), default=False, null=False, blank=False)

    obs = models.TextField(_('Observações'), blank=True, null=True)
    criado = models.DateTimeField(_('Criado em'), auto_now_add=True)
    status = models.BooleanField(_('Status'), default=True, null=False, blank=False)

    class Meta:
        db_table = 'morador'
        verbose_name = 'Morador'
        verbose_name_plural = 'Moradores'
        ordering = ['fk_apartamento', 'fk_condomino_morador__nome']

    def __str__(self):
        return f'{self.fk_apartamento} - {self.fk_condomino_morador}'


class Veiculo(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    fk_apartamento = models.ForeignKey(Apartamento, on_delete=models.PROTECT, limit_choices_to={'status': True})
    fk_condomino_morador = models.ForeignKey(Condomino, on_delete=models.PROTECT, blank=True, null=True)
    marca = models.CharField(_('Marca'), max_length=255, blank=False, null=False)
    modelo = models.CharField(_('Modelo'), max_length=255, blank=False, null=False)
    cor = models.CharField(_('Cor'), max_length=45, blank=False, null=False)
    placa = models.CharField(_('Placa'), max_length=15, blank=False, null=False, unique=True, help_text='Registro caracteres especiais.')

    obs = models.TextField(_('Observações'), blank=True, null=True)
    criado = models.DateTimeField(_('Criado em'), auto_now_add=True)
    status = models.BooleanField(_('Status'), default=True, null=False, blank=False)

    class Meta:
        db_table = 'veiculos'
        verbose_name = 'Veiculo'
        verbose_name_plural = 'Veículos'

    def __str__(self):
        return f'{self.placa}'


class Visitante(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    fk_apartamento = models.ForeignKey(Apartamento, on_delete=models.PROTECT)
    placa_veiculo = models.CharField(_('Placa veículo'), max_length=15, blank=False, null=False)

    nome = models.CharField(_('Nome'), max_length=255, blank=False, null=False)
    rg = models.CharField(_('RG'), max_length=15, blank=False, null=False)

    data_entrada = models.DateTimeField(_('Data/Hora entrada'), auto_now_add=True)
    cracha_veiculo = models.BooleanField(_('Devolução crachá veículo?'), default=False, null=False, blank=False)

    data_saida = models.DateTimeField(_('Data/Hora saída'), auto_now=False, blank=True, null=True)

    obs = models.TextField(_('Observações'), blank=True, null=True)
    status = models.BooleanField(_('Status'), default=True, null=False, blank=False)

    class Meta:
        db_table = 'visitante'
        verbose_name = 'Visitante'
        verbose_name_plural = 'Visitantes'
        ordering = ['fk_apartamento', 'data_entrada', ]

    def __str__(self):
        return f'{self.fk_apartamento}'



class BoletimOcorrencia(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    fk_apartamento = models.ForeignKey(Apartamento, on_delete=models.PROTECT)
    fk_user =  models.ForeignKey(User, on_delete=models.PROTECT)
    obs = models.TextField(_('Observações'), blank=True, null=True)
    criado = models.DateTimeField(_('Criado em'), auto_now_add=True)
    status = models.BooleanField(_('Status'), default=True, null=False, blank=False)

    class Meta:
        db_table = 'boletim_ocorrencias'
        verbose_name = 'Boletim Ocorrência'
        verbose_name_plural = 'Boletim Ocorrências'
        ordering = ['fk_apartamento', 'criado', ]

    def __str__(self):
        return f'{self.fk_apartamento}'


