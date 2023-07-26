# -*- encoding: utf-8 -*-


from django.urls import path, re_path
from apps.home import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),



    
    path('import_excel.html', views.Import_excel, name='/import_excel.html'),
    path('enregistrementdata', views.Enregistrementdata, name='enregistrementdata'),
    path('lire_ingredient.html', views.AffichageIngredient, name='/lire_ingredient.html'),
    path('entrer_ingredient.html', views.EnregistrementIngredient, name='/entrer_ingredient.html'),
    path('lire_levains.html', views.AffichageLevain, name='/lire_levains.html'),
    path('levain.html/<str:pk>/', views.VoirLevain, name='/levain.html'),
    path('levainpdf.html/<str:pk>/', views.TelechagerLevain, name='/levainpdf.html'),
    path('panification.html/<str:pk>/', views.VoirPanification, name='/panification.html'),
    path('panificationpdf.html/<str:pk>/', views.TelechagerPanification, name='/panificationpdf.html'),
    path('entrer_levain.html', views.EnregistrementLevain, name='/entrer_levain.html'),
    path('lire_techniquerafraichissement.html', views.AffichageTechniqueRafraichissement, name='/lire_techniquerafraichissement.html'),
    path('entrer_techniquerafraichissement.html', views.EnregistrementTechniqueRafraichissement, name='/entrer_techniquerafraichissement.html'),
    path('lire_rafraichissement.html', views.AffichageRafraichissement, name='/lire_rafraichissement.html'),
    path('entrer_rafraichissement.html', views.EnregistrementRafraichissement, name='/entrer_rafraichissement.html'),
    path('lire_caracterisationlevain.html', views.AffichageCaraterisationLevain, name='/lire_caracterisationlevain.html'),
    path('entrer_caracterisationlevain.html', views.EnregistrementCaracterisationLevain, name='/entrer_caracterisationlevain.html'),
    path('lire_caracterisationpanification.html', views.AffichageCaraterisationPanification, name='/lire_caracterisationpanification.html'),
    path('entrer_caracterisationpanification.html', views.EnregistrementCaracterisationPanification, name='/entrer_caracterisationpanification.html'),
    path('lire_techniquepanification.html', views.AffichageTechniquePanification, name='/lire_techniquepanification.html'),
    path('entrer_techniquepanification.html', views.EnregistrementTechniquePanification, name='/entrer_techniquepanification.html'),
    path('lire_panification.html', views.AffichagePanification, name='/lire_panification.html'),
    path('entrer_panification.html', views.EnregistrementPanification, name='/entrer_panification.html'),
    path('tabledonneebrute.html', views.Affichagedonneebrute, name='/tabledonneebrute.html'),
    path('affichagegraphedonneebrute', views.Affichagegraphedonneebrute, name='affichagegraphedonneebrute'),
    path('tabledonneecalcule.html', views.Affichagedonneecalcule, name='/tabledonneecalcule.html'),
    path('affichagegraphedonneecalcule', views.Affichagegraphedonneecalcule, name='affichagegraphedonneecalcule'),
    path('recapitulationdonnees.html', views.Recapitulationdonnees, name='/recapitulationdonnees.html'),
    path('recappdf.html', views.TelechagerRecapitulationdonnees, name='/recappdf.html'),
    path('donneesstat.html', views.DonneesStatistiques, name='/donneesstat.html'),
    path('parametre_panif.html', views.Parametrepanification, name='/parametre_panif.html'),
    path('grapheparametrepanif', views.GrapheParametrepanification, name='grapheparametrepanif'),
    path('parametre_co2.html', views.ParametreCO2, name='/parametre_co2.html'),
    path('grapheparametreco2', views.GrapheParametreCO2, name='grapheparametreco2'),
    path('parametre_distance.html', views.ParametreDistance, name='/parametre_distance.html'),
    path('grapheparametredistance', views.GrapheParametreDistance, name='grapheparametredistance'),
    path('parametre_ethanol.html', views.ParametreEthanol, name='/parametre_ethanol.html'),
    path('grapheparametreethanol', views.GrapheParametreEthanol, name='grapheparametreethanol'),
    path('parametre_ph.html', views.ParametrePh, name='/parametre_ph.html'),
    path('grapheparametreph', views.GrapheParametrePh, name='grapheparametreph'),
    path('parametre_massebrute.html', views.ParametreMasseBrute, name='/parametre_massebrute.html'),
    path('grapheparametremassebrute', views.GrapheParametreMasseBrute, name='grapheparametremassebrute'),
    path('parametre_att.html', views.ParametreAtt, name='/parametre_att.html'),
    path('grapheparametreatt', views.GrapheParametreAtt, name='grapheparametreatt'),
    path('parametre_drc_kgpate.html', views.ParametreDRC_Kg_pate, name='/parametre_drc_kgpate.html'),
    path('grapheparametredrckgpate', views.GrapheParametreDRC_Kg_pate, name='grapheparametredrckgpate'),
    path('parametre_co2_vit.html', views.ParametreCO2_Vitesse, name='/parametre_co2_vit.html'),
    path('grapheparametreco2vitesse', views.GrapheParametreCO2_Vitesse, name='grapheparametreco2vitesse'), 
    path('parametre_co2_prod.html', views.ParametreCO2_Prod, name='/parametre_co2_prod.html'),
    path('grapheparametreco2prod', views.GrapheParametreCO2prod, name='grapheparametreco2prod'),
    path('parametre_ethanol_vit.html', views.ParametreEthanol_Vitesse, name='/parametre_ethanol_vit.html'),
    path('grapheparametreethanolvitesse', views.GrapheParametreEthanolVitesse, name='grapheparametreethanolvitesse'), 
    path('parametre_ethanol_prod.html', views.ParametreEthanol_Prod, name='/parametre_ethanol_prod.html'),
    path('grapheparametreethanolprod', views.GrapheParametreEthanolprod, name='grapheparametreethanolprod'),
    path('parametre_att_ph.html', views.Parametre_pH_Att, name='/parametre_att_ph.html'),
    path('grapheparametrephatt', views.GrapheParametrepHAtt, name='grapheparametrephatt'),
    path('parametre_ph_gpate.html', views.ParametrepH_g_pate, name='/parametre_ph_gpate.html'),
    path('grapheparametrephgpate', views.GrapheParametrepH_g_pate, name='grapheparametrephgpate'),

    path('telecharger/', views.telecharger_fichierexcel, name='telecharger_fichierexcel'),
    path('telechargers/', views.telecharger_fichierprocedure, name='telecharger_fichierprocedure'),
    path('grapheindexco2', views.AffichagegrapheindexCO2, name='grapheindexco2'),
    path('grapheindexdrc', views.AffichagegrapheindexDRC, name='grapheindexdrc'),
    path('grapheindexethanol', views.AffichagegrapheindexEthanol, name='grapheindexethanol'),
    path('grapheindexph', views.Affichagegrapheindexph, name='grapheindexph'),





    # Matches any html file
    re_path(r'^.*\.*', views.pages, name='pages'),


]

