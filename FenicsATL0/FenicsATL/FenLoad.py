import pandas as pd
import warnings
warnings.filterwarnings("ignore")



def FenicsData_read(path):
    """This is a function that loads the Fenics dataset, and keeps it formated in column, sub column format, with tuples."""
    loaded_data = pd.read_json(path)
    columns = loaded_data.columns
    tuples = [(column.split(',')[0].replace("(","").replace("'","").strip(), column.split(',')[1].replace(")","").replace("'","").strip()) for column in columns]
    loaded_data.columns = pd.MultiIndex.from_tuples(tuples)
    to_float = lambda d: {k: float(v) if isinstance(v, str) else v for k, v in d.items()} if isinstance(d, dict) else d
    loaded_data = loaded_data.applymap(to_float)
    return loaded_data



def FenicsVers_filter(data,
                      *args,
                      index = True) :
    """
    This is a filtring function that takes the dataset, and the Fenics ids to filter, returns a sliced dataframe.
    data :  (df) fenics dataframe.
    *args : (int) fenics ids.
    Filter11 : (bool) filter or not values of FENICS111, by default it is True.
    index : (bool) decides if you want to ignore index or reset it, by default it is to True.
    """
    Fenics_ids = []
    for arg in args:
        if isinstance(arg, int):  # Check if the argument is an integer
            Fenics_ids.append(arg)
        elif isinstance(arg, list):  # Check if the argument is a list
            Fenics_ids.extend(arg)
        else:
            print(f"Warning: Argument {arg} is not an integer or list.")

    for i,Fenics_id in enumerate(Fenics_ids) :
        if Fenics_id != 2 and Fenics_id != 3 and Fenics_id != 11:
            FENICS_temp = data[data.Board.id == Fenics_id]
            FENICS_temp.Board.date = pd.to_datetime(FENICS_temp.Board.date)
            if i == 0 :
                FENICS = FENICS_temp.sort_values(by= ('Board','date'),ascending = True).reset_index(drop=True)
            else :
                FENICS = pd.concat([FENICS,FENICS_temp.reset_index(drop=True)], ignore_index=index)
        elif Fenics_id == 11:
            continue
        else :
            raise Exception("Fenics board "+ str(Fenics_id) + " is not in the database")
    
    return FENICS



def FenicsTestTable(FENICS,
                    mode,
                    resetIndex = False):
    temp_dict = {}
    exclude = ['GainRatioSC','GainRatioLC']
    if mode.capitalize() == 'Fast' :
        SubCols = [subCol for subCol in FENICS.FastResult.columns]
    elif mode.capitalize() == 'Slow' :
        SubCols = [subCol for subCol in FENICS.SlowResult.columns]
    else :
        raise Exception("Fenics results can only be 'Fast or Slow'")
    
    
    for subCol in SubCols :
        if subCol in exclude :
            temp_dict[('Gain',subCol)] = FENICS.FastResult[subCol]
        else : 
            for key in FENICS[mode.capitalize()+'Result'][subCol].iloc[0]:
                if mode.capitalize() == 'Fast' :
                    for row in FENICS.FastResult[subCol]:
                        if (subCol,key) not in temp_dict:
                            temp_dict[(subCol,key)] = []
                        temp_dict[(subCol,key)].append(row[key])
                elif mode.capitalize() == 'Slow':
                    for subkey in FENICS.SlowResult[subCol].iloc[0][key]:
                        for row in FENICS['SlowResult'][subCol]:
                            if (subCol,key,subkey) not in temp_dict:
                                temp_dict[(subCol,key,subkey)] = []
                            temp_dict[(subCol,key,subkey)].append(float(row[key][subkey]))
    if resetIndex == False :
        return pd.concat([pd.DataFrame(temp_dict, index=FENICS.index)], axis=1)    
    else :                
        return pd.DataFrame(temp_dict)
