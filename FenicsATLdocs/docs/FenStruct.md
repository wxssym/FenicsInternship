# FenStruct module
FenStruct is a module that gather all functions that parse main FENICS tests folder data searching for ``FastResults.json`` and ``SlowResults.json``

##Functions

### FENICS1 data explorer
#### FenStruct.fen1_data_extractor
_func_ **FenStruct.fen1_data_extractor(<i>mainDataDir, burnsTablePath</i>)**
[source](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenStruct.py#L21-L44)

Function that crawl a given directory for FENICS1 boards test data files with a given burntime table csv file. It returns them in a FenDataFrame.

==Important==
It is highly recommended to use this function to gather FENICS1 data, then save it as a ``json`` file then use [`FenLoad.FenicsData_read(path)`](../FenLoad/#read-fenics-data) to read it back.

==Important==
There is **no updating function** to update FENICS DataFrames with new tests, a new scan of all the files with this function is needed.

>**parameters :**
>>***mainDataDir*** (string) :
>>>path to the main directory to crawl for FENICS data.
>
>>***burnsTablePath*** (string) :
>>>path to a CSV file containing the burning hours of FENICS1 boards and their ids.
>
>**Returns :**
>>***FenDataFrame*** (pandas.DataFrame) :
>>>Multilevel columns FenDataFrame.
>
**Example :**

>>      #Directories definition
>>      mainDataDir = "/AtlasDisk/user/FENICS/"
>>      burnTablePath = "/users/divers/atlas/sisaid/home2/data/burns.csv"
>>      
>>      #FENICS1 data collection
>>      FENICS = FATL.fen1_data_extractor(mainDataDir, burnTablePath)
>>      FENICS.to_json('/AtlasDisk/home2/sisaid/data/FENICS_data.json')

>>resulting FenDataFrame :
>><table style="undefined;table-layout: fixed; width: 1277px"><colgroup><col style="width: 79.2px"><col style="width: 74.2px"><col style="width: 35.2px"><col style="width: 55.2px"><col style="width: 69.2px"><col style="width: 52.2px"><col style="width: 92.2px"><col style="width: 103.2px"><col style="width: 111.2px"><col style="width: 107.2px"><col style="width: 42.2px"><col style="width: 81.2px"><col style="width: 78.2px"><col style="width: 73.2px"><col style="width: 75.2px"><col style="width: 71.2px"><col style="width: 77.2px"></colgroup><thead><tr><th colspan="6">Board</th><th colspan="5">FastResult</th><th colspan="6">SlowResult</th></tr></thead><tbody><tr><td>name</td><td>version</td><td>id</td><td>code</td><td>burnings</td><td>...</td><td>NoiseLG</td><td>NoiseLGIG1</td><td>NoiseLGIG2</td><td>NoiseLGIG6</td><td>...</td><td>Gain0</td><td>Gain1</td><td>Gain2</td><td>Gain3</td><td>Gain4</td><td>Gain5</td></tr></tbody></table>

&nbsp;
&nbsp;

### FENICS2 data explorer
#### FenStruct.fen2_data_extractor
_func_ **FenStruct.fen2_data_extractor(<i>mainDataDir</i>)**
[source](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenStruct.py#L47-L77)

Function that crawl a given directory for FENICS2 boards test data. It requires an internet connexion to **CERN** cloud with a tunnel, and database credential to gather burning times and failure status from the **mySQL** FENICS2 database.
The credentials are saved in the OS environnement for the session.

It returns the data as FenDataFrame.

==Important==
We recommend using this function to gather FENICS1 data, then save it as a ``json`` file then use [`FenLoad.FenicsData_read(path)`](../FenLoad/#read-fenics-data) to read it back.

==Important==
There is **no updating function** to update FENICS DataFrames with new tests, a new scan of all the files with this function is needed.

==Important==
Be sure that you are connected to the **CERN** servers with a tunnel on an external terminal. `paramiko` seem to connect with SSH, but cannot make a tunnel, this block the automatisation of the process.

>**parameters :**
>>***mainDataDir*** (string) :
>>>path to the main directory to crawl for FENICS data.
>
>**Returns :**
>>***FenDataFrame*** (pandas.DataFrame) :
>>>Multilevel columns FenDataFrame.
>
**Example :**

>>      #Directories definition
>>      mainDataDir = "/AtlasDisk/user/tilefen/FENICS2/"

>>      #FENICS1 data collection
>>      FENICS2 = FATL.fen2_data_extractor(mainDataDir)
>>      FENICS2.to_json('/AtlasDisk/home2/sisaid/data/FENICS2_data.json')
resulting FenDataFrame :
>><table style="undefined;table-layout: fixed; width: 1277px"><colgroup><col style="width: 79.2px"><col style="width: 74.2px"><col style="width: 35.2px"><col style="width: 55.2px"><col style="width: 69.2px"><col style="width: 52.2px"><col style="width: 92.2px"><col style="width: 103.2px"><col style="width: 111.2px"><col style="width: 107.2px"><col style="width: 42.2px"><col style="width: 81.2px"><col style="width: 78.2px"><col style="width: 73.2px"><col style="width: 75.2px"><col style="width: 71.2px"><col style="width: 77.2px"></colgroup><thead><tr><th colspan="6">Board</th><th colspan="5">FastResult</th><th colspan="6">SlowResult</th></tr></thead><tbody><tr><td>name</td><td>version</td><td>id</td><td>code</td><td>burnings</td><td>...</td><td>NoiseLG</td><td>NoiseLGIG1</td><td>NoiseLGIG2</td><td>NoiseLGIG6</td><td>...</td><td>Gain0</td><td>Gain1</td><td>Gain2</td><td>Gain3</td><td>Gain4</td><td>Gain5</td></tr></tbody></table>

&nbsp;
&nbsp;

### FENICS data parser
#### FenStruct.data_parser
_func_ **FenStruct.data_parser(<i>mainDataDir,path,fen_ver,burnsTable=None,mySQL=None</i>)**
[source](https://github.com/wxssym/FenicsATL/blob/9f4a3a63d2388b0ad19844c0cdf52f226016d0d8/FenicsATL/FenStruct.py#L83-L237)

A multipurpose parsing function for both FENICS1 and FENICS2 data folders.

>**parameters :**
>>***mainDataDir*** (string) :
>>>path to the main directory to crawl for FENICS data.
>
>>***path*** (string) :
>>>relative path of the parsed folder to the main directory.
>
>>***fen_vers*** (integer) :
>>>version number of the parsed FENICS (1 or 2).
>
>>***burnsTable*** (pandas.DataFrame,optional) , *default*=None :
>>> (Only for FENICS1) burnTable dataframe object from the csv file.
>
>>***mySQL*** (mysql.cursor,optional) , *default*=None :
>>> (Only for FENICS2) mySQL cursor of mysql.connector after connection to the mysql database.
>

>
>**Returns :**
>>***parsedFolderData*** (dictionary) :
>>>dictionary of the data parsed inside the folder.
>
**Example :**

>>      for i,FENICS_id_prefix in enumerate(FENICS_to_analyse) :
>>          loadingBar(i,len(FENICS_to_analyse),prefix=f"parsing {FENICS_id_prefix} data...")
>>          filtredFolder = [string for string in os.listdir(mainDataDir) if string.startswith(FENICS_id_prefix) or string == FENICS_id_prefix]
>>              for subfolder in filtredFolder :
>>                  for subsubfolder in os.listdir(mainDataDir+subfolder) :
>>                      for fileName in os.listdir(mainDataDir+subfolder+"/"+subsubfolder) :
>>                          if fileName.endswith("SlowResult.json") and subsubfolder.startswith("20"):
>>                          path = subfolder + "/" +subsubfolder + "/"
>>                          FENICS = FENICS.append(data_parser(mainDataDir,path,1,burnsTable),ignore_index=True)
>>          print(f"Parsing done with success.", end='\r')    
>>          return FENICS

&nbsp;
&nbsp;

