#!/usr/bin/env python3
"""
NAVI CLI Client
Command-line interface for interacting with NAVI AI Agent
"""
import requests
import json
import sys
import argparse
from typing import Dict, Any
import os
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn

# Configuration
API_BASE_URL = os.getenv("NAVI_API_URL", "http://localhost:8081/api")
console = Console()

class NaviCLI:
    """NAVI command-line client"""
    
    def __init__(self, api_url: str = API_BASE_URL):
        self.api_url = api_url
    
    def send_command(self, message: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Send a command to NAVI API"""
        try:
            payload = {
                "message": message,
                "context": context or {}
            }
            
            response = requests.post(
                f"{self.api_url}/command",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                return {
                    "error": f"API error: {response.status_code}",
                    "detail": response.text
                }
                
        except requests.exceptions.ConnectionError:
            return {
                "error": "Connection failed",
                "detail": f"Cannot connect to NAVI API at {self.api_url}"
            }
        except requests.exceptions.Timeout:
            return {
                "error": "Request timeout",
                "detail": "NAVI took too long to respond"
            }
        except Exception as e:
            return {
                "error": "Client error",
                "detail": str(e)
            }
    
    def check_status(self) -> Dict[str, Any]:
        """Check NAVI system status"""
        try:
            response = requests.get(f"{self.api_url.replace('/api', '')}/status", timeout=10)
            return response.json() if response.status_code == 200 else {"error": "Status check failed"}
        except:
            return {"error": "Cannot reach NAVI"}
    
    def format_response(self, response: Dict[str, Any]) -> None:
        """Format and display response"""
        if "error" in response:
            console.print(Panel(
                f"[red]Error: {response['error']}[/red]\n{response.get('detail', '')}",
                title="⚠️  NAVI Error",
                border_style="red"
            ))
            return
        
        # Main response
        navi_response = response.get("response", "No response")
        console.print(Panel(
            navi_response,
            title="🤖 NAVI",
            border_style="blue"
        ))
        
        # Actions taken
        actions = response.get("actions_taken", [])
        if actions and actions != ["conversation"]:
            actions_text = "\n".join([f"• {action}" for action in actions])
            console.print(Panel(
                actions_text,
                title="⚡ Actions Executed",
                border_style="green"
            ))
        
        # Execution info
        exec_time = response.get("execution_time", 0)
        command_type = response.get("command_type", "unknown")
        status = response.get("status", "unknown")
        
        info_text = f"Type: {command_type} | Status: {status} | Time: {exec_time:.2f}s"
        console.print(f"[dim]{info_text}[/dim]")

def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(description="NAVI AI Agent CLI")
    parser.add_argument("command", nargs="*", help="Command to send to NAVI")
    parser.add_argument("--status", action="store_true", help="Check NAVI status")
    parser.add_argument("--interactive", "-i", action="store_true", help="Start interactive mode")
    parser.add_argument("--api-url", default=API_BASE_URL, help="NAVI API URL")
    
    args = parser.parse_args()
    
    cli = NaviCLI(args.api_url)
    
    # Status check
    if args.status:
        console.print("[yellow]Checking NAVI status...[/yellow]")
        status = cli.check_status()
        
        if "error" in status:
            console.print(f"[red]❌ NAVI is offline: {status['error']}[/red]")
            sys.exit(1)
        else:
            console.print("[green]✅ NAVI is online[/green]")
            console.print(Panel(
                json.dumps(status, indent=2),
                title="System Status",
                border_style="green"
            ))
        return
    
    # Interactive mode
    if args.interactive:
        console.print(Panel(
            "Welcome to NAVI Interactive Mode\nType 'exit' or 'quit' to leave",
            title="🚀 NAVI CLI",
            border_style="cyan"
        ))
        
        while True:
            try:
                command = console.input("\n[cyan]You:[/cyan] ")
                
                if command.lower() in ['exit', 'quit', 'bye']:
                    console.print("[yellow]Goodbye, sir.[/yellow]")
                    break
                
                if not command.strip():
                    continue
                
                with Progress(
                    SpinnerColumn(),
                    TextColumn("[progress.description]{task.description}"),
                    console=console
                ) as progress:
                    task = progress.add_task("NAVI is thinking...", total=None)
                    response = cli.send_command(command)
                
                cli.format_response(response)
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Goodbye, sir.[/yellow]")
                break
            except EOFError:
                break
    
    # Single command mode
    elif args.command:
        command = " ".join(args.command)
        console.print(f"[cyan]Sending command:[/cyan] {command}")
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            task = progress.add_task("NAVI is processing...", total=None)
            response = cli.send_command(command)
        
        cli.format_response(response)
    
    # No command provided
    else:
        console.print("[yellow]No command provided. Use --help for usage information.[/yellow]")
        console.print("[dim]Example: navi 'what time is it?'[/dim]")
        console.print("[dim]Interactive: navi --interactive[/dim]")

if __name__ == "__main__":
    main()
