# -*- coding: utf-8 -*-
import math as m
import numpy as np
import random
from scipy.stats import truncnorm as trunc
import mogli

N = 1000
R = 10
r = 0.7
d_min = 1.4
d_max = 2.1
d_exp = 1.75
element = 'B'

#sprawdza czy atom jest w walcu
def w_walcu(ato):
    x =float(ato.pozycja[0])
    y =float(ato.pozycja[1])
    z =float(ato.pozycja[2])
    if(z>=r and (x**2 +y**2 <= (R-r)**2)):
        return True
    else:
        return False
    
    
#LOSUJE ODLEGŁOŚĆ ZGODNIE Z ROZKŁADEM
def losujd():
    std = 0.7
    a, b = (d_min - d_exp) /std, (d_max - d_exp) /std
    k=trunc.rvs(d_min,d_max,loc=0,scale=1,size=1,random_state=None)
    return k[0]

#sprawdza czy odległość między atomami jest < odl
def dystans(newato,ato,odl):
    d2 = m.sqrt((float(newato.pozycja[0])-float(ato.pozycja[0]))**2 +
                (float(newato.pozycja[1])-float(ato.pozycja[1]))**2 + (float(newato.pozycja[2])-float(ato.pozycja[2]))**2)
    if(d2< odl):
        return True
    else:
        return False

class atom:
    def __init__(self, sigma=0, h=1, pozycja=np.array([])):
        self.pozycja = pozycja
        self.h = h
        self.sigma = (N*(4/3)* 3.1415 *r**3)/( 3.1415 *(R**2)*self.h)
        
    #WYPISANIE LINIJKI W FORACIE JAK DO PLIKU XYZ    
    def __str__(self):
        return ( element + " " + str(self.pozycja[0]) + " "
                + str(self.pozycja[1]) + " " + str(self.pozycja[2]) )
        
class populacja():
    
    def __init__(self, atomy=[], h_max = 2*r):
        self.atomy = atomy
        self.h_max = 2*r
        a0 = atom()
        a0.pozycja = [format(0,'.5f'),format(0,'.5f'),format(r,'.5f')]
        atomy.append(a0)
        
        
        #LOSOWANIE POLOZEN
        
        for i in range(N):
            while True:
                za_blisko = 0
                
                last = atomy[-1] #wybiera ostatni dodany atom jako punkt odniesienia
                
                #losuja współrzędne w ukłądzie sferycznym i przelicza na kartezjańskie
                phi = (random.uniform(0,2*m.pi))
                theta = (random.uniform(0,m.pi))
                d = losujd()
                x = d*m.sin(theta)*m.cos(phi) + float(last.pozycja[0])
                y = d*m.sin(theta)*m.sin(phi) + float(last.pozycja[1])
                z = d*m.cos(theta) + float(last.pozycja[2])
                x = (format(x,'.5f'))
                y =(format(y,'.5f'))
                z = (format(z,'.5f'))
                a = atom( pozycja = np.array( [x,y,z] ) )
                
                #sprawdzanie warunków
                if(not w_walcu(a)):
                    continue
                for at in atomy:
                    if(dystans(a,at,d_min)==True):
                        za_blisko = 1
                        break
                        
                if(za_blisko == 0):
                    break
                    
                    
            #sprawdza h
            if(float(a.pozycja[2])+r > self.h_max):
                self.h_max = float(a.pozycja[2])+r
                
            self.atomy.append( a )
      
    #PRZEKSZTALCA LISTE ATOMY W TEKST GOTOWY DO WKLEJENIA DO PLIKU
    def dane(self):
        tekst = str(N+1) + "\n" + "linia komentarza"
        for element in self.atomy:
            tekst = ( tekst + "\n" + str(element) )
        return tekst
    
    #'{0:s},{1:f}x,{2:f}y,{3:f}z\n'.format('Ar',x[i],y[i],z)
    
    def zapisz(self,nazwa_pliku):
        fout = open(nazwa_pliku,"w+")
        fout.write(self.dane())
        fout.close()


p = populacja(h_max = 1.4)

#parametry
h = p.h_max
V = m.pi*R*R*h
Va = (4/3)* m.pi *r**3
sigma = N*Va/V

#print(p.dane())
print("h =",h, "V =", 2*m.pi*r*h,"sigma =",sigma)
p.zapisz("dane.xyz")

molecules = mogli.read('dane.xyz')
mogli.show(molecules[0],bonds_param=d_max)
