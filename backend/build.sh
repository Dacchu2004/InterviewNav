#!/bin/bash
# Exit on error
set -o errexit

# Install dependencies just in case (Render does this, but good practice)
pip install -r requirements.txt

# Run migrations
flask db upgrade
