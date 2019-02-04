
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import keras
import warnings
import import_ipynb
import pipeline22 as pp2
import json
    
warnings.filterwarnings("ignore")


# In[2]:


def one_hot_encode(s):
    i=0
    
    dict_i = {"A" : 0, "C": 1, "G": 2, "T" : 3,"a":0, "c":1, "g":2, "t":3}
    ohe = np.zeros((len(s), 4))
    
    for k in s:
        
        if k=='N' or k=='n':
            ohe[i,0] = 0.25
            ohe[i,1] = 0.25
            ohe[i,2] = 0.25
            ohe[i,3] = 0.25
            
        else:
            ohe[i,dict_i[k]] = 1
        i+=1
    return ohe


# In[3]:


def deepbind1(df,count):
    
    
    print("Shape is: ",df.shape)
    
    temp_sequences=df['seq']
    temp_target=df['target']
    
    
    ohe_sequences = np.array([one_hot_encode(s) for s in temp_sequences])
    print ohe_sequences
    ohe_sequences.shape
    
    from keras.models import Sequential
    from keras.layers import Dense
    from keras.layers import Conv1D
    from keras.layers import MaxPooling1D
    from keras.layers import Dropout,Flatten
    from sklearn.utils import shuffle
    from sklearn.model_selection import train_test_split

    model = Sequential()
    model.add(Conv1D(filters=10, kernel_size=10, activation='relu', input_shape=(200,4)))
    model.summary()

    model.add(MaxPooling1D(pool_size=10, strides=10))
    model.add(Flatten())
    
    model.add(Dense(200,  activation='relu'))
    
    model.add(Dense(1, activation = "sigmoid"))
    
    model.summary()
    
    model.compile(loss='binary_crossentropy', optimizer='Adam', metrics=['accuracy'])
    
    data_train, data_test, labels_train, labels_test = train_test_split(ohe_sequences, temp_target, test_size=0.30, random_state=42, shuffle=True)
    
    model.fit(data_train, labels_train, epochs=5, verbose=1)
    
    scores = model.evaluate(data_test, labels_test)
    print ("Test loss ", scores[0])
    print ("Test acc ", scores[1])
    model.save_weights("modelweights/model_"+str(count)+"_weights.h5")
    my_json_string = model.to_json()
    jsonData = json.loads(my_json_string)
    print jsonData["config"]
    with open("models/model_"+str(count)+".json", "w") as json_file:
        json_file.write(my_json_string)
    from sklearn.metrics import roc_curve
    keras_model= model
    y_pred_keras = keras_model.predict(data_test).ravel()
    fpr_keras, tpr_keras, thresholds_keras = roc_curve(labels_test, y_pred_keras)
    
    from sklearn.metrics import auc
    auc_keras = auc(fpr_keras, tpr_keras)

    return auc_keras


# In[4]:


# def convertKerasJSONtoDeepLIFT(kerasJSON_str):
#     jsonData = json.loads(kerasJSON_str)
#     layersData = jsonData["config"]["layers"]
#     jsonData["config"] = layersData
#     return json.dumps(jsonData)

