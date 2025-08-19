"""
JARVIS AI Agent - Local Agent Service  
Handles local system actions like installing software, opening apps, file operations
"""
import subprocess
import os
import psutil
import platform
from typing import Dict, Any, List
import shlex
import asyncio

class LocalAgentService:
    """Service for executing local system actions"""
    
    def __init__(self):
        self.system_info = self._get_system_info()
        
    def _get_system_info(self) -> Dict[str, Any]:
        """Get system information"""
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.architecture()[0],
            "processor": platform.processor(),
            "memory_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "cpu_cores": psutil.cpu_count(),
            "python_version": platform.python_version()
        }
    
    async def execute_action(self, action: str) -> str:
        """Execute a system action based on the action string"""
        try:
            # Parse action string (format: "action_type: description")
            if ":" in action:
                action_type, description = action.split(":", 1)
                action_type = action_type.strip()
                description = description.strip()
            else:
                action_type = "unknown"
                description = action
            
            # Always use smart parser for better handling
            return await self._smart_action_parser(description)
                
        except Exception as e:
            return f"Action failed: {str(e)}"
    
    async def _execute_system_command(self, command: str) -> str:
        """Execute a raw system command (be careful!)"""
        try:
            # Basic safety check - prevent dangerous commands
            dangerous_commands = ["rm -rf", "sudo rm", "mkfs", "dd if=", ">(", "curl.*|.*sh"]
            if any(danger in command.lower() for danger in dangerous_commands):
                return "Command blocked for safety reasons"
            
            # Execute command
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                output = stdout.decode().strip()
                return f"Command executed successfully: {output[:200]}..."
            else:
                error = stderr.decode().strip()
                return f"Command failed: {error[:200]}..."
                
        except Exception as e:
            return f"System command error: {str(e)}"
    
    async def _install_package(self, package_name: str) -> str:
        """Install a package using appropriate package manager"""
        try:
            # Ubuntu/Debian
            if os.path.exists("/usr/bin/apt"):
                cmd = f"sudo apt update && sudo apt install -y {shlex.quote(package_name)}"
            # Arch Linux  
            elif os.path.exists("/usr/bin/pacman"):
                cmd = f"sudo pacman -S --noconfirm {shlex.quote(package_name)}"
            # Fedora
            elif os.path.exists("/usr/bin/dnf"):
                cmd = f"sudo dnf install -y {shlex.quote(package_name)}"
            else:
                return "Package manager not supported"
            
            process = await asyncio.create_subprocess_shell(
                cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode == 0:
                return f"Package '{package_name}' installed successfully"
            else:
                error = stderr.decode().strip()
                return f"Package installation failed: {error[:200]}..."
                
        except Exception as e:
            return f"Package installation error: {str(e)}"
    
    async def _open_application(self, app_name: str) -> str:
        """Open an application by name"""
        try:
            # Common application mappings
            app_mappings = {
                "firefox": "/snap/bin/firefox",
                "chrome": "google-chrome",
                "chrom": "google-chrome",  # Short form of chrome
                "chromium": "/snap/bin/chromium", 
                "code": "code",
                "vscode": "code",
                "terminal": "gnome-terminal",
                "files": "nautilus",
                "calculator": "gnome-calculator",
                "discord": "discord",
                "spotify": "spotify",
                "browser": "/snap/bin/chromium"  # Default browser
            }
            
            app_command = app_mappings.get(app_name.lower(), app_name)
            
            # Try the mapped command first
            try:
                process = await asyncio.create_subprocess_shell(
                    f"{app_command} &",
                    stdout=asyncio.subprocess.DEVNULL,
                    stderr=asyncio.subprocess.DEVNULL
                )
                await asyncio.sleep(1)
                return f"Application '{app_name}' opened successfully"
            except:
                # Fallback: try alternative browser commands for chrome-like requests
                if any(browser_term in app_name.lower() for browser_term in ["chrome", "chrom", "chromium", "browser"]):
                    browsers = ["/snap/bin/chromium", "google-chrome", "chromium-browser", "/snap/bin/firefox"]
                    for browser in browsers:
                        try:
                            process = await asyncio.create_subprocess_shell(
                                f"{browser} &",
                                stdout=asyncio.subprocess.DEVNULL,
                                stderr=asyncio.subprocess.DEVNULL
                            )
                            await asyncio.sleep(1)
                            return f"Opened browser ({browser}) successfully"
                        except:
                            continue
                    return "No browser found to open"
                else:
                    return f"Failed to open application '{app_name}'"
            
        except Exception as e:
            return f"Failed to open application '{app_name}': {str(e)}"
    
    async def _smart_action_parser(self, description: str) -> str:
        """Parse natural language description and execute appropriate action"""
        desc_lower = description.lower()
        
        # Install software
        if "install" in desc_lower:
            # Extract package name (simple approach)
            words = description.split()
            if "install" in words:
                install_idx = next(i for i, word in enumerate(words) if word.lower() == "install")
                if install_idx + 1 < len(words):
                    package = words[install_idx + 1]
                    return await self._install_package(package)
            # Fallback - try to extract package name differently
            import re
            package_match = re.search(r'install\s+(\w+)', desc_lower)
            if package_match:
                return await self._install_package(package_match.group(1))
        
        # Open application
        elif any(word in desc_lower for word in ["open", "start", "launch"]):
            words = description.split()
            for word in ["open", "start", "launch"]:
                if word in [w.lower() for w in words]:
                    word_idx = next(i for i, w in enumerate(words) if w.lower() == word)
                    if word_idx + 1 < len(words):
                        app = words[word_idx + 1]
                        return await self._open_application(app)
            
            # If no app specified after open/start/launch, check if browser-related terms exist anywhere
            if any(browser_term in desc_lower for browser_term in ["chrome", "chrom", "chromium", "browser"]):
                # Extract the browser term
                for browser_term in ["chrome", "chrom", "chromium", "browser"]:
                    if browser_term in desc_lower:
                        return await self._open_application(browser_term)
                        break
        
        # System information
        elif any(word in desc_lower for word in ["status", "info", "system"]):
            status = self.get_system_status()
            return f"System Status: CPU {status['cpu_percent']}%, RAM {status['memory_percent']}%, Disk {status['disk_usage']}%"
        
        # Default: try as system command with better safety
        else:
            return f"Command not recognized. Available actions: install <package>, open <app>, system status"
    
    async def execute_file_operation(self, action: str) -> str:
        """Execute file operations like read, write, copy, move"""
        try:
            # Implementation for file operations
            # This is a placeholder - add specific file operation logic
            return f"File operation executed: {action}"
            
        except Exception as e:
            return f"File operation failed: {str(e)}"
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        return {
            "cpu_percent": psutil.cpu_percent(interval=1),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "running_processes": len(psutil.pids()),
            "system_info": self.system_info
        }
