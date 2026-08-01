#!/usr/bin/env bash
# Create the Python virtual environment and install requirements.
# Optional arg: the venv directory name (defaults to "a").
# Updated 08/01/26: honor $1 instead of hardcoding the name.
PYTHON_ENV="${1:-a}"
python3 -m venv ./$PYTHON_ENV \
    && export PATH=./$PYTHON_ENV/bin:$PATH \
    && grep -qxF "source $(pwd)/$PYTHON_ENV/bin/activate" ~/.bashrc \
    || echo "source $(pwd)/$PYTHON_ENV/bin/activate" >> ~/.bashrc
source ./$PYTHON_ENV/bin/activate
if [ -f "./requirements.txt" ]; then
    pip3 install -r "./requirements.txt"
elif [ -f "./requirements/requirements.txt" ]; then
    pip3 install -r "./requirements/requirements.txt"
fi
