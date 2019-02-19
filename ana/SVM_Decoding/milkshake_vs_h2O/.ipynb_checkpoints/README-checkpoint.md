# Chocolate Milkshakes vs. h2O  
<br>
Scripts for decoding on the chocolate milkshakes vs. h2O paradigm.  
<br>
<br>

Location of files on RENCI: 
``` /projects/niblab/bids_projects/Experiments/ChocoData/derivatives/code/decoding/milkshake_vs_h2O```  

Location of image files (.nii & .png) on RENCI:  
```/projects/niblab/bids_projects/Experiments/ChocoData/derivatives/code/decoding/milkshake_vs_h2O/images```

<br>


Find **jupyter notebooks** [here](https://github.com/niblunc/ChocolateData/tree/master/ana/SVM_Decoding/milkshake_vs_h2O/notebooks) with code explanation and outputs, the [images](https://github.com/niblunc/ChocolateData/tree/master/ana/SVM_Decoding/milkshake_vs_h2O/images) directory here holds the SVM weight images (.png).  
* [wave1](https://github.com/niblunc/ChocolateData/blob/master/ana/SVM_Decoding/milkshake_vs_h2O/notebooks/wave1.ipynb) - this is the code and result of decoding on milkshake vs. h2O using subjects that completed 4 waves. This data is divided into two parts for faster processing.   
* [all_waves1-4]() - this is the code and result of decoding on milkshake vs. h2O using all data availabe in waves 1-4. **UPDATING/RUNNING**  
* [code_explanation](https://github.com/niblunc/ChocolateData/blob/master/ana/SVM_Decoding/milkshake_vs_h2O/notebooks/code_explanation.ipynb) - example of code explained in a step by step notebook. *this code is the base for all other analysis*
* [SelectKBest_vs_SelectPercentile](https://github.com/niblunc/ChocolateData/blob/master/ana/SVM_Decoding/milkshake_vs_h2O/notebooks/SelectKBest_vs_SelectPercentile.ipynb) - looking at the differences between feature selection using SelectPercentile vs. SelectKBest
* [Nifti files](https://github.com/niblunc/ChocolateData/blob/master/ana/SVM_Decoding/milkshake_vs_h2O/niftis.zip) - zip file containing decoded (.nii) files, also available on RENCI !! **UPDATING**
** The zip folder holds the nifti images. Each run creates a `_mean` image and a coefficient image. 

Batch jobs (.job) and individual image (.py)  [code](https://github.com/niblunc/ChocolateData/tree/master/ana/SVM_Decoding/milkshake_vs_h2O/code) can be found [here.](https://github.com/niblunc/ChocolateData/tree/master/ana/SVM_Decoding/milkshake_vs_h2O/code)    
  
