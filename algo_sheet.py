from __future__ import print_function
import pickle
import os
#from google_auth_oauthlib.flow import Flow, InstalledAppFlow
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth
import google.auth
import google
from googleapiclient.discovery import build
from google.cloud import storage

from google.oauth2 import service_account
from googleapiclient.errors import HttpError


def name(file):
    liste=[]
    with open (file,'r') as fich:
        for line in fich:
            liste.append(line.rstrip('\n'))
    return liste
        
def create_file(id_folder,name):
    
    
    gauth = GoogleAuth()
    gauth.CommandLineAuth()
    #gauth.LocalWebserverAuth()          
    drive = GoogleDrive(gauth)
    
    #creds = service_account.Credentials.from_service_account_file("C:\\Users\\Administrateur\\Downloads\\createfolder-360917-65f4ef03b560.json")
    file1 = drive.CreateFile({'parents': [{'id': id_folder}],'title': name+'.txt'})  
    file1.SetContentString('Hello World!') 
    file1.Upload()
    
def Create_Service(client_secret_file, api_name, api_version, *scopes):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    print(SCOPES)

    cred = None

    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}.pickle'
    # print(pickle_file)

    if os.path.exists(pickle_file):
        with open(pickle_file, 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

    with open(pickle_file, 'wb') as token:
            pickle.dump(cred, token)

    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, 'service created successfully')
        return service
    except Exception as e:
        print('Unable to connect.')
        print(e)
        return None
    
#def search_file(cred):
 #   client_secret='client_secrets.json'
  #  api_name='drive'
   # api_version='v3'
    #SCOPES = ['https://www.googleapis.com/auth/drive']
    #service=Create_Service(client_secret,api_name,api_version,SCOPES)
    #folderId=cred
    #query=f"parents='{folderId}'"
    #response=service.files().list(q=query).execute()
    #files=response.get('files')
    #nextPageToken=response.get('nextPageToken')
    #while nextPageToken:
    #    response=service.files().list(q=query).execute()
     #   files.extend(response.get('files'))
      #  nextPageToken=response.get('nextPageToken')
    #return files

def search_file(pos,query):
    j=0
    client_secret='client_secrets.json'
    api_name='drive'
    api_version='v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']
    service=Create_Service(client_secret,api_name,api_version,SCOPES)

    #query=f"parents='{'1ToFEFp77TSMfPlpkWDEMna8AbIPoDUSi'}' "
    response=service.files().list(q=query).execute()
    fichiers=[]
#fichiers=response.get('files')
    nextPage=response.get('files')

    nextPageToken=response.get('nextPageToken',None)
    totalFiles=0
    while True:
        nextTotalFiles=len(nextPage)+totalFiles
        if totalFiles <=pos and pos<nextTotalFiles:
            #print("fich trouvé", totalFiles,nextTotalFiles)
            fichiers=nextPage
            break
        if nextPageToken is None:
            break
        response=service.files().list(q=query,pageToken=nextPageToken).execute()
        totalFiles=nextTotalFiles
        nextPage=response.get('files')
        
        nextPageToken=response.get('nextPageToken',None)
        
    j=totalFiles

    for fich in fichiers :
        if j==pos:
            file_metadata={'name':fich['name'] ,'parents':['1_kGPAA1ZyOkglYoEPLzLLCUB7nBWJjW1']}
            service.files().copy(fileId=fich['id'] , body=file_metadata).execute()
            #print('oui',j,fich['name'])
            print(j,fich['name'])
            break
        j+=1
"""
def search_position(name):#prend en paramètre le nom d'un fichier(contenu dans le stego-dossier) et renvoie [le numéro du répertoire qui le contient; sa position dans ce répertoire]
    numfolder=0
    numfile=0
    client_secret='client_secrets.json'
    api_name='drive'
    api_version='v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']
    service=Create_Service(client_secret,api_name,api_version,SCOPES)
#parcours du rep "transactions"
    query=f"parents='{'1oAFPPOYJqcnvZDMKl8WxVeKbQGEQ6m9N'}' "
    response=service.files().list(q=query).execute()
    files=response.get('files')
    nextPageToken=response.get('nextPageToken')
    ctrl=True
    for file in files:
        if file['name']!="rinas":
            numfile=0
            query=f"parents='{file['id']}' " 
            response=service.files().list(q=query).execute()
            fichiers=[]
#fichiers=response.get('files')
            nextPage=response.get('files')
            nextPageToken=response.get('nextPageToken',None)
            while ctrl:
                fichiers=nextPage
                for fich in fichiers:
                    if fich['name']==name:
                        print(file['id']," ",file['name'])
                        ctrl=False
                        break
                    numfile+=1
                if nextPageToken is None:
                    break
                response=service.files().list(q=query,pageToken=nextPageToken).execute()
                nextPage=response.get('files')
                nextPageToken=response.get('nextPageToken',None)
            if ctrl==False:
                break
            numfolder+=1
    return [numfolder,numfile]
"""
def search_position(name):#prend en paramètre le nom d'un fichier(contenu dans le stego-dossier) et renvoie [le numéro du répertoire qui le contient; sa position dans ce répertoire]
    numfolder=0
    numfile=0
    client_secret='client_secrets.json'
    api_name='drive'
    api_version='v3'
    SCOPES = ['https://www.googleapis.com/auth/drive']
    service=Create_Service(client_secret,api_name,api_version,SCOPES)
#parcours du rep "transactions"
    query=f"parents='{'1RnnfGxu6CnzNUjJYmQbBFJiGN9aHbczv'}' "
    response=service.files().list(q=query).execute()
    files=response.get('files')
    nextPageToken=response.get('nextPageToken')
    ctrl=True
    for file in files:
        if file['name']!="rinas":
            numfile=0
            
            if name[0]==(file['name'])[0]:
                query=f"parents='{file['id']}' " 
                response=service.files().list(q=query).execute()
                fichiers=[]
#fichiers=response.get('files')
                nextPage=response.get('files')
                nextPageToken=response.get('nextPageToken',None)
                while ctrl:
                    fichiers=nextPage
                    for fich in fichiers:
                        if fich['name']==name:
                            #print(file['id']," ",file['name'])
                            print("Nom du répertoire de couverture ",file['name'])
                            ctrl=False
                            break
                        numfile+=1
                    if nextPageToken is None:
                        break
                    response=service.files().list(q=query,pageToken=nextPageToken).execute()
                    nextPage=response.get('files')
                    nextPageToken=response.get('nextPageToken',None)
                if ctrl==False:
                    break
            numfolder+=1
    return [numfolder,numfile]
