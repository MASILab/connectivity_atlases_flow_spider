

# connectoflow_spider
Connectoflow Spider from XNAT

Connectoflow [1] is Nextflow [2] pipeline to generate Connectomics [3,4] matrices from tractography data.
The key steps in this version of Connectoflow are:
- Decompose: This step performs the parcel-to-parcel decomposition of the tractogram. It includes streamline-cutting
    operations to ensure streamlines have terminations in the provided atlas. Moreover, connection-wise cleaning processes
    that remove loops, discard spurious streamlines and discard incoherent curvatures are used to remove as many false
    positives as possible [5].
- COMMIT: To further decrease the number of invalid streamlines and assign a quantitative weight to each streamline,
    Convex Optimization Modeling for Micro-structure Informed Tractography (COMMIT) [6,7] is used. This not only allows the
    removal of aberrant or spurious streamlines, but it was shown to increase reproducibility of connectivity measures by
    being more robust to various tractography biases. 
- AFD: Apparent Fiber Density (AFD) [8,9] is subsequently computed connection-wise using streamline orientations
    (fixel), which can be computationally burdensome if done on every pairwise connection of the connectome a posteriori.
    This step will provide a AFD-weighted connectivity matrix.

### References
    [1] Rheault, Francois, et al. "Connectoflow: A cutting-edge Nextflow pipeline for structural connectomics", ISMRM 2021 Proceedings, #710. 
    
    [2] Di Tommaso, Paolo, et al. "Nextflow enables reproducible  computational workflows.", Nature biotechnology 35.4 (2017): 316-319. 
    
    [3] Sotiropoulos, Stamatios N., and Andrew Zalesky. "Building connectomes using diffusion MRI: why, how and but.", NMR in Biomedicine 32.4 (2019): e3752.
    
    [4] Yeh, Chun-Hung, et al. "Mapping structural connectivity using diffusion MRI: challenges and opportunities.", Journal of Magnetic Resonance Imaging (2020). 
    
    [5] Zhang, Zhengwu, et al. "Mapping population-based structural connectomes.", NeuroImage 172 (2018): 130-145. 
    
    [6] Daducci, Alessandro, et al. "COMMIT: convex optimization modeling for microstructure informed tractography.", IEEE transactions on medical imaging 34.1 (2014): 246-257. 
    
    [7] Schiavi, Simona, et al. "A new method for accurate in vivo mapping of human brain connections using microstructural, and anatomical information." Science advances 6.31 (2020): eaba8245. 
    
    [8] Raffelt, David A., et al. "Investigating white matter fibre density and morphology using fixel-based analysis.", Neuroimage 144 (2017): 58-73. 
    
    [9] Dhollander, Thijs, et al. "Fixel-based Analysis of Diffusion MRI: Methods, Applications, Challenges and Opportunities." (2020).


### Inputs
- t1.nii.gz (from Slant)
- labels.nii.gz (from Slant)
- dwi_resampled.nii.gz (from Tractoflow)
- dwi_resampled.nii.gz (from Tractoflow)
- dwi.bval (from Tractoflow)
- dwi.bvec (from Tractoflow)
- fodf.nii.gz (from Tractoflow)
- peaks.nii.gz (from Tractoflow)
- fodf.nii.gz (from Tractoflow)
- output0GenericAffine.mat (from Tractoflow)
- output1Warp.nii.gz (from Tractoflow)
- fa.nii.gz (from Tractoflow)
- md.nii.gz (from Tractoflow)
- rd.nii.gz (from Tractoflow)
- ad.nii.gz (from Tractoflow)
- nufo.nii.gz (from Tractoflow)
- afd_total.nii.gz (from Tractoflow)
- afd_sum.nii.gz (from Tractoflow)
- afd_max.nii.gz (from Tractoflow)
- ensemble.trk (from Tractoflow)

### Outputs
**Reporting**
- report.html
- report.pdf

**Connectivity matrices**
- *.npy

**MNI space data**
- mni_icbm152_nlin_asym_09c_t1_masked.nii.gz (template)
- labels_warped_mni_int16.nii.gz
- t1_mni.nii.gz
- decompose_warped_mni.h5

**Transforms to MNI**
- output0GenericAffine.mat
- output1Warp.nii.gz
- output1InverseWarp.nii.gz

### Input assumptions and parameters choice
Tractogram from Tractoflow should have at least 1M-2M streamlines
Connectoflow is optimized for probabilistic tractography
Connectoflow is robust to lesions/tumors IF the tractography was adapted for the situation AND Slant parcellations is valid
This pipeline does not perform any statistical analysis, this should be planned separately beforehand