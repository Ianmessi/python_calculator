#!/bin/bash

# This script sets up a GitHub repository for the Python Calculator app

echo "Setting up GitHub repository for Python Calculator..."

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "Git is not installed. Please install Git first."
    exit 1
fi

# Initialize git repository if it doesn't exist
if [ ! -d .git ]; then
    echo "Initializing Git repository..."
    git init
fi

# Add all files to git
echo "Adding files to Git..."
git add .

# Commit changes
echo "Committing changes..."
git commit -m "Initial commit of Python Calculator with Streamlit"

echo "Repository is ready for push."
echo ""
echo "To push to GitHub, follow these steps:"
echo "1. Create a new repository on GitHub at https://github.com/new"
echo "2. Name it 'python-calculator' (or whatever you prefer)"
echo "3. Do NOT initialize with README, .gitignore, or license"
echo "4. After creating, run these commands (replace YOUR_USERNAME with your GitHub username):"
echo ""
echo "   git remote add origin https://github.com/YOUR_USERNAME/python-calculator.git"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "5. Then visit Streamlit Cloud at https://share.streamlit.io to deploy" 