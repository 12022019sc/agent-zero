#!/usr/bin/env python3
"""Comprehensive audit logging for all system operations"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, List
from threading import Lock

class AuditLogger:
    """Thread-safe audit logger for tracking system operations"""

    def __init__(self, log_file: str = "/home/shayne/agent-zero/logs/audit.log"):
        self.log_file = log_file
        self.lock = Lock()
        self._ensure_log_directory()

    def _ensure_log_directory(self):
        """Ensure the log directory exists"""
        log_dir = os.path.dirname(self.log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

    def log_command(self, command: str, user: str = "default", status: str = "success", metadata: Optional[Dict] = None):
        """Log a command execution"""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "command": command,
            "user": user,
            "status": status,
            "metadata": metadata or {}
        }
        self._write_entry(entry)

    def log_error(self, error: str, context: Optional[Dict] = None):
        """Log an error event"""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": "error",
            "error": error,
            "context": context or {}
        }
        self._write_entry(entry)

    def log_security_event(self, event_type: str, details: Dict[str, Any]):
        """Log a security-related event"""
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": "security",
            "event_type": event_type,
            "details": details
        }
        self._write_entry(entry)

    def _write_entry(self, entry: Dict[str, Any]):
        """Thread-safe write to log file"""
        with self.lock:
            try:
                with open(self.log_file, 'a') as f:
                    f.write(json.dumps(entry) + '\n')
            except Exception as e:
                print(f"Failed to write audit log: {e}")

    def get_recent_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Retrieve recent log entries"""
        if not os.path.exists(self.log_file):
            return []

        logs = []
        try:
            with open(self.log_file, 'r') as f:
                for line in f:
                    try:
                        logs.append(json.loads(line.strip()))
                    except json.JSONDecodeError:
                        continue
        except Exception as e:
            print(f"Failed to read audit log: {e}")

        return logs[-limit:]

    def clear_logs(self):
        """Clear the audit log"""
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

if __name__ == "__main__":
    logger = AuditLogger("/tmp/test_audit.log")
    logger.log_command("test_command", user="test_user", status="success")
    logger.log_security_event("login_attempt", {"ip": "127.0.0.1", "success": True})
    print("Audit log test complete")
    print("Recent logs:", logger.get_recent_logs())
