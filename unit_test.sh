#!/bin/bash

echo "Lets run a test scenario"

# set up venv
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
pyenv activate dca_dev

# echo "Step 1. Wiping Database and output files..."
# psql -U rylanlorance -d dca_dev_working -c 'TRUNCATE dca.record;'
# echo "Done."
# rm -rf /Users/rylanlorance/Documents/Dear_Ocean/Dear_Ocean_Digital_Coral_Ark_Bot_Working/output_files/*
# rm -rf /Users/rylanlorance/Documents/Dear_Ocean/Dear_Ocean_Digital_Coral_Ark_Bot_Working/input/input_files_cleaned_demo_01_08_23/*

INPUT_DIR="/Users/rylanlorance/Documents/Dear_Ocean/Dear_Ocean_Digital_Coral_Ark_Bot_Working/input/input_files_demo_01_08_23/"
OUTPUT_DIR="/Users/rylanlorance/Documents/Dear_Ocean/Dear_Ocean_Digital_Coral_Ark_Bot_Working/output_files"

echo "Step 2. Running File Validator on Filename"
python app.py validate $INPUT_DIR

echo "Validate failed, so we will need to rename files"
echo ""

echo "Step 3. Running File rename tool with safe mode on."
python app.py rename $INPUT_DIR $OUTPUT_DIR --safe-mode on

# echo "Step 4. Safe mode passed, rename the files."
# python app.py rename $INPUT_DIR $OUTPUT_DIR --safe-mode off

# echo "lets see if those files were created"
# ls -al $OUTPUT_DIR

# echo "moving files to new directory..."

# INPUT_DIR_CLEANED="/Users/rylanlorance/Documents/Dear_Ocean/Dear_Ocean_Digital_Coral_Ark_Bot_Working/input/input_files_cleaned_demo_01_08_23/"
# cp $OUTPUT_DIR/* $INPUT_DIR_CLEANED
# INPUT_DIR=$INPUT_DIR_CLEANED

# echo "Step 5. Run Upload Script with Safe Mode On"
# python app.py upload $INPUT_DIR --safe-mode on

# # echo "Passed!"
# python app.py upload $INPUT_DIR --safe-mode off