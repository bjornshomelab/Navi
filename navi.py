#!/usr/bin/env python3
# NAVI - Your Local-First AI Assistant
# Main entry point for the NAVI AI assistant

import asyncio
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

try:
    from navi.core import NaviCLI, NaviCore
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Make sure you're in the correct directory and dependencies are installed.")
    print("📦 Install dependencies with: pip install -r requirements.txt")
    sys.exit(1)

def print_banner():
    """Print NAVI banner"""
    banner = """
🤖 NAVI - Your Local-First AI Assistant
=======================================
Privacy-focused • Multi-provider • Agent-based
Powered by local models with cloud fallback
    """
    print(banner)

def print_help():
    """Print help information"""
    help_text = """
Usage: python navi.py [options] [message]

Options:
  -h, --help          Show this help message
  -i, --interactive   Start interactive mode (default)
  -s, --status        Show system status
  -a, --agent <name>  Use specific agent
  --list-agents       List available agents
  --list-providers    List available providers
  --setup             Run initial setup

Examples:
  python navi.py                           # Interactive mode
  python navi.py "Hello, how are you?"     # Single message
  python navi.py -a coder "Write a Python function"
  python navi.py --status                  # Show status
  
Agents:
  chat         - General conversation
  coder        - Programming assistance  
  researcher   - Research and analysis
  creative     - Creative writing
  image        - Image generation/analysis

For more help, type 'help' in interactive mode.
    """
    print(help_text)

async def show_status():
    """Show system status"""
    try:
        navi = NaviCore()
        await navi.initialize()
        
        print("📊 NAVI System Status")
        print("=" * 50)
        
        # Provider status
        provider_status = navi.get_provider_status()
        print("\n📡 AI Providers:")
        
        available_count = 0
        for name, status in provider_status.items():
            status_icon = "✅" if status["available"] else "❌"
            print(f"  {status_icon} {name}")
            
            if status["available"]:
                available_count += 1
                models = status.get("models", [])
                if models:
                    model_list = ", ".join(models[:3])
                    if len(models) > 3:
                        model_list += f" (and {len(models) - 3} more)"
                    print(f"      Models: {model_list}")
        
        if available_count == 0:
            print("\n⚠️  No providers available!")
            print("💡 To get started:")
            print("   • Install Ollama: https://ollama.ai")
            print("   • Or set OPENAI_API_KEY environment variable")
        
        # Agent status
        agents = navi.get_agent_list()
        print(f"\n🤖 Available Agents: {len(agents)}")
        for agent in agents:
            print(f"  • {agent}")
        
        # Memory status
        print(f"\n🧠 Memory System: ✅ Active")
        print(f"   Data directory: data/memory/")
        
    except Exception as e:
        print(f"❌ Error checking status: {e}")

async def list_agents():
    """List available agents with descriptions"""
    try:
        navi = NaviCore()
        await navi.initialize()
        
        print("🤖 Available NAVI Agents")
        print("=" * 50)
        
        agent_info = navi.agent_manager.get_all_agents_info()
        
        for name, info in agent_info.items():
            print(f"\n📝 {name}")
            print(f"   Type: {info['type']}")
            print(f"   Description: {info['description']}")
            if info['capabilities']:
                print(f"   Capabilities: {', '.join(info['capabilities'])}")
            if info['routing_keywords']:
                keywords = ', '.join(info['routing_keywords'][:5])
                if len(info['routing_keywords']) > 5:
                    keywords += "..."
                print(f"   Keywords: {keywords}")
        
    except Exception as e:
        print(f"❌ Error listing agents: {e}")

async def list_providers():
    """List available providers"""
    try:
        navi = NaviCore()
        await navi.initialize()
        
        print("📡 AI Provider Status")
        print("=" * 50)
        
        provider_status = navi.get_provider_status()
        
        for name, status in provider_status.items():
            status_icon = "✅" if status["available"] else "❌"
            print(f"\n{status_icon} {name}")
            
            if status["available"]:
                models = status.get("models", [])
                print(f"   Status: Available")
                print(f"   Models: {len(models)} available")
                for model in models[:5]:  # Show first 5 models
                    print(f"     • {model}")
                if len(models) > 5:
                    print(f"     ... and {len(models) - 5} more")
            else:
                print(f"   Status: Not available")
                if "openai" in name.lower():
                    print(f"   Setup: Set OPENAI_API_KEY environment variable")
                elif "ollama" in name.lower():
                    print(f"   Setup: Install Ollama (https://ollama.ai)")
        
    except Exception as e:
        print(f"❌ Error listing providers: {e}")

def run_setup():
    """Run initial setup wizard"""
    print("🛠️  NAVI Setup Wizard")
    print("=" * 50)
    
    print("\n1. Checking directories...")
    
    # Create necessary directories
    dirs = ["config", "data", "data/memory", "logs"]
    for dir_name in dirs:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"   ✅ Created: {dir_name}/")
        else:
            print(f"   ✅ Exists: {dir_name}/")
    
    print("\n2. AI Provider Options:")
    print("   🏠 Local (Recommended for privacy)")
    print("      • Install Ollama: https://ollama.ai")
    print("      • Run: ollama pull llama3.2")
    print("      • Run: ollama pull codellama")
    print()
    print("   ☁️  Cloud (Requires API key)")
    print("      • OpenAI: export OPENAI_API_KEY='your-key-here'")
    print("      • Google: export GOOGLE_API_KEY='your-key-here'")
    
    print("\n3. Test your setup:")
    print("   python navi.py --status")
    print("   python navi.py \"Hello, test message\"")
    
    print("\n✅ Setup complete! Run 'python navi.py' to start.")

async def single_message(message: str, agent: str = None):
    """Process a single message"""
    try:
        navi = NaviCore()
        await navi.initialize()
        
        response = await navi.chat(message, agent=agent)
        print(response.content)
        
    except Exception as e:
        print(f"❌ Error: {e}")

async def main():
    """Main entry point"""
    args = sys.argv[1:]
    
    # Parse arguments
    if not args or (len(args) == 1 and args[0] in ["-i", "--interactive"]):
        # Interactive mode
        print_banner()
        cli = NaviCLI()
        await cli.run_interactive()
    
    elif args[0] in ["-h", "--help"]:
        print_help()
    
    elif args[0] in ["-s", "--status"]:
        await show_status()
    
    elif args[0] == "--list-agents":
        await list_agents()
    
    elif args[0] == "--list-providers":
        await list_providers()
    
    elif args[0] == "--setup":
        run_setup()
    
    elif args[0] in ["-a", "--agent"]:
        if len(args) < 3:
            print("❌ Usage: python navi.py --agent <agent_name> <message>")
            sys.exit(1)
        
        agent_name = args[1]
        message = " ".join(args[2:])
        await single_message(message, agent=agent_name)
    
    else:
        # Single message mode
        message = " ".join(args)
        await single_message(message)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
