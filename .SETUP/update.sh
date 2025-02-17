#!/bin/bash

# Update package lists
echo "Updating package lists..."
sudo apt update -y

# Upgrade all packages
echo "Upgrading packages..."
sudo apt full-upgrade -y

# Remove unnecessary packages and clean up
echo "Removing unnecessary packages..."
sudo apt autoremove -y
sudo apt clean

# Upgrade the Kali tools (specifically)
echo "Upgrading Kali tools..."
sudo apt dist-upgrade -y

# Optional: Install missing dependencies for all installed packages
echo "Installing missing dependencies..."
sudo apt --fix-broken install -y