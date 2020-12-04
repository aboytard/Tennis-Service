import matplotlib.pyplot as plt
import numpy as np
import itertools
import pickle
import time

x0=np.array([1.0,2.0])
A=np.array([[2.0,0.5],[0.5,1.0]])
b=np.array([-1.0,-2.0])
c=np.zeros(1)
pas=1.0e-2
e=1.0e-10

fonction={'A':A, 'b':b, 'c':c}

##A=np.array([[2.0,0.5],[0.5,1.0]])
##print(A)
##X=np.array([2.0,1.0])
##b=np.array([-1.0,-2.0])

##méthode d'évaluation de la fonction f
def function(A,b,c,X) :
    shape=X[0].shape
    print(shape)
    Z=np.zeros_like(X[0])
    print(Z)
    for item in itertools.product(*map(range,shape)):
        vect=list()
        for elem in X:
            vect.append(elem[item])
        vec=np.array(vect,ndmin=1)
        print(vec)
        Z[item]=0.5*np.dot(vec.T,A.dot(vec))-np.dot(vec.T,b) + c
    return Z

##calcul du gradient
def gradient(A,b,x):
    
    return A.dot(x)-b

##méthode de la descente de gradient à pas fixe
def pas_fixe(x0,fonction,pas,e,itermax):
    print (fonction)
    A=fonction['A']
    b=fonction['b']
    c=fonction['c']

    #***** Initialisation *****
    X=[x0]
    dir=-gradient(A,b,x0)
    residu= [np.linalg.norm(gradient(A,b,x0))]

    k=0
    while residu[k]>e and k<itermax:
        #----- Calcul de x(k+1) -----
        X.append([X[-1]+pas*dir])
        print(X[-1])
        #----- Calcul de la nouvelle direction de descente d(x+1) -----
        dir = (-1)*gradient(A,b,X[k+1])
        print('yototo')
        print(dir)
        #----- Calcul du residu r(k+1) -----
        residu.append(np.linalg.norm(dir))
        print(residu)
        k+=1
        return {'X':np.asarray(X),'residu':np.asarray(residu)}


##méthode de la descente de gradient à pas variable
    


