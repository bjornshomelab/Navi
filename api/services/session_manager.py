"""
JARVIS AI Agent - Session Manager
Handles session timeouts and cleanup for inactive sessions
"""
import asyncio
import time
from typing import Dict, Optional
from datetime import datetime, timedelta
import threading
import logging

# Configure logging to show session manager messages
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SessionManager:
    """Manages user sessions with automatic timeout and cleanup"""
    
    def __init__(self, timeout_minutes: int = 5):
        self.timeout_seconds = timeout_minutes * 60
        self.sessions: Dict[str, dict] = {}
        self.cleanup_task = None
        self.running = False
        self.lock = threading.Lock()
        
        print(f"🕐 Session manager initialized with {timeout_minutes} minute timeout")
        
    def start_cleanup_task(self):
        """Start the background cleanup task (called when first session is created)"""
        if not self.running:
            self.running = True
            # Start cleanup in a background thread instead of async task
            threading.Thread(target=self._cleanup_thread, daemon=True).start()
            print(f"🕐 Session cleanup started")
    
    def _cleanup_thread(self):
        """Background thread that checks for expired sessions"""
        while self.running:
            try:
                self._cleanup_expired_sessions_sync()
                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                logger.error(f"Session cleanup error: {e}")
                time.sleep(60)  # Wait longer on error
    
    def _cleanup_expired_sessions_sync(self):
        """Remove expired sessions and perform cleanup (synchronous version)"""
        current_time = time.time()
        expired_sessions = []
        
        with self.lock:
            for session_id, session_data in self.sessions.items():
                if current_time - session_data['last_activity'] > self.timeout_seconds:
                    expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            self._cleanup_session_sync(session_id)
    
    def update_activity(self, session_id: str, user_id: Optional[str] = None):
        """Update last activity time for a session"""
        current_time = time.time()
        
        with self.lock:
            if session_id not in self.sessions:
                # Create new session
                self.sessions[session_id] = {
                    'user_id': user_id,
                    'created_at': current_time,
                    'last_activity': current_time,
                    'command_count': 0,
                    'active_workflows': [],
                    'resources': []
                }
                print(f"📝 New session created: {session_id}")
                
                # Start cleanup task when first session is created
                if not self.running:
                    self.start_cleanup_task()
            else:
                # Update existing session
                self.sessions[session_id]['last_activity'] = current_time
            
            self.sessions[session_id]['command_count'] += 1
    
    def add_resource(self, session_id: str, resource_type: str, resource_id: str):
        """Add a resource to track for cleanup (browser, file, workflow, etc.)"""
        with self.lock:
            if session_id in self.sessions:
                resource = {
                    'type': resource_type,
                    'id': resource_id,
                    'created_at': time.time()
                }
                self.sessions[session_id]['resources'].append(resource)
                logger.debug(f"📎 Added resource {resource_type}:{resource_id} to session {session_id}")
    
    def remove_resource(self, session_id: str, resource_type: str, resource_id: str):
        """Remove a resource from session tracking"""
        with self.lock:
            if session_id in self.sessions:
                self.sessions[session_id]['resources'] = [
                    r for r in self.sessions[session_id]['resources']
                    if not (r['type'] == resource_type and r['id'] == resource_id)
                ]
    
    async def cleanup_session(self, session_id: str):
        """Clean up an expired session and its resources"""
        self._cleanup_session_sync(session_id)
    
    def _cleanup_session_sync(self, session_id: str):
        """Clean up an expired session and its resources (synchronous version)"""
        session_data = None
        
        with self.lock:
            if session_id in self.sessions:
                session_data = self.sessions.pop(session_id)
        
        if session_data:
            print(f"🧹 Cleaning up expired session: {session_id}")
            
            # Clean up session resources
            for resource in session_data.get('resources', []):
                self._cleanup_resource_sync(resource)
            
            # Log session statistics
            duration = time.time() - session_data['created_at']
            print(f"📊 Session {session_id}: {duration:.1f}s duration, {session_data['command_count']} commands")
    
    async def _cleanup_resource(self, resource: dict):
        """Clean up a specific resource"""
        self._cleanup_resource_sync(resource)
    
    def _cleanup_resource_sync(self, resource: dict):
        """Clean up a specific resource (synchronous version)"""
        try:
            resource_type = resource['type']
            resource_id = resource['id']
            
            if resource_type == 'temp_file':
                # Remove temporary files
                import os
                if os.path.exists(resource_id):
                    os.remove(resource_id)
                    logger.debug(f"🗑️ Removed temp file: {resource_id}")
                    
            logger.debug(f"✅ Cleaned up {resource_type}: {resource_id}")
            
        except Exception as e:
            logger.error(f"❌ Failed to cleanup {resource['type']}:{resource['id']}: {e}")
    
    def get_session_info(self, session_id: str) -> Optional[dict]:
        """Get information about a session"""
        with self.lock:
            if session_id in self.sessions:
                session_data = self.sessions[session_id].copy()
                current_time = time.time()
                session_data['age_seconds'] = current_time - session_data['created_at']
                session_data['idle_seconds'] = current_time - session_data['last_activity']
                session_data['expires_in'] = self.timeout_seconds - session_data['idle_seconds']
                return session_data
        return None
    
    def get_all_sessions(self) -> dict:
        """Get information about all active sessions"""
        current_time = time.time()
        sessions_info = {}
        
        with self.lock:
            for session_id, session_data in self.sessions.items():
                info = session_data.copy()
                info['age_seconds'] = current_time - session_data['created_at']
                info['idle_seconds'] = current_time - session_data['last_activity']
                info['expires_in'] = self.timeout_seconds - info['idle_seconds']
                sessions_info[session_id] = info
        
        return sessions_info
    
    async def force_cleanup_session(self, session_id: str):
        """Manually force cleanup of a specific session"""
        await self.cleanup_session(session_id)
        return True
    
    def stop(self):
        """Stop the session manager and cleanup all sessions"""
        self.running = False
        if self.cleanup_task:
            self.cleanup_task.cancel()
        
        # Force cleanup all remaining sessions
        session_ids = list(self.sessions.keys())
        for session_id in session_ids:
            asyncio.create_task(self.cleanup_session(session_id))
        
        logger.info("🛑 Session manager stopped")

# Global session manager instance
session_manager = SessionManager(timeout_minutes=5)
