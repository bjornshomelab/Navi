"""
JARVIS AI Agent - Self-Improvement Service
Enables JARVIS to analyze and improve its own code and functionality
"""
import ast
import os
import shutil
import time
import asyncio
from typing import Dict, Any, List, Optional, Tuple
from pathlib import Path
import json
import subprocess
from datetime import datetime
import hashlib

class SelfImprovementService:
    """Service that enables JARVIS to improve its own code"""
    
    def __init__(self, project_root: str = "/home/bjorn/Skrivbord/Jarvis"):
        self.project_root = Path(project_root)
        self.backup_dir = self.project_root / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        
        # Safety settings
        self.auto_apply_improvements = False  # Manual approval required
        self.max_file_size_kb = 100  # Only modify small files automatically
        self.safe_patterns = [
            "# JARVIS-SAFE-MODIFY",
            "# Auto-improvement allowed"
        ]
        
        # Code analysis patterns
        self.improvement_patterns = {
            "error_handling": {
                "pattern": r"except.*:\s*pass",
                "improvement": "Add proper error logging and handling",
                "priority": "high"
            },
            "hardcoded_values": {
                "pattern": r"['\"][A-Z_]+['\"]",  # Hardcoded strings
                "improvement": "Move to configuration file",
                "priority": "medium"
            },
            "performance": {
                "pattern": r"for.*in.*range\(len\(",
                "improvement": "Use enumerate() for better performance",
                "priority": "low"
            }
        }
        
        print("🔧 Self-Improvement System initialized")
    
    async def analyze_codebase(self) -> Dict[str, Any]:
        """Analyze the entire codebase for improvement opportunities"""
        try:
            analysis_results = {
                "timestamp": datetime.now().isoformat(),
                "files_analyzed": 0,
                "improvements_found": [],
                "code_quality_score": 0.0,
                "recommendations": []
            }
            
            # Analyze Python files in the project
            python_files = list(self.project_root.rglob("*.py"))
            
            for file_path in python_files:
                if self._is_safe_to_analyze(file_path):
                    file_analysis = await self._analyze_file(file_path)
                    analysis_results["improvements_found"].extend(file_analysis["improvements"])
                    analysis_results["files_analyzed"] += 1
            
            # Calculate quality score
            total_issues = len(analysis_results["improvements_found"])
            analysis_results["code_quality_score"] = max(0.0, 100.0 - (total_issues * 2.5))
            
            # Generate recommendations
            analysis_results["recommendations"] = self._generate_recommendations(analysis_results["improvements_found"])
            
            return analysis_results
            
        except Exception as e:
            return {"error": f"Codebase analysis failed: {str(e)}"}
    
    async def _analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single Python file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            improvements = []
            
            # Check for AST parsing errors
            try:
                tree = ast.parse(content)
                improvements.extend(self._analyze_ast(tree, file_path))
            except SyntaxError as e:
                improvements.append({
                    "type": "syntax_error",
                    "file": str(file_path),
                    "line": e.lineno,
                    "description": f"Syntax error: {e.msg}",
                    "priority": "critical"
                })
            
            # Pattern-based analysis
            improvements.extend(self._analyze_patterns(content, file_path))
            
            # Check for specific JARVIS improvements
            improvements.extend(self._analyze_jarvis_specific(content, file_path))
            
            return {
                "file": str(file_path),
                "improvements": improvements,
                "analysis_timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                "file": str(file_path),
                "error": str(e),
                "improvements": []
            }
    
    def _analyze_ast(self, tree: ast.AST, file_path: Path) -> List[Dict[str, Any]]:
        """Analyze AST for code improvements"""
        improvements = []
        
        for node in ast.walk(tree):
            # Check for bare except clauses
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                improvements.append({
                    "type": "bare_except",
                    "file": str(file_path),
                    "line": node.lineno,
                    "description": "Bare except clause should specify exception type",
                    "priority": "medium",
                    "suggested_fix": "except Exception as e:"
                })
            
            # Check for TODO comments in docstrings
            if isinstance(node, ast.Str) and "TODO" in node.s:
                improvements.append({
                    "type": "todo_found",
                    "file": str(file_path),
                    "line": node.lineno,
                    "description": f"TODO found: {node.s[:100]}...",
                    "priority": "low"
                })
        
        return improvements
    
    def _analyze_patterns(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Analyze content using regex patterns"""
        import re
        improvements = []
        
        lines = content.split('\n')
        
        for pattern_name, pattern_info in self.improvement_patterns.items():
            pattern = pattern_info["pattern"]
            
            for line_num, line in enumerate(lines, 1):
                if re.search(pattern, line):
                    improvements.append({
                        "type": pattern_name,
                        "file": str(file_path),
                        "line": line_num,
                        "description": pattern_info["improvement"],
                        "priority": pattern_info["priority"],
                        "code_snippet": line.strip()
                    })
        
        return improvements
    
    def _analyze_jarvis_specific(self, content: str, file_path: Path) -> List[Dict[str, Any]]:
        """Analyze for JARVIS-specific improvements"""
        improvements = []
        
        # Check for missing docstrings in JARVIS functions
        if "def " in content and '"""' not in content:
            improvements.append({
                "type": "missing_docstring",
                "file": str(file_path),
                "description": "JARVIS functions should have descriptive docstrings",
                "priority": "medium"
            })
        
        # Check for hardcoded API endpoints
        if "localhost:808" in content:
            improvements.append({
                "type": "hardcoded_endpoint",
                "file": str(file_path),
                "description": "API endpoints should be configurable",
                "priority": "medium",
                "suggested_fix": "Use environment variables or config file"
            })
        
        # Check for missing error handling in service calls
        if "service." in content and "try:" not in content:
            improvements.append({
                "type": "missing_error_handling",
                "file": str(file_path),
                "description": "Service calls should have error handling",
                "priority": "high"
            })
        
        return improvements
    
    def _generate_recommendations(self, improvements: List[Dict[str, Any]]) -> List[str]:
        """Generate high-level recommendations based on improvements"""
        recommendations = []
        
        # Count improvement types
        type_counts = {}
        for improvement in improvements:
            imp_type = improvement["type"]
            type_counts[imp_type] = type_counts.get(imp_type, 0) + 1
        
        # Generate recommendations based on patterns
        if type_counts.get("missing_error_handling", 0) > 3:
            recommendations.append("Implement comprehensive error handling across all services")
        
        if type_counts.get("hardcoded_endpoint", 0) > 0:
            recommendations.append("Create a centralized configuration system")
        
        if type_counts.get("missing_docstring", 0) > 5:
            recommendations.append("Add comprehensive documentation to all functions")
        
        if type_counts.get("bare_except", 0) > 2:
            recommendations.append("Replace bare except clauses with specific exception handling")
        
        # JARVIS-specific recommendations
        recommendations.append("Consider implementing incremental learning from user feedback")
        recommendations.append("Add more sophisticated context awareness between commands")
        recommendations.append("Implement command chaining for complex multi-step tasks")
        
        return recommendations
    
    async def suggest_code_improvements(self, file_path: str) -> Dict[str, Any]:
        """Suggest specific code improvements for a file"""
        try:
            file_path = Path(file_path)
            
            if not self._is_safe_to_analyze(file_path):
                return {"error": "File not safe for analysis"}
            
            analysis = await self._analyze_file(file_path)
            
            # Generate specific code suggestions
            suggestions = []
            for improvement in analysis["improvements"]:
                if improvement["priority"] in ["high", "critical"]:
                    suggestion = await self._generate_code_suggestion(improvement)
                    if suggestion:
                        suggestions.append(suggestion)
            
            return {
                "file": str(file_path),
                "analysis": analysis,
                "code_suggestions": suggestions,
                "auto_applicable": len([s for s in suggestions if s.get("safe_to_apply", False)])
            }
            
        except Exception as e:
            return {"error": f"Code suggestion failed: {str(e)}"}
    
    async def _generate_code_suggestion(self, improvement: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate specific code suggestion for an improvement"""
        try:
            suggestion = {
                "improvement_type": improvement["type"],
                "description": improvement["description"],
                "priority": improvement["priority"],
                "safe_to_apply": False
            }
            
            # Generate specific fixes
            if improvement["type"] == "bare_except":
                suggestion["original_code"] = "except:"
                suggestion["improved_code"] = "except Exception as e:\n    print(f'Error: {e}')"
                suggestion["safe_to_apply"] = True
            
            elif improvement["type"] == "missing_error_handling":
                suggestion["description"] = "Add try-except block around service calls"
                suggestion["improved_code"] = """try:
    result = service.some_method()
except Exception as e:
    print(f'Service error: {e}')
    result = None"""
            
            elif improvement["type"] == "hardcoded_endpoint":
                suggestion["improved_code"] = """# Add to config.py
API_BASE_URL = os.getenv('JARVIS_API_URL', 'http://localhost:8081')

# Use in code
endpoint = f'{API_BASE_URL}/api/command'"""
            
            return suggestion
            
        except Exception as e:
            print(f"Code suggestion generation error: {e}")
            return None
    
    async def apply_safe_improvements(self, improvements: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Apply improvements that are marked as safe"""
        try:
            if not self.auto_apply_improvements:
                return {"error": "Auto-apply is disabled. Manual approval required."}
            
            applied_count = 0
            failed_count = 0
            results = []
            
            for improvement in improvements:
                if improvement.get("safe_to_apply", False):
                    try:
                        # Create backup before modifying
                        backup_path = await self._create_backup(improvement["file"])
                        
                        # Apply improvement
                        success = await self._apply_improvement(improvement)
                        
                        if success:
                            applied_count += 1
                            results.append({
                                "file": improvement["file"],
                                "improvement": improvement["type"],
                                "status": "applied",
                                "backup": str(backup_path)
                            })
                        else:
                            failed_count += 1
                            results.append({
                                "file": improvement["file"],
                                "improvement": improvement["type"],
                                "status": "failed"
                            })
                            
                    except Exception as e:
                        failed_count += 1
                        results.append({
                            "file": improvement["file"],
                            "improvement": improvement["type"],
                            "status": "error",
                            "error": str(e)
                        })
            
            return {
                "applied_improvements": applied_count,
                "failed_improvements": failed_count,
                "results": results,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"error": f"Improvement application failed: {str(e)}"}
    
    async def _create_backup(self, file_path: str) -> Path:
        """Create backup of file before modification"""
        file_path = Path(file_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{file_path.stem}_{timestamp}{file_path.suffix}"
        backup_path = self.backup_dir / backup_name
        
        shutil.copy2(file_path, backup_path)
        return backup_path
    
    async def _apply_improvement(self, improvement: Dict[str, Any]) -> bool:
        """Apply a specific improvement to a file"""
        try:
            file_path = Path(improvement["file"])
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Apply improvement based on type
            if improvement["type"] == "bare_except":
                content = content.replace(
                    improvement.get("original_code", "except:"),
                    improvement.get("improved_code", "except Exception as e:")
                )
            
            # Write back modified content
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            return True
            
        except Exception as e:
            print(f"Improvement application error: {e}")
            return False
    
    def _is_safe_to_analyze(self, file_path: Path) -> bool:
        """Check if file is safe to analyze and potentially modify"""
        # Skip system files and directories
        if any(skip in str(file_path) for skip in [".git", "__pycache__", ".venv", "jarvis/lib"]):
            return False
        
        # Check file size
        if file_path.exists() and file_path.stat().st_size > self.max_file_size_kb * 1024:
            return False
        
        # Check for safety markers
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                if any(pattern in content for pattern in self.safe_patterns):
                    return True
        except:
            pass
        
        # Allow analysis of JARVIS core files
        jarvis_files = ["services", "routes", "models"]
        return any(part in str(file_path) for part in jarvis_files)
    
    async def get_improvement_stats(self) -> Dict[str, Any]:
        """Get statistics about code improvements"""
        try:
            analysis = await self.analyze_codebase()
            
            priority_counts = {}
            type_counts = {}
            
            for improvement in analysis.get("improvements_found", []):
                priority = improvement.get("priority", "unknown")
                imp_type = improvement.get("type", "unknown")
                
                priority_counts[priority] = priority_counts.get(priority, 0) + 1
                type_counts[imp_type] = type_counts.get(imp_type, 0) + 1
            
            return {
                "total_files_analyzed": analysis.get("files_analyzed", 0),
                "total_improvements": len(analysis.get("improvements_found", [])),
                "code_quality_score": analysis.get("code_quality_score", 0.0),
                "improvements_by_priority": priority_counts,
                "improvements_by_type": type_counts,
                "recommendations": analysis.get("recommendations", []),
                "last_analysis": analysis.get("timestamp", "")
            }
            
        except Exception as e:
            return {"error": f"Stats generation failed: {str(e)}"}
