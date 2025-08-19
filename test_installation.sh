#!/bin/bash

# JARVIS Quick Test Script
# Verify that JARVIS is working correctly after installation

echo "🤖 JARVIS Quick Test Suite"
echo "========================="

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Test results
TESTS_PASSED=0
TESTS_FAILED=0

test_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ PASS${NC}: $2"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}❌ FAIL${NC}: $2"
        ((TESTS_FAILED++))
    fi
}

echo "🔍 Testing JARVIS installation..."

# Test 1: Python virtual environment
echo "📍 Test 1: Virtual environment"
if [ -d "jarvis" ] && [ -f "jarvis/bin/python" ]; then
    test_result 0 "Virtual environment exists"
else
    test_result 1 "Virtual environment missing"
fi

# Test 2: Core imports
echo "📍 Test 2: Core Python imports"
source jarvis/bin/activate 2>/dev/null
python3 -c "
try:
    from api.services.enhanced_voice import EnhancedVoiceService
    from api.main import app
    print('Core imports successful')
    exit(0)
except ImportError as e:
    print(f'Import error: {e}')
    exit(1)
" 2>/dev/null
test_result $? "Core Python modules"

# Test 3: Voice dependencies
echo "📍 Test 3: Voice system dependencies"
python3 -c "
try:
    import edge_tts
    import pygame
    print('Voice dependencies OK')
    exit(0)
except ImportError:
    exit(1)
" 2>/dev/null
test_result $? "Voice dependencies (edge-tts, pygame)"

# Test 4: System TTS
echo "📍 Test 4: System TTS availability"
if command -v spd-say >/dev/null 2>&1; then
    test_result 0 "Speech dispatcher available"
elif command -v espeak >/dev/null 2>&1; then
    test_result 0 "eSpeak available"
else
    test_result 1 "No system TTS found"
fi

# Test 5: Edge TTS Swedish voices
echo "📍 Test 5: Swedish voice availability"
if jarvis/bin/edge-tts --list-voices 2>/dev/null | grep -q "sv-SE"; then
    test_result 0 "Swedish voices available in Edge TTS"
else
    test_result 1 "Swedish voices not found"
fi

# Test 6: Audio system
echo "📍 Test 6: Audio system"
if [ -d "/proc/asound" ] || command -v pulseaudio >/dev/null 2>&1; then
    test_result 0 "Audio system detected"
else
    test_result 1 "No audio system detected"
fi

# Test 7: API server startup (quick test)
echo "📍 Test 7: API server startup test"
timeout 5 python3 -c "
import uvicorn
from api.main import app
print('API server can start')
" 2>/dev/null
test_result $? "API server startup capability"

# Test 8: Voice service initialization
echo "📍 Test 8: Voice service initialization"
python3 -c "
from api.services.enhanced_voice import EnhancedVoiceService
voice = EnhancedVoiceService()
status = voice.get_status()
if status['engines']:
    print(f'Voice service OK with {len(status[\"engines\"])} engines')
    exit(0)
else:
    exit(1)
" 2>/dev/null
test_result $? "Voice service initialization"

deactivate 2>/dev/null

# Summary
echo ""
echo "📊 Test Summary:"
echo "================"
echo -e "Tests passed: ${GREEN}$TESTS_PASSED${NC}"
echo -e "Tests failed: ${RED}$TESTS_FAILED${NC}"

if [ $TESTS_FAILED -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 All tests passed! JARVIS is ready to use.${NC}"
    echo ""
    echo "Quick start commands:"
    echo "  jarvis-start  # Start JARVIS server"
    echo "  jarvis-gui    # Start GUI"
    echo "  jarvis-voice  # Test voice"
    echo ""
    echo "Try saying: 'Hej JARVIS, vad är klockan?'"
    exit 0
else
    echo ""
    echo -e "${YELLOW}⚠️  Some tests failed. JARVIS may have limited functionality.${NC}"
    echo ""
    echo "Troubleshooting:"
    echo "1. Run: ./install.sh"
    echo "2. Check: INSTALL.md"
    echo "3. Report issues: https://github.com/bjornshomelab/jarvis/issues"
    exit 1
fi
