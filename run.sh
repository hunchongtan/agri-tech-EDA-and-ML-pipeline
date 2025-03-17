#!/bin/bash

# Ensure script stops on first error
set -e

# Install required Python dependencies
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Ask user which task they want to run
echo "Which task would you like to run?"
echo "1. Task 2A (Predicting Temperature - regression)"
echo "2. Task 2B (Categorising Plant Type-Stage - classification)"
echo "3. Both"
read -p "Enter 1, 2, or 3: " task

# Map user input to task type
if [ "$task" == "1" ]; then
    task_type="regression"
elif [ "$task" == "2" ]; then
    task_type="classification"
elif [ "$task" == "3" ]; then
    task_type="both"
else
    echo "Invalid input. Exiting."
    exit 1
fi

# Update config.yaml with the selected task
echo "task: \"$task_type\"" > config.yaml
echo "Updated config.yaml with task: $task_type"

# Navigate to src directory and execute the pipeline
cd src
python main.py

# Execution done!
echo "Script executed properly! See you again!"
