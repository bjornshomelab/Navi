#!/bin/bash

# NAVI Uninstaller
# Removes NAVI global installation and cleans up files

echo "🗑️  NAVI Uninstaller"
echo "==================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

# Ask for confirmation
echo "This will remove:"
echo "  • Global NAVI commands (navi, navi-cli, navi-status)"
echo "  • Shell aliases from ~/.bashrc"
echo "  • NAVI virtual environment (optional)"
echo ""
echo -n "Are you sure you want to uninstall NAVI? [y/N]: "
read -r confirm

if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Uninstall cancelled."
    exit 0
fi

echo ""
print_info "Removing NAVI..."

# Remove global commands
INSTALL_DIR="$HOME/.local/bin"
for cmd in navi navi-cli navi-status; do
    if [ -f "$INSTALL_DIR/$cmd" ]; then
        rm "$INSTALL_DIR/$cmd"
        print_status "Removed global command: $cmd"
    fi
done

# Remove aliases from shell configs
for rcfile in "$HOME/.bashrc" "$HOME/.zshrc"; do
    if [ -f "$rcfile" ]; then
        # Remove NAVI aliases
        sed -i '/alias navi=/d' "$rcfile" 2>/dev/null || true
        sed -i '/alias navi-cli=/d' "$rcfile" 2>/dev/null || true
        sed -i '/alias navi-status=/d' "$rcfile" 2>/dev/null || true
        sed -i '/alias navi-help=/d' "$rcfile" 2>/dev/null || true
        print_status "Cleaned up aliases in $rcfile"
    fi
done

# Ask about removing virtual environment
if [ -d "navi_env" ]; then
    echo ""
    echo -n "Remove NAVI virtual environment? [y/N]: "
    read -r remove_venv
    
    if [[ "$remove_venv" =~ ^[Yy]$ ]]; then
        rm -rf navi_env
        print_status "Removed virtual environment"
    else
        print_info "Kept virtual environment"
    fi
fi

# Ask about removing data
if [ -d "data" ]; then
    echo ""
    echo -n "Remove NAVI data (memory, logs)? [y/N]: "
    read -r remove_data
    
    if [[ "$remove_data" =~ ^[Yy]$ ]]; then
        rm -rf data logs
        print_status "Removed data directories"
    else
        print_info "Kept data directories"
    fi
fi

echo ""
print_status "🎉 NAVI uninstalled successfully!"
echo ""
print_info "To reinstall NAVI, run: ./setup.sh"
print_warning "You may need to restart your terminal for changes to take effect."
