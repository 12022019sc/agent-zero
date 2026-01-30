#!/usr/bin/env python3
"""Enhanced command executor with security, performance, and monitoring"""

import os
import json
import time
import re
from datetime import datetime
from typing import Dict, Any, Optional, Tuple

# Import enhancement modules
import sys
sys.path.insert(0, os.path.dirname(__file__))

from error_sanitizer import ErrorSanitizer
from rate_limiter import CommandRateLimiter
from audit_logger import AuditLogger
from command_cache import CommandCache
from metrics_collector import MetricsCollector
from alert_system import AlertSystem

class EnhancedCommandExecutor:
    """Enhanced command executor with all security, performance, and monitoring features"""

    def __init__(self, commands_dir: str = "/home/shayne/agent-zero/commands"):
        self.commands_dir = commands_dir

        # Initialize enhancement components
        self.error_sanitizer = ErrorSanitizer()
        self.rate_limiter = CommandRateLimiter()
        self.audit_logger = AuditLogger()
        self.command_cache = CommandCache()
        self.metrics = MetricsCollector()
        self.alert_system = AlertSystem()

        # Preload cache
        self.command_cache.preload()

        # Set up alert handler
        self.alert_system.add_handler(self._handle_alert)

        print(f"Enhanced Command Executor initialized")
        print(f"Security: Error sanitization, Rate limiting, Audit logging")
        print(f"Performance: Command caching, Metrics collection")
        print(f"Monitoring: Pattern analysis, Alert system")

    def _handle_alert(self, alert: Dict[str, Any]):
        """Handle alerts from the monitoring system"""
        # Log alert to audit logger
        self.audit_logger.log_command(
            command="alert",
            user="system",
            status="triggered",
            metadata=alert
        )

    def execute_command(self, command_name: str, user: str = "default", context: Optional[Dict] = None) -> Tuple[bool, str]:
        """Execute a command with full enhancement pipeline"""
        start_time = time.time()
        specialist = "default"
        
        try:
            # Check rate limit
            allowed, reason = self.rate_limiter.is_command_allowed(command_name, user)
            if not allowed:
                error_msg = self.error_sanitizer.sanitize_error(
                    f"Rate limit exceeded for command: {command_name}. Reason: {reason}"
                )
                self.metrics.record_command_end(command_name, user, False, error_msg)
                return False, error_msg
            
            # Check cache first (Note: current cache implementation only supports command_name)
            # Context-aware caching would require extending CommandCache
            cached_result = self.command_cache.get(command_name)
            if cached_result is not None:
                self.metrics.record_command_end(command_name, user, True)
                return True, json.dumps(cached_result)
            
            # Load command definition
            cmd_file = os.path.join(self.commands_dir, f"{command_name}.json")
            if not os.path.exists(cmd_file):
                error_msg = self.error_sanitizer.sanitize_error(
                    f"Command definition not found: {command_name}"
                )
                self.metrics.record_command_end(command_name, user, False, error_msg)
                return False, error_msg
            
            with open(cmd_file, 'r') as f:
                cmd_def = json.load(f)
            
            # Record command start
            specialist = cmd_def.get("specialist_role", "default")
            self.metrics.record_command_start(command_name, user, specialist)

            # Simulate command execution
            # In a real implementation, this would delegate to the specialist agent
            workflow = cmd_def.get("workflow", [])

            result = f"Command executed by {specialist} specialist.\n"
            result += f"Workflow steps:\n"
            for i, step in enumerate(workflow, 1):
                result += f"{i}. {step}\n"
            
            # Note: Caching result is skipped as CommandCache doesn't support setting arbitrary results
            # The cache only preloads command definitions from disk
            
            # Record metrics
            execution_time = time.time() - start_time
            self.metrics.record_command_end(command_name, user, True)
            
            # Log to audit
            self.audit_logger.log_command(
                command=command_name,
                user=user,
                status="success",
                metadata={
                    "execution_time": execution_time,
                    "specialist": specialist,
                    "context": context
                }
            )
            
            return True, result
            
        except Exception as e:
            error_msg = self.error_sanitizer.sanitize_error(str(e))
            self.metrics.record_command_end(command_name, user, False, error_msg)
            self.audit_logger.log_command(
                command=command_name,
                user=user,
                status="error",
                metadata={"error": error_msg}
            )
            return False, error_msg

    def get_statistics(self) -> Dict[str, Any]:
        """Get system statistics"""
        return {
            "metrics": self.metrics.get_metrics(),
            "cache_stats": self.command_cache.get_stats()
        }

if __name__ == "__main__":
    executor = EnhancedCommandExecutor()
    success, result = executor.execute_command("security_audit")
    print(f"Success: {success}")
    print(f"Result: {result}")
