import numpy as np
import matplotlib.pyplot as plt
import itertools
import pickle
import time

##données utilisées pour l'exercice TEST 1
x0=np.array([1.0,2.0])
A=np.array([[2.0,0.5],[0.5,1.0]])
b=np.array([-1.0,-2.0])
c=np.zeros(1)

fonction={'A':A, 'b':b, 'c':c}

## méthode d'évaluation de la fonction f

def function(A,b,c,xx):
    shape=xx[0].shape
    ZZ=np.zeros_like(xx[0])
    for item in itertools.product(*map(range,shape)):
        vect=list()
        for elem in xx:
            vect.append(elem[item])
        vec=np.array(vect,ndmin=1)
        ZZ[item]=0.5*np.dot(vec.T,A.dot(vec))-np.dot(vec.T,b) + c
    return ZZ

##méthode du gradient

def gradient(A,b,x):
    return A.dot(x)-b

##méthode de descente du gradient à pas fixe

def pas_fixe(x0,fonction,pas=1.0e-2,tol=1.0e-10,itermax=10000):
    A=fonction['A']
    b=fonction['b']
    c=fonction['c']
    xx=[x0]
    dir=(-1)*gradient(A,b,xx[-1])
    residu=np.linalg.norm(dir)
    k=0
    while k<itermax and residu>tol:
        xx.append(xx[-1]+pas*dir)
        dir=(-1)*gradient(A,b,xx[-1])
        residu=np.linalg.norm(dir)
        k+=1
    return {'xx':np.asarray(xx),'residu':np.asarray(residu)}

## méthode de descente du gradient conjugué

def conjugate(x0,fonction,tol=1.0e-10,itermax=10000):
    A=fonction['A']
    b=fonction['b']
    c=fonction['c']

    #***** Initialisation *****
    xx=[x0]
    dir=(-1)*gradient(A,b,x0)
    residu=[np.linalg.norm(gradient(A,b,x0))]


    k=0
    while residu[-1]>=tol and k<=itermax:
        #----- Calcul de rho(k) -----
        rho=(-1)*(gradient(A,b,xx[-1])@dir)/(A@dir@dir)
        
        #----- Calcul de x(k+1) -----
        xx.append(xx[-1] + rho*dir)
        
        #----- Calcul de la nouvelle direction de descente d(x+1) -----
        print((A@gradient(A,b,xx[-1]))@dir)
        beta=(A@gradient(A,b,xx[-1]))@dir/(A@dir@dir)
        dir= (-1)*gradient(A,b,xx[-1]) + beta * dir
        
        #----- Calcul du residu r(k+1) -----
        residu.append(np.linalg.norm(gradient(A,b,xx[-1])))
        
        k +=1


    return {'xx':np.asarray(xx),'residu':np.asarray(residu)}

##affichage
def plot(xx,res):
    plt.figure()
    ax1=plt.gca()
    
    X1, X2 = np.meshgrid(np.linspace(-5.0,5.0,101),np.linspace(-5.0,5.0,101))
    Z=function(A,b,c,[X1,X2])
    
    ax1.contour(X1,X2,Z)

    ax1.plot(xx.T[0,0],xx.T[0,1],'k-x')

    ax1.set_aspect('equal')
    
    plt.figure()
    plt.plot(res)
    plt.yscale('log')
    plt.grid()
    plt.xlabel('Iterations')
    plt.ylabel(r'$||\nabla f(x) ||_2$')
    plt.title('Convergence')

    plt.show()


###----- Pas fixe -----
##cas_01=pas_fixe(x0,fonction,1.0e-1,1.0e-6,10000)
##print(cas_01['xx'][-1], len(cas_01['xx'])-1)
##
##plot(cas_01['xx'],cas_01['residu'])
##
###----- Gradient conjugue -----
##cas_02=conjugate(x0,fonction,1.0e-6,10000)
##print(cas_02['xx'][-1], len(cas_02['xx'])-1)
##
##plot(cas_02['xx'],cas_02['residu'])


##exercice 2


