import csv

from django.contrib import admin
from datetime import datetime

from django.http import HttpResponse

from .models import (Condomino, Predio, Apartamento, Morador, Veiculo, Visitante, BoletimOcorrencia)


admin.site.register(Condomino)
admin.site.register(Predio)


@admin.register(Apartamento)
class ApartamentoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'fk_condomino_proprietario',)
    list_filter = ('fk_predio',)
    ordering = ('num', 'fk_predio',)


@admin.register(Morador)
class MoradorAdmin(admin.ModelAdmin):

    def get_celular(self, obj):
        return obj.fk_condomino_morador.tel_celular

    def get_proprietario(self, obj):
        return obj.fk_condomino_morador.proprietario

    list_display = ('__str__', 'get_celular', 'get_proprietario', 'status')
    list_filter = ('fk_apartamento', 'status')
    actions = ['saida_morador', 'export_as_csv', ]

    @admin.action(permissions=['change'])
    def saida_morador(self, request, queryset):
        queryset.update(data_saida=datetime.now(), status=False)

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
        return response



@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'fk_apartamento', 'fk_condomino_morador')
    list_filter = ('fk_apartamento',)
    ordering = ('fk_apartamento', 'marca',)


@admin.register(Visitante)
class VisitanteAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'nome', 'data_entrada', 'data_saida', 'status')
    list_filter = ('fk_apartamento',)
    ordering = ('fk_apartamento', 'data_entrada', 'status')
    list_editable = ('status', 'data_saida',)
    actions = ['saida_visitante', 'export_as_csv']
    date_hierarchy = 'data_entrada'

    @admin.action(permissions=['change'])
    def saida_visitante(self, request, queryset):
        queryset.update(data_saida=datetime.now(), status=False, cracha_veiculo=True)

    def export_as_csv(self, request, queryset):
        meta = self.model._meta
        field_names = [field.name for field in meta.fields]
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
        return response


admin.site.register(BoletimOcorrencia)
