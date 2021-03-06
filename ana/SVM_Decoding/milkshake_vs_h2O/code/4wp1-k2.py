
# coding: utf-8

# In[ ]:


# coding: utf-8

# In[ ]:


#this imports all the commands needed for the script to work#
import os
import numpy as np
import nilearn
import glob
import nibabel as nib
import pandas as pd 
import numpy as np
import warnings
import matplotlib
from sklearn.model_selection import cross_val_score
from nilearn.input_data import NiftiMasker 


matplotlib.use('Agg')
warnings.filterwarnings("ignore")
np.seterr(divide='ignore', invalid='ignore')




#image mask
imag_mask='/projects/niblab/bids_projects/Experiments/ChocoData/images/bin_mask.nii.gz'



#our behavioral csv file 
stim = '/projects/niblab/bids_projects/Experiments/ChocoData/behavorial_data/4w_part1.csv'

#our dataset concatenated image 
dataset='/projects/niblab/bids_projects/Experiments/ChocoData/images/4w_part1.nii.gz'
#load behavioral data into a pandas df
behavioral = pd.read_csv(stim, sep="\t")



#grab conditional labels and set up milkshake

behavioral["Label"] = behavioral.replace(['HF_LS_receipt', 'LF_LS_receipt', 'LF_HS_receipt', 'HF_HS_receipt'], 'milkshake')

y = behavioral["Label"]
#print(y.unique())


#restrict data to our target analysis 
condition_mask = behavioral["Label"].isin(['milkshake', "h20_receipt"])
y = y[condition_mask]
#confirm we have the # of condtions needed
print(y.unique())





masker = NiftiMasker(mask_img=imag_mask, standardize=True, memory="nilearn_cache", memory_level=1)
X = masker.fit_transform(dataset)
# Apply our condition_mask
X = X[condition_mask]




"""

from sklearn.svm import SVC
svc = SVC(kernel='linear')

from sklearn.feature_selection import SelectaPercentile, f_classif
feature_selection = SelectKBest(f_classif, percentile=5)

# We have our classifier (SVC), our feature selection (SelectKBest), and now,
# we can plug them together in a *pipeline* that performs the two operations
# successively:
from sklearn.pipeline import Pipeline


anova_svc = Pipeline([('anova', feature_selection), ('svc', svc)])
anova_svc.fit(X,y)
y_pred = anova_svc.predict(X)
from sklearn.model_selection import LeaveOneGroupOut, cross_val_score

# Define the cross-validation scheme used for validation.
# Here we use a LeaveOneGroupOut cross-validation on the session group
# which corresponds to a leave-one-session-out
cv = LeaveOneGroupOut()

# Compute the prediction accuracy for the different folds (i.e. session)

percentiles = [1, 5, 10, 15, 20]
grid = GridSearchCV(anova_svc, param_grid={'anova__percentile': percentiles}, verbose=1, n_jobs=1, cv=5)
nested_cv_scores = cross_val_score(grid, X, y,  cv=cv, groups=session)
"""




from sklearn.svm import SVC
svc = SVC(kernel='linear')

from sklearn.feature_selection import SelectKBest, f_classif
feature_selection = SelectKBest(f_classif, k=500)

# We have our classifier (SVC), our feature selection (SelectKBest), and now,
# we can plug them together in a *pipeline* that performs the two operations
# successively:
from sklearn.pipeline import Pipeline


anova_svc = Pipeline([('anova', feature_selection), ('svc', svc)])
anova_svc.fit(X,y)
y_pred = anova_svc.predict(X)

# Here we run gridsearch
from sklearn.model_selection import GridSearchCV

k_range = [10, 100, 500, 1000]
grid = GridSearchCV(anova_svc, param_grid={'anova__k': k_range}, verbose=1, n_jobs=1, cv=5)
nested_cv_scores = cross_val_score(grid, X, y, cv=5)

#NEST_SCORE = np.mean(nested_cv_scores)
print("Nested CV score: %.4f" % np.mean(nested_cv_scores))





# Here is the image 
coef = svc.coef_
# reverse feature selection
coef = feature_selection.inverse_transform(coef)
# reverse masking
weight_img = masker.inverse_transform(coef)


# Use the mean image as a background to avoid relying on anatomical data
from nilearn import image
mean_img = image.mean_img(dataset)
mean_img.to_filename('/projects/niblab/bids_projects/Experiments/ChocoData/derivatives/code/decoding/milkshake_vs_h2O/w4/4wp1_k2_mean_nimask.nii')

# Create the figure
from nilearn.plotting import plot_stat_map, show
display = plot_stat_map(weight_img, mean_img, title='SVM weights LF_HS vs h2O 4 waves part 1')
display.savefig('/projects/niblab/bids_projects/Experiments/ChocoData/derivatives/code/decoding/milkshake_vs_h2O/w4/4wp1_k2_SVM_nimask.png')
# Saving the results as a Nifti file may also be important
weight_img.to_filename('/projects/niblab/bids_projects/Experiments/ChocoData/derivatives/code/decoding/milkshake_vs_h2O/w4/4wp1_k2_SVM_nimask.nii')

