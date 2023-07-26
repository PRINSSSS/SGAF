# -*- encoding: utf-8 -*-
import os
import io
from django.http import FileResponse
from django.http import FileResponse, HttpResponse
from django.conf import settings
import pandas as pd
import decimal
from datetime import datetime, time
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .models import * 
from django.contrib import messages
from django.db import transaction
from django.shortcuts import render
from .resources import *
from django.http import JsonResponse
import json
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from import_export.formats import base_formats
from django.db.models import Q
import pdfkit
from django.template.loader import get_template








@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    ingredients = Ingredient.objects.all()
    nbr_ing = len(ingredients)

    levains = Levain.objects.all()
    nbr_lev = len(levains)

    panifications = Panification.objects.select_related('levain','technique').all()
    nbr_panif = len(panifications)

    n=10
    top_values = []


    for panif in panifications:
        num = panif.temps_fin_panif
        # Si la liste 'top_values' est vide ou si le nombre est plus petit que le premier élément de 'top_values'
        if not top_values or num < top_values[0]:
            top_values.insert(0, num)
        else:
            # Parcourir la liste 'top_values' pour trouver l'emplacement d'insertion approprié
            for i in range(len(top_values)):
                if num < top_values[i]:
                    top_values.insert(i, num)
                    break
                elif i == len(top_values) - 1:
                    top_values.append(num)
                    break

        # Garder la liste 'top_values' de taille n en supprimant les éléments supplémentaires
        if len(top_values) > n:
            top_values.pop()
    liste = []
    for pa in panifications :
        for value in top_values:
            if pa.temps_fin_panif == value:
                liste.append(pa) 
    
    valeur = []
    data = []
    for i in range (len(liste)) :
        valeur.append(liste[i].temps_fin_panif)
        data.append(liste[i].num_test)
    

    def decimal_to_float(d):
        return float(d)

    # Convertir la liste en une liste de floats (ou vous pouvez utiliser str() si vous préférez des chaînes)
    valeur = [decimal_to_float(item) for item in valeur]
    
    df1 = pd.DataFrame()
    for Panif in liste :
        numtest=Panif.num_test
        colonne1 = pd.DataFrame()
        df11, names = DataframeDonneesPanif(Panif)
        colonne1[f'T{numtest}']=df11['CO2- ppm'].astype(float)
        df1 = pd.concat([df1, colonne1], axis=1)
    df1.dropna(inplace = True)
    temps1 =pd.DataFrame()
    
    temps1['temps']=df11['Temps - min'].astype(float)
    df1 = pd.concat([temps1, df1], axis=1)
  
    datas1 = df1.to_dict(orient='records')
    request.session['df1'] = datas1



    
    df2 = pd.DataFrame()
    for Panif in liste :
        numtest=Panif.num_test
        colonne1 = pd.DataFrame()
        df22, names = DataframeDonneesPanif(Panif)
        colonne1[f'T{numtest}']=df22['Distance'].astype(float)
        df2 = pd.concat([df2, colonne1], axis=1)
    df2.dropna(inplace = True)
    temps2 =pd.DataFrame()
  
    temps2['temps']=df22['Temps - min'].astype(float)
    df2 = pd.concat([temps2, df2], axis=1)
  
    datas2 = df2.to_dict(orient='records')
    request.session['df2'] = datas2



    df3 = pd.DataFrame()
    for Panif in liste :
        numtest=Panif.num_test
        colonne1 = pd.DataFrame()
        df33, names = DataframeDonneesPanif(Panif)
        colonne1[f'T{numtest}']=df33['Ethanol'].astype(float)
        df3 = pd.concat([df3, colonne1], axis=1)
    df3.dropna(inplace = True)
    temps3 =pd.DataFrame()
   
    temps3['temps']=df33['Temps - min'].astype(float)
    df3 = pd.concat([temps3, df3], axis=1)
  
    datas3 = df3.to_dict(orient='records')
    request.session['df3'] = datas3



    df4 = pd.DataFrame()
    for Panif in liste :
        numtest=Panif.num_test
        colonne1 = pd.DataFrame()
        df44, names = DataframeDonneesPanif(Panif)
        colonne1[f'T{numtest}']=df44['pH-PATE'].astype(float)
        df4 = pd.concat([df4, colonne1], axis=1)
    df4.dropna(inplace = True)
    temps4 =pd.DataFrame()
   
    temps4['temps']=df44['Temps - min'].astype(float)
    df4 = pd.concat([temps4, df4], axis=1)
  
    datas4 = df4.to_dict(orient='records')
    request.session['df4'] = datas4


    
    print(df1)
    print (liste)
    print(top_values)
    print(nbr_panif) 
    print(nbr_lev)
    print(nbr_ing) 

    context = {
        'segment': 'index',
        'valeur' : valeur,
        'data' : data,
        'top_values' : top_values,
        'nbr_panif' : nbr_panif,
        'nbr_lev' : nbr_lev,
        'nbr_ing' : nbr_ing,
    }


    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))




@login_required(login_url="/login/")
def AffichagegrapheindexCO2(request):
     datas1=request.session['df1'] 
     return JsonResponse(datas1, safe=False)




@login_required(login_url="/login/")
def AffichagegrapheindexDRC(request):
     datas2=request.session['df2'] 
     return JsonResponse(datas2, safe=False)




@login_required(login_url="/login/")
def AffichagegrapheindexEthanol(request):
     datas3=request.session['df3'] 
     return JsonResponse(datas3, safe=False)





@login_required(login_url="/login/")
def Affichagegrapheindexph(request):
     datas4=request.session['df4'] 
     return JsonResponse(datas4, safe=False)





#affichage des ingredients dans un tableau
@login_required(login_url="/login/")
def AffichageIngredient(request):

    ingredients = Ingredient.objects.all()

    context = {
        'ingredients':ingredients, 
    }
    html_template = loader.get_template('home/lire_ingredient.html')
    return HttpResponse(html_template.render(context, request))





#enregistrement des donnees des ingredients dans la base de donnee
@login_required(login_url="/login/")
@transaction.atomic()
def EnregistrementIngredient(request):

    context = {}
    if request.method == 'POST':
        data = {
            'nom_ing' : request.POST.get('nom_ing'),
            'type_ing' : request.POST.get('type_ing'),
            'nature' : request.POST.get('nature'),
        }
        try:
            created = Ingredient.objects.create(**data)
            if created :
                messages.success(request, "Ingredient ajouté avec succès")
            else:
                messages.error(request, "Désolé veuillez réessayer encore")
        except Exception as e:
                    messages.error(request, f"Désolé, notre systeme a détecter un probléme {e}")

    html_template = loader.get_template('home/entrer_ingredient.html')
    return HttpResponse(html_template.render(context, request))





#affichage des levains dans un tableau
@login_required(login_url="/login/")
def AffichageLevain(request):

    levains = Levain.objects.all()
    ingredients = CompositionLevain.objects.select_related('levain').all()


    # modificating an levain 
    if request.POST.get('id_modifier'):

            code = request.POST.get('id_modifier')
            date = request.POST.get('date')
            types = request.POST.get('type_levain')
            att = request.POST.get('Att')
            pH = request.POST.get('pH')

            try: 

                levain = Levain.objects.get(code_levain=code)
                levain.type_levain =  types
                levain.date =  date
                levain.pH =  pH
                levain.att =  att
                levain.save() 
                print(levain)


                messages.success(request,  "Change made successfully.")

            except Exception as e:   

                messages.error(request, f"Sorry, the following error has occured {e}.")      

        # deleting an levain    

    if request.POST.get('id_supprimer'):
        code = request.POST.get('id_supprimer')

        try:

                levain = Levain.objects.get(code_levain=code)
                levain.delete()

                messages.success(request, "The deletion was successful.")   

        except Exception as e:

                messages.error(request, f"Sorry, the following error has occured {e}.")  


    context = {
        'levains':levains,
        'ingredients':ingredients, 
    }
    html_template = loader.get_template('home/lire_levains.html')
    return HttpResponse(html_template.render(context, request))





#Voir les Details des levains dans une carte
@login_required(login_url="/login/")
def VoirLevain(request, pk):

    levains = Levain.objects.get(code_levain = pk)
    ingredients = CompositionLevain.objects.filter(levain = levains)

    liste = []
    col = []
    for ing in ingredients :
        a = ing.nom_ing
        col.append(a)
        c = ing.masse_ing 
        liste.append(c)


    listecarac = []
    colcarac = []
    n = levains.date
    carac = CaracterisationLevain.objects.filter(levain = levains, date_caracterisation = n, num_rep = 1)

    for ing in carac :
        a = ing.nom_parametre
        colcarac.append(a)
        c = ing.valeur 
        listecarac.append(c)

    context = {
        'pk': pk,
        'levains':levains,
        'ingredients':ingredients, 
        'liste': liste,
        'col' : col,
        'listecarac':listecarac,
        'colcarac' : colcarac
        }
    
    html_template = loader.get_template('home/levain.html')
    return HttpResponse(html_template.render(context, request))





#Telechagement des Details des levains dans un cadre
def TelechagerLevain(request, pk):

    levains = Levain.objects.get(code_levain = pk)
    ingredients = CompositionLevain.objects.filter(levain = levains)

    liste = []
    col = []
    for ing in ingredients :
        a = ing.nom_ing
        col.append(a)
        c = ing.masse_ing 
        liste.append(c)


    listecarac = []
    colcarac = []
    n = levains.date
    carac = CaracterisationLevain.objects.filter(levain = levains, date_caracterisation = n, num_rep = 1)

    for ing in carac :
        a = ing.nom_parametre
        colcarac.append(a)
        c = ing.valeur 
        listecarac.append(c)

    context = {
        'pk': pk,
        'levains':levains,
        'ingredients':ingredients, 
        'liste': liste,
        'col' : col,
        'listecarac':listecarac,
        'colcarac' : colcarac
        }

        # get html file
    template = get_template('home/levainpdf.html')

    # render html with context variables

    html = template.render(context)

    # options of pdf format 

    options = {
        'page-size': 'Letter',
        'margin-top': '0in',
        'margin-right': '0in',
        'margin-bottom': '0in',
        'margin-left': '0in',
        'encoding': 'UTF-8',
        "enable-local-file-access": ""
    }

    # generate pdf 

    pdf = pdfkit.from_string(html, False, options)

    response = HttpResponse(pdf, content_type='application/pdf')

    response['Content-Disposition'] = "attachement"

    return response






#enregistrement des donnees du formulaire dans la base de donnee
@login_required(login_url="/login/")
@transaction.atomic()
def EnregistrementLevain(request):
    ingredients = Ingredient.objects.all()

    context = {
         'ingredients': ingredients,
    }
    items=[]

    if request.method == 'POST':
        try :   
            data = {
                'code_levain' : request.POST.get('code_levain'),
                'type_levain' : request.POST.get('type_levain'),
                'date' : request.POST.get('date'),
                'pH' : request.POST.get('pH'),
                'att' : request.POST.get('Att'),
            }
            created = Levain.objects.create(**data)

            
            ings = request.POST.getlist('ing')
            qte = request.POST.getlist('qte')
            
            for index, ing in enumerate(ings):
                data1 = CompositionLevain(
                    levain = created,
                    nom_ing = ing,
                    masse_ing = qte[index],
                    )
                items.append(data1)
                
            created1 = CompositionLevain.objects.bulk_create(items)
 
            if created and created1:
                messages.success(request, "Levain ajouté avec succès")
            else:
                messages.error(request, "Désolé veuillez réessayer encore")
        except Exception as e:
            messages.error(request, f"Désolé, notre systeme a détecter un probléme {e}")


    html_template = loader.get_template('home/entrer_levain.html')
    return HttpResponse(html_template.render(context, request))





#affichage des techniques de rafraichissement dans un tableau
@login_required(login_url="/login/")
def AffichageTechniqueRafraichissement(request):

    techniques = TechniqueRafraichissement.objects.all()
    
    context = {
        'techniques':techniques, 
    }
    html_template = loader.get_template('home/lire_techniquerafraichissement.html')
    return HttpResponse(html_template.render(context, request))





#enregistrement des donnees des techniques de rafraichissement dans la base de donnee
@login_required(login_url="/login/")
@transaction.atomic()
def EnregistrementTechniqueRafraichissement(request):

    context = {}
    if request.method == 'POST':
        data = {
            'nom_tech' : request.POST.get('nom_tech'),
            'description' : request.POST.get('description'),
        }
        try:
            created = TechniqueRafraichissement.objects.create(**data)
            if created :
                messages.success(request, "Technique de rafraichissement ajouté avec succès")
            else:
                messages.error(request, "Désolé veuillez réessayer encore")
        except Exception as e:
                    messages.error(request, f"Désolé, notre systeme a détecter un probléme {e}")

    html_template = loader.get_template('home/entrer_techniquerafraichissement.html')
    return HttpResponse(html_template.render(context, request))





#affichage des rafraichissement dans un tableau
@login_required(login_url="/login/")
def AffichageRafraichissement(request):

    ingredients = Ingredient.objects.all()
    levainss = Levain.objects.all()
    techniques = TechniqueRafraichissement.objects.all()
    rafraichissements = Rafraichissement.objects.select_related('levain','technique').all()

    liste = []
    for levain in levainss:

        output_tableau = []
        groupes = {}
        
        code_levain = levain.code_levain
        #li.append(num_test)
        carac = Rafraichissement.objects.filter(levain = levain)

        for element in carac:
            z = code_levain  
            n = element.technique.nom_tech 
            d = element.date_rafraichissement
            s = element.num_rafraichit 
            parametre = element.nom_ing
            valeur = element.masse_ing
         
            cle = (z, n, d, s)
            if cle in groupes:
                groupes[cle].append((parametre, valeur))
            else:
                groupes[cle] = [(parametre, valeur)]

        for cle, valeurs in groupes.items():
            element = list(cle) + valeurs
            output_tableau.append(element)

        for tableau in output_tableau :
            liste.append(tableau)
    

    # modificating an rafraichissement 
    if request.POST.get('id_modifier'):

            lev = request.POST.get('id_modifier')
            date = request.POST.get('date')
            num_rafraichit = request.POST.get('num_rafraichit')
            nom_tech = request.POST.get('nom_tech')
            ing= request.POST.get('ing')
            val= request.POST.get('qte')

            try: 
                levain = Levain.objects.get(code_levain=lev)
                raf = Rafraichissement.objects.filter(levain=levain, nom_ing=ing,num_rafraichit=num_rafraichit)
                raf.date_rafraichissement = date
                raf.technique = nom_tech
                raf.masse_ing = val
              
                raf.save() 
                print(raf)


                messages.success(request,  "Change made successfully.")

            except Exception as e:   

                messages.error(request, f"Sorry, the following error has occured {e}.")      

        # deleting an rafraichissement    

    if request.POST.get('id_supprimer'):
        lev = request.POST.get('id_supprimer')
        num_rafraichit = request.POST.get('id_rep')
        ing = request.POST.get('id_ing')

        try:

                levain = Levain.objects.get(code_levain=lev)
                raf = Rafraichissement.objects.filter(levain=levain, nom_ing=ing,num_rafraichit=num_rafraichit)
                levain.delete()

                messages.success(request, "The deletion was successful.")   

        except Exception as e:

                messages.error(request, f"Sorry, the following error has occured {e}.")  



    context = {
        'rafraichissements':rafraichissements,
        'liste' : liste,   
        'levainss':levainss,
        'techniques':techniques,
        'ingredients':ingredients,
    }

    html_template = loader.get_template('home/lire_rafraichissement.html')
    return HttpResponse(html_template.render(context, request))





#enregistrement des donnees de rafraichissement du formulaire dans la base de donnee
@login_required(login_url="/login/")
@transaction.atomic()
def EnregistrementRafraichissement(request):

    levains = Levain.objects.all()
    ingredients = Ingredient.objects.all()
    techniques = TechniqueRafraichissement.objects.all()

    context = {
        'levains':levains,
        'ingredients':ingredients, 
        'techniques':techniques,
    }
    items=[]
    
    if request.method == 'POST':
        
        levain = Levain.objects.get(code_levain = request.POST.get('levain'))
        technique = TechniqueRafraichissement.objects.get(nom_tech = request.POST.get('nom_tech'))
        date_rafraichissement = request.POST.get('date')
        num_rafraichit = request.POST.get('num_rafraichit')
        ings = request.POST.getlist('ing')
        qte = request.POST.getlist('qte')
            
        for index, ing in enumerate(ings):
            data1 = Rafraichissement(
                levain = levain,
                technique = technique,
                date_rafraichissement = date_rafraichissement,
                num_rafraichit = num_rafraichit,
                nom_ing = ing,
                masse_ing = qte[index],
                )
            items.append(data1)
        try:
            created1 = Rafraichissement.objects.bulk_create(items)
            if created1 :
                messages.success(request, "Rafraichissement ajouté avec succès")
            else:
                messages.error(request, "Désolé veuillez réessayer encore")
        except Exception as e:
                    messages.error(request, f"Désolé, notre systeme a détecter un probléme {e}")

    html_template = loader.get_template('home/entrer_rafraichissement.html')
    return HttpResponse(html_template.render(context, request))





#affichage des Caracteristique des Levains dans un tableau
@login_required(login_url="/login/")
def AffichageCaraterisationLevain(request):

    levains = Levain.objects.all()

    liste = []
    for levain in levains:

        output_tableau = []
        groupes = {}
        
        code_levain = levain.code_levain
        
        carac = CaracterisationLevain.objects.filter(levain = levain)

        for element in carac:
            z = code_levain  
            n = element.date_caracterisation 
            d = element.num_rep 
            valeur = element.valeur
         
            cle = (z, n, d)
            if cle in groupes:
                groupes[cle].append(valeur)
            else:
                groupes[cle] = [valeur]

        for cle, valeurs in groupes.items():
            element = list(cle) + valeurs
            output_tableau.append(element)

        for tableau in output_tableau :
            liste.append(tableau)
    
   
    context = {
        'liste' : liste,
    }

    html_template = loader.get_template('home/lire_caracterisationlevain.html')
    return HttpResponse(html_template.render(context, request))





#enregistrement des Caracteristique des Levains dans la base de donnee
@login_required(login_url="/login/")
@transaction.atomic()
def EnregistrementCaracterisationLevain(request):

    levains = Levain.objects.all()
    parametres = Parametre.objects.all()
    
    context = {
        'levains':levains,
        'parametres':parametres, 
    }
    items=[]
    
    if request.method == 'POST':
        
        levain = Levain.objects.get(code_levain = request.POST.get('levain'))
        date_caracterisation = request.POST.get('date')
        num_rep = request.POST.get('num_rep')
        nom_parametres = request.POST.getlist('nom_parametre')
        valeurs = request.POST.getlist('valeur')
            
        for index, nom_parametre in enumerate(nom_parametres):
            data1 = CaracterisationLevain(
                levain = levain,
                date_caracterisation = date_caracterisation,
                num_rep = num_rep,
                nom_parametre = nom_parametre,
                valeur = valeurs[index],
                )
            items.append(data1)
        try:
            created1 = CaracterisationLevain.objects.bulk_create(items)
            if created1 :
                messages.success(request, "Caracteristique Levain ajouté avec succès")
            else:
                messages.error(request, "Désolé veuillez réessayer encore")
        except Exception as e:
                    messages.error(request, f"Désolé, notre systeme a détecter un probléme {e}")

    html_template = loader.get_template('home/entrer_caracterisationlevain.html')
    return HttpResponse(html_template.render(context, request))





#affichage des techniques de panification dans un tableau
@login_required(login_url="/login/")
def AffichageTechniquePanification(request):

    techniques = TechniquePanification.objects.all()
    
    context = {
        'techniques':techniques, 
    }
    html_template = loader.get_template('home/lire_techniquepanification.html')
    return HttpResponse(html_template.render(context, request))





#enregistrement des donnees des techniques de panification dans la base de donnee
@login_required(login_url="/login/")
@transaction.atomic()
def EnregistrementTechniquePanification(request):

    context = {}
    if request.method == 'POST':
        data = {
            'nom_tech' : request.POST.get('nom_tech'),
            'description' : request.POST.get('description'),
        }
        try:
            created = TechniquePanification.objects.create(**data)
            if created :
                messages.success(request, "Technique de panification ajouté avec succès")
            else:
                messages.error(request, "Désolé veuillez réessayer encore")
        except Exception as e:
                    messages.error(request, f"Désolé, notre systeme a détecter un probléme {e}")

    html_template = loader.get_template('home/entrer_techniquepanification.html')
    return HttpResponse(html_template.render(context, request))





#affichage des tests de panification dans un tableau
@login_required(login_url="/login/")
def AffichagePanification(request):
    
    panifications = Panification.objects.select_related('levain','technique').all()
    levains = Levain.objects.all()
    techniques = TechniquePanification.objects.all()


    # modificating an panification 
    if request.POST.get('id_modifier'):

            numtest = request.POST.get('id_modifier')
            date = request.POST.get('date')
            repetition = request.POST.get('repetition')
            apport = request.POST.get('apport')
            tech = request.POST.get('technique')
            lev = request.POST.get('levain')

            try: 

                levain = Levain.objects.get(code_levain=lev)
                technique = TechniquePanification.objects.get(nom_tech=tech)
                panification = Panification.objects.get(num_test = numtest)
                panification.technique = technique
                panification.levain = levain
                panification.date_panification = date
                panification.num_repetition = repetition
                panification.apport = apport
                panification.save() 
                print(panification)


                messages.success(request,  "Change made successfully.")

            except Exception as e:   

                messages.error(request, f"Sorry, the following error has occured {e}.")      

        # deleting an levain    

    if request.POST.get('id_supprimer'):
        numtest = request.POST.get('id_supprimer')

        try:
                panification = Panification.objects.get(num_test = numtest)
                panification.delete()

                messages.success(request, "The deletion was successful.")   

        except Exception as e:

                messages.error(request, f"Sorry, the following error has occured {e}.")


    context = {
        'panifications':panifications, 
        'levains': levains,
        'techniques' : techniques,

    }
    html_template = loader.get_template('home/lire_panification.html')
    return HttpResponse(html_template.render(context, request))





#Voir les Details des tests dans un cadre
@login_required(login_url="/login/")
def VoirPanification(request, pk):

    panification = Panification.objects.get(num_test = pk)
    ingredients = CompositionPanification.objects.filter(panification = panification)
    print(panification)
    liste = []
    col = []
    for ing in ingredients :
        a = ing.nom_ing
        col.append(a)
        c = ing.masse_ing 
        liste.append(c)
   

    listecarac = []
    colcarac = []
    carac = CaracterPanification.objects.filter(panification = panification)

    for ing in carac :
        a = ing.nom_parametre
        colcarac.append(a)
        c = ing.valeur 
        listecarac.append(c)

    context = {
        'pk': pk,
        'panification':panification,
        'ingredients':ingredients, 
        'liste': liste,
        'col' : col,
        'listecarac':listecarac,
        'colcarac' : colcarac
        }
    
    html_template = loader.get_template('home/panification.html')
    return HttpResponse(html_template.render(context, request))






#Telechagement des Details des tests dans un cadre
def TelechagerPanification(request, pk):

    panification = Panification.objects.get(num_test = pk)
    ingredients = CompositionPanification.objects.filter(panification = panification)
    print(panification)
    liste = []
    col = []
    for ing in ingredients :
        a = ing.nom_ing
        col.append(a)
        c = ing.masse_ing 
        liste.append(c)
   
    listecarac = []
    colcarac = []
    carac = CaracterPanification.objects.filter(panification = panification)

    for ing in carac :
        a = ing.nom_parametre
        colcarac.append(a)
        c = ing.valeur 
        listecarac.append(c)
    
  

    context = {
        'pk': pk,
        'panification':panification,
        'ingredients':ingredients, 
        'liste': liste,
        'col' : col,
        'listecarac':listecarac,
        'colcarac' : colcarac
        }

        # get html file
    template = get_template('home/panificationpdf.html')

    # render html with context variables

    html = template.render(context)

    # options of pdf format 

    options = {
        'page-size': 'Letter',
        'margin-top': '0in',
        'margin-right': '0in',
        'margin-bottom': '0in',
        'margin-left': '0in',
        'encoding': 'UTF-8',
        "enable-local-file-access": ""
    }

    # generate pdf 

    pdf = pdfkit.from_string(html, False, options)

    response = HttpResponse(pdf, content_type='application/pdf')

    response['Content-Disposition'] = "attachement"

    return response
    
  




#affichage des Caracteristique des panifications dans un tableau
@login_required(login_url="/login/")
def AffichageCaraterisationPanification(request):
    
    CaracterisationPanifications = CaracterPanification.objects.select_related('panification').all()
    panifications = Panification.objects.select_related('levain','technique').all()

    liste = []
    for panif in panifications:
         li = []
         num_test = panif.num_test
         li.append(num_test)
         carac = CaracterPanification.objects.filter(panification=panif)
         for ca in carac :
              c = ca.valeur 
              li.append(c)
         liste.append(li)
    
    context = {
        'CaracterisationPanifications' : CaracterisationPanifications,
        'liste' : liste,
    }

    html_template = loader.get_template('home/lire_caracterisationpanification.html')
    return HttpResponse(html_template.render(context, request))





#enregistrement des Caracteristique des Levains dans la base de donnee
@login_required(login_url="/login/")
@transaction.atomic()
def EnregistrementCaracterisationPanification(request):

    panifications = Panification.objects.all()
    parametres = Parametre.objects.all()
    
    context = {
        'panifications': panifications,
        'parametres':parametres, 
    }

    items=[]
    
    if request.method == 'POST':
        
        panif=request.POST.get('panif')
        panification = Panification.objects.get(num_test = panif)

        nom_parametres = request.POST.getlist('nom_parametre')
        valeurs = request.POST.getlist('valeur')

        for index, nom_parametre in enumerate(nom_parametres):
            data1 = CaracterPanification(
                panification = panification,
                nom_parametre = nom_parametre,
                valeur = valeurs[index],
                )
            items.append(data1)
        try:
            created1 = CaracterPanification.objects.bulk_create(items)
            if created1 :
                messages.success(request, "Caracteristique panification ajouté avec succès")
            else:
                messages.error(request, "Désolé veuillez réessayer encore")
        except Exception as e:
                    messages.error(request, f"Désolé, notre systeme a détecter un probléme {e}")

    html_template = loader.get_template('home/entrer_caracterisationpanification.html')
    return HttpResponse(html_template.render(context, request))






#enregistrement des donnees des test de panification dans la base de donnee
@login_required(login_url="/login/")
@transaction.atomic()
def EnregistrementPanification(request):

    levains = Levain.objects.all()
    ingredients = Ingredient.objects.all()
    techniques = TechniquePanification.objects.all()
            
    context = {
        'techniques': techniques,
        'ingredients':ingredients,
        'levains' : levains,
    }
    items = []
    if request.method == 'POST':
        try:    
            levain = Levain.objects.get(code_levain = request.POST.get('levain'))
            techniques = TechniquePanification.objects.get(nom_tech = request.POST.get('technique'))

            data = {
                'num_test' : request.POST.get('num_test'),
                'levain' : levain,
                'technique': techniques,
                'date_panification' : request.POST.get('date'),
                'num_repetition' : request.POST.get('repetition'),
                'apport' : request.POST.get('apport'),
            } 
            created = Panification.objects.create(**data)

            ings = request.POST.getlist('ing')
            qte = request.POST.getlist('qte')
            
            for index, ing in enumerate(ings):
                data1 = CompositionPanification(
                    panification = created,
                    nom_ing = ing,
                    masse_ing = qte[index],
                    )
                items.append(data1)
                
            created1 = CompositionPanification.objects.bulk_create(items)
    
            if created and created1:
                messages.success(request, "Test de panification ajouté avec succès")
            else:
                messages.error(request, "Désolé veuillez réessayer encore")
        except Exception as e:
                messages.error(request, f"Désolé, notre systeme a détecter un probléme {e}")

    html_template = loader.get_template('home/entrer_panification.html')
    return HttpResponse(html_template.render(context, request))





#Importation des donnees d'acquisition sous formant excel,
# affichage des donnees dans un tableau et leur enregistrement dans la base de donnee
@login_required(login_url="/login/")
def Import_excel(request):

    Panifications = Panification.objects.select_related('technique','levain').all()

    context = {
         'Panifications': Panifications,
    }
    columns = None
    rows = None
    df = None

    if request.method == 'POST' and request.POST.get('panif'):

        Panificationss = Panification.objects.get(num_test = request.POST.get('panif'))
        # Stocker l'instance du modèle Panification dans une variable de session
        request.session['selected_panification'] = Panificationss.num_test

        context = {
            'Panifications': Panifications,
            'Panificationss':Panificationss,
        }
    if 'selected_panification' in request.session:
        selected_panification_id = request.session['selected_panification']
        selected_panification = Panification.objects.get(num_test=selected_panification_id)
       
        if request.method == 'POST' and 'excel_file' in request.FILES :
            try:
                excel_file = request.FILES['excel_file']
                df = pd.read_excel(excel_file)
                df.drop_duplicates(inplace = True)

                # Traitez les données comme vous le souhaitez, par exemple, les enregistrer dans la base de données
                # Supposons que vous avez déjà lu le fichier excel et stocké les données dans un objet DataFrame appelé df
                columns = df.columns
                rows = df.values.tolist()

                context={
                    'df': df.to_html(),
                    'columns':columns,
                    'rows': rows,
                    'Panifications': Panifications,
                    'selected_panification':selected_panification,
                }
                if not df.empty :
                    messages.success(request, "Methode de test de panification ajouté avec succès")
                else:
                    messages.error(request, "Désolé veuillez réessayer encore")
            except Exception as e:
                    messages.error(request, f"Désolé, notre systeme a détecter un probléme {e}")
               
    else:
            messages.error(request, "Veuillez sélectionner une instance de modèle Panification pour importer des données")

       
    html_template = loader.get_template('home/import_excel.html')
    return HttpResponse(html_template.render(context, request))





def telecharger_fichierprocedure(request):
    # Chemin complet vers le fichier exemple.txt
    chemin_fichier = os.path.join(settings.MEDIA_ROOT, "Procedure dimportation des donnees de panification.txt")

    # Ouvrir le fichier en mode binaire (b) pour téléchargement
    with open(chemin_fichier, 'rb') as fichier:
       
        fichier_en_memoire = io.BytesIO(fichier.read())

        # Définir le type de contenu pour le téléchargement
    response = HttpResponse(fichier_en_memoire, content_type='text/plain')
        # Définir l'en-tête de contenu pour le téléchargement
    response['Content-Disposition'] = 'attachment; filename="Procedure dimportation des donnees de panification.txt"'

    return response




def telecharger_fichierexcel(request):
    # Chemin complet vers le fichier excel (par exemple, Données_SGAF.xlsx)
    chemin_fichier = os.path.join(settings.MEDIA_ROOT, 'Données_SGAF.xlsx')

    # Ouvrir le fichier en mode binaire (b) pour le téléchargement
    with open(chemin_fichier, 'rb') as fichier:
        # Utiliser io.BytesIO pour stocker le contenu du fichier en mémoire
        fichier_en_memoire = io.BytesIO(fichier.read())

    # Créer une réponse en utilisant io.BytesIO
    response = HttpResponse(fichier_en_memoire, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    # Définir l'en-tête de contenu pour le téléchargement avec le nom du fichier (par exemple, "Données_SGAF.xlsx")
    response['Content-Disposition'] = 'attachment; filename="Données_SGAF.xlsx"'

    return response



# Enregistrement des donnees dans la base de donnee a travers une requete ajax et sous formant json
@csrf_exempt
@login_required(login_url="/login/")
def Enregistrementdata(request):

    if request.method == 'POST':

        # Récupérer les données envoyées via la requête AJAX
        json_data = request.body.decode('utf-8')
        data = json.loads(json_data)

        # Parcourir les données et créer une instance du modèle pour chaque produit
        for i in range(2,8):
            item = []
            for parametre_data in data:
                panification = Panification.objects.get(num_test = parametre_data['panification'])
                parametre1 = CaracterisationPanification(
                    panification = panification,
                    heure_panification = parametre_data['heure'], 
                    nom_parametre = parametre_data[f'parametre{i}'],
                    valeur = Decimal(parametre_data[f'val_parametre{i}'])
                    )
                item.append(parametre1)
            created1 = CaracterisationPanification.objects.bulk_create(item)

        if created1:
            messages.success(request, "Les donnees de panification ont été importees avec succès")
        else:
            messages.error(request, "Désolé veuillez réessayer encore")
       
        response_data = {'message': 'Les donnees de panification ont été importees avec succès.'}
        return JsonResponse(response_data)
    else:
        response_data = {'message': 'Méthode HTTP non autorisée. Seules les requêtes POST sont autorisées.'}
        return JsonResponse(response_data, status=405)





# fonction qui permet de recuperer dans la base de donnees les donnees d'un test de panification et qui le converti en un dataframe pandas 
def DataframeDonneesPanif(panificationss):

    parametres = CaracterisationPanification.objects.filter(panification=panificationss)
    n=0
    change_i= ''
    liste = []
    names=[1]
            
    for parametre in parametres :
        if parametre.nom_parametre != change_i :
            n += 1
            liste.append(parametre.nom_parametre)
            names.append(n+1)
        change_i = parametre.nom_parametre

    for i in range(2):
        names.pop(0)
        
    nb = int(len(parametres)/n)
    my_dict = {}
    lis1=[]
    lis2=[]
    for j in range(nb):
        pa=parametres[j]
        lis1.append(panificationss.num_test)
        lis2.append(pa.heure_panification)
    my_dict['N°Test'] = lis1
    my_dict['Heure'] = lis2
    for i in range(n):
        li=[]
        for j in range(nb):
            p=parametres[(i*nb) + j]
            li.append(p.valeur)
        my_dict[liste[i]] = li
    df = pd.DataFrame(my_dict)
    return df, names





# affichage des donnees brutes dans un tableau provenant de la base de donnees en fonction du test de panif choisie
@login_required(login_url="/login/")
def Affichagedonneebrute(request):
     
    Panifications = Panification.objects.select_related('levain','technique').all()
    
    context = {
        'Panifications':Panifications,
    }
    if request.method == 'POST' and request.POST.get('panif'):
         num_test =request.POST.get('panif')
         request.session['selected_panification'] = num_test
         selected_panification = request.session['selected_panification']
         Panificationss = Panification.objects.get(num_test = selected_panification)
         
         dft, names = DataframeDonneesPanif(Panificationss)

         df1 = dft.iloc[:, :2]
         df2 = dft.iloc[:, 2:]
         df2=df2.round(2).applymap('{:.2f}'.format)
         df2['Temps - min'] = df2['Temps - min'].apply(lambda x: x.split('.')[0])
         df = pd.concat([df1, df2], axis=1)


         columns = df.columns
         rows = df.values.tolist()
        
         datas = df.to_dict(orient='records')
         context = {
            
            'Panifications':Panifications,
            'columns':columns,
            'rows': rows,
            'datas':datas,
            'names':names,
         }

    # modification des donnees brutes 
    elif request.method == 'POST' and request.POST.get('id_Heure')  and request.POST.get('CO2') and request.POST.get('Distance'):

        heure = request.POST.get('id_Heure')
        numtest = request.POST.get('id_Test')
        
        heures = datetime.strptime(heure, "%H:%M").time()

        co2 = request.POST.get('CO2')
        distance = request.POST.get('Distance')
        ethanol = request.POST.get('Ethanol')
        pH = request.POST.get('pH')
        masse = request.POST.get('Masse')

        try:
            panificationss = Panification.objects.get(num_test = numtest)
            parametress = CaracterisationPanification.objects.filter( panification = panificationss, heure_panification=heures)
            for parametre in parametress:
                if parametre.nom_parametre == 'CO2- ppm' :
                    parametre.valeur = co2
                elif parametre.nom_parametre == 'Distance' :
                    parametre.valeur = distance
                elif parametre.nom_parametre == 'Ethanol' :
                    parametre.valeur = ethanol
                elif parametre.nom_parametre == 'pH-PATE' :
                    parametre.valeur = pH
                elif parametre.nom_parametre == 'Masse brut' :
                    parametre.valeur = masse
                parametre.save()

            dft, names = DataframeDonneesPanif(panificationss)

            df1 = dft.iloc[:, :2]
            df2 = dft.iloc[:, 2:]
            df2=df2.round(2).applymap('{:.2f}'.format)
            df2['Temps - min'] = df2['Temps - min'].apply(lambda x: x.split('.')[0])
            df = pd.concat([df1, df2], axis=1)

            columns = df.columns
            rows = df.values.tolist()
            
            datas = df.to_dict(orient='records')
            context = {
               
                'Panifications':Panifications,
                'columns':columns,
                'rows': rows,
                'datas':datas,
                'names':names,
            }
            
            messages.success(request, "Changements effectués avec succès.")

        except Exception as e:
            messages.error(request, f"Désolé, notre système a détecté un problème : {e}")


    # suppression des donnees brutes
    elif request.method == 'POST' and request.POST.get('id_Heure_s') :

        heure = request.POST.get('id_Heure_s')
        numtest = request.POST.get('id_Test_s')
        heures = datetime.strptime(heure, "%H:%M").time()

        try:
            panificationss = Panification.objects.get(num_test = numtest)
            parametress = CaracterisationPanification.objects.filter( panification = panificationss, heure_panification=heures)
        
            for parametre in parametress:
                parametre.delete()

            dft, names = DataframeDonneesPanif(panificationss)

            df1 = dft.iloc[:, :2]
        
          
            df2 = dft.iloc[:, 2:]
            
            df2=df2.round(2).applymap('{:.2f}'.format)
            df2['Temps - min'] = df2['Temps - min'].apply(lambda x: x.split('.')[0])
            df = pd.concat([df1, df2], axis=1)
            
            columns = df.columns
            rows = df.values.tolist()
            
            datas = df.to_dict(orient='records')
            context = {
                'Panifications':Panifications,
                'columns':columns,
                'rows': rows,
                'datas':datas,
                'names':names,
            }

        except Exception as e:
            messages.error(request, f"Désolé, notre système a détecté un problème : {e}")



    html_template = loader.get_template('home/tabledonneebrute.html')
    return HttpResponse(html_template.render(context, request))






# affichage des graphes des donnees brutes provenant de la base de donnees en fonction du test de panif choisie
@login_required(login_url="/login/")
def Affichagegraphedonneebrute(request):
         
         selected_panification = request.session['selected_panification']
         Panificationss = Panification.objects.get(num_test = selected_panification)

         dft, names = DataframeDonneesPanif(Panificationss)

         df1 = dft.iloc[:, :2]
         df2 = dft.iloc[:, 2:]
         df2=df2.round(3).applymap('{:.3f}'.format)
         df2['Temps - min'] = df2['Temps - min'].apply(lambda x: x.split('.')[0])
         df = pd.concat([df1, df2], axis=1)

         data_dict = df.to_dict(orient='records')
         
         return JsonResponse(data_dict, safe=False)





#Fonction qui permet de traiter les donnees brutes importees et transformees en dataframe pandas
def TraitementDonneesBrute(panificationss):
        
        caracteristiques = CaracterPanification.objects.filter(panification=panificationss)
        for carac in caracteristiques:
            if carac.nom_parametre == 'Att f' :
                ATTf = decimal.Decimal(carac.valeur)
            elif carac.nom_parametre == 'Att i' :
                ATT0 = decimal.Decimal(carac.valeur)
            elif carac.nom_parametre == 'Tarre' :
                Tarre = decimal.Decimal(carac.valeur)
            elif carac.nom_parametre == 'Masse brute i' :
                massei = decimal.Decimal(carac.valeur)
            elif carac.nom_parametre == 'Masse brute f' :
                massef = decimal.Decimal(carac.valeur)
            elif carac.nom_parametre == 'pH i' :
                phi = decimal.Decimal(carac.valeur)
            elif carac.nom_parametre == 'pH f' :
                phf = decimal.Decimal(carac.valeur)


        parametres = CaracterisationPanification.objects.filter(panification=panificationss)
        n=0
        change_i= ''
        liste = []
        names=[1]
                
        for parametre in parametres :
            if parametre.nom_parametre != change_i :
                n += 1
                liste.append(parametre.nom_parametre)
                names.append(n+1)
            change_i = parametre.nom_parametre

        for i in range(2):
            names.pop(0)
            
        nb = int(len(parametres)/n)
        my_dict = {}
        lis1=[]
        lis2=[]
        for j in range(nb):
            pa=parametres[j]
            lis1.append(panificationss.num_test)
            lis2.append(pa.heure_panification)
        my_dict['N°Test'] = lis1
        my_dict['Heure'] = lis2
        for i in range(n):
            li=[]
            for j in range(nb):
                p=parametres[(i*nb) + j]
                li.append(p.valeur)
            my_dict[liste[i]] = li
        dft = pd.DataFrame(my_dict)

        temps_exp=dft['Temps - min'].iloc[-1]
        
        dft['ATT'] = pd.Series([],dtype=float)
        dft['Masse_Net'] = pd.Series([],dtype=float)
        dft['DRC/Kg_pate'] = pd.Series([],dtype=float)
        dft['∆DRC'] = pd.Series([],dtype=float)
        dft['Cumul_DRC'] = pd.Series([],dtype=float)
        dft['∆DRC/Kg_pate'] = pd.Series([],dtype=float)
        dft['DRC/PERTE'] = pd.Series([],dtype=float)
        dft['cumul_DRC/Cumul_PERTE'] = pd.Series([],dtype=float)
        dft['∆DRC/Cumul_PERTE'] = pd.Series([],dtype=float)
        dft['∆DRC/g_perdu'] = pd.Series([],dtype=float)
        dft['Perte_masse_NET'] = pd.Series([],dtype=float)
        dft['Cumul_perte_NET'] = pd.Series([],dtype=float)
        dft['CO2/Masse_Net'] = pd.Series([],dtype=float)
        dft['ml_CO2/g_perdu'] = pd.Series([],dtype=float)
        dft['Vol_CO2_L'] = pd.Series([],dtype=float)
        dft['CO2_L/Kg_pate'] = pd.Series([],dtype=float)
        dft['Vitesse_production_CO2_ml/100g/h'] = pd.Series([],dtype=float)
        dft['Volume_Ehanol_L'] = pd.Series([],dtype=float)
        dft['Ethanol/Masse_Net'] = pd.Series([],dtype=float)
        dft['Ethanol_L/kg_pate'] = pd.Series([],dtype=float)
        dft['Vitesse_production_Ethanol_ml/100g/h'] = pd.Series([],dtype=float)
        dft['Ethanol/perte_masse'] = pd.Series([],dtype=float)
        dft['pH/g_pate'] = pd.Series([],dtype=float)
        dft['pH/g_perdu'] = pd.Series([],dtype=float)
        dft['pH/ATT'] = pd.Series([],dtype=float)


        perte_masse_NET0 = decimal.Decimal(0.002556)
        DRC0 = decimal.Decimal(0.1)
        #Tarre= decimal.Decimal(50.0)
        #temps_exp=decimal.Decimal(1440)
        #ATT0=decimal.Decimal(32.3)
        #ATTf=decimal.Decimal(110.4)

        d_ATT=ATTf-ATT0
        ATT_min=d_ATT/temps_exp


        dft.loc[0, "ATT"]=ATT0
        for i in range(1, dft.shape[0]):
            
            dft.loc[i, "ATT"]=dft.loc[i-1, "ATT"]+ATT_min

        
        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "Masse_Net"]=dft.loc[i, "Masse brut"]-Tarre
            
        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "DRC/Kg_pate"]=dft.loc[i, "Distance"]*1000/dft.loc[i, "Masse_Net"]

        
        dft.loc[0, "∆DRC"]=DRC0
        for i in range(1, dft.shape[0]):
            
            dft.loc[i, "∆DRC"]=dft.loc[i-1, "Distance"]-dft.loc[i, "Distance"]

        dft.loc[0, "Cumul_DRC"]=dft.loc[0, "∆DRC"]
        for i in range(1, dft.shape[0]):
            
            dft.loc[i, "Cumul_DRC"]=dft.loc[i, "∆DRC"]-dft.loc[i-1, "Cumul_DRC"]

        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "∆DRC/Kg_pate"]=dft.loc[i, "∆DRC"]*1000/dft.loc[i, "Masse_Net"]
        
        dft.loc[0, "Perte_masse_NET"] = perte_masse_NET0
        for i in range(1, dft.shape[0]):
            
            dft.loc[i, "Perte_masse_NET"]=dft.loc[i-1, "Masse_Net"]-dft.loc[i, "Masse_Net"]
        
        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "DRC/PERTE"]=dft.loc[i, "Distance"]/dft.loc[i, "Perte_masse_NET"]

        dft.loc[0, "Cumul_perte_NET"]=dft.loc[0, "Perte_masse_NET"]
        for i in range(1, dft.shape[0]):
            
            dft.loc[i, "Cumul_perte_NET"]=dft.loc[i-1, "Cumul_perte_NET"]+dft.loc[i, "Perte_masse_NET"]
            
        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "cumul_DRC/Cumul_PERTE"]=dft.loc[i, "Cumul_DRC"]/dft.loc[i, "Cumul_perte_NET"]
            
        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "∆DRC/Cumul_PERTE"]=dft.loc[i, "∆DRC"]/dft.loc[i, "Cumul_perte_NET"]
            
        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "∆DRC/g_perdu"]=dft.loc[i, "∆DRC"]/dft.loc[i, "Perte_masse_NET"]

        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "CO2/Masse_Net"]=dft.loc[i, "CO2- ppm"]/dft.loc[i, "Masse_Net"]
            
        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "Vol_CO2_L"]=dft.loc[i, "CO2- ppm"]*decimal.Decimal(0.04032)/1000
            
        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "ml_CO2/g_perdu"]=dft.loc[i, "Vol_CO2_L"]/dft.loc[i, "Perte_masse_NET"]

        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "CO2_L/Kg_pate"]=dft.loc[i, "Vol_CO2_L"]*1000/dft.loc[i, "Masse_Net"]

        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "Vitesse_production_CO2_ml/100g/h"]=dft.loc[i, "Vol_CO2_L"]*100000/dft.loc[1, "Masse_Net"]

        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "Volume_Ehanol_L"]=dft.loc[i, "Ethanol"]*decimal.Decimal(0.04032)/1000
            
        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "Ethanol/Masse_Net"]=dft.loc[i, "Ethanol"]/dft.loc[i, "Masse_Net"]
            
        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "Ethanol_L/kg_pate"]=dft.loc[i, "Volume_Ehanol_L"]*1000/dft.loc[i, "Masse_Net"]

        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "Vitesse_production_Ethanol_ml/100g/h"]=dft.loc[i, "Volume_Ehanol_L"]*100000/dft.loc[1, "Masse_Net"]

        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "Ethanol/perte_masse"]=dft.loc[i, "Ethanol"]/dft.loc[i, "Perte_masse_NET"]
            
        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "pH/g_pate"]=dft.loc[i, "pH-PATE"]/dft.loc[i, "Masse_Net"]
            
        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "pH/g_perdu"]=dft.loc[i, "pH-PATE"]/dft.loc[i, "Perte_masse_NET"]

        for i in range(0, dft.shape[0]):
            dft.loc[i, "pH/ATT"]=dft.loc[i, "pH-PATE"]/dft.loc[i, "ATT"]

        return {
            'dft': dft,
            'names': names,
            'temps_exp': temps_exp,
            'ATTf': ATTf,
            'ATT0': ATT0,
            'Tarre': Tarre,
            'massei': massei,
            'massef': massef,
            'phi': phi,
            'phf': phf,
        }






# affichage des donnees brutes dans un tableau provenant de la base de donnees en fonction du test de panif choisie
@login_required(login_url="/login/")
def Affichagedonneecalcule(request):
     
    Panifications = Panification.objects.select_related('levain','technique').all()

    
    context = {
        'Panifications':Panifications,
    }

    if request.method == 'POST' and request.POST.get('panif'):
        num_test =request.POST.get('panif')
        request.session['selected_panification'] = num_test
        selected_panification = request.session['selected_panification']
        Panificationss = Panification.objects.get(num_test = selected_panification)

        traitement = TraitementDonneesBrute(Panificationss)
        dft = traitement['dft']
        names = traitement['names']
       
        #request.session['dft'] = dft
        df1 = dft['Heure']

        dft=dft.round(3).applymap('{:.3f}'.format)
        dft['Temps - min'] = dft['Temps - min'].apply(lambda x: x.split('.')[0])
        dft['N°Test'] = dft['N°Test'].apply(lambda x: x.split('.')[0])
        datas = dft.to_dict(orient='records')

        dft['Heure'] = df1
 
        x=len(names)
        k=27+x
        z=x+2

        for i in range(z,k+1):
             names.append(i)
             
        columns = dft.columns
        rows = dft.values.tolist()
        
        request.session['dft'] = datas

        context = {
           
            'Panifications':Panifications,
            'columns':columns,
            'rows': rows,
            'names':names,
        }     

    elif request.method == 'POST' and request.POST.get('id_finpanif'):
        numtest = request.POST.get('id_finpanif')
        temps = request.POST.get('temps_finpanif')
        print(numtest)
        print(temps)

        try:
            panificationss = Panification.objects.get(num_test = numtest)
            panificationss.temps_fin_panif =  temps
            panificationss.save() 

            traitement = TraitementDonneesBrute(panificationss)
            dft = traitement['dft']
            names = traitement['names']

            #request.session['dft'] = dft


            dft=dft.round(3).applymap('{:.3f}'.format)
            dft['Temps - min'] = dft['Temps - min'].apply(lambda x: x.split('.')[0])
            dft['N°Test'] = dft['N°Test'].apply(lambda x: x.split('.')[0])
            datas = dft.to_dict(orient='records')

            x=len(names)
            k=27+x
            z=x+2

            for i in range(z,k+1):
                names.append(i)
                
            columns = dft.columns
            rows = dft.values.tolist()
            
            
            request.session['dft'] = datas

            context = {
            
                'Panifications':Panifications,
                'columns':columns,
                'rows': rows,
                'names':names,
            }

            messages.success(request,  "Temps de fin de la fermentation enregistre avec succes")
        except Exception as e:   
            messages.error(request, f"Sorry, the following error has occured {e}.")  


    html_template = loader.get_template('home/tabledonneescalcule.html')
    return HttpResponse(html_template.render(context, request))





@login_required(login_url="/login/")
def Affichagegraphedonneecalcule(request):
     datas=request.session['dft'] 
     return JsonResponse(datas, safe=False)






def Consolidationdonnees(panificationss):
     
        numero_test = panificationss.num_test
        lev = panificationss.levain
        levain = lev.code_levain
        numero_repetition = panificationss.num_repetition
        date_panification = panificationss.date_panification
        Taux_incorporation = panificationss.apport
        temps_fin_panif = panificationss.temps_fin_panif


        caracteristiques = CaracterPanification.objects.filter(panification=panificationss)
        for carac in caracteristiques:
            if carac.nom_parametre == 'Att f' :
                ATTf = decimal.Decimal(carac.valeur)
            elif carac.nom_parametre == 'Att i' :
                ATT0 = decimal.Decimal(carac.valeur)
            elif carac.nom_parametre == 'Tarre' :
                Tarre = decimal.Decimal(carac.valeur)
            elif carac.nom_parametre == 'Masse brute i' :
                massei = decimal.Decimal(carac.valeur)
            elif carac.nom_parametre == 'Masse brute f' :
                massef = decimal.Decimal(carac.valeur)
            elif carac.nom_parametre == 'pH i' :
                phi = decimal.Decimal(carac.valeur)
            elif carac.nom_parametre == 'pH f' :
                phf = decimal.Decimal(carac.valeur)


        parametres = CaracterisationPanification.objects.filter(panification=panificationss)
        n=0
        change_i= ''
        liste = []
        names=[1]
                
        for parametre in parametres :
            if parametre.nom_parametre != change_i :
                n += 1
                liste.append(parametre.nom_parametre)
                names.append(n+1)
            change_i = parametre.nom_parametre

        for i in range(2):
            names.pop(0)
            
        nb = int(len(parametres)/n)
        my_dict = {}
        lis1=[]
        lis2=[]
        for j in range(nb):
            pa=parametres[j]
            lis1.append(panificationss.num_test)
            lis2.append(pa.heure_panification)
        my_dict['N°Test'] = lis1
        my_dict['Heure'] = lis2
        for i in range(n):
            li=[]
            for j in range(nb):
                p=parametres[(i*nb) + j]
                li.append(p.valeur)
            my_dict[liste[i]] = li
        dft = pd.DataFrame(my_dict)

        temps_exp=dft['Temps - min'].iloc[-1]
        
        dft['ATT'] = pd.Series([],dtype=float)
        dft['Masse_Net'] = pd.Series([],dtype=float)
        dft['DRC/Kg_pate'] = pd.Series([],dtype=float)
        dft['∆DRC'] = pd.Series([],dtype=float)
        dft['Cumul_DRC'] = pd.Series([],dtype=float)
        dft['∆DRC/Kg_pate'] = pd.Series([],dtype=float)
        dft['DRC/PERTE'] = pd.Series([],dtype=float)
        dft['cumul_DRC/Cumul_PERTE'] = pd.Series([],dtype=float)
        dft['∆DRC/Cumul_PERTE'] = pd.Series([],dtype=float)
        dft['∆DRC/g_perdu'] = pd.Series([],dtype=float)
        dft['Perte_masse_NET'] = pd.Series([],dtype=float)
        dft['Cumul_perte_NET'] = pd.Series([],dtype=float)
        dft['CO2/Masse_Net'] = pd.Series([],dtype=float)
        dft['ml_CO2/g_perdu'] = pd.Series([],dtype=float)
        dft['Vol_CO2_L'] = pd.Series([],dtype=float)
        dft['CO2_L/Kg_pate'] = pd.Series([],dtype=float)
        dft['Vitesse_production_CO2_ml/100g/h'] = pd.Series([],dtype=float)
        dft['Volume_Ehanol_L'] = pd.Series([],dtype=float)
        dft['Ethanol/Masse_Net'] = pd.Series([],dtype=float)
        dft['Ethanol_L/kg_pate'] = pd.Series([],dtype=float)
        dft['Vitesse_production_Ethanol_ml/100g/h'] = pd.Series([],dtype=float)
        dft['Ethanol/perte_masse'] = pd.Series([],dtype=float)
        dft['pH/g_pate'] = pd.Series([],dtype=float)
        dft['pH/g_perdu'] = pd.Series([],dtype=float)
        dft['pH/ATT'] = pd.Series([],dtype=float)


        perte_masse_NET0 = decimal.Decimal(0.002556)
        DRC0 = decimal.Decimal(0.1)
        #Tarre= decimal.Decimal(50.0)
        #temps_exp=decimal.Decimal(1440)
        #ATT0=decimal.Decimal(32.3)
        #ATTf=decimal.Decimal(110.4)

        d_ATT=ATTf-ATT0
        ATT_min=d_ATT/temps_exp


        dft.loc[0, "ATT"]=ATT0
        for i in range(1, dft.shape[0]):
            
            dft.loc[i, "ATT"]=dft.loc[i-1, "ATT"]+ATT_min

        
        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "Masse_Net"]=dft.loc[i, "Masse brut"]-Tarre
            
        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "DRC/Kg_pate"]=dft.loc[i, "Distance"]*1000/dft.loc[i, "Masse_Net"]

        
        dft.loc[0, "∆DRC"]=DRC0
        for i in range(1, dft.shape[0]):
            
            dft.loc[i, "∆DRC"]=dft.loc[i-1, "Distance"]-dft.loc[i, "Distance"]

        dft.loc[0, "Cumul_DRC"]=dft.loc[0, "∆DRC"]
        for i in range(1, dft.shape[0]):
            
            dft.loc[i, "Cumul_DRC"]=dft.loc[i, "∆DRC"]-dft.loc[i-1, "Cumul_DRC"]

        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "∆DRC/Kg_pate"]=dft.loc[i, "∆DRC"]*1000/dft.loc[i, "Masse_Net"]
        
        dft.loc[0, "Perte_masse_NET"] = perte_masse_NET0
        for i in range(1, dft.shape[0]):
            
            dft.loc[i, "Perte_masse_NET"]=dft.loc[i-1, "Masse_Net"]-dft.loc[i, "Masse_Net"]
        
        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "DRC/PERTE"]=dft.loc[i, "Distance"]/dft.loc[i, "Perte_masse_NET"]

        dft.loc[0, "Cumul_perte_NET"]=dft.loc[0, "Perte_masse_NET"]
        for i in range(1, dft.shape[0]):
            
            dft.loc[i, "Cumul_perte_NET"]=dft.loc[i-1, "Cumul_perte_NET"]+dft.loc[i, "Perte_masse_NET"]
            
        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "cumul_DRC/Cumul_PERTE"]=dft.loc[i, "Cumul_DRC"]/dft.loc[i, "Cumul_perte_NET"]
            
        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "∆DRC/Cumul_PERTE"]=dft.loc[i, "∆DRC"]/dft.loc[i, "Cumul_perte_NET"]
            
        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "∆DRC/g_perdu"]=dft.loc[i, "∆DRC"]/dft.loc[i, "Perte_masse_NET"]

        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "CO2/Masse_Net"]=dft.loc[i, "CO2- ppm"]/dft.loc[i, "Masse_Net"]
            
        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "Vol_CO2_L"]=dft.loc[i, "CO2- ppm"]*decimal.Decimal(0.04032)/1000
            
        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "ml_CO2/g_perdu"]=dft.loc[i, "Vol_CO2_L"]/dft.loc[i, "Perte_masse_NET"]

        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "CO2_L/Kg_pate"]=dft.loc[i, "Vol_CO2_L"]*1000/dft.loc[i, "Masse_Net"]

        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "Vitesse_production_CO2_ml/100g/h"]=dft.loc[i, "Vol_CO2_L"]*100000/dft.loc[1, "Masse_Net"]

        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "Volume_Ehanol_L"]=dft.loc[i, "Ethanol"]*decimal.Decimal(0.04032)/1000
            
        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "Ethanol/Masse_Net"]=dft.loc[i, "Ethanol"]/dft.loc[i, "Masse_Net"]
            
        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "Ethanol_L/kg_pate"]=dft.loc[i, "Volume_Ehanol_L"]*1000/dft.loc[i, "Masse_Net"]

        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "Vitesse_production_Ethanol_ml/100g/h"]=dft.loc[i, "Volume_Ehanol_L"]*100000/dft.loc[1, "Masse_Net"]

        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "Ethanol/perte_masse"]=dft.loc[i, "Ethanol"]/dft.loc[i, "Perte_masse_NET"]
            
        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "pH/g_pate"]=dft.loc[i, "pH-PATE"]/dft.loc[i, "Masse_Net"]
            
        for i in range(0, dft.shape[0]):
            
            dft.loc[i, "pH/g_perdu"]=dft.loc[i, "pH-PATE"]/dft.loc[i, "Perte_masse_NET"]

        for i in range(0, dft.shape[0]):
            dft.loc[i, "pH/ATT"]=dft.loc[i, "pH-PATE"]/dft.loc[i, "ATT"]


        masse_net_i = massei - Tarre


        #Temps
        temps_exp = temps_exp
        temps_fin_panif = temps_fin_panif

        #DRC
        DRC0 = dft['Distance'][0]
        DRC_min = dft['Distance'].min()
        d_DRC_experience = DRC0 - DRC_min

        index = dft[dft['Temps - min'] == temps_fin_panif].index[0]
        DRC_fin_panif = dft.loc[index, 'Distance']
        d_DRC_panification = DRC0 - DRC_fin_panif
        surface_recipient = decimal.Decimal(113.0973355)
        volume_pate = d_DRC_panification*surface_recipient
        volume_specifique = volume_pate/masse_net_i

        #Masse
        massei = massei
        masse_net_i = masse_net_i
        perte_masse_fin_experience = massei - massef
        taux_perte_masse_fin_experience = (perte_masse_fin_experience/masse_net_i)*decimal.Decimal(100)
        perte_par_min = perte_masse_fin_experience/temps_exp
        masse_brute_fin_panification = dft.loc[index, 'Masse brut']
        perte_masse_fin_panification = massei - masse_brute_fin_panification
        taux_perte_masse_fin_panification = (perte_masse_fin_panification/masse_net_i)*decimal.Decimal(100)

        #pH
        phi=phi
        pHi_arduino = dft['pH-PATE'][0]
        phf_panification = dft.loc[index, 'pH-PATE']
        phf = phf
        d_ph_panification = phi-phf_panification
        d_ph_experience = phi- phf

        #ATT
        ATT0 = ATT0
        ATTf_panification = dft.loc[index, 'ATT'] 
        ATTf = ATTf
        d_ATT_panification = ATTf_panification - ATT0
        d_ATT_experience = ATTf - ATT0 

        #CO2
        CO2_fin_panification = dft.loc[index, 'CO2- ppm']
        CO2_max = dft['CO2- ppm'].max()
        production_CO2_par_kgpate_fin = dft.loc[index, 'CO2_L/Kg_pate']
        vitesse_production_CO2 = dft.loc[index, 'Vitesse_production_CO2_ml/100g/h']

        #Ethanol
        Ethanol_fin_panification = dft.loc[index, 'Ethanol']
        Ethanol_max = dft['Ethanol'].max()
        production_Ethanol_par_kgpate_fin = dft.loc[index, 'Ethanol_L/kg_pate']
        vitesse_production_Ethanol = dft.loc[index, 'Vitesse_production_Ethanol_ml/100g/h']


        recap = [levain, numero_repetition, date_panification, Taux_incorporation, numero_test, temps_exp, temps_fin_panif, DRC0,
                    DRC_min, d_DRC_experience, DRC_fin_panif, d_DRC_panification, volume_pate, volume_specifique, massei, masse_net_i,
                        perte_masse_fin_experience, taux_perte_masse_fin_experience, perte_par_min, masse_brute_fin_panification, perte_masse_fin_panification, taux_perte_masse_fin_panification,
                            phi, pHi_arduino, phf_panification, phf, d_ph_panification, d_ph_experience, ATT0, ATTf_panification, ATTf, d_ATT_panification, d_ATT_experience,
                                CO2_fin_panification, CO2_max, production_CO2_par_kgpate_fin, vitesse_production_CO2, Ethanol_fin_panification, Ethanol_max, production_Ethanol_par_kgpate_fin,
                                    vitesse_production_Ethanol ]
        
       
        
        stat = [levain, temps_exp, temps_fin_panif, d_DRC_panification, volume_specifique, taux_perte_masse_fin_panification,
                    phi, phf_panification, d_ph_panification, ATT0, ATTf_panification, d_ATT_panification, CO2_fin_panification, 
                        CO2_max, production_CO2_par_kgpate_fin, vitesse_production_CO2, Ethanol_fin_panification, 
                            Ethanol_max, production_Ethanol_par_kgpate_fin, vitesse_production_Ethanol ]

     

        return recap, stat





#affichage de la recapitulation des tests dans un tableau
@login_required(login_url="/login/")
def Recapitulationdonnees(request):


    Panifications = Panification.objects.select_related('levain','technique').all()
    
    context = {
        'Panifications':Panifications,
    }
    if request.method == 'POST':
         
         num_test1 =request.POST.get('panif1')
         num_test2 =request.POST.get('panif2')
         num_test3 =request.POST.get('panif3')
         num_test4 =request.POST.get('panif4')
         num_test5 =request.POST.get('panif5')
         request.session['selected_panification1'] = num_test1
         request.session['selected_panification2'] = num_test2
         request.session['selected_panification3'] = num_test3
         request.session['selected_panification4'] = num_test4
         request.session['selected_panification5'] = num_test5
         selected_panification1 = request.session['selected_panification1']
         selected_panification2 = request.session['selected_panification2']
         selected_panification3 = request.session['selected_panification3']
         selected_panification4 = request.session['selected_panification4']
         selected_panification5 = request.session['selected_panification5']
         Panificationss1 = Panification.objects.get(num_test = selected_panification1)
         Panificationss2 = Panification.objects.get(num_test = selected_panification2)
         Panificationss3 = Panification.objects.get(num_test = selected_panification3)
         Panificationss4 = Panification.objects.get(num_test = selected_panification4)
         Panificationss5 = Panification.objects.get(num_test = selected_panification5)


         Panifications = [Panificationss1, Panificationss2, Panificationss3, Panificationss4, Panificationss5]

         Liste = []
         for Panif in Panifications :
             Parametre = CaracterisationPanification.objects.filter(panification =Panif)
             if Parametre is not None :
        
                 recap, stat = Consolidationdonnees(Panif)
                 Liste.append(recap)
         dft = pd.DataFrame(Liste, columns=['LEVAIN', 'REPETITION', 'DATE',  "TAUX D'INCORPORATION",'NUMERO TEST', "TEMPS DE L'EXPERIENCE", 'FIN DE PANIFICATION',
                                                'DRC INITIALE', 'DRC_MIN', '∆DRC EXPERIENCE','DRC FIN PANIFICATION', '∆DRC PANIFICATION', 'Volume pate ','Volume spécifique', 'Masse brut intiale', 'Masse net initiale',
                                                'Perte de masse  fin experience', 'Taux de perte de masse experience', 'Perte/min','Masse brut fin panification', 'Perte de masse fin panification', 'Taux de perte fin panif',
                                                'pH INTIALE-eutech', 'pH INTIALE-ARDUINO', 'pH FINpani','pH FIN expérience ', 'ΔpH i-panif', 'ΔpH i-experience','ATT INITIALE', 'ATT FINPANIFICATION', 'ATT FINexperience','ΔATT finpanif'
                                                , 'ΔATT fin experience', 'CO2 fin panif','CO2 Max fermentation', 'Production du CO2 L/Kgde pate fin pani','Vitesse de production du CO2 ml/100g/h', 'ETHANOL fin panif','ETHANOL Max fermentation', 'Production du ETHANOL L/Kgde pate fin panif',
                                                'Vitesse de production du ETHANOL ml/100g/h'
                                                ])
            
         df1 = dft.iloc[:, :5]
         df2 = dft.iloc[:, 5:]
         df2=df2.round(2).applymap('{:.2f}'.format)
         df = pd.concat([df1, df2], axis=1)

         columns = df.columns
         rows = df.values.tolist()

         context = {
                'Panifications' : Panifications,
                'columns':columns,
                'rows': rows,  
                'df' : df
         }

    html_template = loader.get_template('home/recapitulationdonnees.html')
    return HttpResponse(html_template.render(context, request))






def TelechagerRecapitulationdonnees(request):

    Panifications = Panification.objects.select_related('levain','technique').all()

    Liste = []
    for Panif in Panifications :
        Parametre = CaracterisationPanification.objects.filter(panification =Panif)
        if Parametre is not None :
    
            recap, stat = Consolidationdonnees(Panif)
            Liste.append(recap)
    dft = pd.DataFrame(Liste, columns=['LEVAIN', 'REPETITION', 'DATE',  "TAUX D'INCORPORATION",'NUMERO TEST', "TEMPS DE L'EXPERIENCE", 'FIN DE PANIFICATION',
                                            'DRC INITIALE', 'DRC_MIN', '∆DRC EXPERIENCE','DRC FIN PANIFICATION', '∆DRC PANIFICATION', 'Volume pate ','Volume spécifique', 'Masse brut intiale', 'Masse net initiale',
                                            'Perte de masse  fin experience', 'Taux de perte de masse experience', 'Perte/min','Masse brut fin panification', 'Perte de masse fin panification', 'Taux de perte fin panif',
                                            'pH INTIALE-eutech', 'pH INTIALE-ARDUINO', 'pH FINpani','pH FIN expérience ', 'ΔpH i-panif', 'ΔpH i-experience','ATT INITIALE', 'ATT FINPANIFICATION', 'ATT FINexperience','ΔATT finpanif'
                                            , 'ΔATT fin experience', 'CO2 fin panif','CO2 Max fermentation', 'Production du CO2 L/Kgde pate fin pani','Vitesse de production du CO2 ml/100g/h', 'ETHANOL fin panif','ETHANOL Max fermentation', 'Production du ETHANOL L/Kgde pate fin panif',
                                            'Vitesse de production du ETHANOL ml/100g/h'
                                            ])
        
    df1 = dft.iloc[:, :5]
    df2 = dft.iloc[:, 5:]
    df2=df2.round(2).applymap('{:.2f}'.format)
    df = pd.concat([df1, df2], axis=1)

    columns = df.columns
    rows = df.values.tolist()

    context = {
            'Panifications' : Panifications,
            'columns':columns,
            'rows': rows,  
            'df' : df
    }

    html_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'templates', 'home', 'recappdf.html')

    html_template = render(request, 'home/recappdf.html', context)

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_template.content.decode('utf-8'))

    # Options de configuration pour pdfkit
    options = {
        'page-size': 'A3',
        'orientation': 'Landscape',
        'margin-top': '0.5in',
        'margin-right': '0.5in',
        'margin-bottom': '0.5in',
        'margin-left': '0.5in',
        'encoding': "UTF-8",
        
    }

    # Convertissez le contenu HTML en PDF en utilisant pdfkit
    pdf_file = pdfkit.from_file(html_file, False, options=options)

    

    # Définissez les en-têtes de la réponse pour le téléchargement du fichier PDF
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="recappdf.pdf"'

    return response





#affichage de donnees statistiques des tests dans un tableau
@login_required(login_url="/login/")
def DonneesStatistiques(request):
        
    Panifications = Panification.objects.select_related('levain','technique').all()
    
    context = {
        'Panifications':Panifications,
    }
    if request.method == 'POST':
         
         num_test1 =request.POST.get('panif1')
         num_test2 =request.POST.get('panif2')
         num_test3 =request.POST.get('panif3')
         num_test4 =request.POST.get('panif4')
         num_test5 =request.POST.get('panif5')
         request.session['selected_panification1'] = num_test1
         request.session['selected_panification2'] = num_test2
         request.session['selected_panification3'] = num_test3
         request.session['selected_panification4'] = num_test4
         request.session['selected_panification5'] = num_test5
         selected_panification1 = request.session['selected_panification1']
         selected_panification2 = request.session['selected_panification2']
         selected_panification3 = request.session['selected_panification3']
         selected_panification4 = request.session['selected_panification4']
         selected_panification5 = request.session['selected_panification5']
         Panificationss1 = Panification.objects.get(num_test = selected_panification1)
         Panificationss2 = Panification.objects.get(num_test = selected_panification2)
         Panificationss3 = Panification.objects.get(num_test = selected_panification3)
         Panificationss4 = Panification.objects.get(num_test = selected_panification4)
         Panificationss5 = Panification.objects.get(num_test = selected_panification5)


         Panifications = [Panificationss1, Panificationss2, Panificationss3, Panificationss4, Panificationss5]
    

         Liste = []
         for Panif in Panifications :
             Parametre = CaracterisationPanification.objects.filter(panification =Panif)
           
             if Parametre is not None:
                 recap, stat = Consolidationdonnees(Panif)
                 Liste.append(stat)
         dft = pd.DataFrame(Liste, columns=['LEVAIN', "TEMPS DE L'EXPERIENCE", 'FIN DE PANIFICATION',
                                            '∆DRC PANIFICATION','Volume spécifique', 
                                            'Taux de perte fin panif',
                                            'pH INTIALE-eutech',  'pH FIN pani', 'ΔpH i-panif','ATT INITIALE', 'ATT FINPANIFICATION', 'ΔATT finpanif'
                                            , 'CO2 fin panif','CO2 Max fermentation', 'Production du CO2 L/Kgde pate fin pani','Vitesse de production du CO2 ml/100g/h', 'ETHANOL fin panif','ETHANOL Max fermentation', 'Production du ETHANOL L/Kgde pate fin panif',
                                            'Vitesse de production du ETHANOL ml/100g/h'
                                            ])
        
         df1 = dft.iloc[:, :1]
         df2 = dft.iloc[:, 1:]
         df2=df2.round(2).applymap('{:.2f}'.format)
         df = pd.concat([df1, df2], axis=1)

         columns = df.columns
         rows = df.values.tolist()

         context = {
            'Panifications' : Panifications,
            'columns':columns,
            'rows': rows,  
            'df' : df
         }

    html_template = loader.get_template('home/donneesstat.html')
    return HttpResponse(html_template.render(context, request))





@login_required(login_url="/login/")
def Parametrepanification(request):
     
    Panifications = Panification.objects.select_related('levain','technique').all()
   

    
    context = {
        'Panifications': Panifications,
        
    }
    if request.method == 'POST':
        
        parametre = request.POST.get('nom_parametre')
        num_test1 =request.POST.get('panif1')
        num_test2 =request.POST.get('panif2')
        num_test3 =request.POST.get('panif3')
        request.session['selected_panification1'] = num_test1
        request.session['selected_panification2'] = num_test2
        request.session['selected_panification3'] = num_test3
        selected_panification1 = request.session['selected_panification1']
        selected_panification2 = request.session['selected_panification2']
        selected_panification3 = request.session['selected_panification3']
        Panificationss1 = Panification.objects.get(num_test = selected_panification1)
        Panificationss2 = Panification.objects.get(num_test = selected_panification2)
        Panificationss3 = Panification.objects.get(num_test = selected_panification3)
        rep1=Panificationss1.num_repetition
        rep2=Panificationss2.num_repetition
        rep3=Panificationss3.num_repetition
        lev1 = Panificationss1.levain.code_levain
        lev2 = Panificationss2.levain.code_levain
        lev3 = Panificationss3.levain.code_levain

        
        if parametre == 'CO2/temps' :

            df1, names = DataframeDonneesPanif(Panificationss1)
            colonne1=df1['CO2- ppm'].astype(float)

            df2, names = DataframeDonneesPanif(Panificationss2)
            colonne2=df2['CO2- ppm'].astype(float)

            df3, names = DataframeDonneesPanif(Panificationss3)
            colonne3=df3['CO2- ppm'].astype(float)

            colonne0=df3['Temps - min'].astype(float)


            df = pd.DataFrame({f'CO2 {lev1}-R{rep1}': colonne1, f'CO2-{lev2}-R{rep2}': colonne2, f'CO2_{lev3}-R{rep3}':colonne3})
            moyenne_colonnes = df.mean(axis=1)
            df['moyenne CO2'] = moyenne_colonnes
            df['moyenne CO2']=df['moyenne CO2'].astype(float)
            dft= pd.concat([colonne0, df], axis=1)
            dft.dropna(inplace = True)

            datas1 = dft.to_dict(orient='records')
            request.session['dft1'] = datas1
            dft=dft.round(3).applymap('{:.3f}'.format)
            columns = dft.columns
            rows = dft.values.tolist()
        
            context = {
                'Panifications':Panifications,
                'columns':columns,
                'rows':rows,  
                'parametre' :parametre,                
                }
            
        elif parametre == 'DRC/temps' :

            df1, names = DataframeDonneesPanif(Panificationss1)
            colonne1=df1['Distance'].astype(float)

            df2, names = DataframeDonneesPanif(Panificationss2)
            colonne2=df2['Distance'].astype(float)

            df3, names = DataframeDonneesPanif(Panificationss3)
            colonne3=df3['Distance'].astype(float)

            colonne0=df3['Temps - min'].astype(float)
            

            df = pd.DataFrame({ 
                f'DRC {lev1}-R{rep1}': colonne1,
                f'DRC-{lev2}-R{rep2}': colonne2,
                f'DRC{lev3}-R{rep3}': colonne3
            })
            
            moyenne_colonnes = df.mean(axis=1)
            df['moyenne DRC'] = moyenne_colonnes
            df['moyenne DRC']=df['moyenne DRC'].astype(float)
            dft= pd.concat([colonne0, df], axis=1)
            dft.dropna(inplace = True)
            
            datas2 = dft.to_dict(orient='records')
            request.session['dft2'] = datas2

            dft=dft.round(3).applymap('{:.3f}'.format)
            columns = dft.columns
            rows = dft.values.tolist()
        
            context = {
                'Panifications':Panifications,
                'columns':columns,
                'rows':rows,   
                'parametre' :parametre,               
                }

        elif parametre == 'Ethanol/temps' :

            df1, names = DataframeDonneesPanif(Panificationss1)
            colonne1=df1['Ethanol'].astype(float)

            df2, names = DataframeDonneesPanif(Panificationss2)
            colonne2=df2['Ethanol'].astype(float)

            df3, names = DataframeDonneesPanif(Panificationss3)
            colonne3=df3['Ethanol'].astype(float)

            colonne0=df3['Temps - min'].astype(float)
        

            df = pd.DataFrame({f'Ethanol {lev1}-R{rep1}': colonne1, f'Ethanol-{lev2}-R{rep2}': colonne2, f'Ethanol_R{lev3}-{rep3}':colonne3})
            moyenne_colonnes = df.mean(axis=1)
            df['moyenne Ethanol'] = moyenne_colonnes
            df['moyenne Ethanol']=df['moyenne Ethanol'].astype(float)
            dft= pd.concat([colonne0, df], axis=1)
            dft.dropna(inplace = True)

            datas3 = dft.to_dict(orient='records')
            request.session['dft3'] = datas3

            dft=dft.round(3).applymap('{:.3f}'.format)
            columns = dft.columns
            rows = dft.values.tolist()
            context = {
                'Panifications':Panifications,
                'columns':columns,
                'rows':rows,      
                'parametre' :parametre,            
                }

        elif parametre == 'pH/temps' :

            df1, names = DataframeDonneesPanif(Panificationss1)
            colonne1=df1['pH-PATE'].astype(float)

            df2, names = DataframeDonneesPanif(Panificationss2)
            colonne2=df2['pH-PATE'].astype(float)

            df3, names = DataframeDonneesPanif(Panificationss3)
            colonne3=df3['pH-PATE'].astype(float)

            colonne0=df3['Temps - min'].astype(float)

        
            df = pd.DataFrame({f'pH {lev1}-R{rep1}': colonne1, f'pH-{lev2}-R{rep2}': colonne2, f'pH_{lev3}-R{rep3}':colonne3})
            moyenne_colonnes = df.mean(axis=1)
            df['moyenne pH'] = moyenne_colonnes
            df['moyenne pH']=df['moyenne pH'].astype(float)
            dft= pd.concat([colonne0, df], axis=1)
            dft.dropna(inplace = True)

            datas4 = dft.to_dict(orient='records')
            request.session['dft4'] = datas4

            dft=dft.round(3).applymap('{:.3f}'.format)
            columns = dft.columns
            rows = dft.values.tolist()
            context = {
                'Panifications':Panifications,
                'columns':columns,
                'rows':rows,      
                'parametre' :parametre,            
                }
            
        elif parametre == 'CO2/DRC' :

            df1, names = DataframeDonneesPanif(Panificationss1)
            colonne1=df1['CO2- ppm'].astype(float)

            df2, names = DataframeDonneesPanif(Panificationss2)
            colonne2=df2['CO2- ppm'].astype(float)

            df3, names = DataframeDonneesPanif(Panificationss3)
            colonne3=df3['CO2- ppm'].astype(float)

            colonne0=df3['Distance'].astype(float)


            df = pd.DataFrame({f'CO2 R{rep1}': colonne1, f'CO2-R{rep2}': colonne2, f'CO2_R{rep3}':colonne3})
            moyenne_colonnes = df.mean(axis=1)
            df['moyenne CO2/DRC'] = moyenne_colonnes
            df['moyenne CO2/DRC']=df['moyenne CO2/DRC'].astype(float)
            dft= pd.concat([colonne0, df], axis=1)
            dft.dropna(inplace = True)

            datas1 = dft.to_dict(orient='records')
            request.session['dft1'] = datas1
            dft=dft.round(3).applymap('{:.3f}'.format)
            columns = dft.columns
            rows = dft.values.tolist()
        
            context = {
                'Panifications':Panifications,
                'columns':columns,
                'rows':rows, 
                'parametre' :parametre,                 
                }
            
        elif parametre == 'DRC/CO2' :

            df1, names = DataframeDonneesPanif(Panificationss1)
            colonne1=df1['Distance'].astype(float)

            df2, names = DataframeDonneesPanif(Panificationss2)
            colonne2=df2['Distance'].astype(float)

            df3, names = DataframeDonneesPanif(Panificationss3)
            colonne3=df3['Distance'].astype(float)

            colonne0=df3['CO2- ppm'].astype(float)
            

            df = pd.DataFrame({ 
                f'DRC {lev1}-R{rep1}': colonne1,
                f'DRC-{lev2}-R{rep2}': colonne2,
                f'DRC{lev3}-R{rep3}': colonne3
            })
            
            moyenne_colonnes = df.mean(axis=1)
            df['moyenne DRC/CO2'] = moyenne_colonnes
            df['moyenne DRC/CO2']=df['moyenne DRC/CO2'].astype(float)
            dft= pd.concat([colonne0, df], axis=1)
            dft.dropna(inplace = True)
            
            datas2 = dft.to_dict(orient='records')
            request.session['dft2'] = datas2

            dft=dft.round(3).applymap('{:.3f}'.format)
            columns = dft.columns
            rows = dft.values.tolist()
        
            context = {
                'Panifications':Panifications,
                'columns':columns,
                'rows':rows,      
                'parametre' :parametre,            
                }
            
        elif parametre == 'DRC/Ethanol' :

            df1, names = DataframeDonneesPanif(Panificationss1)
            colonne1=df1['Distance'].astype(float)

            df2, names = DataframeDonneesPanif(Panificationss2)
            colonne2=df2['Distance'].astype(float)

            df3, names = DataframeDonneesPanif(Panificationss3)
            colonne3=df3['Distance'].astype(float)

            colonne0=df3['Ethanol'].astype(float)
            

            df = pd.DataFrame({ 
                f'DRC {lev1}-R{rep1}': colonne1,
                f'DRC-{lev2}-R{rep2}': colonne2,
                f'DRC{lev3}-R{rep3}': colonne3
            })
            
            moyenne_colonnes = df.mean(axis=1)
            df['moyenne DRC/Ethanol'] = moyenne_colonnes
            df['moyenne DRC/Ethanol']=df['moyenne DRC/Ethanol'].astype(float)
            dft= pd.concat([colonne0, df], axis=1)
            dft.dropna(inplace = True)
            
            datas2 = dft.to_dict(orient='records')
            request.session['dft2'] = datas2

            dft=dft.round(3).applymap('{:.3f}'.format)
            columns = dft.columns
            rows = dft.values.tolist()
        
            context = {
                'Panifications':Panifications,
                'columns':columns,
                'rows':rows,     
                'parametre' :parametre,             
                }

        elif parametre == 'Ethanol/DRC' :
            df1, names = DataframeDonneesPanif(Panificationss1)
            colonne1=df1['Ethanol'].astype(float)

            df2, names = DataframeDonneesPanif(Panificationss2)
            colonne2=df2['Ethanol'].astype(float)

            df3, names = DataframeDonneesPanif(Panificationss3)
            colonne3=df3['Ethanol'].astype(float)

            colonne0=df3['Distance'].astype(float)
        

            df = pd.DataFrame({f'Ethanol {lev1}-R{rep1}': colonne1, f'Ethanol-{lev2}-R{rep2}': colonne2, f'Ethanol_{lev3}-R{rep3}':colonne3})
            moyenne_colonnes = df.mean(axis=1)
            df['moyenne Ethanol/DRC'] = moyenne_colonnes
            df['moyenne Ethanol/DRC']=df['moyenne Ethanol/DRC'].astype(float)
            dft= pd.concat([colonne0, df], axis=1)
            dft.dropna(inplace = True)

            datas3 = dft.to_dict(orient='records')
            request.session['dft3'] = datas3

            dft=dft.round(3).applymap('{:.3f}'.format)
            columns = dft.columns
            rows = dft.values.tolist()
            context = {
                'Panifications':Panifications,
                'columns':columns,
                'rows':rows,  
                'parametre' :parametre,                
                }

    html_template = loader.get_template('home/parametre_panif.html')
    return HttpResponse(html_template.render(context, request))





@login_required(login_url="/login/")
def GrapheParametrepanification(request):
     datas1 = request.session['dft1'] 
     return JsonResponse(datas1, safe=False)






@login_required(login_url="/login/")
def ParametreCO2(request):
     
    Panifications = Panification.objects.select_related('levain','technique').all()
    
    context = {
        'Panifications':Panifications,
    }
    if request.method == 'POST':
         
         num_test1 =request.POST.get('panif1')
         num_test2 =request.POST.get('panif2')
         num_test3 =request.POST.get('panif3')
         request.session['selected_panification1'] = num_test1
         request.session['selected_panification2'] = num_test2
         request.session['selected_panification3'] = num_test3
         selected_panification1 = request.session['selected_panification1']
         selected_panification2 = request.session['selected_panification2']
         selected_panification3 = request.session['selected_panification3']
         Panificationss1 = Panification.objects.get(num_test = selected_panification1)
         Panificationss2 = Panification.objects.get(num_test = selected_panification2)
         Panificationss3 = Panification.objects.get(num_test = selected_panification3)
         rep1=Panificationss1.num_repetition
         rep2=Panificationss2.num_repetition
         rep3=Panificationss3.num_repetition
         lev1 = Panificationss1.levain.code_levain
         lev2 = Panificationss2.levain.code_levain
         lev3 = Panificationss3.levain.code_levain


         df1, names = DataframeDonneesPanif(Panificationss1)
         colonne1=df1['CO2- ppm'].astype(float)

         df2, names = DataframeDonneesPanif(Panificationss2)
         colonne2=df2['CO2- ppm'].astype(float)

         df3, names = DataframeDonneesPanif(Panificationss3)
         colonne3=df3['CO2- ppm'].astype(float)

         colonne0=df3['Temps - min'].astype(float)


         df = pd.DataFrame({f'CO2 {lev1}-R{rep1}': colonne1, f'CO2-{lev2}-R{rep2}': colonne2, f'CO2_{lev3}-R{rep3}':colonne3})
         moyenne_colonnes = df.mean(axis=1)
         df['moyenne'] = moyenne_colonnes
         df['moyenne']=df['moyenne'].astype(float)
         dft= pd.concat([colonne0, df], axis=1)
         dft.dropna(inplace = True)

         datas1 = dft.to_dict(orient='records')
         request.session['dft1'] = datas1
         dft=dft.round(3).applymap('{:.3f}'.format)
         columns = dft.columns
         rows = dft.values.tolist()
       
         context = {
            'Panifications':Panifications,
            'columns':columns,
            'rows':rows,                  
            }
              
    html_template = loader.get_template('home/parametre_co2.html')
    return HttpResponse(html_template.render(context, request))





@login_required(login_url="/login/")
def GrapheParametreCO2(request):
     datas1 = request.session['dft1'] 
     return JsonResponse(datas1, safe=False)





@login_required(login_url="/login/")
def ParametreDistance(request):
     
    Panifications = Panification.objects.select_related('levain','technique').all()
    
    context = {
        'Panifications':Panifications,
    }
    if request.method == 'POST':
         
         num_test1 =request.POST.get('panif1')
         num_test2 =request.POST.get('panif2')
         num_test3 =request.POST.get('panif3')
         request.session['selected_panification1'] = num_test1
         request.session['selected_panification2'] = num_test2
         request.session['selected_panification3'] = num_test3
         selected_panification1 = request.session['selected_panification1']
         selected_panification2 = request.session['selected_panification2']
         selected_panification3 = request.session['selected_panification3']
         Panificationss1 = Panification.objects.get(num_test = selected_panification1)
         Panificationss2 = Panification.objects.get(num_test = selected_panification2)
         Panificationss3 = Panification.objects.get(num_test = selected_panification3)
         rep1=Panificationss1.num_repetition
         rep2=Panificationss2.num_repetition
         rep3=Panificationss3.num_repetition
         lev1 = Panificationss1.levain.code_levain
         lev2 = Panificationss2.levain.code_levain
         lev3 = Panificationss3.levain.code_levain


         df1, names = DataframeDonneesPanif(Panificationss1)
         colonne1=df1['Distance'].astype(float)

         df2, names = DataframeDonneesPanif(Panificationss2)
         colonne2=df2['Distance'].astype(float)

         df3, names = DataframeDonneesPanif(Panificationss3)
         colonne3=df3['Distance'].astype(float)

         colonne0=df3['Temps - min'].astype(float)
        

         df = pd.DataFrame({ 
            f'DRC {lev1}-R{rep1}': colonne1,
            f'DRC-{lev2}-R{rep2}': colonne2,
            f'DRC{lev3}-R{rep3}':colonne3
        })
         
         moyenne_colonnes = df.mean(axis=1)
         df['moyenne'] = moyenne_colonnes
         df['moyenne']=df['moyenne'].astype(float)
         dft= pd.concat([colonne0, df], axis=1)
         dft.dropna(inplace = True)
         
         datas2 = dft.to_dict(orient='records')
         request.session['dft2'] = datas2

         dft=dft.round(3).applymap('{:.3f}'.format)
         columns = dft.columns
         rows = dft.values.tolist()
      
         context = {
            'Panifications':Panifications,
            'columns':columns,
            'rows':rows,                  
            }
              
    html_template = loader.get_template('home/parametre_distance.html')
    return HttpResponse(html_template.render(context, request))





@login_required(login_url="/login/")
def GrapheParametreDistance(request):
     datas2 = request.session['dft2'] 
     return JsonResponse(datas2, safe=False)





@login_required(login_url="/login/")
def ParametreEthanol(request):
     
    Panifications = Panification.objects.select_related('levain','technique').all()
    
    context = {
        'Panifications':Panifications,
    }
    if request.method == 'POST':
         
         num_test1 =request.POST.get('panif1')
         num_test2 =request.POST.get('panif2')
         num_test3 =request.POST.get('panif3')
         request.session['selected_panification1'] = num_test1
         request.session['selected_panification2'] = num_test2
         request.session['selected_panification3'] = num_test3
         selected_panification1 = request.session['selected_panification1']
         selected_panification2 = request.session['selected_panification2']
         selected_panification3 = request.session['selected_panification3']
         Panificationss1 = Panification.objects.get(num_test = selected_panification1)
         Panificationss2 = Panification.objects.get(num_test = selected_panification2)
         Panificationss3 = Panification.objects.get(num_test = selected_panification3)
         rep1=Panificationss1.num_repetition
         rep2=Panificationss2.num_repetition
         rep3=Panificationss3.num_repetition
         lev1 = Panificationss1.levain.code_levain
         lev2 = Panificationss2.levain.code_levain
         lev3 = Panificationss3.levain.code_levain



         df1, names = DataframeDonneesPanif(Panificationss1)
         colonne1=df1['Ethanol'].astype(float)

         df2, names = DataframeDonneesPanif(Panificationss2)
         colonne2=df2['Ethanol'].astype(float)

         df3, names = DataframeDonneesPanif(Panificationss3)
         colonne3=df3['Ethanol'].astype(float)

         colonne0=df3['Temps - min'].astype(float)
    

         df = pd.DataFrame({f'Ethanol {lev1}-R{rep1}': colonne1, f'Ethanol-{lev2}-R{rep2}': colonne2, f'Ethanol_{lev3}-R{rep3}':colonne3})
         moyenne_colonnes = df.mean(axis=1)
         df['moyenne'] = moyenne_colonnes
         df['moyenne']=df['moyenne'].astype(float)
         dft= pd.concat([colonne0, df], axis=1)
         dft.dropna(inplace = True)

         datas3 = dft.to_dict(orient='records')
         request.session['dft3'] = datas3

         dft=dft.round(3).applymap('{:.3f}'.format)
         columns = dft.columns
         rows = dft.values.tolist()
         context = {
            'Panifications':Panifications,
            'columns':columns,
            'rows':rows,                  
            }
              
    html_template = loader.get_template('home/parametre_ethanol.html')
    return HttpResponse(html_template.render(context, request))





@login_required(login_url="/login/")
def GrapheParametreEthanol(request):
     datas3 = request.session['dft3'] 
     return JsonResponse(datas3, safe=False)





@login_required(login_url="/login/")
def ParametrePh(request):
     
    Panifications = Panification.objects.select_related('levain','technique').all()
    
    context = {
        'Panifications':Panifications,
    }
    if request.method == 'POST':
         
         num_test1 =request.POST.get('panif1')
         num_test2 =request.POST.get('panif2')
         num_test3 =request.POST.get('panif3')
         request.session['selected_panification1'] = num_test1
         request.session['selected_panification2'] = num_test2
         request.session['selected_panification3'] = num_test3
         selected_panification1 = request.session['selected_panification1']
         selected_panification2 = request.session['selected_panification2']
         selected_panification3 = request.session['selected_panification3']
         Panificationss1 = Panification.objects.get(num_test = selected_panification1)
         Panificationss2 = Panification.objects.get(num_test = selected_panification2)
         Panificationss3 = Panification.objects.get(num_test = selected_panification3)
         rep1=Panificationss1.num_repetition
         rep2=Panificationss2.num_repetition
         rep3=Panificationss3.num_repetition
         lev1 = Panificationss1.levain.code_levain
         lev2 = Panificationss2.levain.code_levain
         lev3 = Panificationss3.levain.code_levain


         df1, names = DataframeDonneesPanif(Panificationss1)
         colonne1=df1['pH-PATE'].astype(float)

         df2, names = DataframeDonneesPanif(Panificationss2)
         colonne2=df2['pH-PATE'].astype(float)

         df3, names = DataframeDonneesPanif(Panificationss3)
         colonne3=df3['pH-PATE'].astype(float)

         colonne0=df3['Temps - min'].astype(float)

    
         df = pd.DataFrame({f'pH {lev1}-R{rep1}': colonne1, f'pH-{lev2}-R{rep2}': colonne2, f'pH_{lev3}-R{rep3}':colonne3})
         moyenne_colonnes = df.mean(axis=1)
         df['moyenne'] = moyenne_colonnes
         df['moyenne']=df['moyenne'].astype(float)
         dft= pd.concat([colonne0, df], axis=1)
         dft.dropna(inplace = True)

         datas4 = dft.to_dict(orient='records')
         request.session['dft4'] = datas4

         dft=dft.round(3).applymap('{:.3f}'.format)
         columns = dft.columns
         rows = dft.values.tolist()
         context = {
            'Panifications':Panifications,
            'columns':columns,
            'rows':rows,                  
            }
              
    html_template = loader.get_template('home/parametre_ph.html')
    return HttpResponse(html_template.render(context, request))





@login_required(login_url="/login/")
def GrapheParametrePh(request):
     datas4 = request.session['dft4'] 
     return JsonResponse(datas4, safe=False)





@login_required(login_url="/login/")
def ParametreMasseBrute(request):
     
    Panifications = Panification.objects.select_related('levain','technique').all()
    
    context = {
        'Panifications':Panifications,
    }
    if request.method == 'POST':
         
         num_test1 =request.POST.get('panif1')
         num_test2 =request.POST.get('panif2')
         num_test3 =request.POST.get('panif3')
         request.session['selected_panification1'] = num_test1
         request.session['selected_panification2'] = num_test2
         request.session['selected_panification3'] = num_test3
         selected_panification1 = request.session['selected_panification1']
         selected_panification2 = request.session['selected_panification2']
         selected_panification3 = request.session['selected_panification3']
         Panificationss1 = Panification.objects.get(num_test = selected_panification1)
         Panificationss2 = Panification.objects.get(num_test = selected_panification2)
         Panificationss3 = Panification.objects.get(num_test = selected_panification3)
         rep1=Panificationss1.num_repetition
         rep2=Panificationss2.num_repetition
         rep3=Panificationss3.num_repetition
         lev1 = Panificationss1.levain.code_levain
         lev2 = Panificationss2.levain.code_levain
         lev3 = Panificationss3.levain.code_levain


         df1, names = DataframeDonneesPanif(Panificationss1)
         colonne1=df1['Masse brut'].astype(float)

         df2, names = DataframeDonneesPanif(Panificationss2)
         colonne2=df2['Masse brut'].astype(float)

         df3, names = DataframeDonneesPanif(Panificationss3)
         colonne3=df3['Masse brut'].astype(float)

         colonne0=df3['Temps - min'].astype(float)


    
         df = pd.DataFrame({f'MasseBrute_{lev1}-R{rep1}': colonne1, f'Masse Brute {lev2}-R{rep2}': colonne2, f'Masse Brute_{lev3}-R{rep3}':colonne3})
         moyenne_colonnes = df.mean(axis=1)
         df['moyenne'] = moyenne_colonnes
         df['moyenne']=df['moyenne'].astype(float)
         dft= pd.concat([colonne0, df], axis=1)
         dft.dropna(inplace = True)

         datas5 = dft.to_dict(orient='records')
         request.session['dft5'] = datas5

         dft=dft.round(3).applymap('{:.3f}'.format)
         columns = dft.columns
         rows = dft.values.tolist()
         context = {
            'Panifications':Panifications,
            'columns':columns,
            'rows':rows,                  
            }
              
    html_template = loader.get_template('home/parametre_massebrute.html')
    return HttpResponse(html_template.render(context, request))





@login_required(login_url="/login/")
def GrapheParametreMasseBrute(request):
     datas5 = request.session['dft5'] 
     return JsonResponse(datas5, safe=False)





@login_required(login_url="/login/")
def ParametreAtt(request):
     
    Panifications = Panification.objects.select_related('levain','technique').all()
    
    context = {
        'Panifications':Panifications,
    }
    if request.method == 'POST':
         
        num_test1 =request.POST.get('panif1')
        num_test2 =request.POST.get('panif2')
        num_test3 =request.POST.get('panif3')
        request.session['selected_panification1'] = num_test1
        request.session['selected_panification2'] = num_test2
        request.session['selected_panification3'] = num_test3
        selected_panification1 = request.session['selected_panification1']
        selected_panification2 = request.session['selected_panification2']
        selected_panification3 = request.session['selected_panification3']
        Panificationss1 = Panification.objects.get(num_test = selected_panification1)
        Panificationss2 = Panification.objects.get(num_test = selected_panification2)
        Panificationss3 = Panification.objects.get(num_test = selected_panification3)
        rep1=Panificationss1.num_repetition
        rep2=Panificationss2.num_repetition
        rep3=Panificationss3.num_repetition
        lev1 = Panificationss1.levain.code_levain
        lev2 = Panificationss2.levain.code_levain
        lev3 = Panificationss3.levain.code_levain

       
        traitement = TraitementDonneesBrute(Panificationss1)
        df1 = traitement['dft']
        colonne1=df1['ATT'].astype(float)


        traitement = TraitementDonneesBrute(Panificationss2)
        df2 = traitement['dft']
        colonne2=df2['ATT'].astype(float)


        traitement = TraitementDonneesBrute(Panificationss3)
        df3 = traitement['dft']
        colonne3=df3['ATT'].astype(float)
         
        colonne0=df3['Temps - min'].astype(float)

    
        df = pd.DataFrame({f'Att {lev1}-R{rep1}': colonne1, f'Att-{lev2}-R{rep2}': colonne2, f'Att_{lev3}-R{rep3}':colonne3})
        moyenne_colonnes = df.mean(axis=1)
        df['moyenne'] = moyenne_colonnes
        df['moyenne']=df['moyenne'].astype(float)
        dft= pd.concat([colonne0, df], axis=1)
        dft.dropna(inplace = True)

        datas6 = dft.to_dict(orient='records')
        request.session['dft6'] = datas6

        dft=dft.round(3).applymap('{:.3f}'.format)
        columns = dft.columns
        rows = dft.values.tolist()
        context = {
            'Panifications':Panifications,
            'columns':columns,
            'rows':rows,                  
            }
    html_template = loader.get_template('home/parametre_att.html')
    return HttpResponse(html_template.render(context, request))




@login_required(login_url="/login/")
def GrapheParametreAtt(request):
     datas6 = request.session['dft6'] 
     return JsonResponse(datas6, safe=False)




@login_required(login_url="/login/")
def ParametreDRC_Kg_pate(request):
     
    Panifications = Panification.objects.select_related('levain','technique').all()
    
    context = {
        'Panifications':Panifications,
    }
    if request.method == 'POST':
         
        num_test1 =request.POST.get('panif1')
        num_test2 =request.POST.get('panif2')
        num_test3 =request.POST.get('panif3')
        request.session['selected_panification1'] = num_test1
        request.session['selected_panification2'] = num_test2
        request.session['selected_panification3'] = num_test3
        selected_panification1 = request.session['selected_panification1']
        selected_panification2 = request.session['selected_panification2']
        selected_panification3 = request.session['selected_panification3']
        Panificationss1 = Panification.objects.get(num_test = selected_panification1)
        Panificationss2 = Panification.objects.get(num_test = selected_panification2)
        Panificationss3 = Panification.objects.get(num_test = selected_panification3)
        rep1=Panificationss1.num_repetition
        rep2=Panificationss2.num_repetition
        rep3=Panificationss3.num_repetition
        lev1 = Panificationss1.levain.code_levain
        lev2 = Panificationss2.levain.code_levain
        lev3 = Panificationss3.levain.code_levain


        traitement = TraitementDonneesBrute(Panificationss1)
        df1 = traitement['dft']
        colonne1=df1['DRC/Kg_pate'].astype(float)


        traitement = TraitementDonneesBrute(Panificationss2)
        df2 = traitement['dft']
        colonne2=df2['DRC/Kg_pate'].astype(float)


        traitement = TraitementDonneesBrute(Panificationss3)
        df3 = traitement['dft']
        colonne3=df3['DRC/Kg_pate'].astype(float)
         
        colonne0=df3['Temps - min'].astype(float)

    
        df = pd.DataFrame({f'DRC/Kgpate_{lev1}-R{rep1}': colonne1, f'DRC/Kg pate_{lev2}-R{rep2}': colonne2, f'DRC/Kg_pate_{lev3}-R{rep3}':colonne3})
        moyenne_colonnes = df.mean(axis=1)
        df['moyenne'] = moyenne_colonnes
        df['moyenne']=df['moyenne'].astype(float)
        dft= pd.concat([colonne0, df], axis=1)
        dft.dropna(inplace = True)

        datas7 = dft.to_dict(orient='records')
        request.session['dft7'] = datas7

        dft=dft.round(3).applymap('{:.3f}'.format)
        columns = dft.columns
        rows = dft.values.tolist()
        context = {
            'Panifications':Panifications,
            'columns':columns,
            'rows':rows,                  
            }
    html_template = loader.get_template('home/parametre_drc_kgpate.html')
    return HttpResponse(html_template.render(context, request))




@login_required(login_url="/login/")
def GrapheParametreDRC_Kg_pate(request):
     datas7 = request.session['dft7'] 
     return JsonResponse(datas7, safe=False)





@login_required(login_url="/login/")
def ParametreCO2_Prod(request):
     
    Panifications = Panification.objects.select_related('levain','technique').all()
    
    context = {
        'Panifications':Panifications,
    }
    if request.method == 'POST':
         
        num_test1 =request.POST.get('panif1')
        num_test2 =request.POST.get('panif2')
        num_test3 =request.POST.get('panif3')
        request.session['selected_panification1'] = num_test1
        request.session['selected_panification2'] = num_test2
        request.session['selected_panification3'] = num_test3
        selected_panification1 = request.session['selected_panification1']
        selected_panification2 = request.session['selected_panification2']
        selected_panification3 = request.session['selected_panification3']
        Panificationss1 = Panification.objects.get(num_test = selected_panification1)
        Panificationss2 = Panification.objects.get(num_test = selected_panification2)
        Panificationss3 = Panification.objects.get(num_test = selected_panification3)
        rep1=Panificationss1.num_repetition
        rep2=Panificationss2.num_repetition
        rep3=Panificationss3.num_repetition
        lev1 = Panificationss1.levain.code_levain
        lev2 = Panificationss2.levain.code_levain
        lev3 = Panificationss3.levain.code_levain


        traitement = TraitementDonneesBrute(Panificationss1)
        df1 = traitement['dft']
        colonne1=df1['CO2_L/Kg_pate'].astype(float)


        traitement = TraitementDonneesBrute(Panificationss2)
        df2 = traitement['dft']
        colonne2=df2['CO2_L/Kg_pate'].astype(float)


        traitement = TraitementDonneesBrute(Panificationss3)
        df3 = traitement['dft']
        colonne3=df3['CO2_L/Kg_pate'].astype(float)
         
        colonne0=df3['Temps - min'].astype(float)

    
        df = pd.DataFrame({f'CO2_Prod {lev1}-R{rep1}': colonne1, f'CO2 Prod_{lev2}-R{rep2}': colonne2, f'CO2_Prod_{lev3}-R{rep3}':colonne3})
        moyenne_colonnes = df.mean(axis=1)
        df['moyenne'] = moyenne_colonnes
        df['moyenne']=df['moyenne'].astype(float)
        dft= pd.concat([colonne0, df], axis=1)
        dft.dropna(inplace = True)

        datas8 = dft.to_dict(orient='records')
        request.session['dft8'] = datas8

        dft=dft.round(3).applymap('{:.3f}'.format)
        columns = dft.columns
        rows = dft.values.tolist()
        context = {
            'Panifications':Panifications,
            'columns':columns,
            'rows':rows,                  
            }
    html_template = loader.get_template('home/parametre_co2_prod.html')
    return HttpResponse(html_template.render(context, request))





@login_required(login_url="/login/")
def GrapheParametreCO2prod(request):
     datas8 = request.session['dft8'] 
     return JsonResponse(datas8, safe=False)





@login_required(login_url="/login/")
def ParametreCO2_Vitesse(request):
     
    Panifications = Panification.objects.select_related('levain','technique').all()
    
    context = {
        'Panifications':Panifications,
    }
    if request.method == 'POST':
         
        num_test1 =request.POST.get('panif1')
        num_test2 =request.POST.get('panif2')
        num_test3 =request.POST.get('panif3')
        request.session['selected_panification1'] = num_test1
        request.session['selected_panification2'] = num_test2
        request.session['selected_panification3'] = num_test3
        selected_panification1 = request.session['selected_panification1']
        selected_panification2 = request.session['selected_panification2']
        selected_panification3 = request.session['selected_panification3']
        Panificationss1 = Panification.objects.get(num_test = selected_panification1)
        Panificationss2 = Panification.objects.get(num_test = selected_panification2)
        Panificationss3 = Panification.objects.get(num_test = selected_panification3)
        rep1=Panificationss1.num_repetition
        rep2=Panificationss2.num_repetition
        rep3=Panificationss3.num_repetition
        lev1 = Panificationss1.levain.code_levain
        lev2 = Panificationss2.levain.code_levain
        lev3 = Panificationss3.levain.code_levain


        traitement = TraitementDonneesBrute(Panificationss1)
        df1 = traitement['dft']
        colonne1=df1['Vitesse_production_CO2_ml/100g/h'].astype(float)


        traitement = TraitementDonneesBrute(Panificationss2)
        df2 = traitement['dft']
        colonne2=df2['Vitesse_production_CO2_ml/100g/h'].astype(float)


        traitement = TraitementDonneesBrute(Panificationss3)
        df3 = traitement['dft']
        colonne3=df3['Vitesse_production_CO2_ml/100g/h'].astype(float)
         
        colonne0=df3['Temps - min'].astype(float)

    
        df = pd.DataFrame({f'Vitesse _production CO2 ml/100g/h {lev1}-R{rep1}': colonne1, f'Vitesse production_CO2 ml/100g/h {lev2}-R{rep2}': colonne2, f'Vitesse_production_CO2 ml/100g/h {lev3}-R{rep3}':colonne3})
        moyenne_colonnes = df.mean(axis=1)
        df['moyenne'] = moyenne_colonnes
        df['moyenne']=df['moyenne'].astype(float)
        dft= pd.concat([colonne0, df], axis=1)
        dft.dropna(inplace = True)

        datas9 = dft.to_dict(orient='records')
        request.session['dft9'] = datas9

        dft=dft.round(3).applymap('{:.3f}'.format)
        columns = dft.columns
        rows = dft.values.tolist()
        context = {
            'Panifications':Panifications,
            'columns':columns,
            'rows':rows,                  
            }
    html_template = loader.get_template('home/parametre_co2_vit.html')
    return HttpResponse(html_template.render(context, request))




@login_required(login_url="/login/")
def GrapheParametreCO2_Vitesse(request):
     datas9 = request.session['dft9'] 
     return JsonResponse(datas9, safe=False)





@login_required(login_url="/login/")
def ParametreEthanol_Prod(request):
     
    Panifications = Panification.objects.select_related('levain','technique').all()
    
    context = {
        'Panifications':Panifications,
    }
    if request.method == 'POST':
         
        num_test1 =request.POST.get('panif1')
        num_test2 =request.POST.get('panif2')
        num_test3 =request.POST.get('panif3')
        request.session['selected_panification1'] = num_test1
        request.session['selected_panification2'] = num_test2
        request.session['selected_panification3'] = num_test3
        selected_panification1 = request.session['selected_panification1']
        selected_panification2 = request.session['selected_panification2']
        selected_panification3 = request.session['selected_panification3']
        Panificationss1 = Panification.objects.get(num_test = selected_panification1)
        Panificationss2 = Panification.objects.get(num_test = selected_panification2)
        Panificationss3 = Panification.objects.get(num_test = selected_panification3)
        rep1=Panificationss1.num_repetition
        rep2=Panificationss2.num_repetition
        rep3=Panificationss3.num_repetition
        lev1 = Panificationss1.levain.code_levain
        lev2 = Panificationss2.levain.code_levain
        lev3 = Panificationss3.levain.code_levain


        traitement = TraitementDonneesBrute(Panificationss1)
        df1 = traitement['dft']
        colonne1=df1['Ethanol_L/kg_pate'].astype(float)


        traitement = TraitementDonneesBrute(Panificationss2)
        df2 = traitement['dft']
        colonne2=df2['Ethanol_L/kg_pate'].astype(float)


        traitement = TraitementDonneesBrute(Panificationss3)
        df3 = traitement['dft']
        colonne3=df3['Ethanol_L/kg_pate'].astype(float)
         
        colonne0=df3['Temps - min'].astype(float)

    
        df = pd.DataFrame({f'Ethanol_Prod {lev1}-R{rep1}': colonne1, f'Ethanol Prod_{lev2}-R{rep2}': colonne2, f'Ethanol_Prod_{lev3}-R{rep3}':colonne3})
        moyenne_colonnes = df.mean(axis=1)
        df['moyenne'] = moyenne_colonnes
        df['moyenne']=df['moyenne'].astype(float)
        dft= pd.concat([colonne0, df], axis=1)
        dft.dropna(inplace = True)

        datas10 = dft.to_dict(orient='records')
        request.session['dft10'] = datas10

        dft=dft.round(3).applymap('{:.3f}'.format)
        columns = dft.columns
        rows = dft.values.tolist()
        context = {
            'Panifications':Panifications,
            'columns':columns,
            'rows':rows,                  
            }
    html_template = loader.get_template('home/parametre_ethanol_prod.html')
    return HttpResponse(html_template.render(context, request))





@login_required(login_url="/login/")
def GrapheParametreEthanolprod(request):
     datas10 = request.session['dft10'] 
     return JsonResponse(datas10, safe=False)





@login_required(login_url="/login/")
def ParametreEthanol_Vitesse(request):
     
    Panifications = Panification.objects.select_related('levain','technique').all()
    
    context = {
        'Panifications':Panifications,
    }
    if request.method == 'POST':
         
        num_test1 =request.POST.get('panif1')
        num_test2 =request.POST.get('panif2')
        num_test3 =request.POST.get('panif3')
        request.session['selected_panification1'] = num_test1
        request.session['selected_panification2'] = num_test2
        request.session['selected_panification3'] = num_test3
        selected_panification1 = request.session['selected_panification1']
        selected_panification2 = request.session['selected_panification2']
        selected_panification3 = request.session['selected_panification3']
        Panificationss1 = Panification.objects.get(num_test = selected_panification1)
        Panificationss2 = Panification.objects.get(num_test = selected_panification2)
        Panificationss3 = Panification.objects.get(num_test = selected_panification3)
        rep1=Panificationss1.num_repetition
        rep2=Panificationss2.num_repetition
        rep3=Panificationss3.num_repetition
        lev1 = Panificationss1.levain.code_levain
        lev2 = Panificationss2.levain.code_levain
        lev3 = Panificationss3.levain.code_levain


        traitement = TraitementDonneesBrute(Panificationss1)
        df1 = traitement['dft']
        colonne1=df1['Vitesse_production_Ethanol_ml/100g/h'].astype(float)


        traitement = TraitementDonneesBrute(Panificationss2)
        df2 = traitement['dft']
        colonne2=df2['Vitesse_production_Ethanol_ml/100g/h'].astype(float)


        traitement = TraitementDonneesBrute(Panificationss3)
        df3 = traitement['dft']
        colonne3=df3['Vitesse_production_Ethanol_ml/100g/h'].astype(float)
         
        colonne0=df3['Temps - min'].astype(float)

    
        df = pd.DataFrame({f'Vitesse _production Ethanol ml/100g/h {lev1}-R{rep1}': colonne1, f'Vitesse production_Ethanol ml/100g/h {lev2}-R{rep2}': colonne2, f'Vitesse_production_Ethanol ml/100g/h {lev3}-R{rep3}':colonne3})
        moyenne_colonnes = df.mean(axis=1)
        df['moyenne'] = moyenne_colonnes
        df['moyenne']=df['moyenne'].astype(float)
        dft= pd.concat([colonne0, df], axis=1)
        dft.dropna(inplace = True)

        datas11 = dft.to_dict(orient='records')
        request.session['dft11'] = datas11

        dft=dft.round(3).applymap('{:.3f}'.format)
        columns = dft.columns
        rows = dft.values.tolist()
        context = {
            'Panifications':Panifications,
            'columns':columns,
            'rows':rows,                  
            }
    html_template = loader.get_template('home/parametre_ethanol_vit.html')
    return HttpResponse(html_template.render(context, request))




@login_required(login_url="/login/")
def GrapheParametreEthanolVitesse(request):
     datas11 = request.session['dft11'] 
     return JsonResponse(datas11, safe=False)





@login_required(login_url="/login/")
def Parametre_pH_Att(request):
     
    Panifications = Panification.objects.select_related('levain','technique').all()
    
    context = {
        'Panifications':Panifications,
    }
    if request.method == 'POST':
         
        num_test1 =request.POST.get('panif1')
        num_test2 =request.POST.get('panif2')
        num_test3 =request.POST.get('panif3')
        request.session['selected_panification1'] = num_test1
        request.session['selected_panification2'] = num_test2
        request.session['selected_panification3'] = num_test3
        selected_panification1 = request.session['selected_panification1']
        selected_panification2 = request.session['selected_panification2']
        selected_panification3 = request.session['selected_panification3']
        Panificationss1 = Panification.objects.get(num_test = selected_panification1)
        Panificationss2 = Panification.objects.get(num_test = selected_panification2)
        Panificationss3 = Panification.objects.get(num_test = selected_panification3)
        rep1=Panificationss1.num_repetition
        rep2=Panificationss2.num_repetition
        rep3=Panificationss3.num_repetition
        lev1 = Panificationss1.levain.code_levain
        lev2 = Panificationss2.levain.code_levain
        lev3 = Panificationss3.levain.code_levain

       
        traitement = TraitementDonneesBrute(Panificationss1)
        df1 = traitement['dft']
        colonne1=df1['pH/ATT'].astype(float)


        traitement = TraitementDonneesBrute(Panificationss2)
        df2 = traitement['dft']
        colonne2=df2['pH/ATT'].astype(float)


        traitement = TraitementDonneesBrute(Panificationss3)
        df3 = traitement['dft']
        colonne3=df3['pH/ATT'].astype(float)
         
        colonne0=df3['Temps - min'].astype(float)

    
        df = pd.DataFrame({f'Att {lev1}-R{rep1}': colonne1, f'Att-{lev2}-R{rep2}': colonne2, f'Att_{lev3}-R{rep3}':colonne3})
        moyenne_colonnes = df.mean(axis=1)
        df['moyenne'] = moyenne_colonnes
        df['moyenne']=df['moyenne'].astype(float)
        dft= pd.concat([colonne0, df], axis=1)
        dft.dropna(inplace = True)

        datas12 = dft.to_dict(orient='records')
        request.session['dft12'] = datas12

        dft=dft.round(3).applymap('{:.3f}'.format)
        columns = dft.columns
        rows = dft.values.tolist()
        context = {
            'Panifications':Panifications,
            'columns':columns,
            'rows':rows,                  
            }
    html_template = loader.get_template('home/parametre_att_ph.html')
    return HttpResponse(html_template.render(context, request))




@login_required(login_url="/login/")
def GrapheParametrepHAtt(request):
     datas12 = request.session['dft12'] 
     return JsonResponse(datas12, safe=False)





@login_required(login_url="/login/")
def ParametrepH_g_pate(request):
     
    Panifications = Panification.objects.select_related('levain','technique').all()
    
    context = {
        'Panifications':Panifications,
    }
    if request.method == 'POST':
         
        num_test1 =request.POST.get('panif1')
        num_test2 =request.POST.get('panif2')
        num_test3 =request.POST.get('panif3')
        request.session['selected_panification1'] = num_test1
        request.session['selected_panification2'] = num_test2
        request.session['selected_panification3'] = num_test3
        selected_panification1 = request.session['selected_panification1']
        selected_panification2 = request.session['selected_panification2']
        selected_panification3 = request.session['selected_panification3']
        Panificationss1 = Panification.objects.get(num_test = selected_panification1)
        Panificationss2 = Panification.objects.get(num_test = selected_panification2)
        Panificationss3 = Panification.objects.get(num_test = selected_panification3)
        rep1=Panificationss1.num_repetition
        rep2=Panificationss2.num_repetition
        rep3=Panificationss3.num_repetition
        lev1 = Panificationss1.levain.code_levain
        lev2 = Panificationss2.levain.code_levain
        lev3 = Panificationss3.levain.code_levain


        traitement = TraitementDonneesBrute(Panificationss1)
        df1 = traitement['dft']
        colonne1=df1['pH/g_pate'].astype(float)


        traitement = TraitementDonneesBrute(Panificationss2)
        df2 = traitement['dft']
        colonne2=df2['pH/g_pate'].astype(float)


        traitement = TraitementDonneesBrute(Panificationss3)
        df3 = traitement['dft']
        colonne3=df3['pH/g_pate'].astype(float)
         
        colonne0=df3['Temps - min'].astype(float)

    
        df = pd.DataFrame({f'DRC/Kgpate_{lev1}-R{rep1}': colonne1, f'DRC/Kg pate_{lev2}-R{rep2}': colonne2, f'DRC/Kg_pate_{lev3}-R{rep3}':colonne3})
        moyenne_colonnes = df.mean(axis=1)
        df['moyenne'] = moyenne_colonnes
        df['moyenne']=df['moyenne'].astype(float)
        dft= pd.concat([colonne0, df], axis=1)
        dft.dropna(inplace = True)

        datas13 = dft.to_dict(orient='records')
        request.session['dft13'] = datas13

        dft=dft.round(3).applymap('{:.3f}'.format)
        columns = dft.columns
        rows = dft.values.tolist()
        context = {
            'Panifications':Panifications,
            'columns':columns,
            'rows':rows,                  
            }
    html_template = loader.get_template('home/parametre_ph_gpate.html')
    return HttpResponse(html_template.render(context, request))




@login_required(login_url="/login/")
def GrapheParametrepH_g_pate(request):
     datas13 = request.session['dft13'] 
     return JsonResponse(datas13, safe=False)






@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
    


















