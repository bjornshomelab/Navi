"""
JARVIS AI Agent - Enhanced Local Agent Service
Advanced local computer integration with file management, desktop control, and automation
"""
import subprocess
import os
import psutil
import platform
import shutil
import glob
import mimetypes
import hashlib
from typing import Dict, Any, List, Optional, Tuple
import shlex
import asyncio
import json
from datetime import datetime, timedelta
from pathlib import Path
import re

class EnhancedLocalAgentService:
    """Enhanced service for comprehensive local system control"""
    
    def __init__(self):
        self.system_info = self._get_system_info()
        self.safe_operations = True  # Safety mode enabled by default
        
        # Define security levels
        self.SAFE_ACTIONS = {
            "read_file", "list_directory", "get_status", "search_files", 
            "get_file_info", "open_application", "take_screenshot"
        }
        
        self.RESTRICTED_ACTIONS = {
            "write_file", "delete_file", "move_file", "copy_file", 
            "install_package", "system_command", "create_directory"
        }
        
        self.DANGEROUS_ACTIONS = {
            "format_disk", "modify_system_files", "delete_system_directory",
            "change_permissions_system"
        }
        
        print("🚀 Enhanced Local Agent Service initialized")
        print(f"💻 System: {self.system_info['os']} {self.system_info['os_version']}")
        print(f"🧠 Memory: {self.system_info['memory_gb']} GB")
    
    def _get_system_info(self) -> Dict[str, Any]:
        """Get comprehensive system information"""
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "architecture": platform.architecture()[0],
            "processor": platform.processor(),
            "memory_gb": round(psutil.virtual_memory().total / (1024**3), 2),
            "cpu_cores": psutil.cpu_count(),
            "python_version": platform.python_version(),
            "hostname": platform.node(),
            "user": os.getenv('USER', 'unknown')
        }
    
    async def execute_enhanced_action(self, action: str, **kwargs) -> Dict[str, Any]:
        """Execute enhanced local actions with detailed response"""
        try:
            action_lower = action.lower().strip()
            
            # File operations
            if any(keyword in action_lower for keyword in ["fil", "file", "mapp", "folder", "directory"]):
                return await self._handle_file_operations(action, **kwargs)
            
            # Application management
            elif any(keyword in action_lower for keyword in ["öppna", "open", "starta", "start", "kör", "run"]):
                return await self._handle_application_operations(action, **kwargs)
            
            # System operations
            elif any(keyword in action_lower for keyword in ["system", "status", "info", "dator", "computer"]):
                return await self._handle_system_operations(action, **kwargs)
            
            # Search operations
            elif any(keyword in action_lower for keyword in ["sök", "search", "hitta", "find"]):
                return await self._handle_search_operations(action, **kwargs)
            
            # Automation sequences
            elif any(keyword in action_lower for keyword in ["automation", "sekvens", "workflow"]):
                return await self._handle_automation_sequences(action, **kwargs)
            
            else:
                return {
                    "success": False,
                    "message": "Kommando inte igenkänt. Försök med fil-, app- eller systemoperationer.",
                    "suggestions": ["list files", "open firefox", "system status", "search for *.py"]
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Fel vid kommandokörning: {str(e)}",
                "error": str(e)
            }
    
    async def _handle_file_operations(self, action: str, **kwargs) -> Dict[str, Any]:
        """Handle comprehensive file operations"""
        action_lower = action.lower()
        
        try:
            # List files/directories
            if any(keyword in action_lower for keyword in ["lista", "list", "visa", "show"]):
                path = kwargs.get('path', '.')
                return await self._list_directory_enhanced(path)
            
            # Read file
            elif any(keyword in action_lower for keyword in ["läs", "read", "visa innehåll", "show content"]):
                file_path = kwargs.get('file_path') or self._extract_file_path(action)
                if file_path:
                    return await self._read_file_enhanced(file_path)
            
            # Write file
            elif any(keyword in action_lower for keyword in ["skriv", "write", "skapa", "create"]):
                file_path = kwargs.get('file_path') or self._extract_file_path(action)
                content = kwargs.get('content', '')
                if file_path:
                    return await self._write_file_enhanced(file_path, content)
            
            # Copy file/directory
            elif any(keyword in action_lower for keyword in ["kopiera", "copy"]):
                return await self._copy_file_enhanced(action, **kwargs)
            
            # Move file/directory
            elif any(keyword in action_lower for keyword in ["flytta", "move"]):
                return await self._move_file_enhanced(action, **kwargs)
            
            # Delete file/directory
            elif any(keyword in action_lower for keyword in ["ta bort", "delete", "radera", "remove"]):
                return await self._delete_file_enhanced(action, **kwargs)
            
            # Organize files
            elif any(keyword in action_lower for keyword in ["organisera", "organize", "sortera", "sort"]):
                path = kwargs.get('path', os.path.expanduser('~/Desktop'))
                return await self._organize_files(path)
            
            # Backup operations
            elif any(keyword in action_lower for keyword in ["backup", "säkerhetskopia"]):
                return await self._create_backup(action, **kwargs)
            
            else:
                return {
                    "success": False,
                    "message": "Filoperationen kunde inte identifieras",
                    "available_operations": [
                        "lista filer", "läs fil", "skriv fil", "kopiera", 
                        "flytta", "ta bort", "organisera", "backup"
                    ]
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Filoperationen misslyckades: {str(e)}",
                "error": str(e)
            }
    
    async def _list_directory_enhanced(self, path: str) -> Dict[str, Any]:
        """Enhanced directory listing with file info"""
        try:
            expanded_path = os.path.expanduser(path)
            if not os.path.exists(expanded_path):
                return {
                    "success": False,
                    "message": f"Sökvägen {path} existerar inte"
                }
            
            items = []
            total_size = 0
            
            for item in os.listdir(expanded_path):
                item_path = os.path.join(expanded_path, item)
                stat_info = os.stat(item_path)
                
                item_info = {
                    "name": item,
                    "type": "directory" if os.path.isdir(item_path) else "file",
                    "size": stat_info.st_size,
                    "size_human": self._human_readable_size(stat_info.st_size),
                    "modified": datetime.fromtimestamp(stat_info.st_mtime).isoformat(),
                    "permissions": oct(stat_info.st_mode)[-3:]
                }
                
                if os.path.isfile(item_path):
                    item_info["mime_type"] = mimetypes.guess_type(item_path)[0]
                    total_size += stat_info.st_size
                
                items.append(item_info)
            
            # Sort items: directories first, then files
            items.sort(key=lambda x: (x["type"] == "file", x["name"].lower()))
            
            return {
                "success": True,
                "message": f"Hittade {len(items)} objekt i {path}",
                "path": expanded_path,
                "items": items,
                "total_files": sum(1 for item in items if item["type"] == "file"),
                "total_directories": sum(1 for item in items if item["type"] == "directory"),
                "total_size": self._human_readable_size(total_size)
            }
            
        except PermissionError:
            return {
                "success": False,
                "message": f"Ingen behörighet att läsa {path}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Kunde inte lista innehållet: {str(e)}"
            }
    
    async def _read_file_enhanced(self, file_path: str) -> Dict[str, Any]:
        """Enhanced file reading with encoding detection and preview"""
        try:
            expanded_path = os.path.expanduser(file_path)
            
            if not os.path.exists(expanded_path):
                return {
                    "success": False,
                    "message": f"Filen {file_path} existerar inte"
                }
            
            if not os.path.isfile(expanded_path):
                return {
                    "success": False,
                    "message": f"{file_path} är inte en fil"
                }
            
            # Get file info
            stat_info = os.stat(expanded_path)
            file_size = stat_info.st_size
            
            # Check if file is too large (>10MB)
            if file_size > 10 * 1024 * 1024:
                return {
                    "success": False,
                    "message": f"Filen är för stor ({self._human_readable_size(file_size)}). Max 10MB."
                }
            
            # Try to read with different encodings
            encodings = ['utf-8', 'latin-1', 'cp1252']
            content = None
            used_encoding = None
            
            for encoding in encodings:
                try:
                    with open(expanded_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    used_encoding = encoding
                    break
                except UnicodeDecodeError:
                    continue
            
            if content is None:
                return {
                    "success": False,
                    "message": "Kunde inte läsa filen - okänd encoding"
                }
            
            # Truncate if too long for display
            preview = content[:2000] + "..." if len(content) > 2000 else content
            
            return {
                "success": True,
                "message": f"Läste filen {file_path}",
                "file_path": expanded_path,
                "content": content,
                "preview": preview,
                "size": self._human_readable_size(file_size),
                "encoding": used_encoding,
                "lines": len(content.splitlines()),
                "mime_type": mimetypes.guess_type(expanded_path)[0]
            }
            
        except PermissionError:
            return {
                "success": False,
                "message": f"Ingen behörighet att läsa {file_path}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Kunde inte läsa filen: {str(e)}"
            }
    
    async def _write_file_enhanced(self, file_path: str, content: str) -> Dict[str, Any]:
        """Enhanced file writing with backup and safety checks"""
        try:
            expanded_path = os.path.expanduser(file_path)
            
            # Check if this is a restricted operation
            if not self._is_safe_file_operation(expanded_path, "write"):
                return {
                    "success": False,
                    "message": "Kan inte skriva till systemfiler eller skyddade områden"
                }
            
            # Create backup if file exists
            backup_path = None
            if os.path.exists(expanded_path):
                backup_path = f"{expanded_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                shutil.copy2(expanded_path, backup_path)
            
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(expanded_path), exist_ok=True)
            
            # Write file
            with open(expanded_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return {
                "success": True,
                "message": f"Skrev till filen {file_path}",
                "file_path": expanded_path,
                "size": self._human_readable_size(len(content.encode('utf-8'))),
                "lines": len(content.splitlines()),
                "backup_created": backup_path is not None,
                "backup_path": backup_path
            }
            
        except PermissionError:
            return {
                "success": False,
                "message": f"Ingen behörighet att skriva till {file_path}"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Kunde inte skriva filen: {str(e)}"
            }
    
    async def _organize_files(self, path: str) -> Dict[str, Any]:
        """Intelligent file organization by type and date"""
        try:
            expanded_path = os.path.expanduser(path)
            
            if not os.path.exists(expanded_path):
                return {
                    "success": False,
                    "message": f"Sökvägen {path} existerar inte"
                }
            
            # File type mappings
            file_types = {
                'Documents': ['.pdf', '.doc', '.docx', '.txt', '.odt', '.rtf'],
                'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
                'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm'],
                'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.m4a'],
                'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'],
                'Code': ['.py', '.js', '.html', '.css', '.cpp', '.java', '.php'],
                'Spreadsheets': ['.xls', '.xlsx', '.ods', '.csv']
            }
            
            organized_files = {}
            total_moved = 0
            
            for item in os.listdir(expanded_path):
                item_path = os.path.join(expanded_path, item)
                
                if os.path.isfile(item_path):
                    file_ext = os.path.splitext(item)[1].lower()
                    
                    # Find appropriate category
                    category = 'Other'
                    for cat, extensions in file_types.items():
                        if file_ext in extensions:
                            category = cat
                            break
                    
                    # Create category directory if needed
                    category_path = os.path.join(expanded_path, category)
                    os.makedirs(category_path, exist_ok=True)
                    
                    # Move file
                    new_path = os.path.join(category_path, item)
                    if not os.path.exists(new_path):
                        shutil.move(item_path, new_path)
                        
                        if category not in organized_files:
                            organized_files[category] = []
                        organized_files[category].append(item)
                        total_moved += 1
            
            return {
                "success": True,
                "message": f"Organiserade {total_moved} filer i {path}",
                "organized_files": organized_files,
                "total_moved": total_moved,
                "categories_created": list(organized_files.keys())
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Kunde inte organisera filer: {str(e)}"
            }
    
    async def _handle_application_operations(self, action: str, **kwargs) -> Dict[str, Any]:
        """Handle application launching and management"""
        try:
            action_lower = action.lower()
            
            # Enhanced application mappings
            app_mappings = {
                # Browsers
                "firefox": "/snap/bin/firefox",
                "chrome": "google-chrome",
                "chromium": "/snap/bin/chromium",
                "browser": "/snap/bin/firefox",
                
                # Development
                "code": "code",
                "vscode": "code", 
                "terminal": "gnome-terminal",
                "git": "git-gui",
                
                # Media
                "vlc": "vlc",
                "spotify": "spotify",
                "musik": "rhythmbox",
                
                # Office
                "libreoffice": "libreoffice",
                "writer": "libreoffice --writer",
                "calc": "libreoffice --calc",
                
                # System
                "files": "nautilus",
                "filhanterare": "nautilus",
                "calculator": "gnome-calculator",
                "settings": "gnome-control-center",
                
                # Communication
                "discord": "discord",
                "skype": "skype",
                "teams": "teams"
            }
            
            # Extract application name
            app_name = None
            words = action.split()
            for word in ["öppna", "open", "starta", "start", "kör", "run"]:
                if word.lower() in [w.lower() for w in words]:
                    word_idx = next(i for i, w in enumerate(words) if w.lower() == word.lower())
                    if word_idx + 1 < len(words):
                        app_name = words[word_idx + 1].lower()
                        break
            
            if not app_name:
                # Try to find app name in the action
                for app in app_mappings.keys():
                    if app in action_lower:
                        app_name = app
                        break
            
            if not app_name:
                return {
                    "success": False,
                    "message": "Kunde inte identifiera applikationen att öppna",
                    "available_apps": list(app_mappings.keys())
                }
            
            # Get command
            app_command = app_mappings.get(app_name, app_name)
            
            # Launch application
            try:
                process = await asyncio.create_subprocess_shell(
                    f"{app_command} &",
                    stdout=asyncio.subprocess.DEVNULL,
                    stderr=asyncio.subprocess.DEVNULL
                )
                await asyncio.sleep(1)
                
                return {
                    "success": True,
                    "message": f"Öppnade {app_name} framgångsrikt",
                    "application": app_name,
                    "command": app_command
                }
                
            except Exception as e:
                # Try alternative commands for popular apps
                alternatives = {
                    "browser": ["/snap/bin/chromium", "google-chrome", "firefox"],
                    "editor": ["code", "gedit", "nano"],
                    "terminal": ["gnome-terminal", "konsole", "xterm"]
                }
                
                for alt_cmd in alternatives.get(app_name, []):
                    try:
                        process = await asyncio.create_subprocess_shell(
                            f"{alt_cmd} &",
                            stdout=asyncio.subprocess.DEVNULL,
                            stderr=asyncio.subprocess.DEVNULL
                        )
                        await asyncio.sleep(1)
                        
                        return {
                            "success": True,
                            "message": f"Öppnade {app_name} med alternativ kommando ({alt_cmd})",
                            "application": app_name,
                            "command": alt_cmd
                        }
                    except:
                        continue
                
                return {
                    "success": False,
                    "message": f"Kunde inte öppna {app_name}: {str(e)}",
                    "error": str(e)
                }
                
        except Exception as e:
            return {
                "success": False,
                "message": f"Applikationsoperationen misslyckades: {str(e)}"
            }
    
    def _human_readable_size(self, size_bytes: int) -> str:
        """Convert bytes to human readable size"""
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} PB"
    
    def _extract_file_path(self, action: str) -> Optional[str]:
        """Extract file path from action string"""
        # Look for quoted paths
        quoted_match = re.search(r'["\']([^"\']+)["\']', action)
        if quoted_match:
            return quoted_match.group(1)
        
        # Look for paths that look like file paths
        path_match = re.search(r'(/[^\s]+|[~.]/?[^\s]*)', action)
        if path_match:
            return path_match.group(1)
        
        return None
    
    def _is_safe_file_operation(self, file_path: str, operation: str) -> bool:
        """Check if file operation is safe"""
        if not self.safe_operations:
            return True
        
        dangerous_paths = [
            '/etc/', '/usr/', '/bin/', '/sbin/', '/boot/', '/dev/', '/proc/', '/sys/'
        ]
        
        for dangerous_path in dangerous_paths:
            if file_path.startswith(dangerous_path):
                return False
        
        return True
    
    async def _handle_system_operations(self, action: str, **kwargs) -> Dict[str, Any]:
        """Handle system information and status operations"""
        try:
            # Get detailed system status
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            return {
                "success": True,
                "message": "Systemstatus hämtad",
                "system_info": {
                    "cpu_usage": f"{cpu_percent}%",
                    "memory_usage": f"{memory.percent}%",
                    "memory_available": self._human_readable_size(memory.available),
                    "disk_usage": f"{disk.percent}%",
                    "disk_free": self._human_readable_size(disk.free),
                    "running_processes": len(psutil.pids()),
                    "uptime": self._get_uptime(),
                    "load_average": os.getloadavg() if hasattr(os, 'getloadavg') else "N/A"
                },
                "hardware_info": self.system_info
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Kunde inte hämta systemstatus: {str(e)}"
            }
    
    async def _handle_search_operations(self, action: str, **kwargs) -> Dict[str, Any]:
        """Handle file and content search operations"""
        # Implementation for search functionality
        return {
            "success": True,
            "message": "Sökfunktion kommer snart...",
            "note": "Implementeras i nästa version"
        }
    
    async def _handle_automation_sequences(self, action: str, **kwargs) -> Dict[str, Any]:
        """Handle automation workflow sequences"""
        # Implementation for automation sequences
        return {
            "success": True,
            "message": "Automationssekvenser kommer snart...",
            "note": "Implementeras i nästa version"
        }
    
    def _get_uptime(self) -> str:
        """Get system uptime"""
        try:
            with open('/proc/uptime', 'r') as f:
                uptime_seconds = float(f.readline().split()[0])
            
            days = int(uptime_seconds // 86400)
            hours = int((uptime_seconds % 86400) // 3600)
            minutes = int((uptime_seconds % 3600) // 60)
            
            return f"{days}d {hours}h {minutes}m"
        except:
            return "Unknown"
    
    def get_capabilities(self) -> Dict[str, Any]:
        """Get service capabilities"""
        return {
            "file_operations": [
                "list_directory", "read_file", "write_file", "copy_file", 
                "move_file", "delete_file", "organize_files", "create_backup"
            ],
            "application_operations": [
                "open_browser", "open_editor", "open_terminal", "open_media_player",
                "open_office_apps", "open_development_tools"
            ],
            "system_operations": [
                "get_status", "get_hardware_info", "monitor_resources",
                "get_processes", "get_uptime"
            ],
            "search_operations": [
                "search_files", "search_content", "find_by_type", "find_by_date"
            ],
            "safety_features": [
                "backup_before_changes", "restricted_system_access", 
                "permission_checking", "safe_file_operations"
            ]
        }
