#!/bin/bash

BASE_DIR="./"
NEW_DIR="${BASE_DIR}/new_folder"

# List of directories to process
DIRS=(
  "alldataset_noPretrain_noHyper_noDenoise"
  "alldataset_noPretrain_noHyper_noDenoise_delInput"
  "del_input_noise"
  "denoise_hyper_floor"
  "denoise_hyper_floor_delInput"
  "denoise_hyper_nofloor"
  "denoise_pretrain_hyper_floor"
  "denoise_pretrain_hyper_nofloor"
  "denoise_pretrain_hyper_nofloor_test"
  "save_ae_ply_data"
  "save_ae_ply_hyper_pre_data"
  "save_ele_data"
  "save_ele_hyper_data"
)

# Create the new base directory
mkdir -p "$NEW_DIR"

# Iterate over the directories
for dir in "${DIRS[@]}"; do
  # Create corresponding directory in new_folder
  mkdir -p "${NEW_DIR}/${dir}"

  # Handle special cases
  if [[ "$dir" == "alldataset_noPretrain_noHyper_noDenoise_delInput" || "$dir" == "denoise_hyper_floor_delInput" ]]; then
    # Copy only the special case files for these directories
    cp "${BASE_DIR}/${dir}/ground_114_gt.ply" "${NEW_DIR}/${dir}/" 2>/dev/null
    cp "${BASE_DIR}/${dir}/ground_114_pc_recon_denoised.ply" "${NEW_DIR}/${dir}/" 2>/dev/null
  else
    # Copy the standard .ply files for all other directories
    cp "${BASE_DIR}/${dir}/ground_114_gt.ply" "${NEW_DIR}/${dir}/" 2>/dev/null
    cp "${BASE_DIR}/${dir}/ground_114_pc.ply" "${NEW_DIR}/${dir}/" 2>/dev/null
    cp "${BASE_DIR}/${dir}/ground_114_pc_recon.ply" "${NEW_DIR}/${dir}/" 2>/dev/null
  fi
done

echo "Copying specified .ply files completed."

