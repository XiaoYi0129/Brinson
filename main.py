import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plot
import os

def handle_file(file):
    df = pd.read_csv(file, sep='\\t', encoding='UTF-16LE', engine='python',
                     skiprows=1, header=None).replace(np.NaN, 0)
    dfshape = df.shape
    # i=0
    # j=0
    # if df.iloc[0,12]!=df.iloc[0,12]:
    #     print('Yes')
    # if df.iloc[1,14]==None:
    #     print('Yes')
    for i in range(dfshape[0]):
        for j in range(dfshape[1]):
            this_data = df.iloc[i, j]
            if this_data != 0:
                df.iloc[i, j] = df.iloc[i, j].replace('\"', '')

    df.columns = df.iloc[0]
    df = df.drop(0)

    group_df = df.groupby(by='Industry')
    head_w='w'
    head_g='g'
    if file[2]=='C':
        head_w='hscei_w'
        head_g='hscei_g'
    else:
        head_w='hsi_w'
        head_g='hsi_g'
    result = pd.DataFrame([[0, 0, 0]], columns=['industry', head_w, head_g])

    for i in group_df:
        df = i[1]
        df_shape = df.shape
        for j in range(8, df_shape[1]):
            df.iloc[:, j] = pd.to_numeric(df.iloc[:, j])
        industry = df['Industry'].iloc[0]
        w = df['Weighting (%)'].sum()
        g = 0

        for k in range(df_shape[0]):
            object = df.iloc[k]
            g = g + object.loc['% Change'] * object.loc['Weighting (%)']
        g = g / w
        result.loc[result.shape[0], :] = [industry, w, g]
    result = result.drop(0)
    return result

def file_arr(file):
    arr=[]
    for root, dirs, files in os.walk(file):
        for file in files:
            path = os.path.join(root, file)
            arr.append(path)
    return arr


def handle_day(hsi_file,hscei_file):
    result_hsi=handle_file(hsi_file)
    result_hscei=handle_file(hscei_file)
    result = pd.DataFrame(result_hscei['industry'], columns=['industry'])

    result['hscei_w'] = result_hscei['hscei_w']
    #print(result_hsi)
    #print(result)
    result['hsi_w'] = result_hsi['hsi_w']
    result['hscei_g'] = result_hscei['hscei_g']
    result['hsi_g'] = result_hsi['hsi_g']
    #result.index = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    #print(result)


    result.loc[len(result)] = ['total', result['hscei_w'].sum()
        , result['hsi_w'].sum(), result['hscei_g'].sum(), result['hsi_g'].sum()]
    s_alloc = pd.Series([])
    s_select = pd.Series([])
    s_inteact = pd.Series([])
    result_shape = result.shape
    for i in range(result_shape[0]):
        object = result.iloc[i, :]
        #print(result)
        b_alloc = result.iloc[-1,:]['hsi_g']
        alloc = (object['hscei_w'] - object['hsi_w']) * (object['hsi_g'] - b_alloc) / 100
        s_alloc[i] = alloc

        select = object['hsi_w'] * (object['hscei_g'] - object['hsi_g']) / 100
        s_select[i] = select

        inteact = (object['hscei_w'] - object['hsi_w']) * (object['hscei_g'] - object['hsi_g']) / 100
        s_inteact[i] = inteact

    result['allocation'] = s_alloc
    result['selection'] = s_select
    #print(result)
    #===================================================
    #print(result['selection'].sum())
    result['interaction'] = s_inteact
    result.iloc[-1,5] = result['allocation'].sum()
    result.iloc[-1,6] = result['selection'].sum()
    result.iloc[-1,7] = result['interaction'].sum()
    #print(result)
    return result


hsi_arr=file_arr(r'HSI/CSV_Format')
hsi_arr.sort(key=lambda x:x[24:29])

hscei_arr=file_arr(r'HSCEI/CSV_Format')
hscei_arr.sort(key=lambda x:x[28:33])

brinson=pd.DataFrame([[0,0,0,0,0,0,0,0]],columns=['date','hscei_w','hsi_w','hscei_g','hsi_g','allocation','selection','interaction'])

for i in range(len(hsi_arr)):

     result=handle_day(hsi_arr[i],hscei_arr[i])
     #print(result)
     #print(result)
     #result1=result.rename(columns={'industry':'date'})
     #print(i)
     #print(result)
     #object=result.iloc[10,:]
     #brinson.iloc[i,:]=object
     #result_shape=result.shape
     object=result.iloc[-1,:]
     date=hsi_arr[i][19:29]
     object=object._append(pd.Series([date],['date']))
     #print(object)
     brinson.loc[len(brinson)]=object

brinson=brinson.drop(0)

brinson.to_csv(r'result.csv')











#result=handle_day('HSI/CSV_Format/HSI_2019_06_03.csv','HSCEI/CSV_Format/HSCEI_2019_06_03.csv')


#result_hsi=handle_file('HSI/CSV_Format/HSI_2019_06_03.csv')
#result_hscei=handle_file('HSCEI/CSV_Format/HSCEI_2019_06_03.csv')
#result=handle_day('HSI/CSV_Format/HSI_2019_06_03.csv','HSCEI/CSV_Format/HSCEI_2019_06_03.csv')
#print(result)








