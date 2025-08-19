#!/usr/bin/env python3
"""
JARVIS Agent Dependencies Installer
Installerar alla bibliotek som agents behöver
"""

import subprocess
import sys
import os
from pathlib import Path

class AgentDependencyInstaller:
    """Installerar alla dependencies för JARVIS agents"""
    
    def __init__(self):
        self.packages = {
            # Data Science & ML
            'data_science': [
                'pandas', 'numpy', 'matplotlib', 'seaborn', 'scipy',
                'scikit-learn', 'jupyter', 'notebook', 'plotly',
                'statsmodels', 'openpyxl', 'xlrd'
            ],
            
            # Web & API Development
            'web_dev': [
                'fastapi', 'uvicorn', 'requests', 'beautifulsoup4',
                'selenium', 'flask', 'django', 'aiohttp'
            ],
            
            # Document Processing
            'documents': [
                'pypdf2', 'python-docx', 'pandoc', 'markdown',
                'jinja2', 'pyyaml', 'toml'
            ],
            
            # Image & Media
            'media': [
                'pillow', 'opencv-python', 'imageio', 'moviepy'
            ],
            
            # Google Cloud & AI
            'google_cloud': [
                'google-cloud-aiplatform', 'google-cloud-storage',
                'google-auth', 'google-auth-oauthlib', 'google-auth-httplib2'
            ],
            
            # Development Tools
            'dev_tools': [
                'black', 'flake8', 'pytest', 'mypy', 'isort',
                'pre-commit', 'tox'
            ],
            
            # System & Automation
            'system': [
                'psutil', 'schedule', 'python-crontab', 'watchdog',
                'paramiko', 'fabric'
            ],
            
            # Utilities
            'utilities': [
                'rich', 'click', 'tqdm', 'python-dotenv',
                'configparser', 'pathlib2'
            ]
        }
    
    def install_category(self, category: str) -> bool:
        """Installera en kategori av packages"""
        if category not in self.packages:
            print(f"❌ Okänd kategori: {category}")
            return False
        
        packages = self.packages[category]
        print(f"📦 Installerar {category} packages ({len(packages)} st)...")
        
        try:
            cmd = [sys.executable, '-m', 'pip', 'install'] + packages
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print(f"✅ {category} packages installerade!")
                return True
            else:
                print(f"❌ Fel vid installation av {category}: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Exception vid installation av {category}: {e}")
            return False
    
    def install_all(self) -> dict:
        """Installera alla categories"""
        print("🚀 Startar installation av alla agent dependencies...\n")
        
        results = {}
        for category in self.packages.keys():
            results[category] = self.install_category(category)
            print()  # Empty line between categories
        
        # Summary
        successful = sum(results.values())
        total = len(results)
        
        print(f"\n📊 Installation Summary:")
        print(f"✅ Framgångsrika: {successful}/{total}")
        print(f"❌ Misslyckade: {total - successful}/{total}")
        
        if successful == total:
            print("\n🎉 Alla agent dependencies installerade!")
        else:
            print(f"\n⚠️ {total - successful} kategorier misslyckades. Kolla loggar ovan.")
        
        return results
    
    def check_installation(self) -> dict:
        """Kontrollera vilka packages som är installerade"""
        print("🔍 Kontrollerar installerade packages...\n")
        
        status = {}
        for category, packages in self.packages.items():
            status[category] = {}
            print(f"📦 {category}:")
            
            for package in packages:
                try:
                    __import__(package.replace('-', '_'))
                    status[category][package] = True
                    print(f"  ✅ {package}")
                except ImportError:
                    status[category][package] = False
                    print(f"  ❌ {package}")
            print()
        
        return status
    
    def install_pandoc_system(self):
        """Installera pandoc via system package manager"""
        print("📄 Installerar pandoc via system package manager...")
        
        try:
            # För Ubuntu/Debian
            cmd = ['sudo', 'apt', 'install', '-y', 'pandoc']
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ Pandoc installerat via apt!")
                return True
            else:
                print(f"❌ Kunde inte installera pandoc: {result.stderr}")
                return False
                
        except Exception as e:
            print(f"❌ Exception vid pandoc installation: {e}")
            return False

def main():
    """Main function"""
    installer = AgentDependencyInstaller()
    
    print("🤖 JARVIS Agent Dependencies Installer")
    print("=====================================\n")
    
    # Visa meny
    while True:
        print("Välj en åtgärd:")
        print("1. Installera alla dependencies")
        print("2. Installera specifik kategori")
        print("3. Kontrollera installerade packages")
        print("4. Installera pandoc (system)")
        print("5. Avsluta")
        
        choice = input("\nDitt val (1-5): ").strip()
        
        if choice == '1':
            installer.install_all()
        
        elif choice == '2':
            print("\nTillgängliga kategorier:")
            for i, category in enumerate(installer.packages.keys(), 1):
                print(f"{i}. {category}")
            
            try:
                cat_choice = int(input("\nVälj kategori nummer: ")) - 1
                categories = list(installer.packages.keys())
                if 0 <= cat_choice < len(categories):
                    installer.install_category(categories[cat_choice])
                else:
                    print("❌ Ogiltigt val")
            except ValueError:
                print("❌ Ange ett nummer")
        
        elif choice == '3':
            installer.check_installation()
        
        elif choice == '4':
            installer.install_pandoc_system()
        
        elif choice == '5':
            print("👋 Avslutar installer")
            break
        
        else:
            print("❌ Ogiltigt val")
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    main()
