
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import keras
import warnings
import import_ipynb
import pipeline22 as pp2
import DeepBind22 as db22
import os
warnings.filterwarnings("ignore")

dir(db22)


# In[2]:


filenames1 = ['ENCFF379CMJ_EP300.bed']


# In[3]:


filenames2 = ['ENCFF379CMJ_EP300.bed','ENCFF624XRN_H2AFZ.bed','ENCFF498CMP_H3K36me3.bed','ENCFF183UQD_H3K4me1.bed','ENCFF894VEM_H3K9me3.bed','ENCFF139CKE_H4K20me1.bed','ENCFF099LMD_H3K4me2.bed']


# In[4]:


df_final = pd.DataFrame(columns=['File1','File2','Accuracy'])

print len(filenames1)
print len(filenames2)


# In[ ]:


from Bio import SeqIO
count=0
for i in range(len(filenames1)):
    for j in range(i+1,len(filenames2)):
        f1 = filenames1[i]
        f2 = filenames2[j]
        pp2.pipe(f1,f2)
        
        file1, file_extension1 = os.path.splitext(f1)
        file2, file_extension2 = os.path.splitext(f2)
        
        class0= file1+"_70"+".fa"
        class1= file2+"_70"+".fa"

        list0=[]
        list1=[]

        for record in SeqIO.parse(class0, "fasta"):
            list0.append(str(record.seq))
        for record in SeqIO.parse(class1, "fasta"):
            list1.append(str(record.seq))
        target=[]
    
    
        for t in range(len(list0)):
            target.append(0)
        
        for m in range(len(list1)):
            target.append(1)
        
        sequences=list0+list1

        dict = {'seq': sequences, 'target': target}
        df = pd.DataFrame(dict)
        
        accuracy= db22.deepbind1(df,count)
        print("File1: ",f1,"\n")
        print("File2: ",f2,"\n")
        print("Accuracy: ",accuracy,"\n")
        df_final.loc[count,['File1']] = str(f1)
        df_final.loc[count, ['File2']] = str(f2)
        print accuracy
        df_final.loc[count, ['Accuracy']] = accuracy
        
        count=count+1


# In[6]:


print df_final


# In[7]:


df_final.to_csv("FinalAccuracies_withmodel.csv")


# In[8]:


print df_final


# In[9]:


matrix = np.full((55, 55), 12)
acc = df_final["Accuracy"]
print acc
for i in range(0,54):
    for j in range(0,54):
        matrix[i][j] = acc[i]
        matrix[j][i] = acc[i]
print matrix


# In[ ]:


df_final.sort_values(['Accuracy'], ascending=[0])

