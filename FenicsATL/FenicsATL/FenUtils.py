import os
from getpass import getpass
import paramiko
import mysql.connector
import socket
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

def Normalizer(To_normalize):
    # Instantiate the MinMaxScaler
    scaler = MinMaxScaler()
    normalized = scaler.fit_transform(To_normalize)
    normalized = pd.DataFrame(normalized, columns=To_normalize.columns)
    return normalized

def FenicsColors():
    filtred_id = [15,14,13,12,10,9,8,7,6,5,4]
    colors = plt.rcParams['axes.prop_cycle'].by_key()['color'] # get default color cycle
    color_dict = dict(zip(filtred_id, colors)) # create a dict of id-color pairs
    color_dict[4] = '#8F00FF'
    return color_dict

def Fenics_version(id_col):
    id_col = id_col.mode()
    if len(id_col) == 1:
        numeric = id_col[0]
        FENICS_version = f'FENICS {numeric}'
    else : 
        FENICS_version = f'FENICS {id_col[0]} & {id_col[1]}'
        numeric = 0
    
    return FENICS_version , numeric


def uniqueVals(X,Y):
    sums = {}
    counts = {}
    for x, y in zip(X, Y):
        if x in sums:
            sums[x] += y
            counts[x] += 1
        else:
            sums[x] = y
            counts[x] = 1

    # Calculate the mean Y value for each unique X value
    X_unique = []
    Y_mean = []
    for x in sums:
        X_unique.append(x)
        Y_mean.append(sums[x] / counts[x])
    return X_unique,Y_mean


def dropOutSigma(data,testTable,sigma,filter_id=False,return_index=True,columns=False):   

    if filter_id==False:
        filter_id = data.Board.id.unique()
    if columns == False :
        mask = pd.Series().reindex(data.index,fill_value=True)
        for column in testTable.columns :
            mask_perCol = pd.Series()
            for id in filter_id:
                id_filter = testTable[data.Board.id == id].index
                means = testTable.loc[id_filter][column].mean()
                stds = testTable.loc[id_filter][column].std()
                lower_bounds = means - sigma * stds
                upper_bounds = means + sigma * stds
                mask_perId = (testTable.loc[id_filter][column] >= lower_bounds) & (testTable.loc[id_filter][column] <= upper_bounds)
                mask_perCol = mask_perCol.append(mask_perId, ignore_index=False)
            mask = mask & mask_perCol

    if columns != False :
        mask = pd.Series().reindex(data.index,fill_value=True)
        for column in columns :
            mask_perCol = pd.Series()   
            for id in filter_id:
                id_filter = testTable[data.Board.id == id].index
                means = testTable.loc[id_filter][column].mean()
                stds = testTable.loc[id_filter][column].std()
                lower_bounds = means - sigma * stds
                upper_bounds = means + sigma * stds
                mask_perId = (testTable.loc[id_filter][column] >= lower_bounds) & (testTable.loc[id_filter][column] <= upper_bounds)
                mask_perCol = mask_perCol.append(mask_perId, ignore_index=False)
            mask = mask & mask_perCol
        
    
    if return_index :
        return data[mask].index
    else :
        mask


def checkFolderAt(path):
    if not os.path.exists(path):
        print(f'\r\x1b[2K Created folder at {path}',end='\n')
        os.makedirs(path)

def burningTimeCumulativeCalc(burnsTable,id,burnings):
    reindexed_burnsTable = burnsTable['1'+id][burnsTable['1'+id]!=0].reset_index(drop=True)
    if int(burnings) > reindexed_burnsTable.shape[0]:
        raise Exception("You are trying to call a burning stage not updated in the burnsTable, please update it")
    
    return reindexed_burnsTable[range(0,int(burnings))].sum()




def FenSSHtunnel():
    # Define SSH connection parameters
    ssh_host = "lxtunnel.cern.ch"
    ssh_port = 22
    ssh_username = "wsisaid"
    
    # Define local port forwarding parameters
    local_port = 5501
    remote_host = "dbod-fenicsdb.cern.ch"
    remote_port = 5509

    # Create an SSH client object
    ssh_client = paramiko.SSHClient()

    # Automatically add the remote host's key to the local host's known_hosts file
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    for attempt in range(5) :
        try :
            os.environ['ENV_SSH_PASSWORD']
            ssh_client.connect(ssh_host, port=ssh_port, username=ssh_username, password=os.environ['ENV_SSH_PASSWORD'])
            print('\x1B[1m SSH :'.ljust(40)+'\x1B[42m\x1B[30m\x1B[1m Connected \x1B[0m',end='\n')
            break
        except KeyError:
            print('\x1B[43m\x1B[1m\x1B[30m NO SSH PASSWORD SAVED \x1B[0m',end='\n')
            os.environ['ENV_SSH_PASSWORD'] = getpass(f'SSH tunnel PASSWORD :')
            print('\x1B[42m\x1B[30m\x1B[1m SSH PASSWORD SAVED \x1B[0m',end='\n')
            continue
        except :
            print('\x1B[41m\x1B[1m WRONG SSH PASSWORD \x1B[0m',end='\n')
            os.environ['ENV_SSH_PASSWORD'] = getpass(f' attempt {attempt} SSH tunnel PASSWORD :')
            continue

    else :
        print(f'\x1B[41m\x1B[1m Maximum number of attempts reached : {attempt} \x1B[0m')
        
    ssh_tunnel = ssh_client.get_transport().open_channel('direct-tcpip', (remote_host, remote_port), ('', local_port))
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    try:
        s.connect(('127.0.0.1', local_port))
        print('\x1B[1m TUNNEL :'.ljust(40)+'\x1B[42m\x1B[30m\x1B[1m Connected \x1B[0m',end='\n')
    except Exception as e:
        print('\x1B[41m\x1B[1m Tunnel is not working:', e,end='\n')
    finally:
        s.close()    
    
    return ssh_client , ssh_tunnel

def credentialsSetup():
    for attempt in range(5) :
        try :
            os.environ['ENV_MYSQL_USER'] = 'fenread'
            os.environ['ENV_MYSQL_PASSWORD']
            mydb = mysql.connector.connect(
                    host="127.0.0.1",
                    port="5501",
                    user= os.environ['ENV_MYSQL_USER'],
                    password= os.environ['ENV_MYSQL_PASSWORD'],
                    database="fenicsDB"
                )
            print('\x1B[1m DATABASE :'.ljust(40)+'\x1B[42m\x1B[30m\x1B[1m Connected \x1B[0m',end='\n')
            return mydb
        
        except mysql.connector.errors.DatabaseError as e:
            print(f"Caught a DatabaseError: {e} \x1B[0m",end='\n')
            os.environ['ENV_MYSQL_PASSWORD'] = getpass('MYSQL database PASSWORD')
            continue
        except KeyError:
            print('\x1B[43m\x1B[1m\x1B[30m NO MYSQL PASSWORD SAVED \x1B[0m',end='\n')
            os.environ['ENV_MYSQL_PASSWORD'] = getpass('MYSQL database PASSWORD')
            print('\x1B[42m\x1B[30m\x1B[1m MYSQL PASSWORD SAVED \x1B[0m',end='\n')
            continue

        except :
            print('\x1B[41m\x1B[1m WRONG MYSQL DATABASE PASSWORD \x1B[0m',end='\n')
            os.environ['ENV_MYSQL_PASSWORD'] = getpass(f'attempt  MYSQL database PASSWORD :')
            continue
                
    else:
        print(f'\x1B[41m\x1B[1m Maximum number of attempts reached : {attempt} \x1B[0m')

    
def loadingBar(current_iter,num_iterations,prefix='',suffix=''):
    num_iterations = num_iterations - 1 
    message_len = 54  # 54 is the length of the loading bar message without prefix/suffix
    total_prefix_len = len(prefix)
    total_suffix_len = len(suffix)
    total_message_len = message_len + total_prefix_len + total_suffix_len
    
    if len(suffix)>1:
        suffix = suffix.ljust(80)

    if current_iter == num_iterations:
        suffix = ''.ljust(len(suffix))
        print('\r\x1b[2K'+prefix+'|\x1B[47m'+50*' '+'\x1B[0m| progress: \x1B[1m100%\x1B[0m '+suffix+' \x1B[42m\x1B[30m\x1B[1m DONE \x1B[0m', end='\n')
        return
    
    progress = int((current_iter / num_iterations) * 100)
    num_hashes = int(progress / 2)
    num_dashes = 50 - num_hashes
    progress_str = f'progress: \x1B[1m{progress}%\x1B[0m'
    progress_str = progress_str.ljust(20)
    loading_bar = prefix + f'|\x1B[47m{num_hashes * " "}\x1B[0m{num_dashes * " "}| {progress_str} ' + '\x1B[2m'+suffix
    loading_bar = loading_bar.ljust(total_message_len)  # pad with spaces if necessary
    print('\r\x1b[2K'+loading_bar, end='')