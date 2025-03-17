#!/bin/bash

# Ensure script stops on first error
set -e

# Install required Python dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Set task to "both" in config.yaml
echo 'task: "both"' > config.yaml

# Navigate to src directory and execute the pipeline
cd src
python main.py

# Execution done!
echo "Script executed properly! See you again!"