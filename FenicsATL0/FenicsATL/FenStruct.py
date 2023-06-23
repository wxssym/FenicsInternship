from .FenUtils import *
from .FenGraphs import *

import pandas as pd
import warnings
warnings.filterwarnings("ignore")
import matplotlib.pyplot as plt
import os
import datetime

import re

def FilterbyUniqueChannels(FENICS):
    temp_allindex = []
    for id in FENICS.Board.id.unique() :
        temp_index = FENICS[FENICS.Board.id == id][FENICS.Board.channel == FENICS[FENICS.Board.id == id].Board.channel.value_counts().index[0]].index.tolist()
        temp_allindex = temp_allindex + temp_index
    return FENICS.loc[temp_allindex]

#Folder scanning function : Function that scans the folders looking for needed json files
def fen1_data_extractor(mainDataDir, burnTablePath) :
    FENICS_to_analyse = ['FENICS115','FENICS114','FENICS113','FENICS112','FENICS111','FENICS110','FENICS109','FENICS108','FENICS107','FENICS106','FENICS105','FENICS104','FENICS101']
    burnsTable = pd.read_csv(burnTablePath)
    tuples = [('Board', 'name'), ('Board', 'version'),
          ('Board', 'id'), ('Board', 'code'),('Board', 'burnings'),('Board','burnTime'),
          ('Board','date'),('Board','time'),
          ('Board','specialTests'),('Board','channel'),('Board','StatusFast'),('Board','StatusSlow')]
          #('FastResult','FastResult'),('SlowResult','SlowResult')]
    mux = pd.MultiIndex.from_tuples(tuples)
    FENICS = pd.DataFrame(columns=mux)
    
    """function that explores given repertory list to get FENICS data
    Takes a list of folders, and an empty dataframe, returns a dataframe filled with data"""
    for i,FENICS_id_prefix in enumerate(FENICS_to_analyse) :
        loadingBar(i,len(FENICS_to_analyse),prefix=f"parsing {FENICS_id_prefix} data...")
        filtredFolder = [string for string in os.listdir(mainDataDir) if string.startswith(FENICS_id_prefix) or string == FENICS_id_prefix]
        for subfolder in filtredFolder :
            for subsubfolder in os.listdir(mainDataDir+subfolder) :
                for fileName in os.listdir(mainDataDir+subfolder+"/"+subsubfolder) :
                    if fileName.endswith("SlowResult.json") and subsubfolder.startswith("20"):
                        path = subfolder + "/" +subsubfolder + "/"
                        FENICS = FENICS.append(data_parser(mainDataDir,path,1,burnsTable),ignore_index=True)
    print(f"Parsing done with success.", end='\r')    
    return FENICS  


def fen2_data_extractor(mainDataDir):
    
    FOLDERS_to_analyse = (os.listdir(mainDataDir))
    
    tuples = [('Board', 'name'), ('Board', 'version'),
          ('Board', 'id'), ('Board', 'code'),('Board', 'burnings'),('Board','burnTime'),
          ('Board','date'),('Board','time'),
          ('Board','specialTests'),('Board','channel'),('Board','StatusFast'),('Board','StatusSlow')]

    mux = pd.MultiIndex.from_tuples(tuples)
    data = pd.DataFrame(columns=mux)
    
    
    SSH_client,SSH_Tunnel = FenSSHtunnel()
    
    mydb = credentialsSetup()
    
    mycursor = mydb.cursor()
    for i,subfolder in enumerate([string for string in os.listdir(mainDataDir) if string.startswith('02') and string in FOLDERS_to_analyse]) :
        loadingBar(i,len([string for string in os.listdir(mainDataDir) if string.startswith('02') and string in FOLDERS_to_analyse]),prefix=f"parsing {subfolder} data...")
        for subsubfolder in os.listdir(mainDataDir+subfolder) :
            if subsubfolder not in "2022-06-22_16-50-0" :
                for fileName in os.listdir(mainDataDir+subfolder+"/"+subsubfolder) :
                    if fileName.endswith("SlowResult.json") and subsubfolder.startswith("20") :
                        path = subfolder + "/" +subsubfolder + "/"
                        data = data.append(data_parser(mainDataDir,path,2,mySQL=mycursor),ignore_index=True)
                
    mydb.close()
    SSH_client.close()
    print('\r\x1b[2K\x1B[1m DATA PARSING :'.ljust(40)+'\x1B[42m\x1B[30m\x1B[1m ENDED \x1B[0m', end='\r')  
    return data




#Parsing the folders : Parsing the path name infos as a dictionary using regular expressions.
def data_parser(mainDataDir,path,fen_ver,burnsTable=None,mySQL=None):
    if fen_ver == 1 :
        #covering all naming conventions used in the folders using regular expressions (regex)
        subfolder_regex= r'([A-Z]+)(\d)(\d+)([A-Za-z]+)(\d*)'
        subsubfolder_regex = r'(\d{4})[-_]?(\d{2})?[-_]?(\d{2})?[-_]?(\d{2})?[-_]?(\d{2})?[-_]?([A-Za-z]+[\dA-Za-z]+)?[-_]?([A-Za-z]+[\dA-Za-z]+)?[-_]?'
        
        parsed_path = path.split('/')
        temp_dict = {}
        Fast_failed = [11,1]
        Slow_failed = [11,1,7]
        #Parsing subfolder informations
        match = re.match(subfolder_regex,parsed_path[0])    
        if match :
            temp_dict = {
                ('Board','name') : match.group(1),
                ('Board','version') : match.group(2),
                ('Board','id') : match.group(3),
                ('Board','code') : match.group(4),
                ('Board','burnings') : match.group(5) if match.group(5) else '1',
            }
            
        try :
            temp_dict[('Board','burnTime')] = burningTimeCumulativeCalc(burnsTable,temp_dict[('Board','id')],temp_dict[('Board','burnings')])
        except Exception:
            raise Exception("Please update the burnTable. the burning table provided is some cycle late.")
        
        temp_dict['Board','version']=int(temp_dict['Board','version'])
        temp_dict['Board','id']=int(temp_dict['Board','id'])
        temp_dict['Board','burnings']=int(temp_dict['Board','burnings'])
        
        if temp_dict[('Board','id')] in Fast_failed :
            temp_dict[('Board','StatusFast')] = 0
        else :
            temp_dict[('Board','StatusFast')] = 1
            
        if temp_dict[('Board','id')] in Slow_failed :
            temp_dict[('Board','StatusSlow')] = 0
        else :
            temp_dict[('Board','StatusSlow')] = 1
            
        #parsing subsubfolder informations
        match = re.match(subsubfolder_regex,parsed_path[1])
        
        if match:
            temp_dict[('Board','date')]=f'{match.group(1)}-{match.group(2)}-{match.group(3)}' #formated year-month-day
            if match.group(4) == None and match.group(5) == None :
                temp_dict[('Board','time')]= None #No time for test
            else :
                temp_dict[('Board','time')]=f'{match.group(4)}:{match.group(5)}' #formated Hours:Minutes
                    
            if match.group(6) != match.group(7) : #checking if it got special tests
                temp_dict[('Board','specialTests')] = f'{match.group(6)}-{match.group(7)}'
            else :
                temp_dict[('Board','specialTests')] = 'None'
            
        #parsing the channel
        match = re.search(r"(\d+)$",parsed_path[1]) 
        if match : temp_dict[('Board','channel')] = match.group(1)
        
        #Loading the json data in the dataframe
        temp_fastResult = pd.read_json(mainDataDir+path+'FastResult.json',typ='series')
        for index in temp_fastResult.index :
            temp_dict[('FastResult',index)] = temp_fastResult[index]

        temp_slowResult = pd.read_json(mainDataDir+path+'SlowResult.json')
        for index, row in temp_slowResult.iterrows() :
            temp_dict[('SlowResult','Gain'+str(row.name))] = row
        
        return temp_dict
    
    elif fen_ver == 2:
        #covering all naming conventions used in the folders using regular expressions (regex)
        subfolder_regex= r"(\d{2})(0*)(\d*)"
        subsubfolder_regex = r'(\d{4})[-_]?(\d{2})?[-_]?(\d{2})?[-_]?(\d{2})?[-_]?(\d{2})?[-_]?([A-Za-z]+[\dA-Za-z]?[-_]?[A-Za-z]+[\dA-Za-z])?[-_]?(\d*)'
        
        parsed_path = path.split('/')
        temp_dict = {}
        
        #Parsing subfolder informations
        match = re.match(subfolder_regex,parsed_path[0])   
        if match :
            temp_dict = {
                ('Board','name') : 'FENICS',
                ('Board','version') : match.group(1)[1],
                ('Board','id') : match.group(3),
                ('Board','code') : None,
                ('Board','burnings') : None,
            }
            
        #parsing subsubfolder informations
        match = re.match(subsubfolder_regex,parsed_path[1])
        
        if match:
            temp_dict[('Board','date')]=f'{match.group(1)}-{match.group(2)}-{match.group(3)}' #formated year-month-day
            if match.group(4) == None and match.group(5) == None :
                temp_dict[('Board','time')]= None #No time for test
            else :
                temp_dict[('Board','time')]=f'{match.group(4)}:{match.group(5)}' #formated Hours:Minutes
                    
            if match.group(6) != None : #checking if it got special tests
                temp_dict[('Board','specialTests')] = f'{match.group(6)}'
                temp_dict[('Board','burnTime')] = 0
                temp_dict[('Board','StatusFast')] = -1
                temp_dict[('Board','StatusSlow')] = -1
            else :
                temp_dict[('Board','specialTests')] = None
                
                date_str = temp_dict[('Board', 'date')]
                date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
                start_date = date_obj  # subtract 2 days
                end_date = date_obj + datetime.timedelta(days=2)
                query=f"SELECT statusBurned,StatusFast,StatusSlow FROM FenicsHist WHERE fenics='{parsed_path[0]}' AND datetime BETWEEN '{start_date}%' AND '{end_date} %'"
                
                mySQL.execute(query)
                results = mySQL.fetchall()
                
                if len(results) !=0 :
                    temp_dict[('Board','burnTime')] = results[-1][0]

                    if results[-1][1] == "PASS" :
                        temp_dict[('Board','StatusFast')] = 1
                    elif results[-1][1] == "FAIL" : 
                        temp_dict[('Board','StatusFast')] = 0
                    else :
                        temp_dict[('Board','StatusFast')] = -1
                        
                    if results[-1][2] == "PASS" :
                        temp_dict[('Board','StatusSlow')] = 1
                    elif results[-1][2] == "FAIL" : 
                        temp_dict[('Board','StatusSlow')] = 0
                    else :
                        temp_dict[('Board','StatusSlow')] = -1
                    
                else : 
                    temp_dict[('Board','burnTime')] = None
                    temp_dict[('Board','StatusFast')] = -1
                    temp_dict[('Board','StatusSlow')] = -1

                        
                temp_dict[('Board','channel')] = match.group(7)
        
        
        #Loading the json data in the dataframe
        temp_fastResult = pd.read_json(mainDataDir+path+'/FastResult.json',typ='series')
        for index in temp_fastResult.index :
            temp_dict[('FastResult',index)] = temp_fastResult[index]

        temp_slowResult = pd.read_json(mainDataDir+path+'/SlowResult.json')
        for index, row in temp_slowResult.iterrows() :
            temp_dict[('SlowResult','Gain'+str(row.name))] = row
        
        return temp_dict

    else :
        raise Exception("You are trying to call a FENICS version that do not exist.")



