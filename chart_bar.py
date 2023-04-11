import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
import os

df = pd.read_csv('result.csv',sep=',')
df=df.drop(columns=['Unnamed: 0'])
fig=plt.figure(figsize=(8,5),dpi=300)

hscei_g=df['hscei_g']
hsi_g=df['hsi_g']
ax1=fig.add_subplot(111)

x=np.arange(df.shape[0])
total_width,n=0.8,2
width = total_width/n
x = x -(total_width-width)/2
plt.bar(x,hscei_g,width=width,label='hscei gain')
plt.bar(x+width,hsi_g,width=width,label='hsi gain')
plt.legend()

locs=np.linspace(0,55,8).astype(int)
label=[]
for i in locs:
    label.append(df['date'][i])
plt.xticks(locs,label,size=4,rotation=-30,)

#plt.xticks(locs,label,size=4,rotation=-30,)
plt.title('Gain',loc='center')
plt.savefig('chart_bar.png')
plt.show()