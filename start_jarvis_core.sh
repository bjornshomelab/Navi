#!/bin/bash

# JARVIS Core - Terminal AI Agent Launcher
# Fokuserad på intelligens utan GUI/voice distractions

set -e

JARVIS_DIR="/home/bjorn/Skrivbord/Jarvis"
cd "$JARVIS_DIR"

# Färger för output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🤖 JARVIS Core - Terminal AI Agent${NC}"
echo -e "${YELLOW}🎯 Fokuserad på intelligens och automation${NC}\n"

# Aktivera virtual environment
echo -e "${BLUE}📦 Aktiverar virtual environment...${NC}"
source jarvis/bin/activate

# Kontrollera dependencies
echo -e "${BLUE}🔧 Kontrollerar core services...${NC}"

# Starta core terminal interface
echo -e "${GREEN}🚀 Startar JARVIS Core...${NC}\n"
python jarvis_core.py

echo -e "\n${GREEN}👋 JARVIS Core session avslutad${NC}"
