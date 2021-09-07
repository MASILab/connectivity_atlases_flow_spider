

# connectivity atlases spider
This pipeline facilitates the creation of atlases for Connectoflow [1].
It creates atlases from the Freesurfer output: Brainnetome [2], Glasser [3], Schaefer [4], Lausanne multi-scales [5] and lobes. All atlases are free of WM and CSF labels, ready for connectomics.
All output atlases have the following files associated with them:
- atlas_*_v4.nii.gz (parcellation as computed)
- atlas_*_v4_dilate.nii.gz (parcellation with cortical labels dilate into the WM)
- atlas_*_v4_LUT.json (Links the labels number to its name)
- atlas_*_v4_LUT.txt (Links the labels number to its name and color scheme for Freeview)
- atlas_*_v4_labels_list.txt (Contains the list of expected labels number)



### References
    [1] Rheault, Francois, et al. "Connectoflow: A cutting-edge Nextflow pipeline for structural connectomics",
        ISMRM 2021 Proceedings, #710.
    [2] Fan, Lingzhong, et al. "The human brainnetome atlas: a new brain atlas based on connectional architecture.",
        Cerebral cortex 26.8 (2016): 3508-3526.
    [3] Glasser, Matthew F., et al. "A multi-modal parcellation of human cerebral cortex.",
        Nature 536.7615 (2016): 171-178.
    [4] Schaefer, Alexander, et al. "Local-global parcellation of the human cerebral cortex from intrinsic functional connectivity MRI.",
        Cerebral cortex 28.9 (2018): 3095-3114.
    [5] Tourbier, Sebastien et al. "Multi-scale-brain-parcellator-a-bids-app-for-the-lausanne-connectome-parcellation",
        OHBM 2019 Annual Meeting.

### Inputs
- t1.nii.gz (Same as the one given to Tractoflow)

### Outputs
**Reporting**
- report.html
- report.pdf

**Atlases**
- *freesurfer*.[nii.gz,txt,json]
- *brainnetome*.[nii.gz,txt,json]
- *glasser*.[nii.gz,txt,json]
- *lobes*.[nii.gz,txt,json]
- *schaefer_100*.[nii.gz,txt,json]
- *schaefer_200*.[nii.gz,txt,json]
- *schaefer_400*.[nii.gz,txt,json]
- *lausanne_2008_scale_1*.[nii.gz,txt,json]
- *lausanne_2008_scale_2*.[nii.gz,txt,json]
- *lausanne_2008_scale_3*.[nii.gz,txt,json]
- *lausanne_2008_scale_4*.[nii.gz,txt,json]
- *lausanne_2008_scale_5*.[nii.gz,txt,json]

### Input assumptions
- The input T1w image should not have been skull strip.
- If the goal is to use this pipeline with Connectoflow, they need the same T1w as input
