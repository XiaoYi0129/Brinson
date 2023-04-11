import pandas as pd
import csv
import numpy as np
import matplotlib.pyplot as plt
import os

df = pd.read_csv('result.csv',sep=',')
df=df.drop(columns=['Unnamed: 0'])
fig=plt.figure(figsize=(8,5),dpi=300)

alloc=df['allocation']
select=df['selection']
interact=df['interaction']

ax1=fig.add_subplot(111)

line1,=ax1.plot(alloc,color='lightcoral',label='allocation effect')
line2,=ax1.plot(select,color='orange',linestyle=':',label='selection effect')
line3,=ax1.plot(interact,color='cornflowerblue',label='interaction effect')

plt.legend((line1,line2,line3),('allocation effect','selection effect','interaction effect'),loc='center',
           bbox_to_anchor=(0.45, 0.1))
plt.xlabel('date')
locs=np.linspace(0,55,11).astype(int)


label=[]
for i in locs:
    label.append(df['date'][i])

plt.xticks(locs,label,size=4,rotation=-30,)
plt.title('Effect',loc='center')

plt.savefig('chart_line.png')
plt.show()


