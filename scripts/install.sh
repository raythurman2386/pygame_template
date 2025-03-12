#!/bin/bash

GREEN='\033[0;32m'
NC='\033[0m' # No Color

echo -e "${GREEN}Creating virtual environment...${NC}"
python3 -m venv venv
echo -e "${GREEN}Activating virtual environment...${NC}"
source venv/bin/activate

echo -e "${GREEN}Installing package and dependencies...${NC}"
pip install -e .

echo -e "${GREEN}Building executable with PyInstaller...${NC}"
pyinstaller pygame_template.spec

echo -e "${GREEN}Build complete! Executable is in the dist folder.${NC}"