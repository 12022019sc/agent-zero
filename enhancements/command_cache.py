
#!/usr/bin/env python3
"""In-memory cache for command definitions"""

import json
import time
import threading
from typing import Dict, Optional, Any
from pathlib import Path

class CommandCache:
    """Thread-safe in-memory cache for command definitions"""

    def __init__(self, cache_ttl: int = 300):  # 5 minutes TTL
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.timestamps: Dict[str, float] = {}
        self.lock = threading.Lock()
        self.cache_ttl = cache_ttl
        self.commands_dir = Path("/home/shayne/agent-zero/commands")

    def get(self, command_name: str) -> Optional[Dict[str, Any]]:
        """Get command from cache, load from disk if not cached or expired"""
        with self.lock:
            # Check if cache is valid
            if (command_name in self.cache and 
                command_name in self.timestamps and
                time.time() - self.timestamps[command_name] < self.cache_ttl):
                return self.cache[command_name].copy()

        # Load from disk
        return self._load_from_disk(command_name)

    def _load_from_disk(self, command_name: str) -> Optional[Dict[str, Any]]:
        """Load command definition from disk"""
        command_file = self.commands_dir / f"{command_name}.json"

        if not command_file.exists():
            return None

        try:
            with open(command_file, 'r') as f:
                cmd_def = json.load(f)

            # Update cache
            with self.lock:
                self.cache[command_name] = cmd_def
                self.timestamps[command_name] = time.time()

            return cmd_def.copy()
        except Exception as e:
            return None

    def refresh(self, command_name: str = None):
        """Refresh cache for specific command or all commands"""
        if command_name:
            with self.lock:
                if command_name in self.timestamps:
                    del self.timestamps[command_name]
                if command_name in self.cache:
                    del self.cache[command_name]
        else:
            with self.lock:
                self.cache.clear()
                self.timestamps.clear()

    def preload(self):
        """Preload all commands into cache"""
        if not self.commands_dir.exists():
            return

        for command_file in self.commands_dir.glob("*.json"):
            command_name = command_file.stem
            self.get(command_name)

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        with self.lock:
            return {
                "cached_commands": len(self.cache),
                "cache_ttl": self.cache_ttl,
                "commands": list(self.cache.keys())
            }
