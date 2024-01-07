#!/bin/bash

echo "Lets run a test scenario"

# set up venv
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"
pyenv activate dca_dev


# Step 1. Wipe database
psql -U rylanlorance -d dca_dev_working -c 'TRUNCATE dca.record;'


# 