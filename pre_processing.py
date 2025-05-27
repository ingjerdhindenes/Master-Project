import os
import subprocess
import time
import glob

# This script works on the basis of the existence of a folder "pre_processing with the folowing structure (sub folders)"

# Pre_processing
    # 0_merged_files
    # 1_dwi_denoised
    # 2_deGibbs
    # 3_eddy_corrected
    # 4_normalized_for_TE
    # 5_segmentation
        # B0_images
        # masks
        # process_files
        # T1_images


# Before use, merged files containing all dwi shells must be put into the 0_merged folder, and 
# T1 images (to be used during segmentation) must be put into the T1_images folder in the 5_segmentation folder

start_time = time.time()

os.environ['FSLOUTPUTTYPE'] = 'NIFTI_GZ' #'Nifti_GZ'
print('FSLOUTPUTTYPE set to:', os.environ.get('FSLOUTPUTTYPE'))

all_files =[''] # Input all base filenames to be processed (i.e. the name of the merged file). 
                # Note that name of dwi file and T1 image for the same subject is the same filename 
                # What the file contains is identified by the location in the subfolders not by the name

for file in all_files:
    print('pre processing file:', file)

    # Organise the paths to the folders
    path_base = '/hus/home/hining/data/pre_processing'
    merged_path = path_base + '/0_merged_files/' + file
    denoise_path = path_base + '/1_dwidenoised/' + file
    degibbs_path = path_base + '/2_deGibbs/' + file
    eddy_path = path_base + '/3_eddy_corrected/' + file
    normalized_path = path_base + '/4_normalized_for_TE/' + file

    # Run dwidenoise to denoise image
    subprocess.run(['dwidenoise', merged_path, denoise_path]) #Virker
    
    # Run nrdegibbs to reduce gibbs ringing artefact
    subprocess.run(['mrdegibbs', denoise_path, degibbs_path]) #Virker

    # Run eddy_correct to correct for eddy current artefacts
    subprocess.run(['eddy_correct', degibbs_path, eddy_path, '0']) #Virker

    # Normalize image using python file B0_normalize.py
    subprocess.run(['/hus/home/hining/.conda/envs/master_ingjerd/bin/python3', 'B0_normalize.py', eddy_path, normalized_path])


    # Segmentering (bruker b0_bilder fra etter eddy_correct er kjørt men uten normalisering)
    #Paths within the segmentation folder
    B0_path = path_base + '/5_segmentation/B0_images/' + file
    T1_path = path_base + '/5_segmentation/T1_images/' + file[:-3] 
    segmentation_output_path = path_base + '/5_segmentation/process_files/' + file[:-7] 
    transfer_masks_input_path = segmentation_output_path + '_all_fast_firstseg.nii.gz' #.nii.gz
    T1_transfered_path =  path_base + '/5_segmentation/process_files/T1_transfered_' + file
    transfer_matrix_path = path_base + '/5_segmentation/process_files/' + file[:-7] + '_transfer_matrix.mat'
    mask_path = path_base + '/5_segmentation/masks/' + file

    # Extract B0-images from eddy_correct results
    subprocess.run(['fslroi', eddy_path, B0_path, '0', '1'] )

    # Calculate masks using fsl run_first_all
    subprocess.run(['run_first_all', '-i', T1_path, '-o', segmentation_output_path])

    # remove all extra segmentation files (they all contain '-')
    segmentation_files = glob.glob(f'{segmentation_output_path}-*')
    for file in segmentation_files:
        if '-' in file:
            os.remove(file)

    # Transfer T1 image to domain of B0 image
    subprocess.run(['flirt', '-in', T1_path, '-ref', B0_path, '-out', T1_transfered_path, '-omat', transfer_matrix_path] )

    # Transfer mask to domain of B0 image
    subprocess.run(['flirt', '-in', transfer_masks_input_path, '-ref', B0_path, '-out', mask_path,
                     '-init', transfer_matrix_path, '-applyxfm', '-interp', 'nearestneighbour'])


end_time = time.time()
execution_time = end_time-start_time
print(f'Execution time:{execution_time:.2} seconds')

