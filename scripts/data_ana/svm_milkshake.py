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

#image mask
imag_mask='/projects/niblab/bids_projects/Experiments/ChocoData/images/power_roimask_4bi.nii.gz'
#our behavioral csv file 
stim = '/projects/niblab/bids_projects/Experiments/ChocoData/behavorial_data/w1_milkshake_all.csv'
#our dataset concatenated image 
dataset='/projects/niblab/bids_projects/Experiments/ChocoData/images/w1_milkshake_all.nii.gz'
#load behavioral data into a pandas df
behavioral = pd.read_csv(stim, sep="\t")
#grab conditional labels 
y = behavioral["Label"]
#restrict data to our target analysis 
condition_mask = behavioral["Label"].isin(['LF_HS_receipt', "h20_receipt"])
y = y[condition_mask]

# Record these as an array of sessions, with fields for condition and run 
session = behavioral['sess']
masker = NiftiMasker(mask_img=imag_mask, standardize=True, memory="nilearn_cache", memory_level=1)
X = masker.fit_transform(dataset)
#Apply our condition mask
X=X[condition_mask]
session=session[condition_mask]

from sklearn.svm import SVC
svc = SVC(kernel='linear')


# Define the dimension reduction to be used.
# Here we use a classical univariate feature selection based on F-test,
# namely Anova. We set the number of features to be selected to 500
from sklearn.feature_selection import SelectKBest, f_classif
feature_selection = SelectKBest(f_classif, k=500)

# We have our classifier (SVC), our feature selection (SelectKBest), and now,
# we can plug them together in a *pipeline* that performs the two operations
# successively:
from sklearn.pipeline import Pipeline
anova_svc = Pipeline([('anova', feature_selection), ('svc', svc)])

from sklearn.model_selection import cross_val_score

k_range = [10, 50, 150, 300, 500, 1000,3000]
from sklearn.model_selection import GridSearchCV
# We are going to tune the parameter 'k' of the step called 'anova' in
# the pipeline. Thus we need to address it as 'anova__k'.

# Note that GridSearchCV takes an n_jobs argument that can make it go
# much faster
grid = GridSearchCV(anova_svc, param_grid={'anova__k': k_range}, verbose=1,
                    cv=3, n_jobs=4)
nested_cv_scores = cross_val_score(grid, X, y, cv=3)
fileout=("/projects/niblab/bids_projects/Experiments/ChocoData/Nested_CV_scores_milkshake.txt", "a")
fileout.write("Nested CV score: %.4f" % np.mean(nested_cv_scores))
fileout.close()
coef = svc.coef_
# reverse feature selection
coef = feature_selection.inverse_transform(coef)
# reverse masking
weight_img = masker.inverse_transform(coef)


# Use the mean image as a background to avoid relying on anatomical data
from nilearn import image
mean_img = image.mean_img(dataset)

# Create the figure
from nilearn.plotting import plot_stat_map
plot_stat_map(weight_img, mean_img, title='SVM weights')

# Saving the results as a Nifti file may also be important
weight_img.to_filename('/projects/niblab/bids_projects/Experiments/ChocoData/milkshake_svm_nested.nii')