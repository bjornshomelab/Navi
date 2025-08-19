#!/usr/bin/env python3
"""
Test Enhanced Local Agent Service
"""
import asyncio
import sys
import os
from pathlib import Path

# Add paths
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "api"))

async def test_enhanced_local_agent():
    """Test the enhanced local agent"""
    try:
        print("🧪 Testing Enhanced Local Agent Service...")
        
        from api.services.enhanced_local_agent import EnhancedLocalAgentService
        agent = EnhancedLocalAgentService()
        
        print("✅ Service initialized successfully")
        
        # Test 1: List files in current directory
        print("\n📁 Test 1: List files")
        result = await agent.execute_enhanced_action("lista filer", path=".")
        if result["success"]:
            print(f"   ✅ Found {result.get('total_files', 0)} files and {result.get('total_directories', 0)} directories")
        else:
            print(f"   ❌ Failed: {result['message']}")
        
        # Test 2: Get system status
        print("\n💻 Test 2: System status")
        result = await agent.execute_enhanced_action("systemstatus")
        if result["success"]:
            sys_info = result.get("system_info", {})
            print(f"   ✅ CPU: {sys_info.get('cpu_usage', 'N/A')}, RAM: {sys_info.get('memory_usage', 'N/A')}")
        else:
            print(f"   ❌ Failed: {result['message']}")
        
        # Test 3: Application capabilities
        print("\n🎯 Test 3: Get capabilities")
        capabilities = agent.get_capabilities()
        print(f"   ✅ File ops: {len(capabilities['file_operations'])}")
        print(f"   ✅ App ops: {len(capabilities['application_operations'])}")
        print(f"   ✅ System ops: {len(capabilities['system_operations'])}")
        
        print("\n🎉 All tests completed successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = asyncio.run(test_enhanced_local_agent())
    sys.exit(0 if success else 1)
