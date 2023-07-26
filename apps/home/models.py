# -*- encoding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User







class Ingredient(models.Model):
    #Table des ingredients

    nom_ing = models.CharField(primary_key=True, max_length=150)
    type_ing = models.CharField( max_length=150, null=True, blank=True)
    nature = models.CharField( max_length=150, null=True, blank=True)

    class Meta:
        db_table = 'ingredients'
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return self.nom_ing



class Parametre(models.Model):
    #Table des parametres a mesuree

    nom_parametre = models.CharField(primary_key=True, max_length=150)
    unite= models.CharField( max_length=150, null=True, blank=True)


    class Meta:
        db_table = 'Parametre'
        verbose_name = 'Parametre'
        verbose_name_plural = 'Parametre'

    def __str__(self):
        return self.nom_parametre



class Levain(models.Model):
    # Table des Levains

    TYPE = (
        ('F', 'Frais'),
        ('L', 'Liquide'),
        ('Lyo', 'Lyophilisé'),
        ('S', 'Séché'),
    )
    code_levain = models.CharField( primary_key=True, max_length=150, null=False)
    type_levain = models.CharField(max_length=3, choices=TYPE, null=False)
    date = models.DateField(auto_now=False, null=False)
    pH = models.DecimalField(default=0 ,max_digits=50, decimal_places=2)
    att = models.DecimalField(default=0 ,max_digits=50, decimal_places=2)

    class Meta:
        db_table = 'levain'
        verbose_name = 'Levain' 

    def __str__(self):
        return self.code_levain
    


class CompositionLevain(models.Model):
    # Table des ingredients des levains

    id = models.BigAutoField(primary_key=True)
    levain = models.ForeignKey(Levain, on_delete=models.PROTECT)
    nom_ing = models.CharField( max_length=150)
    masse_ing = models.DecimalField(max_digits=50, decimal_places=2)

    class Meta:
        db_table = 'Composition_Levain'
        verbose_name = 'CompositionLevain'
        verbose_name_plural = 'CompositionLevains'
        
    def __str__(self):
        return self.nom_ing
    


class TechniqueRafraichissement(models.Model):
    #Table des Techniques de Rafraichissement

    nom_tech = models.CharField(primary_key=True, max_length=150)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Technique_Rafraichissement'
        verbose_name = 'TechniqueRafraichissement'
        verbose_name_plural = 'TechniqueRafraichissements'

    def __str__(self):
        return self.nom_tech


    
class Rafraichissement(models.Model):
    # Table des rafraichissements des levains

    id = models.BigAutoField(primary_key=True)
    levain = models.ForeignKey(Levain, on_delete=models.PROTECT)
    technique = models.ForeignKey(TechniqueRafraichissement, on_delete=models.PROTECT)
    date_rafraichissement = models.DateField(auto_now=False)
    num_rafraichit = models.IntegerField()
    nom_ing = models.CharField( max_length=150)
    masse_ing = models.DecimalField(max_digits=50, decimal_places=2, default=0)
   
    class Meta:
        db_table = 'Rafraichissement'
        verbose_name = 'Rafraichissement'
        verbose_name_plural = 'Rafraichissements' 
    


class CaracterisationLevain(models.Model):
    # Table des caracteristiques des levains

    id = models.BigAutoField(primary_key=True)
    levain = models.ForeignKey(Levain, on_delete=models.PROTECT)
    date_caracterisation = models.DateField(auto_now=False)
    num_rep = models.IntegerField()
    nom_parametre = models.CharField( max_length=150)
    valeur = models.DecimalField(max_digits=50, decimal_places=2)

    class Meta:
        db_table = 'Caracterisation_Levain'
        verbose_name = 'CaracterisationLevain'
        verbose_name_plural = 'CaracterisationLevain' 



class TechniquePanification(models.Model):
    #Table des Technique de panification

    nom_tech = models.CharField(primary_key=True, max_length=150)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'Technique_Panification'
        verbose_name = 'TechniquePanification'
        verbose_name_plural = 'TechniquePanifications'

    def __str__(self):
        return self.nom_tech
    


class Panification(models.Model):
    # Table des tests de panification

    num_test = models.IntegerField(primary_key=True)
    technique = models.ForeignKey(TechniquePanification, on_delete=models.PROTECT)
    levain = models.ForeignKey(Levain, on_delete=models.PROTECT)
    date_panification = models.DateField(auto_now=False)
    num_repetition = models.IntegerField()
    apport = models.DecimalField(default=0 ,max_digits=50, decimal_places=1)
    temps_fin_panif = models.DecimalField(max_digits=50, decimal_places=3, null=True, blank=True)
    

    class Meta:
        db_table = 'test_panification'
        verbose_name = 'Panification'
        verbose_name_plural = 'Panifications' 



class CompositionPanification(models.Model):
    # Table des ingredients de panification

    id = models.BigAutoField(primary_key=True)
    panification = models.ForeignKey(Panification, on_delete=models.PROTECT)
    nom_ing = models.CharField( max_length=150)
    masse_ing = models.DecimalField(max_digits=50, decimal_places=2)

    class Meta:
        db_table = 'Composition_Panification'
        verbose_name = 'CompositionPanification'
        verbose_name_plural = 'CompositionPanifications'
        
    def __str__(self):
        return self.nom_ing




class CaracterPanification(models.Model):
    # Table des caracteristiques des tests de panification

    id = models.BigAutoField(primary_key=True)
    panification = models.ForeignKey(Panification, on_delete=models.PROTECT)
    nom_parametre = models.CharField( max_length=150,null=True,blank=True)
    valeur = models.DecimalField(max_digits=50, decimal_places=2,null=True,blank=True)
   

    class Meta:
        db_table = 'Caracter_Panification'
        verbose_name = 'Caracter_Panification'
        verbose_name_plural = 'Caracter_Panification' 




class CaracterisationPanification(models.Model):
    # Table des caracteristiques des tests de panification

    id = models.BigAutoField(primary_key=True)
    panification = models.ForeignKey(Panification, on_delete=models.PROTECT)
    heure_panification = models.TimeField(auto_now=False,null=True,blank=True)
    nom_parametre = models.CharField( max_length=150)
    valeur = models.DecimalField(max_digits=50, decimal_places=6, null=True, blank=True)

    class Meta:
        db_table = 'Caracterisation_Panification'
        verbose_name = 'CaracterisationPanification'
        verbose_name_plural = 'CaracterisationPanifications' 




    






