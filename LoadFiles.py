import os
import glob
import pandas as pd
#import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets

df_keys = ["RowNumber","Channel_1", "Channel_2", "Channel_3", "Channel_4", "Channel_5",
            "Channel_6", "Channel_7", "Time", "TimeStamp"]

#0, 58.85, 17.47, 34.56, -201.89, 0.000, 0.000, 0.000, 01:45:01.663, 1553067901663

def get_dataframe(force):
    cur_dir = os.getcwd()
    #print(cur_dir)
    
    #df_total = pd.DataFrame()
    df_cur   = pd.DataFrame()
    df_acc   = pd.DataFrame()
    
    if force == True:
        if 'input' not in cur_dir:
            os.chdir('input')
            cur_dir = os.getcwd()
            print(f'Change to <{cur_dir}> directory')

        #print(f'Already into <{cur_dir}> directory')
        files_list = [str(f) for f in glob.glob("*.txt")]
        if len(files_list) > 0:
            for file_str in files_list:
                print(f'Loading file <{file_str}>...')
                df_cur = pd.read_csv(file_str,skiprows=6, encoding='latin-1', header=None,  names=df_keys)
                #df_cur = df_cur[df_keys]
                df_acc = df_acc.append(df_cur)            
                #print(df_acc['Order Date'].count())
                #print(df_total['Order Date'].count())

            #df_total = df_acc    
            #print(df_total['Order Date'].count())            
            
            print('Dataframe generated')
            os.chdir('../')  
            df_acc.to_csv("output/main_dataframe.csv", encoding='utf-8', index=False)
    else:
        print(f'Loading from file <output/main_dataframe.csv>...')
        try:
            df_acc = pd.read_csv("output/main_dataframe.csv", encoding='latin-1')
        except :
            print('Error: file <output/main_dataframe.csv> not found')
        print('Dataframe generated')
        
    return df_acc                 


    

#data_frame = pd.DataFrame()
#try:
#    data_frame = get_dataframe(True)    
#except:
#    print('File not found')
#    
#if data_frame.empty:
#    print('Dataframe empty, please verify')
#    #sys.exit()
#else:        
#    data_frame.head()
#    
#data_frame.head()    
    
    
    