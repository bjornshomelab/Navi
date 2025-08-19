#!/bin/bash

# JARVIS Full Start Script - Startar server + GUI automatiskt
# Skapad: 19 augusti 2025

set -e

JARVIS_DIR="/home/bjorn/Skrivbord/Jarvis"
cd "$JARVIS_DIR"

# Färger för output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🤖 JARVIS AI Assistant - Full Start${NC}"
echo -e "${YELLOW}Startar server och GUI automatiskt...${NC}\n"

# Aktivera virtual environment
echo -e "${BLUE}📦 Aktiverar virtual environment...${NC}"
source jarvis/bin/activate

# Kontrollera om servern redan körs
if curl -s http://localhost:8081/api/status >/dev/null 2>&1; then
    echo -e "${GREEN}✅ JARVIS server körs redan${NC}"
else
    echo -e "${BLUE}🚀 Startar JARVIS server...${NC}"
    # Start server using simple launcher (suppress output)
    python simple_server.py >/dev/null 2>&1 &
    SERVER_PID=$!
    
    # Vänta på att servern startar
    echo -e "${YELLOW}⏳ Väntar på att servern startar...${NC}"
    for i in {1..20}; do
        if curl -s http://localhost:8081/api/status >/dev/null 2>&1; then
            echo -e "${GREEN}✅ Server startad framgångsrikt!${NC}"
            break
        fi
        echo -n "."
        sleep 1
    done
    
    if ! curl -s http://localhost:8081/api/status >/dev/null 2>&1; then
        echo -e "\n${RED}❌ Kunde inte starta servern automatiskt${NC}"
        echo -e "${YELLOW}🔧 Försöker manuell start...${NC}"
        
        # Kill the background process
        kill $SERVER_PID 2>/dev/null
        
        # Try manual start for debugging
        cd /home/bjorn/Skrivbord/Jarvis
        source jarvis/bin/activate
        
        echo -e "${CYAN}Startar server manuellt för debugging...${NC}"
        timeout 5 python simple_server.py 2>&1 | head -10
        
        exit 1
    fi
fi

# Ge användaren möjlighet att välja GUI
echo -e "\n${BLUE}🎨 Vilken GUI vill du använda?${NC}"
echo -e "${YELLOW}1.${NC} Modern GUI (Rekommenderas)"
echo -e "${YELLOW}2.${NC} Klassisk GUI" 
echo -e "${YELLOW}3.${NC} Visa design-väljare"
echo -e "${YELLOW}Enter${NC} = Modern GUI (standard)"

read -t 5 -p "Välj (1-3, eller Enter för standard): " choice

case $choice in
    2)
        echo -e "\n${BLUE}🏠 Startar Klassisk GUI...${NC}"
        python gui/main_window.py
        ;;
    3)
        echo -e "\n${BLUE}🎯 Startar Design-väljare...${NC}"
        ./launch_gui.sh
        ;;
    *)
        echo -e "\n${BLUE}🎨 Startar Modern GUI...${NC}"
        python gui/modern_gui.py
        ;;
esac

echo -e "\n${GREEN}👋 JARVIS session avslutad${NC}"
