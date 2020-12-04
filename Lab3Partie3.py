# -*- coding: utf-8 -*-
"""
Created on Sat Apr  4 14:21:03 2020

@author: alban
"""
import sqlite3

from sqlite3 import Error


def sql_connection(): # établir la connexion avec la db

    try:

        con = sqlite3.connect('D:\Ecole Quarantaine\Informatique\Lab\Lab3\Partie3\Lab3Partie3.db')

        return con

    except Error:

        print(Error)

def sql_table(con): # créer la table dans la db

    cursorObj = con.cursor()

    cursorObj.execute("CREATE TABLE if not exists Lab3Partie3(id integer, date datetime , latitude real, longitude real)")

    con.commit()
    
def sql_table_mobile(con): # créer la table dans la db

    cursorObj = con.cursor()

    cursorObj.execute("CREATE table if not EXISTS mobile as SELECT DISTINCT id,'mobile' || id from Lab3Partie3 order by id")

    con.commit()
    
def sql_table_drop(con): # supprimer la table dans la db
    
    cursorObj = con.cursor()

    cursorObj.execute("DROP TABLE Lab3Partie3")

    con.commit()

def sql_insert(con, entities): # insérer des données dans la table

    cursorObj = con.cursor()
    
    cursorObj.execute('INSERT INTO Lab3Partie3(id, date, latitude, longitude) VALUES(?, ?, ?, ?)', entities)
    
    con.commit()
    
def sql_insert_mobile(con, entities): # insérer des données dans la table

    cursorObj = con.cursor()
    
    cursorObj.execute('INSERT INTO mobile(id, nom) VALUES(?, ?)', entities)
    
    con.commit()
    

  
def sql_fetch(con): #récupérer un jeu de données de la db

    cursorObj = con.cursor()

    cursorObj.execute('SELECT * FROM Lab3Partie3')
#    cursorObj.execute('SELECT id, name FROM employees WHERE salary > 800.0')
    rows = cursorObj.fetchall() # le fetch correspond aux enregistrements de ma table

    for row in rows:

        print(row)
        
#################################################
    
con = sql_connection() ## ouverture du lien avec la db
#sql_table_drop(con)
sql_table(con) ## création de la table dans la db

#################################################          

def init_Positions(con,portableEnCours): ## permet de charger un tableau de positions pour le mobile i
    cursorObj = con.cursor()
    cursorObj.execute('SELECT date,latitude,longitude FROM Lab3Partie3 WHERE id =' + str(portableEnCours) + ' order by 1') ## voir comment prendre en compte le i
    rows = cursorObj.fetchall()
    k=0 ## pour tester sur 10 lignes
    # alpha = alpha(con,portableEnCours) comment utiliser plusieurs curseurs
    Positions =[]
    for row in rows:
        if k <=100 :        
            G = Position(row[0],row[1],row[2])
            Positions.append(G)
            k+=1
        else:
            pass
#            return True
#            return(latitude_point,longitude_point)
    return Positions
            

def affiche_position(con,positions):
    for position in positions:
        position.affiche()               

    ##################
class Position():
    
    def __init__(self,date,latitude,longitude):  ##constructeur objet
        
        self.date = date
        self.latitude = latitude
        self.longitude = longitude
        self.x = (float(self.longitude)- min_longitude)*rectangle_x/(max_longitude-min_longitude)
        self.y = (float(self.latitude)- min_latitude)*rectangle_y/(max_latitude-min_latitude) 
        ## voir comment translater dans la carte
        ## fixer l'origine du repère

        
        
    def modification(self,latitude,longitude,date):
        self.latitude = latitude
        self.longitude = longitude
        self.date = date
    
    def affiche(self):
        print('latitude = ', self.latitude)
        print('longitude = ', self.longitude)
        print('date =', self.date)
        print('x = '), self.x
    
    def transformer_coordonnees_x(self,x):
        self.x = self.longitude
    
    def transformer_coordonnees_y(self,y):
        self.y = self.latitude
    
    def dessiner_position(self,cannevas): ### à partir des propriétés de la position, va dessiner un point dans une fenêtre
        
        pass
###########################


############################ 
import tkinter as tk
## Travail sur écran        


def afficher_ecran1(monEcran1):  ## récupère une valeur d'un portable qu'on va utiliser en global

    global portableEnCours ## pour pouvoir utiliser une variable global dans la fonction
    
    canvas1 = tk.Canvas(monEcran1, width = 800, height = 800,  relief = 'raised')
    canvas1.pack()

    label1 = tk.Label(monEcran1, text='Sélection d un mobile')
    label1.config(font=('helvetica', 14))
    canvas1.create_window(200, 25, window=label1)
    
    text = tk.StringVar()
    text.set(str(portableEnCours))
    text_tb = tk.Entry (monEcran1, textvariable=text) 
    canvas1.create_window(200, 100, window=text_tb)    
    
    label2 = tk.Label(monEcran1, text='Resultat de la requête')
    label2.config(font=('helvetica', 10))
    canvas1.create_window(200, 140, window=label2)
    
    def ValiderMobile():
        global portableEnCours ## pour pouvoir modifier une variable globale dans une fonction
        global Positions
        portableEnCours = text_tb.get()
        Positions = init_Positions(con,portableEnCours)
        
    buttonValiderMobile = tk.Button(text='Enregistrer le mobile', command= ValiderMobile, bg='brown', fg='white', font=('helvetica', 9, 'bold'), height = 3, width = 3)    
    canvas1.create_window(600, 160, window=buttonValiderMobile)
 
def dessiner_canvasCercle(canvasCible,x,y,grosseurPoint):
    x1 = x + grosseurPoint
    y1 = y + grosseurPoint
    canvasCible.create_oval(x,y,x1,y1,width = 2,outline = "blue")
    


def afficher_ecran2(monEcran2):
    
    global portableEnCours
    global Positions
      
    canvas1 = tk.Canvas(monEcran2, width = 800, height = 800,  relief = 'raised')
    canvas1.pack()
    
#        for position in Positions:
#            position.affiche()
    label1 = tk.Label(monEcran2, text='On travaille sur le mobile n°' + str(portableEnCours))
    label1.config(font=('helvetica', 14))
    canvas1.create_window(200, 25, window=label1)
    
    label2 = tk.Label(monEcran2, text='Affichage du détail')
    label2.config(font=('helvetica', 10))
    canvas1.create_window(200, 100, window=label2)
    
    canvas2 = tk.Canvas(monEcran2, width = rectangle_x, height = rectangle_y, relief = 'raised',borderwidth = 1)
    canvas1.create_window(rectangle_x, rectangle_y, window=canvas2)

    for position in Positions:
        dessiner_canvasCercle(canvas2,position.x,position.y,1)
    canvas2.bind('<Button-1>',left_click)
    

def left_click(event): ## event est un objet non défini
    ## Quand l'évênement va être déclenché, le event s'instancie grâce au frameword du type click_souris
    X = event.x
    Y= event.y
    print(X)
    print(Y)
 ####################   



        
###########################        

def max_longitude(con,mobile):
    cursorObj = con.cursor()
    cursorObj.execute('Select max(longitude) from Lab3Partie3 where Id =' + str(mobile))
    rows = cursorObj.fetchall()
    return rows[0][0]
    
def min_longitude(con,mobile):
    cursorObj = con.cursor()
    cursorObj.execute('Select min(longitude) from Lab3Partie3 where Id =' + str(mobile))
    rows = cursorObj.fetchall()
    return rows[0][0]
    
def max_latitude(con,mobile):
    cursorObj = con.cursor()
    cursorObj.execute('Select max(latitude) from Lab3Partie3 where Id =' + str(mobile))
    rows = cursorObj.fetchall()
    return rows[0][0]

def min_latitude(con,mobile):
    cursorObj = con.cursor()
    cursorObj.execute('Select min(latitude) from Lab3Partie3 where Id =' + str(mobile))
    rows = cursorObj.fetchall()
    return rows[0][0]

# main

portableEnCours = 1
Positions = []
rectangle_x = 500
rectangle_y = 500
min_longitude= min_longitude(con,portableEnCours)
max_longitude= max_longitude(con,portableEnCours)
min_latitude= min_latitude(con,portableEnCours)
max_latitude= max_latitude(con,portableEnCours)



monEcran1 = tk.Tk()
afficher_ecran1(monEcran1)
monEcran1.mainloop()
 
# affilialie_coordonnées_x_position(con,portableEnCours,Positions) 

print("portable en cours vaut " + str(portableEnCours))
print(Positions)



monEcran2 = tk.Tk()
afficher_ecran2(monEcran2)
monEcran2.mainloop()  

# fin de main   
    
########################## 


### exemple plot de la courbe pour le mobile 1 sur les 100 premiers éléments

import matplotlib.pyplot as plt
import numpy as np






    
#def affilialie_coordonnées_y_position(con,mobile,position,beta):
#    beta = (max_latitude(con,mobile)-min_latitude(con,mobile))/500
#    #vérifier la taille de l'échelle avec la taille du cannevas
#    for position in Positions:
#        position.transformer_coordonnees_x(float(alpha*position.latitude))       
    
       
    
    
    
 



    

import csv

fname = "D:\Ecole Quarantaine\Informatique\Lab\Lab3\Partie3\donnees.csv"
file = open(fname,"r")

#cursorObj = con.cursor()
#cursorObj.execute("INSERT INTO Lab3Partie3 VALUES(5,'2017-01-04 15:45:00',5,17)") # test insert   
#con.commit() ## attention!! A ne surtout pas oublier, sinon les instructions précédentes ne sont pas prisese en compte dans la db

####### script pour remplir la bdd

#try : ## Attention j'ai supprimé manuellement la première ligne
#    reader = csv.reader(file)
#    i=0
#    for row in reader: 
#        if i !=0: ## on ne veut pas garder l'entête du fichier csv dans la bdd
#        A = row[0].split(';')
#        sql_insert(con,A)
#        i = 1
#finally:
#    file.close()    
#    
#sql_table_mobile(con)   
 
#####   


##affilialie_coordonnées_x_position(con,portableEnCours,Positions)## à affilier en même temps que la lecture de la bdd..

















    
    