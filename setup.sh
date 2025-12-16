#!/bin/bash

# ============================================
# MetaTrader 5 API Project Setup Script
# ============================================

echo "=================================="
echo "MetaTrader 5 API - Setup"
echo "=================================="

# Kontrollera om Python finns
if ! command -v python &> /dev/null; then
    echo "ERROR: Python ar inte installerat."
    exit 1
fi

echo "Python version: $(python --version)"

# Skapa virtual environment om det inte finns
if [ ! -d "venv" ]; then
    echo ""
    echo "Skapar virtual environment..."
    python -m venv venv
    echo "Virtual environment skapad."
else
    echo "Virtual environment finns redan."
fi

# Aktivera virtual environment
echo ""
echo "Aktiverar virtual environment..."
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Installera beroenden
echo ""
echo "Installerar beroenden fran requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# Skapa Download-mappen om den inte finns
if [ ! -d "Download" ]; then
    mkdir Download
    echo "Download-mappen skapad."
fi

echo ""
echo "=================================="
echo "Setup klar!"
echo "=================================="
echo ""
echo "For att aktivera miljoen manuellt:"
echo "  Windows: .\\venv\\Scripts\\activate"
echo "  Linux/Mac: source venv/bin/activate"
echo ""
echo "For att testa anslutningen till MT5:"
echo "  python main.py"
echo ""
