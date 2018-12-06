
# coding: utf-8

# In[ ]:


#this imports all the commands needed for the script to work#
import os
import numpy as np
import nilearn
import glob
#import matplotlib
import nibabel as nib
import pandas as pd 
from nilearn.input_data import NiftiMasker 
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import warnings
warnings.filterwarnings("ignore")
import matplotlib
matplotlib.use('Agg')


# ### Load Data | Subject Count: 48

# In[ ]:


#image mask
imag_mask='/projects/niblab/bids_projects/Experiments/ChocoData/images/power_roimask_4bi.nii.gz'
#our behavioral csv file 
stim = '/projects/niblab/bids_projects/Experiments/ChocoData/behavorial_data/w1_milkshake_100.csv'
#our dataset concatenated image 
dataset='/projects/niblab/bids_projects/Experiments/ChocoData/images/w1_milkshake_100.nii.gz'
#load behavioral data into a pandas df
behavioral = pd.read_csv(stim, sep="\t")
#grab conditional labels  
y = behavioral["Label"]
session = behavioral["sess"]


# In[ ]:


# look at unique labels and to see if we want to remove uninteresting ones
print(y.unique())


# ['rest' 'milkshake_pic' 'LF_HS_receipt' 'rinse' 'HF_HS_receipt'
#  'LF_LS_receipt' 'h20_pic' 'h20_receipt' 'HF_LS_receipt']

# In[ ]:


#remove rest 
non_rest = (y != 'rest')
y = y[non_rest]
#verify rest is out
print(y.unique())


# ['milkshake_pic' 'LF_HS_receipt' 'rinse' 'HF_HS_receipt' 'LF_LS_receipt'
#  'h20_pic' 'h20_receipt' 'HF_LS_receipt']

# In[ ]:


# Get labels of the numerical conditions represented by the y vector 
unique_conditions, order = np.unique(y, return_index=True)
# Sort the conditions by order of appearance
unique_conditions = unique_conditions[np.argsort(order)]


# In[ ]:


# Prep data
from sklearn.preprocessing import Imputer
masker = NiftiMasker(mask_img=imag_mask, standardize=True, memory="nilearn_cache", sessions=session, memory_level=1)
X = masker.fit_transform(dataset)


imputer = Imputer(missing_values="NaN", strategy="mean", axis=0)
imputer = imputer.fit(X)
X = imputer.transform(X)

X = X[non_rest]
session=session[non_rest]


# In[ ]:


from sklearn.svm import SVC
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.multiclass import OneVsOneClassifier, OneVsRestClassifier
from sklearn.pipeline import Pipeline

svc_ovo = OneVsOneClassifier(Pipeline([
    ('anova', SelectKBest(f_classif, k=500)),
    ('svc', SVC(kernel='linear'))
]), n_jobs=4)

svc_ova = OneVsRestClassifier(Pipeline([
    ('anova', SelectKBest(f_classif, k=500)),
    ('svc', SVC(kernel='linear'))
]), n_jobs=4)


# In[ ]:


from sklearn.model_selection import cross_val_score

cv_scores_ovo = cross_val_score(svc_ovo, X, y, cv=5, verbose=1)

cv_scores_ova = cross_val_score(svc_ova, X, y, cv=5, verbose=1)

print('OvO:', cv_scores_ovo.mean())
print('OvA:', cv_scores_ova.mean())
stringA = 'OvO:', cv_scores_ovo.mean()
stringB = 'OvA:', cv_scores_ova.mean()
fileout = open("/projects/niblab/bids_projects/Experiments/ChocoData/multi_class_strats_milk.txt", "a")
fileout.write(stringA)
fileout.write(stringB)


# In[ ]:


from matplotlib import pyplot as plt
display = plt.figure(figsize=(4,3))
display = plt.boxplot([cv_scores_ova, cv_scores_ovo])
display = plt.xticks([1,2], ["Onve vs All", "One vs One"])
display = plt.title("Prediction:Accuracy score")
display.savefig("/projects/niblab/bids_projects/Experiments/ChocoData/multi_class_milk.png")


# In[ ]:


from sklearn.metrics import confusion_matrix
from nilearn.plotting import plot_matrix

svc.ovo.fit(X[session < 1], y[session < 1])
y_pred_ovo = svc.ovo = svc.ovo.predict(X[session == 1])

matrix1 =plot_matrix(confusion_matrix(y_pred_ovo, y[session==1]),
            label=unique_conditions,
            title="Confusion matrix: One vs. One", cmap="hot_r")

svc.ova.fit(X[session < 1], y[session < 1])
y_pred_ova = svc.ova = svc.ova.predict(X[session == 1])

matrix2 =plot_matrix(confusion_matrix(y_pred_ova, y[session==1]),
            label=unique_conditions,
            title="Confusion matrix: One vs. All", cmap="hot_r")

matrix1.savefig("/projects/niblab/bids_projects/Experiments/ChocoData/one_v_one_matrix.png")
matrix2.savefig("/projects/niblab/bids_projects/Experiments/ChocoData/one_v_all_matrix.png")

