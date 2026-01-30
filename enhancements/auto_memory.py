#!/usr/bin/env python3
"""
Auto Memory Enhancement

Automatically saves important information to the knowledge graph
after significant interactions.

This enhancement addresses the critical issue where Agent Zero
retrieves information from memory but doesn't automatically save
new information back to the knowledge graph.
"""

import sys
import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any

# Add instruments to path
sys.path.append('/home/shayne/agent-zero/instruments')
from memory_interface import remember, recall, connect, learn


class AutoMemory:
    """Automatic memory management for Agent Zero."""

    def __init__(self):
        self.logger = self._setup_logger()
        self.memory_interface = None
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logger for auto memory."""
        logger = logging.getLogger('AutoMemory')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler(sys.stderr)
            formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def analyze_and_save(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze conversation context and automatically save important information.
        
        Args:
            context: Dictionary containing conversation context with keys:
                - user_message: The user's message
                - ai_response: The AI's response
                - tools_used: List of tools used
                - task_completed: Whether a task was completed
                - new_discoveries: List of new discoveries
                - decisions_made: List of decisions made
        
        Returns:
            Dictionary with save results
        """
        results = {
            'saved_facts': [],
            'saved_insights': [],
            'saved_connections': [],
            'total_saved': 0
        }
        
        try:
            # Extract information from context
            user_message = context.get('user_message', '')
            ai_response = context.get('ai_response', '')
            tools_used = context.get('tools_used', [])
            task_completed = context.get('task_completed', False)
            new_discoveries = context.get('new_discoveries', [])
            decisions_made = context.get('decisions_made', [])
            
            # Save user questions/requests (indicates interests)
            if user_message and self._is_question(user_message):
                fact = f"User asked about: {user_message[:200]}"
                self._safe_remember(fact, "User Interests")
                results['saved_facts'].append(fact)
            
            # Save new discoveries
            for discovery in new_discoveries:
                if discovery:
                    self._safe_remember(discovery, "Discoveries")
                    results['saved_facts'].append(discovery[:100])
            
            # Save decisions made
            for decision in decisions_made:
                if decision:
                    insight = f"Decision: {decision}"
                    outcome = "Decision made to solve a problem or implement a feature"
                    self._safe_learn(insight, outcome, "Decisions")
                    results['saved_insights'].append(decision[:100])
            
            # Save task completions
            if task_completed:
                task_summary = self._extract_task_summary(context)
                if task_summary:
                    self._safe_remember(task_summary, "Completed Tasks")
                    results['saved_facts'].append(task_summary[:100])
            
            # Save tool usage patterns
            if tools_used:
                tools_info = f"Tools used in conversation: {', '.join(tools_used)}"
                self._safe_remember(tools_info, "Tool Usage")
                results['saved_facts'].append(tools_info)
            
            # Extract and save key information from AI response
            if ai_response:
                key_info = self._extract_key_information(ai_response)
                for info in key_info:
                    self._safe_remember(info, "Knowledge Base")
                    results['saved_facts'].append(info[:100])
            
            results['total_saved'] = (
                len(results['saved_facts']) + 
                len(results['saved_insights']) + 
                len(results['saved_connections'])
            )
            
            self.logger.info(f"AutoMemory saved {results['total_saved']} items to knowledge graph")
            
        except Exception as e:
            self.logger.error(f"Error in auto_memory: {e}")
        
        return results
    
    def _safe_remember(self, text: str, area: str = "main") -> bool:
        """Safely remember information with error handling."""
        try:
            remember(text, area)
            return True
        except Exception as e:
            self.logger.warning(f"Failed to remember: {e}")
            return False
    
    def _safe_learn(self, experience: str, outcome: str, area: str = "main") -> bool:
        """Safely learn with error handling."""
        try:
            learn(experience, outcome)
            return True
        except Exception as e:
            self.logger.warning(f"Failed to learn: {e}")
            return False
    
    def _safe_connect(self, concept_a: str, concept_b: str, relationship: str) -> bool:
        """Safely connect concepts with error handling."""
        try:
            connect(concept_a, concept_b, relationship)
            return True
        except Exception as e:
            self.logger.warning(f"Failed to connect: {e}")
            return False
    
    def _is_question(self, text: str) -> bool:
        """Check if text is a question."""
        question_indicators = ['?', 'what', 'how', 'why', 'when', 'where', 'who', 'can you', 'could you']
        text_lower = text.lower()
        return any(indicator in text_lower for indicator in question_indicators)
    
    def _extract_task_summary(self, context: Dict[str, Any]) -> Optional[str]:
        """Extract task summary from context."""
        user_message = context.get('user_message', '')
        ai_response = context.get('ai_response', '')
        
        # Look for task completion indicators
        completion_indicators = ['completed', 'finished', 'done', 'success', 'created', 'deleted', 'updated']
        
        summary_parts = []
        if user_message:
            summary_parts.append(f"Task: {user_message[:150]}")
        
        if ai_response:
            # Extract first meaningful sentence from response
            sentences = ai_response.split('.')
            if sentences:
                summary_parts.append(f"Result: {sentences[0][:200]}")
        
        return ' | '.join(summary_parts) if summary_parts else None
    
    def _extract_key_information(self, text: str) -> List[str]:
        """Extract key information from text."""
        key_info = []
        
        # Look for patterns that indicate important information
        patterns = [
            r'(?:The|This|A) (?:command|tool|feature|system|module) (?:is|provides|supports)\s+[^.]+\.',
            r'(?:Located|Found|Stored) (?:at|in)\s+[^.]+\.',
            r'(?:To|For) (?:use|install|configure|run)\s+[^.]+\.',
            r'Important\s*:?+[^.]+\.',
        ]
        
        import re
        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            key_info.extend(matches[:2])  # Limit to 2 matches per pattern
        
        return key_info[:5]  # Limit total key information
    
    def save_conversation_summary(self, user_message: str, ai_response: str, 
                                   topic: str = "conversation") -> bool:
        """Save a summary of the conversation.
        
        Args:
            user_message: The user's message
            ai_response: The AI's response
            topic: Topic area for categorization
        
        Returns:
            True if saved successfully
        """
        try:
            summary = f"Conversation about {topic}: User asked '{user_message[:100]}...'. Agent provided assistance."
            self._safe_remember(summary, "Conversations")
            return True
        except Exception as e:
            self.logger.error(f"Failed to save conversation summary: {e}")
            return False


# Convenience functions for quick usage
def save_after_conversation(user_message: str, ai_response: str, 
                           tools_used: List[str] = None,
                           task_completed: bool = False) -> Dict[str, Any]:
    """Quick function to save memory after a conversation.
    
    Args:
        user_message: The user's message
        ai_response: The AI's response
        tools_used: List of tools used
        task_completed: Whether a task was completed
    
    Returns:
        Dictionary with save results
    """
    auto_memory = AutoMemory()
    context = {
        'user_message': user_message,
        'ai_response': ai_response,
        'tools_used': tools_used or [],
        'task_completed': task_completed,
        'new_discoveries': [],
        'decisions_made': []
    }
    return auto_memory.analyze_and_save(context)


if __name__ == '__main__':
    # Test the auto memory system
    print("Testing AutoMemory enhancement...")
    
    test_context = {
        'user_message': 'What do you know about the debug command?',
        'ai_response': 'The debug.py command is part of Agent Zero Core Commands. It helps debug code issues systematically.',
        'tools_used': ['memory_load', 'response'],
        'task_completed': True,
        'new_discoveries': [
            'debug.py is located at /home/shayne/agent-zero/instruments/commands/debug.py',
            'debug.py supports --analyze-failures, --logs, --pattern, and --interactive options'
        ],
        'decisions_made': [
            'Used memory_load to retrieve debug command information'
        ]
    }
    
    auto_memory = AutoMemory()
    results = auto_memory.analyze_and_save(test_context)
    
    print(f"\nResults:")
    print(f"  Saved facts: {len(results['saved_facts'])}")
    print(f"  Saved insights: {len(results['saved_insights'])}")
    print(f"  Saved connections: {len(results['saved_connections'])}")
    print(f"  Total saved: {results['total_saved']}")
    print("\n✅ AutoMemory test completed")
