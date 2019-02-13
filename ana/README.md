# Data Analysis  
Decoding with a Support Vector Machine [SVM](https://github.com/niblunc/ChocolateData/tree/master/data_ana/SVM_Decoding) and ANOVA analysis found [here.](https://github.com/niblunc/ChocolateData/tree/master/data_ana/SVM_Decoding) 
<br>
<br>
Go straight to a paradigm folder for relevant files/explanations: 

  * [milkshake vs. h2O](https://github.com/niblunc/ChocolateData/tree/master/ana/SVM_Decoding/milkshake_vs_h2O)
  * [LF_HS vs. h2O](https://github.com/niblunc/ChocolateData/tree/master/data_ana/SVM_Decoding/LF_HS_vs_h2O)  
  * [LF_LS vs. h2O](https://github.com/niblunc/ChocolateData/tree/master/data_ana/SVM_Decoding/LF_LS_vs_h2O)
  * [HF_HS vs. h2O](https://github.com/niblunc/ChocolateData/tree/master/data_ana/SVM_Decoding/HF_HS_vs_h2O)
  * [HF_LS vs. h2O](https://github.com/niblunc/ChocolateData/tree/master/data_ana/SVM_Decoding/HF_LS_vs_h2O)
 

## Experiment Data Setup 
- Concatenating individual subject images (.nii.gz) to a single nifti file (.nii). [FILE](https://github.com/niblunc/ChocolateData/blob/master/ana/higher_ana_prep/Concatenating_Images.ipynb)
- Setting up behavioral (.csv) [FILE](https://github.com/niblunc/ChocolateData/blob/master/ana/higher_ana_prep/Create_behaviorals-milkshake.ipynb)
- Averaging masks [FILE](https://github.com/niblunc/ChocolateData/blob/master/ana/higher_ana_prep/average_masks.ipynb)
- Estimation Parameter search [FILE](https://github.com/niblunc/ChocolateData/blob/master/ana/higher_ana_prep/estimation_parameter_search_milkshake.ipynb)
- Separating waves for partial images [FILE](https://github.com/niblunc/ChocolateData/blob/master/ana/higher_ana_prep/separating_waves.ipynb)

## 
## Decoding Chocolate Data   

### Data Preparation:  
- DICOM to BIDS using Singularity & Heudiconv Converter *link to script*  
- BIDS to fmriprep *link to script*  
- Skull stripping and motion correction *link to script* 
- Feat1 Analysis using FSL *link to script*
- Behavioral *.csv file setup *link to script*

