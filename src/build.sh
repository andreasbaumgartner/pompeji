#!/bin/bash

# ask user for a project name as string
echo "Enter project name: "
read project_name

# run python script
python3 main.py $project_name

# change directory to project name
cd $project_name

# activate virtual environment
if [ -d "venv" ]; then
	source venv/bin/activate
fi
