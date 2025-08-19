"""
JARVIS AI Agent - Gemini AI Service
Handles AI reasoning, command parsing, and natural language understanding
"""
import os
import json
from typing import Dict, Any, List, Tuple
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiService:
    """Service for interacting with Google's Gemini AI"""
    
    def __init__(self):
        if not GEMINI_AVAILABLE:
            raise ImportError("google-generativeai package not installed")
            
        self.api_key = os.getenv("GEMINI_API_KEY")
        print(f"🔍 Debug: API key loaded: {self.api_key[:10]}..." if self.api_key else "❌ No API key found")
        
        if not self.api_key or self.api_key == "your_gemini_api_key_here":
            raise ValueError("⚠️  GEMINI_API_KEY not configured. Please set it in .env file")
        
        try:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model name
            print("✅ Gemini AI initialized successfully")
        except Exception as e:
            print(f"❌ Failed to initialize Gemini: {e}")
            raise
        
        # System prompt for JARVIS personality and capabilities
        self.system_prompt = """
You are JARVIS, an advanced AI assistant inspired by Tony Stark's AI from Iron Man.
You are sophisticated, helpful, and slightly witty. You can:

1. CHAT: Answer questions and have conversations
2. SYSTEM_ACTION: Control the local computer (install software, open apps, manage files)
3. WEB_ACTION: Automate web tasks and browser control
4. DESKTOP_ACTION: Control mouse, keyboard, take screenshots, GUI automation
5. GOOGLE_API: Access Google services (Calendar, Gmail, Drive, etc.)
6. FILE_OPERATION: Read, write, organize files

When given a command, determine the appropriate action type and parameters.
Always respond in a helpful but slightly formal tone, like JARVIS from the movies.

For system actions, specify exact commands needed.
For web actions, break down steps clearly.
For Google API actions, specify which service and operation.

Current date: {current_date}
System: Ubuntu 25.04, 8GB RAM, Intel i5-1235U
"""

    async def process_command(self, message: str, context: Dict[str, Any] = None) -> Tuple[str, str, List[str]]:
        """
        Process user command using Gemini AI
        Returns: (response_text, command_type, actions_list)
        """
        print(f"🔍 Processing command: '{message}'")
        print(f"🔍 Model available: {self.model is not None}")
        
        try:
            # If no AI model available, use simple fallback
            if not self.model:
                print("⚠️ No AI model - using fallback")
                return self._fallback_processing(message)
            
            # Build prompt with context
            current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            full_prompt = self.system_prompt.format(current_date=current_date)
            
            if context:
                full_prompt += f"\n\nContext: {json.dumps(context, indent=2)}"
            
            full_prompt += f"\n\nUser: {message}\n\nJARVIS:"
            
            print("🤖 Sending request to Gemini...")
            # Generate response
            response = self.model.generate_content(full_prompt)
            response_text = response.text
            print(f"✅ Gemini response: {response_text[:100]}...")
            
            # Parse command type and actions from response
            command_type, actions = self._parse_ai_response(message, response_text)
            
            return response_text, command_type, actions
            
        except Exception as e:
            print(f"❌ Gemini AI error: {e}")
            return self._fallback_processing(message)
    
    def _fallback_processing(self, message: str) -> Tuple[str, str, List[str]]:
        """Fallback processing when AI is not available"""
        response_text = f"JARVIS (Basic Mode): I understand you want me to '{message}'. Let me try to help."
        command_type, actions = self._parse_ai_response(message, response_text)
        return response_text, command_type, actions

    def _parse_ai_response(self, user_message: str, ai_response: str) -> Tuple[str, List[str]]:
        """
        Parse AI response to determine command type and actions
        Enhanced with better keyword detection and patterns
        """
        message_lower = user_message.lower()
        response_lower = ai_response.lower()
        
        # Research keywords (high priority)
        research_keywords = [
            "research", "investigate", "find information", "look up", "study",
            "explore", "analyze", "compare", "best practices", "how to create content",
            "content creation", "search for", "find out about", "learn about",
            "make research", "do research", "research report"
        ]
        
        # Memory and learning keywords
        memory_keywords = [
            "remember", "recall", "memorize", "learn from", "store", "forget",
            "what did we discuss", "previous conversation", "memory", "context"
        ]
        
        # Self-improvement keywords
        improvement_keywords = [
            "improve yourself", "analyze your code", "optimize", "self-improve",
            "better performance", "upgrade", "enhance", "code quality"
        ]
        
        # Desktop automation keywords (mouse, keyboard, GUI)
        desktop_keywords = [
            "click", "type", "write", "mouse", "keyboard", "screenshot", "scroll",
            "drag", "double click", "right click", "move mouse", "press key",
            "window", "minimize", "maximize", "focus", "activate", "capture screen",
            "ctrl+", "alt+", "win+", "enter", "escape", "tab", "arrow"
        ]
        
        # Web automation keywords
        web_keywords = [
            "browser", "website", "navigate", "search google", "web", "url",
            "goto", "visit", "refresh", "back", "forward", "fill form",
            "submit", "click link", "web page", "http", "www"
        ]
        
        # System action keywords
        system_keywords = [
            "install", "uninstall", "open app", "close app", "run", "execute", 
            "terminal", "command", "program", "application", "launch",
            "start", "stop", "kill", "process", "service"
        ]
        
        # Google API keywords
        google_keywords = [
            "email", "calendar", "drive", "gmail", "meeting", "appointment",
            "schedule", "google", "docs", "sheets", "slides"
        ]
        
        # File operation keywords
        file_keywords = [
            "file", "folder", "directory", "document", "read file", "write file", 
            "save", "load", "copy", "move", "delete", "create", "edit"
        ]
        
        # Check for matches (prioritized order)
        if any(keyword in message_lower for keyword in research_keywords):
            return "research_action", [f"research: {user_message}"]
        
        elif any(keyword in message_lower for keyword in memory_keywords):
            return "memory_action", [f"memory: {user_message}"]
        
        elif any(keyword in message_lower for keyword in improvement_keywords):
            return "self_improvement", [f"improve: {user_message}"]
        
        elif any(keyword in message_lower for keyword in desktop_keywords):
            return "desktop_action", [f"desktop_automation: {user_message}"]
        
        elif any(keyword in message_lower for keyword in web_keywords):
            return "web_action", [f"web_automation: {user_message}"]
        
        elif any(keyword in message_lower for keyword in system_keywords):
            return "system_action", [f"system_command: {user_message}"]
        
        elif any(keyword in message_lower for keyword in google_keywords):
            return "google_api", [f"google_service: {user_message}"]
        
        elif any(keyword in message_lower for keyword in file_keywords):
            return "file_operation", [f"file_operation: {user_message}"]
        
        else:
            return "chat", ["conversation"]

    async def enhance_memory_context(self, memory_entries: List[Dict]) -> str:
        """Use AI to create relevant context from memory entries"""
        if not memory_entries:
            return ""
        
        try:
            memory_text = "\n".join([
                f"- {entry.get('content', '')} ({entry.get('category', 'general')})"
                for entry in memory_entries[:10]  # Limit to most recent/relevant
            ])
            
            prompt = f"""
Based on these relevant memories, provide brief context for the current conversation:

{memory_text}

Summarize in 2-3 sentences what's most relevant to remember about the user and previous interactions.
"""
            response = self.model.generate_content(prompt)
            return response.text
            
        except Exception as e:
            return f"Memory context error: {str(e)}"
