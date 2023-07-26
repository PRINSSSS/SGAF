# -*- encoding: utf-8 -*-

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *




class AdminIngredient(admin.ModelAdmin):
    list_display = ( 'nom_ing', 'type_ing', 'nature')

class AdminParametre(admin.ModelAdmin):
    list_display = ( 'nom_parametre', 'unite')

class AdminLevain(admin.ModelAdmin):
    list_display = ('code_levain', 'type_levain', 'date', 'pH', 'att')

class AdminCompositionLevain(admin.ModelAdmin):
    list_display = ( 'levain', 'nom_ing', 'masse_ing')

class AdminTechniqueRafraichissement(admin.ModelAdmin):
    list_display = ( 'nom_tech','description')

class AdminRafraichissement(admin.ModelAdmin):
    list_display = ( 'levain','technique', 'date_rafraichissement','num_rafraichit')

class AdminCaracterisationLevain(admin.ModelAdmin):
    list_display = ( 'levain','date_caracterisation', 'num_rep','nom_parametre','valeur')

class AdminTechniquePanification(admin.ModelAdmin):
    list_display = ( 'nom_tech','description')

class AdminPanification(admin.ModelAdmin):
    list_display = ( 'num_test','technique','levain', 'date_panification', 'num_repetition','apport')

class AdminCompositionPanification(admin.ModelAdmin):
    list_display = ( 'panification', 'nom_ing', 'masse_ing')

class AdminCaracterisationPanification(ImportExportModelAdmin):
    list_display = ( 'panification', 'heure_panification', 'nom_parametre', 'valeur')




admin.site.register(Ingredient, AdminIngredient)
admin.site.register(Parametre, AdminParametre)
admin.site.register(Levain, AdminLevain)
admin.site.register(CompositionLevain, AdminCompositionLevain)
admin.site.register(TechniqueRafraichissement, AdminTechniqueRafraichissement)
admin.site.register(Rafraichissement, AdminRafraichissement)
admin.site.register(CaracterisationLevain, AdminCaracterisationLevain)
admin.site.register(TechniquePanification, AdminTechniquePanification)
admin.site.register(Panification, AdminPanification)
admin.site.register(CompositionPanification, AdminCompositionPanification) 
admin.site.register(CaracterisationPanification, AdminCaracterisationPanification) 

