#!/usr/bin/env bash

# run shell script from project root directory, not from bin/
# Exit on any error
set -e

# Define venv directory
VENV_DIR=".venv"

echo "🔧 Setting up Python virtual environment..."

# Create the virtual environment if it doesn't exist
if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
    echo "✅ Virtual environment created at $VENV_DIR"
else
    echo "ℹ️ Virtual environment already exists at $VENV_DIR"
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo "⬆️ Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "📦 Installing dependencies from requirements.txt..."
pip install -r requirements.txt

echo "✅ Setup complete. Virtual environment is ready."
echo "💡 To activate it, run: source $VENV_DIR/bin/activate"
