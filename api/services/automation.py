"""
JARVIS AI Agent - Advanced Desktop & Web Automation Service
Handles mouse clicks, keyboard input, web automation, window management, and screen analysis
"""
import pyautogui
import time
import os
import asyncio
import json
import re
from typing import Dict, Any, List, Tuple, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import cv2
import numpy as np
from PIL import Image

# Optional Linux window management
try:
    import pygetwindow as gw
    WINDOW_MANAGEMENT_AVAILABLE = True
except (ImportError, NotImplementedError):
    WINDOW_MANAGEMENT_AVAILABLE = False
    gw = None
    print("⚠️ Window management not available on this platform")

from pynput import keyboard, mouse

class AutomationService:
    """Advanced service for desktop and web automation"""
    
    def __init__(self):
        # Configure pyautogui
        pyautogui.FAILSAFE = True  # Move mouse to corner to abort
        pyautogui.PAUSE = 0.3  # Faster response
        
        # Web driver (lazy initialization)
        self.driver = None
        
        # Screen resolution
        self.screen_width, self.screen_height = pyautogui.size()
        print(f"🖥️  Screen resolution: {self.screen_width}x{self.screen_height}")
        
        # Window management
        self.windows_cache = {}
        
        # Template matching cache
        self.template_cache = {}
    
    async def execute_automation(self, action: str) -> str:
        """Execute automation action based on description"""
        try:
            desc_lower = action.lower()
            
            # Window management
            if any(word in desc_lower for word in ["window", "app", "application", "program"]):
                return await self._handle_window_action(action)
            
            # Desktop automation
            elif any(word in desc_lower for word in ["click", "mouse", "cursor"]):
                return await self._handle_mouse_action(action)
            
            elif any(word in desc_lower for word in ["type", "write", "keyboard", "key"]):
                return await self._handle_keyboard_action(action)
            
            elif any(word in desc_lower for word in ["screenshot", "screen", "capture", "find", "locate"]):
                return await self._handle_screenshot_action(action)
            
            # Web automation
            elif any(word in desc_lower for word in ["browser", "web", "website", "url", "navigate"]):
                return await self._handle_web_action(action)
            
            elif any(word in desc_lower for word in ["search", "google"]):
                return await self._handle_search_action(action)
            
            elif any(word in desc_lower for word in ["fill", "form", "input", "submit"]):
                return await self._handle_form_action(action)
            
            # File operations
            elif any(word in desc_lower for word in ["file", "folder", "directory", "open", "save"]):
                return await self._handle_file_action(action)
            
            else:
                return f"Automation action not recognized: {action}"
                
        except Exception as e:
            return f"Automation failed: {str(e)}"
    
    async def _handle_window_action(self, action: str) -> str:
        """Handle window management actions"""
        try:
            if not WINDOW_MANAGEMENT_AVAILABLE:
                return "Window management not available on this platform. Try using Alt+Tab for window switching."
            
            desc_lower = action.lower()
            
            if "list" in desc_lower and "window" in desc_lower:
                # List all open windows
                windows = gw.getAllWindows()
                window_list = []
                for i, win in enumerate(windows):
                    if win.title and win.title.strip():
                        window_list.append(f"{i+1}. {win.title} ({win.width}x{win.height})")
                
                if window_list:
                    return f"Open windows:\n" + "\n".join(window_list[:10])  # Limit to 10
                else:
                    return "No windows found"
            
            elif "focus" in desc_lower or "activate" in desc_lower:
                # Focus/activate a window by name
                window_name = self._extract_window_name(action)
                if window_name:
                    windows = gw.getWindowsWithTitle(window_name)
                    if windows:
                        windows[0].activate()
                        return f"Focused window: {windows[0].title}"
                    else:
                        return f"Window not found: {window_name}"
                else:
                    return "No window name specified"
            
            elif "minimize" in desc_lower:
                # Minimize active window
                active_window = gw.getActiveWindow()
                if active_window:
                    active_window.minimize()
                    return f"Minimized window: {active_window.title}"
                else:
                    return "No active window found"
            
            elif "maximize" in desc_lower:
                # Maximize active window
                active_window = gw.getActiveWindow()
                if active_window:
                    active_window.maximize()
                    return f"Maximized window: {active_window.title}"
                else:
                    return "No active window found"
            
            elif "close" in desc_lower:
                # Close active window - use Alt+F4 instead
                pyautogui.hotkey('alt', 'f4')
                return "Sent close command (Alt+F4) to active window"
            
            else:
                return "Window action not recognized"
                
        except Exception as e:
            return f"Window action failed: {str(e)}"
    
    def _extract_window_name(self, text: str) -> str:
        """Extract window name from command text"""
        # Look for common patterns
        patterns = [
            r'focus\s+(\w+)',
            r'activate\s+(\w+)', 
            r'window\s+(\w+)',
            r'"([^"]+)"',
            r"'([^']+)'"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1)
        
        return ""

    async def _handle_mouse_action(self, action: str) -> str:
        """Handle mouse-related actions"""
        try:
            desc_lower = action.lower()
            
            # Extract coordinates if specified
            coords = self._extract_coordinates(action)
            
            if coords:
                x, y = coords
                if "right click" in desc_lower:
                    pyautogui.rightClick(x, y)
                    return f"Right clicked at ({x}, {y})"
                elif "double click" in desc_lower:
                    pyautogui.doubleClick(x, y)
                    return f"Double clicked at ({x}, {y})"
                else:
                    pyautogui.click(x, y)
                    return f"Clicked at ({x}, {y})"
            
            elif "center" in desc_lower or "middle" in desc_lower:
                # Click center of screen
                x, y = self.screen_width // 2, self.screen_height // 2
                pyautogui.click(x, y)
                return f"Clicked center of screen at ({x}, {y})"
            
            elif "right click" in desc_lower:
                # Right click at current position
                pyautogui.rightClick()
                return "Performed right click"
            
            elif "double click" in desc_lower:
                # Double click at current position
                pyautogui.doubleClick()
                return "Performed double click"
            
            elif "drag" in desc_lower:
                # Drag mouse
                return await self._handle_drag_action(action)
            
            elif "scroll up" in desc_lower:
                pyautogui.scroll(3)
                return "Scrolled up"
            
            elif "scroll down" in desc_lower:
                pyautogui.scroll(-3)
                return "Scrolled down"
            
            elif "move" in desc_lower:
                # Move mouse to position
                if coords:
                    x, y = coords
                    pyautogui.moveTo(x, y)
                    return f"Moved mouse to ({x}, {y})"
                else:
                    return "No coordinates specified for mouse move"
            
            else:
                # Simple click
                pyautogui.click()
                return "Performed click"
                
        except Exception as e:
            return f"Mouse action failed: {str(e)}"
    
    def _extract_coordinates(self, text: str) -> Optional[Tuple[int, int]]:
        """Extract x,y coordinates from text"""
        # Look for patterns like "click at 100,200" or "click (100, 200)"
        patterns = [
            r'(\d+)[,\s]+(\d+)',
            r'\((\d+)[,\s]+(\d+)\)',
            r'x[:\s]*(\d+)[,\s]*y[:\s]*(\d+)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    x, y = int(match.group(1)), int(match.group(2))
                    # Validate coordinates are within screen bounds
                    if 0 <= x <= self.screen_width and 0 <= y <= self.screen_height:
                        return (x, y)
                except ValueError:
                    continue
        
        return None
    
    async def _handle_drag_action(self, action: str) -> str:
        """Handle drag and drop actions"""
        try:
            # Extract start and end coordinates
            numbers = re.findall(r'\d+', action)
            if len(numbers) >= 4:
                start_x, start_y, end_x, end_y = map(int, numbers[:4])
                pyautogui.drag(end_x - start_x, end_y - start_y, duration=1, button='left')
                return f"Dragged from ({start_x}, {start_y}) to ({end_x}, {end_y})"
            else:
                return "Not enough coordinates for drag action (need start and end points)"
                
        except Exception as e:
            return f"Drag action failed: {str(e)}"
    
    async def _handle_keyboard_action(self, action: str) -> str:
        """Handle keyboard-related actions"""
        try:
            desc_lower = action.lower()
            
            # Extract text to type
            if "type" in desc_lower or "write" in desc_lower:
                text_to_type = self._extract_text_to_type(action)
                if text_to_type:
                    pyautogui.write(text_to_type, interval=0.05)
                    return f"Typed: '{text_to_type}'"
                else:
                    return "No text found to type"
            
            # Special key combinations
            elif "ctrl+c" in desc_lower or "copy" in desc_lower:
                pyautogui.hotkey('ctrl', 'c')
                return "Pressed Ctrl+C (copy)"
            
            elif "ctrl+v" in desc_lower or "paste" in desc_lower:
                pyautogui.hotkey('ctrl', 'v')
                return "Pressed Ctrl+V (paste)"
            
            elif "ctrl+a" in desc_lower or "select all" in desc_lower:
                pyautogui.hotkey('ctrl', 'a')
                return "Pressed Ctrl+A (select all)"
            
            elif "ctrl+z" in desc_lower or "undo" in desc_lower:
                pyautogui.hotkey('ctrl', 'z')
                return "Pressed Ctrl+Z (undo)"
            
            elif "ctrl+y" in desc_lower or "redo" in desc_lower:
                pyautogui.hotkey('ctrl', 'y')
                return "Pressed Ctrl+Y (redo)"
            
            elif "ctrl+s" in desc_lower or "save" in desc_lower:
                pyautogui.hotkey('ctrl', 's')
                return "Pressed Ctrl+S (save)"
            
            elif "ctrl+o" in desc_lower or "open" in desc_lower:
                pyautogui.hotkey('ctrl', 'o')
                return "Pressed Ctrl+O (open)"
            
            elif "ctrl+n" in desc_lower or "new" in desc_lower:
                pyautogui.hotkey('ctrl', 'n')
                return "Pressed Ctrl+N (new)"
            
            elif "alt+tab" in desc_lower or "switch window" in desc_lower:
                pyautogui.hotkey('alt', 'tab')
                return "Pressed Alt+Tab (switch window)"
            
            elif "alt+f4" in desc_lower or "close app" in desc_lower:
                pyautogui.hotkey('alt', 'f4')
                return "Pressed Alt+F4 (close application)"
            
            elif "win" in desc_lower or "windows key" in desc_lower:
                pyautogui.press('win')
                return "Pressed Windows key"
            
            elif "enter" in desc_lower:
                pyautogui.press('enter')
                return "Pressed Enter"
            
            elif "escape" in desc_lower:
                pyautogui.press('escape')
                return "Pressed Escape"
            
            elif "tab" in desc_lower:
                pyautogui.press('tab')
                return "Pressed Tab"
            
            elif "space" in desc_lower:
                pyautogui.press('space')
                return "Pressed Space"
            
            elif "backspace" in desc_lower:
                pyautogui.press('backspace')
                return "Pressed Backspace"
            
            elif "delete" in desc_lower:
                pyautogui.press('delete')
                return "Pressed Delete"
            
            # Arrow keys
            elif "up arrow" in desc_lower or "arrow up" in desc_lower:
                pyautogui.press('up')
                return "Pressed Up Arrow"
            
            elif "down arrow" in desc_lower or "arrow down" in desc_lower:
                pyautogui.press('down')
                return "Pressed Down Arrow"
            
            elif "left arrow" in desc_lower or "arrow left" in desc_lower:
                pyautogui.press('left')
                return "Pressed Left Arrow"
            
            elif "right arrow" in desc_lower or "arrow right" in desc_lower:
                pyautogui.press('right')
                return "Pressed Right Arrow"
            
            # Function keys
            elif "f1" in desc_lower:
                pyautogui.press('f1')
                return "Pressed F1"
            
            elif "f2" in desc_lower:
                pyautogui.press('f2')
                return "Pressed F2"
            
            elif "f5" in desc_lower or "refresh" in desc_lower:
                pyautogui.press('f5')
                return "Pressed F5 (refresh)"
            
            else:
                return "Keyboard action not recognized"
                
        except Exception as e:
            return f"Keyboard action failed: {str(e)}"
    
    def _extract_text_to_type(self, action: str) -> str:
        """Extract text to type from action description"""
        # Look for quoted text first
        quote_patterns = [r'"([^"]+)"', r"'([^']+)'"]
        
        for pattern in quote_patterns:
            match = re.search(pattern, action)
            if match:
                return match.group(1)
        
        # Look for text after keywords
        keywords = ["type", "write", "input", "enter"]
        words = action.split()
        
        for keyword in keywords:
            if keyword in [w.lower() for w in words]:
                try:
                    keyword_idx = [w.lower() for w in words].index(keyword)
                    if keyword_idx + 1 < len(words):
                        return " ".join(words[keyword_idx + 1:])
                except ValueError:
                    continue
        
        return ""

    async def _handle_screenshot_action(self, action: str) -> str:
        """Handle screenshot and screen analysis with advanced features"""
        try:
            desc_lower = action.lower()
            
            if "find" in desc_lower or "locate" in desc_lower:
                # Find an image on screen
                return await self._find_image_on_screen(action)
            
            elif "save" in desc_lower or "capture" in desc_lower:
                # Take and save screenshot
                screenshot = pyautogui.screenshot()
                screenshot_path = "/tmp/jarvis_screenshot.png"
                screenshot.save(screenshot_path)
                return f"Screenshot saved to {screenshot_path} ({self.screen_width}x{self.screen_height})"
            
            elif "region" in desc_lower:
                # Screenshot of specific region
                coords = self._extract_coordinates(action)
                if coords and len(coords) >= 4:
                    x1, y1, x2, y2 = coords[:4]
                    region = (x1, y1, x2-x1, y2-y1)
                    screenshot = pyautogui.screenshot(region=region)
                    screenshot_path = "/tmp/jarvis_region_screenshot.png"
                    screenshot.save(screenshot_path)
                    return f"Region screenshot saved to {screenshot_path}"
                else:
                    return "Invalid region coordinates"
            
            else:
                # Default screenshot
                screenshot = pyautogui.screenshot()
                screenshot_path = "/tmp/jarvis_screenshot.png"
                screenshot.save(screenshot_path)
                return f"Screenshot saved to {screenshot_path} ({self.screen_width}x{self.screen_height})"
            
        except Exception as e:
            return f"Screenshot failed: {str(e)}"
    
    async def _find_image_on_screen(self, action: str) -> str:
        """Find an image pattern on screen"""
        try:
            # This would require a template image to search for
            # For now, return a placeholder
            return "Image search functionality requires template images (not yet implemented)"
            
        except Exception as e:
            return f"Image search failed: {str(e)}"
    
    async def _handle_web_action(self, action: str) -> str:
        """Handle web browser automation"""
        try:
            desc_lower = action.lower()
            
            # Simple browser opening with system commands
            if "open browser" in desc_lower or "launch browser" in desc_lower:
                # Extract URL if present
                url = self._extract_url(action)
                
                # Try different browsers
                browsers = [
                    ("/snap/bin/chromium", "Chromium"),
                    ("/snap/bin/firefox", "Firefox"),
                    ("google-chrome", "Chrome"),
                    ("firefox", "Firefox"),
                    ("chromium-browser", "Chromium")
                ]
                
                import subprocess
                for browser_cmd, browser_name in browsers:
                    try:
                        if url:
                            # Open browser with URL
                            subprocess.Popen([browser_cmd, url], 
                                           stdout=subprocess.DEVNULL, 
                                           stderr=subprocess.DEVNULL)
                            return f"Opened {browser_name} with {url}"
                        else:
                            # Open browser without URL
                            subprocess.Popen([browser_cmd], 
                                           stdout=subprocess.DEVNULL, 
                                           stderr=subprocess.DEVNULL)
                            return f"Opened {browser_name}"
                    except (FileNotFoundError, OSError):
                        continue
                
                return "No suitable browser found"
            
            # Advanced automation using WebDriver (for complex tasks)
            elif any(word in desc_lower for word in ["fill", "click", "search", "submit"]):
                # Initialize browser if needed for complex automation
                if not self.driver:
                    await self._init_browser()
                
                if "navigate" in desc_lower or "goto" in desc_lower or "visit" in desc_lower:
                    url = self._extract_url(action)
                    if url:
                        self.driver.get(url)
                        return f"Navigated to {url}"
                    else:
                        return "No URL found in command"
                
                elif "back" in desc_lower:
                    self.driver.back()
                    return "Navigated back"
                
                elif "forward" in desc_lower:
                    self.driver.forward()
                    return "Navigated forward"
                
                elif "refresh" in desc_lower or "reload" in desc_lower:
                    self.driver.refresh()
                    return "Page refreshed"
                
                elif "scroll" in desc_lower:
                    if "down" in desc_lower:
                        self.driver.execute_script("window.scrollBy(0, 500);")
                        return "Scrolled down"
                    elif "up" in desc_lower:
                        self.driver.execute_script("window.scrollBy(0, -500);")
                        return "Scrolled up"
                    else:
                        self.driver.execute_script("window.scrollBy(0, 300);")
                        return "Scrolled"
                
                elif "click" in desc_lower:
                    # Click on element by text or selector
                    element_text = self._extract_element_text(action)
                    if element_text:
                        try:
                            # Try to find by text content
                            element = WebDriverWait(self.driver, 5).until(
                                EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(), '{element_text}')]"))
                            )
                            element.click()
                            return f"Clicked on element: {element_text}"
                        except TimeoutException:
                            # Try to find by link text
                            try:
                                element = WebDriverWait(self.driver, 5).until(
                                    EC.element_to_be_clickable((By.LINK_TEXT, element_text))
                                )
                                element.click()
                                return f"Clicked on link: {element_text}"
                            except TimeoutException:
                                return f"Could not find clickable element: {element_text}"
                    else:
                        return "No element text specified for clicking"
                
                elif "search" in desc_lower and "google" in desc_lower:
                    return await self._handle_search_action(action)
                
                elif "close browser" in desc_lower:
                    if self.driver:
                        self.driver.quit()
                        self.driver = None
                        return "Browser closed"
                    else:
                        return "No browser open"
                
                else:
                    return "Web action not recognized"
            
            # Fallback: try to open URL directly
            else:
                url = self._extract_url(action)
                if url:
                    import subprocess
                    try:
                        subprocess.Popen(["/snap/bin/chromium", url], 
                                       stdout=subprocess.DEVNULL, 
                                       stderr=subprocess.DEVNULL)
                        return f"Opened {url} in browser"
                    except:
                        return f"Failed to open {url}"
                else:
                    return "Web action not recognized"
                
        except Exception as e:
            return f"Web automation failed: {str(e)}"
    
    def _extract_url(self, text: str) -> str:
        """Extract URL from text"""
        # Look for URLs
        url_pattern = r'https?://[^\s]+'
        match = re.search(url_pattern, text)
        if match:
            return match.group(0)
        
        # Look for domain names
        domain_patterns = [
            r'www\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            r'[a-zA-Z0-9.-]+\.(com|se|org|net|edu|gov)',
        ]
        
        for pattern in domain_patterns:
            match = re.search(pattern, text)
            if match:
                domain = match.group(0)
                return f"https://{domain}" if not domain.startswith("http") else domain
        
        return ""
    
    def _extract_element_text(self, text: str) -> str:
        """Extract element text to click on"""
        # Look for quoted text
        quote_patterns = [r'"([^"]+)"', r"'([^']+)'"]
        
        for pattern in quote_patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)
        
        # Look for text after "click"
        words = text.split()
        if "click" in [w.lower() for w in words]:
            try:
                click_idx = [w.lower() for w in words].index("click")
                if click_idx + 1 < len(words):
                    return " ".join(words[click_idx + 1:])
            except ValueError:
                pass
        
        return ""
    
    async def _handle_search_action(self, action: str) -> str:
        """Handle search actions"""
        try:
            # Initialize browser if needed
            if not self.driver:
                await self._init_browser()
            
            # Extract search query
            words = action.split()
            if "search" in words:
                search_idx = words.index("search")
                if search_idx + 1 < len(words):
                    query = " ".join(words[search_idx + 1:])
                    
                    # Go to Google
                    self.driver.get("https://www.google.com")
                    
                    # Find search box and search
                    search_box = WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.NAME, "q"))
                    )
                    search_box.clear()
                    search_box.send_keys(query)
                    search_box.send_keys(Keys.RETURN)
                    
                    return f"Searched Google for: '{query}'"
                else:
                    return "No search query provided"
            else:
                return "Search command not understood"
                
        except Exception as e:
            return f"Search failed: {str(e)}"
    
    async def _handle_form_action(self, action: str) -> str:
        """Handle form filling and submission"""
        try:
            desc_lower = action.lower()
            
            # Initialize browser if needed
            if not self.driver:
                await self._init_browser()
            
            if "fill" in desc_lower:
                # Fill form field
                field_name, value = self._extract_form_data(action)
                if field_name and value:
                    try:
                        # Try different strategies to find the field
                        field_selectors = [
                            (By.NAME, field_name),
                            (By.ID, field_name),
                            (By.XPATH, f"//input[@placeholder='{field_name}']"),
                            (By.XPATH, f"//input[contains(@name, '{field_name}')]"),
                            (By.XPATH, f"//textarea[@name='{field_name}']"),
                        ]
                        
                        element = None
                        for selector_type, selector_value in field_selectors:
                            try:
                                element = WebDriverWait(self.driver, 3).until(
                                    EC.presence_of_element_located((selector_type, selector_value))
                                )
                                break
                            except TimeoutException:
                                continue
                        
                        if element:
                            element.clear()
                            element.send_keys(value)
                            return f"Filled field '{field_name}' with '{value}'"
                        else:
                            return f"Could not find form field: {field_name}"
                            
                    except Exception as e:
                        return f"Failed to fill field: {str(e)}"
                else:
                    return "Could not extract field name and value"
            
            elif "submit" in desc_lower:
                # Submit form
                try:
                    # Try to find submit button
                    submit_selectors = [
                        (By.XPATH, "//input[@type='submit']"),
                        (By.XPATH, "//button[@type='submit']"),
                        (By.XPATH, "//button[contains(text(), 'Submit')]"),
                        (By.XPATH, "//input[@value='Submit']"),
                    ]
                    
                    element = None
                    for selector_type, selector_value in submit_selectors:
                        try:
                            element = WebDriverWait(self.driver, 3).until(
                                EC.element_to_be_clickable((selector_type, selector_value))
                            )
                            break
                        except TimeoutException:
                            continue
                    
                    if element:
                        element.click()
                        return "Form submitted"
                    else:
                        # Try to submit by pressing Enter on any input field
                        inputs = self.driver.find_elements(By.TAG_NAME, "input")
                        if inputs:
                            inputs[0].send_keys(Keys.RETURN)
                            return "Form submitted (via Enter)"
                        else:
                            return "Could not find submit button or form"
                            
                except Exception as e:
                    return f"Failed to submit form: {str(e)}"
            
            else:
                return "Form action not recognized"
                
        except Exception as e:
            return f"Form action failed: {str(e)}"
    
    def _extract_form_data(self, text: str) -> Tuple[str, str]:
        """Extract field name and value from form command"""
        # Look for patterns like "fill username with john" or "fill 'email' with 'test@example.com'"
        patterns = [
            r'fill\s+["\']?([^"\']+)["\']?\s+with\s+["\']?([^"\']+)["\']?',
            r'input\s+["\']?([^"\']+)["\']?\s+["\']?([^"\']+)["\']?',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip(), match.group(2).strip()
        
        return "", ""
    
    async def _handle_file_action(self, action: str) -> str:
        """Handle file and folder operations"""
        try:
            desc_lower = action.lower()
            
            if "open file" in desc_lower:
                # Open file dialog
                pyautogui.hotkey('ctrl', 'o')
                return "Opened file dialog"
            
            elif "save file" in desc_lower:
                # Save file dialog
                pyautogui.hotkey('ctrl', 's')
                return "Opened save dialog"
            
            elif "new file" in desc_lower:
                # New file
                pyautogui.hotkey('ctrl', 'n')
                return "Created new file"
            
            elif "open folder" in desc_lower:
                # Open file explorer
                pyautogui.hotkey('win', 'e')
                return "Opened file explorer"
            
            else:
                return "File action not recognized"
                
        except Exception as e:
            return f"File action failed: {str(e)}"
    
    async def _init_browser(self):
        """Initialize web browser with better options"""
        try:
            # Try Firefox first (more reliable on Linux)
            try:
                from selenium.webdriver.firefox.service import Service as FirefoxService
                from selenium.webdriver.firefox.options import Options as FirefoxOptions
                from webdriver_manager.firefox import GeckoDriverManager
                
                options = FirefoxOptions()
                options.add_argument("--width=1920")
                options.add_argument("--height=1080")
                # options.add_argument("--headless")  # Uncomment for headless mode
                
                # Set preferences
                options.set_preference("dom.webnotifications.enabled", False)
                options.set_preference("geo.enabled", False)
                
                service = FirefoxService(GeckoDriverManager().install())
                self.driver = webdriver.Firefox(service=service, options=options)
                
                print("🦊 Using Firefox browser")
                
            except Exception as firefox_error:
                print(f"Firefox failed: {firefox_error}, trying Chrome...")
                
                # Fallback to Chrome/Chromium
                options = webdriver.ChromeOptions()
                options.add_argument("--no-sandbox")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1920,1080")
                options.add_argument("--start-maximized")
                
                # Use unique user data directory to avoid conflicts
                import tempfile
                temp_dir = tempfile.mkdtemp(prefix="jarvis_chrome_")
                options.add_argument(f"--user-data-dir={temp_dir}")
                
                # Use system chromium and chromedriver
                options.binary_location = "/snap/bin/chromium"
                
                # Disable notifications and location requests
                prefs = {
                    "profile.default_content_setting_values.notifications": 2,
                    "profile.default_content_setting_values.geolocation": 2,
                }
                options.add_experimental_option("prefs", prefs)
                
                # Try system chromedriver first, then webdriver-manager
                try:
                    service = Service("/usr/bin/chromedriver")
                    print("🔧 Using system chromedriver")
                except:
                    service = Service(ChromeDriverManager().install())
                    print("🔧 Using webdriver-manager chromedriver")
                
                self.driver = webdriver.Chrome(service=service, options=options)
                print("🌐 Using Chromium browser")
            
            # Set timeouts
            self.driver.implicitly_wait(5)
            self.driver.set_page_load_timeout(30)
            
            print("🌐 Browser initialized with optimized settings")
            
        except Exception as e:
            print(f"❌ Browser initialization failed: {e}")
            raise
    
    def close_browser(self):
        """Clean up browser resources"""
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
                print("🌐 Browser closed")
            except:
                pass
    
    async def get_system_info(self) -> Dict[str, Any]:
        """Get system information for automation"""
        try:
            info = {
                "screen_resolution": f"{self.screen_width}x{self.screen_height}",
                "browser_active": self.driver is not None,
                "available_windows": [],
                "mouse_position": pyautogui.position(),
                "window_management_available": WINDOW_MANAGEMENT_AVAILABLE,
            }
            
            # Get available windows if supported
            if WINDOW_MANAGEMENT_AVAILABLE:
                try:
                    windows = gw.getAllWindows()
                    for win in windows[:10]:  # Limit to 10 windows
                        if win.title and win.title.strip():
                            info["available_windows"].append({
                                "title": win.title,
                                "size": f"{win.width}x{win.height}",
                                "position": f"{win.left},{win.top}",
                                "visible": win.visible
                            })
                except:
                    pass
            else:
                info["available_windows"] = ["Window management not available on this platform"]
            
            return info
            
        except Exception as e:
            return {"error": str(e)}
    
    def __del__(self):
        """Cleanup on destruction"""
        self.close_browser()
