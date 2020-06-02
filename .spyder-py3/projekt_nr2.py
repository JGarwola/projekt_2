# -*- coding: utf-8 -*-

import numpy as np
import random

N = 50
R = 10
r = 0.7
d_min = 1,4
d_max = 2.1
d_exp = 1.75
element = 'B'

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
    def __init__(self, atomy=[]):
        self.atomy = atomy
        
        #TUTAJ BEDZIE MOZNA ZAIMPLEMENTOWAC LOSOWANIE POLOZEN
        #NARAZIE WSPOLZEDNE SA 0 0 i
        pierwszy = atom(pozycja = np.array( [0,0,0]) )
        self.atomy.append(pierwszy)
        for i in range(N):
            a = atom( pozycja = np.array( [0,0,i] ) )
            self.atomy.append( a )
      
    #PRZEKSZTALCA LISTE ATOMY W TEKST GOTOWY DO WKLEJENIA DO PLIKU
    def dane(self):
        tekst = str(N) + "\n" + "linia komentarza"
        for element in self.atomy:
            tekst = ( tekst + "\n" + str(element) )
        return tekst
    
    def zapisz(self,nazwa_pliku):
        fout = open(nazwa_pliku,'w')
        fout.write(self.dane())
        fout.close()
        
a = atom(pozycja = [0,0,0])
print(a)
        
p = populacja()
print(p.dane())
p.zapisz("dane.xyz")