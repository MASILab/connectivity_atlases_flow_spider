#!/bin/bash

IN_DIR=${1}
OUT_DIR=${2}
N_SUBJ=${3}
N_SESS=${4}
IN_T1=${5}

# Prepare input for Connectoflow
cd /TMP/
mkdir raw/${N_SUBJ}_${N_SESS}/ -p
cp ${IN_DIR}/${IN_T1} raw/${N_SUBJ}_${N_SESS}/t1.nii.gz

# Launch pipeline
../nextflow /freesurfer-nf/main.nf --root_fs_input raw/  --nb_threads 1 --processes 1 \
	-resume -with-report report.html

cp -L results_fs/${N_SUBJ}_${N_SESS}/Generate_*/* ${OUT_DIR}/

# Generate PDF
for i in ${OUT_DIR}/*_v4.nii.gz;
	do 
		scil_crop_volume.py ${i} tmp_labels.nii.gz --output_bbox bbox.pkl -f
		scil_crop_volume.py ${IN_DIR}/${IN_T1} tmp_t1.nii.gz --input_bbox bbox.pkl -f
		python3.7 /CODE/get_mosaic.py tmp_labels.nii.gz tmp_t1.nii.gz ${i/nii.gz/png}
		convert ${i/nii.gz/png} -fuzz 7% -trim ${i/nii.gz/png}
		convert ${i/nii.gz/png} -fuzz 7% -trim ${i/nii.gz/png}
done

# Copy relevant outputs
cp report.html ${OUT_DIR}/

python3.7 /CODE/generate_connectivity_atlases_flow_spider_pdf.py ${OUT_DIR}/ ${N_SUBJ}_${N_SESS}
rm ${OUT_DIR}/*.png