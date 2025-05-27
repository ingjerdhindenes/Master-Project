import numpy as np
import nibabel as nib
import sys

def normalize(get_data_path, save_data_path):

    with open('/hus/home/hining/Master_ingjerd/all.bval', 'r') as file:
        bvals = [line.strip().split() for line in file]
    flat_bvals =[item for sublist in bvals for item in sublist] 
    bvalues = np.array(flat_bvals, dtype=float)
    bvalues_SI = bvalues * 1e6 #convert from [s/mm²] to SI unit [s/m²] 

    delta = np.loadtxt('/hus/home/hining/Master_ingjerd/small_delta.txt')*10e-4 #load and convert from [ms] to SI unit [s] 
    Delta = np.loadtxt('/hus/home/hining/Master_ingjerd/big_delta.txt')*10e-4 #load and convert from [ms] to SI unit [s] 

    nifti_file = nib.load(get_data_path)
    dwi_data = nifti_file.get_fdata()

    # Get rid of any negative values, as well as any very small values that appear after mrdegibbs to avoid
    # devision by microscopic numbers, creating realy big values
    dwi_data[dwi_data < 1] = 0 

    # Calculate TE and find all unique values
    TE = Delta +2*delta+0.001
    TE_unique = np.unique(TE)

    # Initialize empty image for storing normalized data
    NormData = np.zeros((256, 256, 44 ,376))   #For the first half of acquisitions
    #NormData = np.zeros((128, 128, 29 ,376))   #For the second half of acquisitions


    # Loop through every unique TE value, normalize data and store in the empty image
    for ii in range(len(TE_unique)):

        #get current TE
        cTE = TE_unique[ii]

        #compute the mean of the TE-specific B0
        B0s_idx = np.where((bvalues_SI == 0) & (TE == cTE))[0] 
        B0_images = dwi_data[:, :, :, B0s_idx] 
        avg_B0 = np.mean(B0_images, axis=3)

        # Find TE spesific data indexes
        TE_idx = np.where(TE == TE_unique[ii])[0]

        for idx in TE_idx:  # Perform normalization
            NormData[:, :, :, idx] = np.divide(dwi_data[:, :, :, idx], avg_B0, out=np.zeros_like(dwi_data[:, :, :, idx]), where=avg_B0 != 0)


    nifti_img = nib.Nifti1Image(NormData, np.eye(4))
    nib.save(nifti_img, save_data_path)




if __name__ == '__main__':
    dwi_data_path = sys.argv[1] # name is dwi data to be normalized
    normalized_data_path = sys.argv[2] 
    normalize(dwi_data_path, normalized_data_path)
