import os
import json
import csv
import numpy as np
from math import *
import PIL
from PIL import Image

def process(adresse):
    img = Image.open(adresse)
    imgNG = img.convert('L')
    im2 = imgNG.resize((512,512))
    return im2

def contrast(image):
    I=np.asarray(image)
    contrast=np.zeros((512,512),np.uint8)
    for k in range (512):
        for l in range (512):
            contrast[k][l]=I[k][l]*1.2
    data=Image.fromarray(contrast)
    return data

def hachage (tab):
    resultat=""
    taille=len(tab)
    for i in range (taille-1):
        com="0"
        if tab[i]>=tab[i+1]:
            com="1"
        resultat+=com
    return resultat

def algo (adresse,b):
    
    im2 = Image.open(adresse)
    width,height=im2.size
    pixlong=height//b
    pixlarg=width//b
    imoy=np.zeros((b,b))
    I=np.asarray(im2)
    
    for i in range(b):
        for j in range (b):
            som=0
            m=0
            if i<b-1:
                if j<b-1:
                    for k in range(pixlong*i+pixlong):
                        for l in range(pixlarg*j+pixlarg):
                            som=som+I[k][l]
                            m+=1
                    som=som//m
                    imoy[i][j]=som
                else:
                    for k in range(pixlong*i+pixlong):
                        for l in range(pixlarg*j+pixlarg+width%b):
                            som=som+I[k][l]
                            m+=1
                    som=som//m
                    imoy[i][j]=som  
            
            else:
                if j<b-1:
                    for k in range(pixlong*i+pixlong+height%b):
                        for l in range(pixlarg*j+pixlarg):
                            som=som+I[k][l]
                            m+=1
                    som=som//m
                    imoy[i][j]=som
                else:
                    for k in range(pixlong*i+pixlong+height%b):
                        for l in range(pixlarg*j+pixlarg+width%b):
                            som=som+I[k][l]
                            m+=1
                    som=som/m
                    imoy[i][j]=som
     
    if b==3:
        hashseq=[imoy[0][0],imoy[0][1],imoy[1][0],imoy[2][0],imoy[1][1],imoy[0][2],imoy[1][2],imoy[2][1],imoy[2][2]]
        #hashseq=[imoy[2][0],imoy[2][1],imoy[2][2],imoy[1][0],imoy[1][1],imoy[1][2],imoy[0][0],imoy[0][1],imoy[0][2]]
    if b==4:
        hashseq=[imoy[3][0],imoy[3][1],imoy[2][0],imoy[2][1],imoy[1][0],imoy[1][1],imoy[0][0],imoy[0][1],imoy[0][2],imoy[0][3],imoy[1][2],imoy[1][3],imoy[2][2],imoy[2][3],imoy[3][2],imoy[3][3]]
    if b==5:
        hashseq=[imoy[4][0],imoy[4][1],imoy[3][0],imoy[3][1],imoy[2][0],imoy[2][1],imoy[1][0],imoy[1][1],imoy[0][0],imoy[0][1],imoy[0][2],imoy[0][3],imoy[0][4],imoy[1][2],imoy[1][3],imoy[1][4],imoy[2][2],imoy[2][3],imoy[2][4],imoy[3][2],imoy[3][3],imoy[3][4],imoy[4][2],imoy[4][3],imoy[4][4]] 

    return hachage(hashseq)

def algochevauch (adresse):
    
    im2 = Image.open(adresse)
    width,height=im2.size
    pixlong=height//3
    pixlarg=width//3
    imoy=np.zeros((5,5))
    I=np.asarray(im2)
    hashseq=list()
    
    for i in range(5):
        for j in range (5):
            som=0
            m=0
            if i<4:
                if j<4:
                    for k in range(int(pixlong*(i/2)+pixlong)):
                        for l in range(int(pixlarg*(j/2)+pixlarg)):
                            som=som+I[k][l]
                            m+=1
                    som=som//m
                    imoy[i][j]=som
                else:
                    for k in range(int(pixlong*(i/2)+pixlong)):
                        for l in range(int(pixlarg*(j/2)+pixlarg+width%3)):
                            som=som+I[k][l]
                            m+=1
                    som=som//m
                    imoy[i][j]=som
                   
            
            else:
                if j<4:
                    for k in range(int(pixlong*(i/2)+pixlong+height%3)):
                        for l in range(int(pixlarg*(j/2)+pixlarg)):
                            som=som+I[k][l]
                            m+=1
                    som=som//m
                    imoy[i][j]=som
                else:
                    for k in range(int(pixlong*(i/2)+pixlong+height%3)):
                        for l in range(int(pixlarg*(j/2)+pixlarg+width%3)):
                            som=som+I[k][l]
                            m+=1
                    som=som/m
                    imoy[i][j]=som
     
    for i in range(5):
        for j in range(5):
            hashseq.append(imoy[i][j])

    return hachage(hashseq)

def binary(a):
    bnr = bin(a).replace('0b','') #la fonction bin renvoie la représentation binaire équivalente à l'entier donné. Mais seulement
    #rajoute '0b' au debut exemple 0b100 pour la rep binaire de 4. La fonction replace remplace donc ce '0b' par la chaine vide 
    #pour la supprimer de la repr
    x = bnr[::-1] 
    while len(x) < 15: #si la taille de la repr n'atteint pas 15 on ajoute des '0' au début.
        x += '0'
        bnr = x[::-1]
    return bnr


def structure(chaine):
    nbre0=0
    for c in chaine:
        if c=="0":
            nbre0+=1
    return nbre0

def possibility():
    arrangement={}
    arrangement1={}
    arrangement2={}
    for i in range(32768):
        cle=str(structure(binary(i)))+"0"
        if cle not in arrangement1.keys():
            arrangement1[cle]=[]
            arrangement1[cle].append([0,binary(i)])
           
        else:
            liste=arrangement1[cle]
            valeur=liste[-1]
            arrangement1[cle].append([valeur[0]+1,binary(i)])
    with open('dataArrangement1.json', 'w') as monfichier1:
        json.dump(arrangement1,monfichier1)
    copy=arrangement1    
    for elt in copy.keys():
        arrangement2[elt+"rev"]=list(reversed(copy[elt]))
       #objectif: mettre les positions des séquences des listes inversées dans le bon ordre.pour ce faire on va récupérer chaque valeur de
    #clé(une liste), récupérer la première valeur de cette liste(qui est une liste), récupérer sa première valeur 'p' pour connaitre le nombre de séquences de cette liste. Faire une boucle sur la liste générale, valeur d'une clé. Ensuite faire à l'intérieur une boucle sur d. Accéder à la première valeur de la liste et lui affecter l'itérateur de la boucle
    for elt in arrangement2.keys():
        pos=len(arrangement2[elt])
        for j in range(pos):
                ((arrangement2[elt])[j])[0]=j  
                
    with open('dataArrangement2.json', 'w') as monfichier2:
        json.dump(arrangement2,monfichier2)
        
    #arrangement1.update(arrangement2)
   
    #arrangement={**arrangement1,**arrangement2}
    
def arrangement():
    input_file=open('dataArrangement1.json', 'r')
    var_json1=json.load(input_file)
    input_file=open('dataArrangement2.json', 'r')
    var_json2=json.load(input_file)
    arrangement={**var_json1,**var_json2}
    with open('dataArrangement.json', 'w') as monfichier:
        json.dump(arrangement,monfichier)

def algoapproach (im2):
#def algoapproach (im2,image):
    input_file=open('dataArrangement.json', 'r')
    var_json=json.load(input_file)
    
    #im2 = Image.open(adresse)
    width,height=im2.size
    pixlong=height//4
    pixlarg=width//4
    imoy=np.zeros(16)
    I=np.asarray(im2)
    hashseq=list()
    datasetseq={}
    possibility={}

    
    for i in range(pixlong):
        blong=i*4
        for j in range (pixlarg):
            blarg=j*4
            m=0
            for k in range (4):
                for l in range (4):
                    
                    imoy[m]=I[blong+k][blarg+l]
                    m+=1
            bloc=128*i+j
            key=hachage(imoy)
            cle=str(structure(key))+"0"
            for elt in var_json.copy():
                if cle == elt:
                    possibility[bloc]=var_json[elt]
                    
                    var_json.pop(elt)
                    cle=""
                    
               # elif cle == elt.replace("rev",""):
                   # possibility[bloc]=var_json[elt]
                    
                   # var_json.pop(elt)
            #rajouter une instruction pour arreter dès qu'on a déjà les blocs qui couvrent toutes les possibilités. Pour cela, à chaque fois que le if est vérifié on supprime l'élément correspondant dans var_json.keys() pour que le prochain bloc qui aura les memes caractéristiques ne soit plus traité
              
            if key not in datasetseq.keys():
                datasetseq[key] = []
          
            datasetseq[key].append(bloc)
      
    #print("nombre de blocs utiles ",len(possibility.keys()))      
    with open("databloc.json", "w") as monfichier:
        json.dump(possibility,monfichier)
    #if len(possibility.keys())==16:
      #  with open("C:\\Users\\Administrateur\\approach\\databloc_mean\\db"+image+".json", "w") as monfichier:
            #json.dump(possibility,monfichier)
    ##return possibility
    
    #monfichier.close()
    #input_file.close()
    #return datasetseq
    
    #pour chaque segment du message: on calcule le nbre de '0' à partir de structure(). Pour chaque valeur de clé on calcule le nbre de '0' de la 2eme valeur de la premiere liste qu'on compare avec pour le segment. Dès qu'il y'a correspondance on compare le segment à la 2eme valeur de chaque sous liste de la liste. Dès qu'il y a équivalence on récupère la position de la séquence qui correspond à la 1ère valeur de la sous-liste. 
    
    
def algoapproachNouv(im2,image):
    input_file=open('dataArrangement.json', 'r')
    var_json=json.load(input_file)
    
    #im2 = Image.open(adresse)
    width,height=im2.size
    pixlong=height//4
    pixlarg=width//4
    imoy=np.zeros(16)
    I=np.asarray(im2)
    hashseq=list()
    datasetseq={}
    possibility={}
    
    for i in range(pixlong):
        blong=i*4
        for j in range (pixlarg):
            blarg=j*4
            m=0
            for k in range (4):
                for l in range (4):
                    
                    imoy[m]=I[blong+k][blarg+l]
                    m+=1
            bloc=128*i+j
            key=hachage(imoy)
            cle=str(structure(key))+"0"
            possibility[bloc]=cle

    
    with open("C:\\Users\\Administrateur\\approach\\newdatablocSP\\db"+image+".json", "w") as monfichier:
    
        json.dump(possibility,monfichier)

def capacite(length): 
    liste=[0]
    liste2=[]
    liste3=[]
    liste1=[0]
    k=0
    m=0
    n=0
    diz="0"
    i=1

    while int(liste[-1])<length:
        taille=len(str(i))
        if taille==1:
            liste.append(i)
            liste1.append(i)
        
        elif taille==2:
            while k<len(liste1):
                liste2.append(diz+(str(liste1[k])))
                liste.append(diz+(str(liste1[k])))
                k+=1
            liste.append(i)
            liste2.append(i)
        elif taille==3:
            while m<len(liste2):
                liste3.append(diz+(str(liste2[m])))
                liste.append(diz+(str(liste2[m])))
                m+=1
            liste.append(i)
            liste3.append(i)
        elif taille==4:
            while n<len(liste3):
            #liste2.append(diz+(str(liste1[k])))
                liste.append(diz+(str(liste3[n])))
                n+=1
            liste.append(i)
            
        
        #j+=1
        i+=1
    return len(liste)

def chiffrement(plain,key,base):#chiffrement en chaine des séquences
    chaine=str(plain)
    i=1
    result=""
    shift=np.zeros(len(chaine))
    shift[0]=str(key)
    for elt in chaine[:-1]:
        shift[i]=elt
        i+=1
    for j in range(len(chaine)):
        result+=str((int(chaine[j])+int(shift[j]))%base)
    return result

def create_folder(folder,cap):
    chemin="C:/Users/Administrateur/Documents/client/client"+folder
    os.makedirs(chemin)
    for i in range(cap):
        with open(chemin+"/"+"client"+folder+"_transaction"+str(i)+".txt","w") as fich:
            fich.write("transaction complete")
            
#fonction qui renvoie le numéro du répertoire auquel correspond un bloc utile
def folder(block):
    it=0
    input_file=open('databloc.json','r')
    var_json=json.load(input_file)
    for elt in var_json.keys():
        
        if elt==block:
            
            break
        it+=1
    return it

#def chiffrementbloc(plain,key,rangement):#chiffrement des blocs, la fonction prend en paramètre la liste des blocs à chiffrer ainsi que la clé des blocs
def chiffrementbloc(plain,key):
    ordre={}
    chif_bloc={}
    for elt in plain:
        
        chif_bloc[elt]=(folder(elt)+key)%16
        #chif_bloc[elt,rangement[elt]]=(folder(elt)+key)%16
    for k,v in sorted(chif_bloc.items(), key=lambda x: x[1]):
      ordre[k]=v
    chif_bloc=ordre
 
    
#chif_bloc=chiffrementbloc(rangement.keys(),9)

#print(chif_bloc)
    with open('chif.json', 'w') as monfichier:
        json.dump(chif_bloc,monfichier)
    #return chif_bloc

def association_bloc():
    association={}
    input_file4=open('rangement.json','r')
    rangement=json.load(input_file4)
    input_file3=open('chif.json','r')
    chif_bloc=json.load(input_file3)
    for cle in chif_bloc.copy():
        if rangement[cle] >=1365:
            association[cle]=""
            for key in chif_bloc.copy():
                if rangement[key] <1365:
                    association[cle]=key
                    chif_bloc.pop(cle)
                    chif_bloc.pop(key)
                    break
    
   
    #print(association)
    with open('association.json', 'w') as monfichier:
        json.dump(association,monfichier)
    #return association
    
#def position(num)
def position(num):
    input_file3=open('chif.json','r')
    chif_bloc=json.load(input_file3)
    for elt in chif_bloc.keys() :
        #if elt[0]==num:
        if elt==num:
            return 1+chif_bloc[elt]
        
def position_seq(seq):
    pos=0
    input_file2=open('correspondance.json','r')
    var_json2=json.load(input_file2)
    while pos<len(var_json2)-1:
        if seq==var_json2[pos]:
            num=pos
            break
            
        pos+=1
    return num

#fonction qui prend en paramètre une position d'un répertoire et renvoie le bloc utile de l'image correspondant
def reversePosition(pos):
    input_file3=open('chif.json','r')
    chif_bloc=json.load(input_file3)
    for elt in chif_bloc.keys() :
        #if elt[0]==num:
        if str(chif_bloc[elt])==str(pos) :
            return elt
        
#focntion qui renvoie la capacité d'un bloc pris en paramètre
def capacity(numbloc):
    input_file3=open('rangement.json','r')
    rangement=json.load(input_file3)
    for elt in rangement.keys() :
        #if elt[0]==num:
        if str(elt)==str(numbloc) :
            return rangement[elt]
        
def decryption_seq(cipher,key):
    chaine=str(cipher)
    result=""
    
    for j in range(len(chaine)):
        if j==0:
            result+=str(((int(chaine[j])-key)+10)%10)
        else:
            result+=str(((int(chaine[j])-int(result[-1]) )+10)%10)
        
    return result

def reversePosition_seq(pos): #prend la position du fichier dans le stego-dossier et renvoie la séquence chiffrée.
    
    input_file2=open('correspondance.json','r')
    var_json2=json.load(input_file2)
    
    return var_json2[pos]

def deciphered(couple):
    input_file=open('databloc.json','r')
    liste=json.load(input_file)
    for elt in liste[str(couple[0])]:
        if elt[0]==int(couple[1]):
            return elt[1]
        
def reverse_asso(block):
    input_file=open('association.json','r')
    association=json.load(input_file)
    for ass in association.keys():
        if association[ass]==block:
            return ass  

def average (adresse): #fonction qui calcule la moyenne d'une image à partir de son emplacement dans l'ordi
    
    img = Image.open(adresse)
    imgNG = img.convert('L')
    im2 = imgNG.resize((512,512))
    width,height=im2.size
    
    I=np.asarray(im2)
    som=0
    m=0
  
    for k in range(height):
        for l in range(width):
            som=som+I[k][l]
            m+=1
    som=som//m
    return som

bin_repr = lambda s, coding="iso-8859-1": ' '.join('{0:08b}'.format(c) for c in s.encode(coding))


#fonction qui calcule la distance de hamming entre 2 chaines binaires
#elle est utilisée pour le calcul du BER(Bit Error Rate) des méthodes
    
def ber(message,message_gf):
    
    d=0
    for l,m in zip(message,message_gf):
       
        if l!=m and m!=" ":
            d+=1
    return d

