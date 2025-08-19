#!/bin/bash

# JARVIS GUI Launcher - Välj mellan klassisk och modern design
# Skapad: 19 augusti 2025

set -e

JARVIS_DIR="/home/bjorn/Skrivbord/Jarvis"
cd "$JARVIS_DIR"

# Färger för output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    🤖 JARVIS AI Assistant                    ║"
echo "║                     GUI Design Selector                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

echo -e "${CYAN}Välj vilken GUI-design du vill använda:${NC}\n"

echo -e "${YELLOW}1. 🎨 MODERN GUI${NC} (Ny design - Rekommenderas)"
echo -e "   • Discord/VS Code-inspirerat mörkt tema"
echo -e "   • Professionell design med moderna komponenter" 
echo -e "   • Förbättrad användarupplevelse och visuell feedback"
echo -e "   • Bar chart audio visualizer"
echo -e "   • Card-baserad layout med hover effects"
echo ""

echo -e "${GREEN}2. 🏠 KLASSISK GUI${NC} (Original design)"
echo -e "   • Standard tkinter-utseende"
echo -e "   • Enkel och funktionell"
echo -e "   • Waveform audio visualizer"
echo -e "   • Traditionell layout"
echo ""

echo -e "${PURPLE}3. 📊 VISA DESIGN RESEARCH${NC}"
echo -e "   • Detaljerad analys av GUI-förbättringar"
echo -e "   • Designtrender och rekommendationer"
echo -e "   • Före/efter-jämförelse"
echo ""

echo -e "${RED}4. ❌ AVSLUTA${NC}"
echo ""

# Kontrollera att servern körs
check_server() {
    if ! curl -s http://localhost:8081/api/status >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠️  JARVIS server verkar inte köra.${NC}"
        echo -e "${CYAN}Startar server automatiskt...${NC}"
        
        # Aktivera virtual environment och starta server i bakgrunden
        source jarvis/bin/activate
        python api/main.py &
        SERVER_PID=$!
        
        # Vänta på att servern startar
        echo -e "${CYAN}Väntar på att servern startar...${NC}"
        for i in {1..10}; do
            if curl -s http://localhost:8081/api/status >/dev/null 2>&1; then
                echo -e "${GREEN}✅ Server startad!${NC}"
                break
            fi
            echo -n "."
            sleep 1
        done
        
        if ! curl -s http://localhost:8081/api/status >/dev/null 2>&1; then
            echo -e "\n${RED}❌ Kunde inte starta servern automatiskt.${NC}"
            echo -e "${YELLOW}Kör manuellt: ./jarvis-server${NC}"
            exit 1
        fi
    else
        echo -e "${GREEN}✅ JARVIS server körs redan${NC}"
    fi
}

# Kör GUI baserat på val
run_gui() {
    local choice=$1
    
    case $choice in
        1)
            echo -e "\n${BLUE}🎨 Startar Modern GUI...${NC}"
            source jarvis/bin/activate
            python gui/modern_gui.py
            ;;
        2)
            echo -e "\n${GREEN}🏠 Startar Klassisk GUI...${NC}"
            source jarvis/bin/activate
            python gui/main_window.py
            ;;
        3)
            echo -e "\n${PURPLE}📊 Öppnar Design Research...${NC}"
            if command -v code >/dev/null 2>&1; then
                code docs/GUI_DESIGN_RESEARCH.md
            elif command -v gedit >/dev/null 2>&1; then
                gedit docs/GUI_DESIGN_RESEARCH.md
            elif command -v nano >/dev/null 2>&1; then
                nano docs/GUI_DESIGN_RESEARCH.md
            else
                cat docs/GUI_DESIGN_RESEARCH.md | less
            fi
            ;;
        4)
            echo -e "\n${RED}❌ Avslutar...${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Ogiltigt val. Försök igen.${NC}"
            return 1
            ;;
    esac
}

# Huvudloop
while true; do
    echo -e "${CYAN}Ange ditt val (1-4): ${NC}"
    read -r choice
    
    if [ "$choice" = "3" ]; then
        run_gui "$choice"
        echo -e "\n${CYAN}Tryck Enter för att fortsätta...${NC}"
        read -r
        continue
    elif [ "$choice" = "4" ]; then
        run_gui "$choice"
        break
    elif [ "$choice" = "1" ] || [ "$choice" = "2" ]; then
        check_server
        run_gui "$choice"
        break
    else
        echo -e "${RED}❌ Ogiltigt val '$choice'. Ange 1, 2, 3 eller 4.${NC}\n"
    fi
done

echo -e "\n${GREEN}👋 Tack för att du använder JARVIS!${NC}"
