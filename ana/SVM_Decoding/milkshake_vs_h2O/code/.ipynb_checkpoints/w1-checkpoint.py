# coding: utf-8

#this imports all the commands needed for the script to work#
import os
import numpy as np
import nilearn
import glob
import nibabel as nib
import pandas as pd 
from nilearn.input_data import NiftiMasker 
import numpy as np
np.seterr(divide='ignore', invalid='ignore')
import warnings
warnings.filterwarnings("ignore")
import matplotlib
matplotlib.use('Agg')
from sklearn.model_selection import cross_val_score



#image mask
imag_mask='/projects/niblab/bids_projects/Experiments/ChocoData/images/bin_mask.nii.gz'


#our behavioral csv file 
stim = '/projects/niblab/bids_projects/Experiments/ChocoData/behavorial_data/w1_milkshake_all.csv'

#our dataset concatenated image 
dataset='/projects/niblab/bids_projects/Experiments/ChocoData/images/w1_milkshake_all.nii.gz'
#load behavioral data into a pandas df
behavioral = pd.read_csv(stim, sep="\t")



#grab conditional labels and set up milkshake

behavioral["Label"] = behavioral.replace(['HF_LS_receipt', 'LF_LS_receipt', 'LF_HS_receipt', 'HF_HS_receipt'], 'milkshake')

y = behavioral["Label"]
print(y.unique())


#restrict data to our target analysis 
condition_mask = behavioral["Label"].isin(['milkshake', "h20_receipt"])
y = y[condition_mask]
#confirm we have the # of condtions needed
print(y.unique())




masker = NiftiMasker(mask_img=imag_mask, standardize=True, memory="nilearn_cache", memory_level=1)
X = masker.fit_transform(dataset)
# Apply our condition_mask
X = X[condition_mask]




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



# Here we run gridsearch with the SVC and feature selection
from sklearn.model_selection import GridSearchCV
k_range = [100, 500, 1000]

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
mean_img.to_filename('/projects/niblab/bids_projects/Experiments/ChocoData/derivatives/code/decoding/milkshake_vs_h2O/images/w1_mean_nimask.nii')

# Create the figure
from nilearn.plotting import plot_stat_map, show
display = plot_stat_map(weight_img, mean_img, title='Milkshake vs. H2O | wave 1 | SVM weights')
display.savefig('/projects/niblab/bids_projects/Experiments/ChocoData/derivatives/code/decoding/milkshake_vs_h2O/images/w1_SVM_nimask.png')
# Saving the results as a Nifti file may also be important
weight_img.to_filename('/projects/niblab/bids_projects/Experiments/ChocoData/derivatives/code/decoding/milkshake_vs_h2O/images/w1_SVM_nimask.nii')

