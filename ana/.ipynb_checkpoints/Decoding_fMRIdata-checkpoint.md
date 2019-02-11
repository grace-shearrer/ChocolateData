https://ftp.nmr.mgh.harvard.edu/pub/docs/SavoyfMRI2014/fmri.april2011.pdf

Loading Data:

The Haxby experiment is unusual because the experimental paradigm is made of many blocks of continuous stimulation. Most cognitive experiments have a more complex temporal structure with rich sequences of events.

The standard approach to decoding consists in fitting a first-level GLM to retrieve one response map (a beta map) per trial. This is sometimes known as “beta-series regressions” (see Mumford et al, Deconvolving bold activation in event-related designs for multivoxel pattern classification analyses, NeuroImage 2012). These maps can then be input to the decoder as below, predicting the conditions associated to trial.

For simplicity, we will work on the raw time-series of the data. However, it is strongly recomended that you fit a first level to include an HRF model and isolate the responses from various confounds.


Loading the behavioral labels: Behavioral information is often stored in a text file such as a CSV, and must be load with numpy.recfromcsv or pandas
Extracting the fMRI data: we then use the nilearn.input_data.NiftiMasker: we extract only the voxels on the mask of the ventral temporal cortex that comes with the data, applying the mask_vt mask to the 4D fMRI data. The resulting data is then a matrix with a shape that is (n_timepoints, n_voxels) (see Masking data: from 4D Nifti images to 2D data arrays for a discussion on using masks).
Sample mask: Masking some of the time points may be useful to restrict to a specific pair of conditions (eg cats versus faces)


