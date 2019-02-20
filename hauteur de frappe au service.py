
import numpy as np
import matplotlib.pyplot as plt
import math
from math import pi


#################################################################################
                ###### MODELES DE SERVICES ########
#################################################################################

##### modèle du service à plat
### Calcul de la trajectoire et de la vitesse instantanée de la balle par méthode d'Euler

## Paramètres d'entrée :
# v : vitesse de translation (m/s)
# i : angle d'incidence (Â°)
# h : hauteur de frappe du service (m)
# pas : pas temporelle de la méthode d'Euler (s)

## Données de sortie:
# (X,Y) : liste des coordonnées (x,y) de position de la balle Ã  chaque instant d'intervalle pas
# (Vx,Vy) : liste des vitesses instantannées (vx, vy) de la balle Ã  chaque instant d'intervalle pas

# Constantes physiques (valeurs numériques)
A=1.1*10**(-3) # Constante dans la formule de trainée (N.s/mÂ²) Formule : A=0.5*pi*p*S*Cx
m=57*10**(-3) # Masse de la balle (kg)
g=9.81 #Constante de pesanteur (N/kgÂ²)
R=0.03 # Rayon de la balle (m)

# Calcul de l'accélération en x et y - Avec Trainée uniquement 
def Traineex(vx,vy):
    return (-0.5*A*(vx**2+vy**2)**(1/2)*vx)/m
def Traineey(vx,vy):
    return ((-0.5*A*(vx**2+vy**2)**(1/2)*vy)/m-g)
# Calcul trajectoire et vitesse instantanée

def vitesse(v,i,h,pas):
    xi=0 # Coordonnée initiale : abscisse
    yi=h # Coordonnée initiale : ordonnée
    X=[xi] # Initialisation : liste des abscisses
    Y=[yi] # Initialisation : liste des ordonnées
    vx=math.cos(i)*v # Vitesse initiale x
    vy=math.sin(i)*v # Vitesse initiale y
    Vx=[vx] #Initialisation : liste des vitesses (x)
    Vy=[vy] #Initialisation : liste des vitesses (y)
    t=0 # temps initial
    T=[t] # Initialisation : liste des temps
    k=0 # Indice d'indentation
    ax=0 # Initialisation : accélération (x)
    ay=0 # Initialisation : accélération (y)
    while Y[k]>0.01:
        ax= Traineex(Vx[k],Vy[k])
        ay=Traineey(Vx[k],Vy[k])
        vx+=ax*pas
        vy+=ay*pas
        t+=pas
        xi+=vx*pas
        yi+=vy*pas
        X.append(xi)
        Y.append(yi)
        Vx.append(vx)
        Vy.append(vy)
        T.append(t)
        k+=1
    return (Vx,Vy,X,Y,T)


##### Modèle du second service (lifté)
### Calcul de la trajectoire et de la vitesse instantanée de la balle par méthode d'Euler
### Même méthode que pour le service Ã  plat avec en plus la prise en compte de l'effet Magnus
# Paramètre d'entrée supplémentaire :
# w : vitesse de rotation (tours/min)

# Coefficient de l'effet Magnus
a=0.5* np.pi *(0.03)**3
# Calcul de l'accélération en x et y - Avec Trainée et effet Magnus
def Magnusy(vx,vy,w):
    return ((-0.5*A*(vx**2+vy**2)**0.5 * vy - a*w*vx)/m - g)
def Magnusx(vx,vy,w):
    return ((-0.5*A*(vx**2+vy**2)**0.5 * vx + a*w*vy)/m)

def vitesse1(v,i,h,pas,w): # i est l'angle d'incidence initiale
    xi=0
    yi=h
    X=[xi] ## liste des abscisses
    Y=[yi] ## liste des ordonnées
    vx=math.cos(i)*v
    vy=math.sin(i)*v
    Vx=[vx]     ## liste des vitesses en abscisses
    Vy=[vy]
    t=0
    T=[t]
    k=0
    ax=0
    ay=0
    while Y[k]>0.01:
        ax= Magnusx(Vx[k],Vy[k],w)
        ay= Magnusy(Vx[k],Vy[k],w)
        vx+=ax*pas
        vy+=ay*pas
        t+=pas
        xi+=vx*pas
        yi+=vy*pas
        X.append(xi)
        Y.append(yi)
        Vx.append(vx)
        Vy.append(vy)
        T.append(t)
        k+=1
        if k >= 500:
            return (Vx,Vy,X,Y,T)
    return (Vx,Vy,X,Y,T)

#################################################################################
                ###### REPRESENTATION GRAPHIQUE ########
#################################################################################

##### Simulation des trajectoires pour le premier et le second modèle(avec effet Magnus)
# Tracé de la trajectoire de la balle
# Tracé du filet et des limites du terrain
def trajectoire1(v,i,h,pas,w):
    Vx,Vy,X,Y,T=vitesse1(v,i,h,pas,w)
    plt.plot(X,Y,'b-o')
    plt.plot(2*[11.8], [0, 0.914], c = 'r', linewidth = 3)
    #plt.plot(2*[11.8+6.4], [0, 0.1], c = 'k', linewidth = 3)
    #plt.plot(2*[23.6], [0, 0.1], c = 'k', linewidth = 3)

trajectoire1(150/3.6,-5.*np.pi/180.,3.3,0.01,0)
trajectoire1(124/3.6,1.*np.pi/180.,2.5,0.01,1397.*np.pi/30.)
plt.ylim([-0.2,3.3])
plt.show()

#################################################################################
                ###### DETERMINATION HAUTEUR OPTIMALE ########
#################################################################################

##### Programme récursif permettant d'obtenir la hauteur optimale
## Paramètres d'entrée : vitesse de translation (v), angle d'incidence (i),
# hauteur initiale(h), pas temporel (pas), vitesse de rotation (w)
## Sortie : hauteur optimale (h) obtenue par récurrence
# Tous les paramètres en unités SI

def filet(X,a):
    j=0
    for i in X:
        if i<a:
            j+=1
        else:
            return j
    return j

def hauteur(v,i,h,pas,w):
    try:
        Vx,Vy,X,Y,T=vitesse1(v,i,h,pas,w)
        p=filet(X,11.8)
        if h >= 10.: return h
        if p==len(X): # tombe dans son propre terrain
            return hauteur(v,i,h+0.1,pas,w)
        t=len(Y)-1
        while Y[p]<0.914 or X[t]<11.8+6.4:
            return hauteur(v,i,h+0.1,pas,w)
        return h
    except RecursionError: return h

##### Instruction pour avoir le graphique des hauteurs
incidence = -1. * np.pi / 180.
pas       = 0.01
href      = 1.

wmin, wmax = 0., 5000.
vmin, vmax = 50., 300.

MapHauteur = []
ListRot = np.arange(wmin, wmax, 250)
ListTrans = np.arange(vmin, vmax, 10.)
for w in ListRot:
    mapH = []

    for v in ListTrans:
        ##print(w, v)
        mapH.append(hauteur(v /3.6, incidence, href, pas, w*np.pi/30.))
    MapHauteur.append(mapH)

MapHauteur = np.array(MapHauteur)

plt.contourf(ListTrans, ListRot, MapHauteur, levels = np.arange(1.5, 3.8, 0.2))
plt.colorbar()
plt.xlabel('vitesse de translation(km/h)')
plt.ylabel('vitesse de rotation(tr/min)')
plt.title('Graphe de la hauteur optimale en fonction des paramÃ¨tres')
plt.show()

