# Master-Project
This Github repository includes all scripts created for, and used, in the master thesis "Exploring MRI diffusion as biomarker of neuroinflammation" by Ingjerd Helstrup Hindenes.

## **Description of scripts:**

**pre_processing.py** is a script designed for automatic pre-processing of DWI data. From merged DWI data files (containing all shells) and T1 images, this scripts performs denoising, gibbs ringing removal, eddy correction, normalization and segmentation.

**B0_normalize.py** performs normalization of DWI data for TE. All DWI shells were acquired using different TE and due to Dmipy not handeling these differences normalizaton was a necessary step. This script is called by pre_processing.py during pre processing.

**model_design_and_testing.ipynb** is a script that is used to test different variations of a multi-compartment model on a selected ROI by adjusting parameter optimization ranges to see if it affects fit quality. The script saves mean squeared error (MSE) and R2 coefficient of determination values to a file. 

**multi_compartment_model.ipynb** is used to aplly the selected model design to all DWI data.

**combine_dataframes.ipynb** merges dataframes. This script was created because issues arose when trying to loop over multiple subjects in the model_design_and_testing.ipynb and multi_compartment_model.ipynb scripts. Therefore a script was created to merge all the single row dataframes saved from these previous scripts.

**correlation_analysis.ipynb** performs correlation analysis between MRI measures and MDD symptom load recorded by questionnaires by calculating the spearman´s rank coeficient and the p-value.

**create_figures.ipynb** is a script for creating figures for visualization of acquired data and results. This includes visualisation of diffusion images and segmented structures as well as scatter plots of MSE and R2 for model selection, histograms of the distribution of fitted parameter values and boxplots showing inter-subject variability.

## Dependencies
The code was run with the following system dependencies and python packages:

- FSL (version 6.0.7.15)
- MRtrix3 (version 3.0.4)
- python (version 3.11.11)
- numpy (version 2.1.3)
- nibabel (version 5.3.2)
- dmipy (version 1.0.5)
- pandas (version 2.2.3)
- scipy (version 1.14.1)
- matplotlib (version 3.9.2)
