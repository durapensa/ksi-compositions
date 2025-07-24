#!/usr/bin/env python3
"""
KSI Event Handler Migration Analyzer

This tool analyzes Python event handlers to identify migration candidates
and suggest appropriate transformer patterns.
"""

import os
import re
import ast
import json
from typing import Dict, List, Tuple, Optional, Set
from pathlib import Path
from dataclasses import dataclass
from enum import Enum


class HandlerPattern(Enum):
    """Types of handler patterns for migration."""
    SIMPLE_FORWARDER = "simple_forwarder"
    FIELD_MAPPER = "field_mapper"
    CONDITIONAL_ROUTER = "conditional_router"
    MULTI_TARGET = "multi_target"
    COMPLEX_LOGIC = "complex_logic"  # Not suitable for migration


@dataclass
class HandlerAnalysis:
    """Analysis result for a single event handler."""
    file_path: str
    function_name: str
    event_pattern: str
    line_start: int
    line_end: int
    pattern_type: HandlerPattern
    complexity_score: int
    emit_events: List[str]
    emit_count: int
    has_conditions: bool
    has_loops: bool
    has_external_calls: bool
    has_database_ops: bool
    migration_priority: str  # high, medium, low, not_suitable
    suggested_transformer: Optional[str]
    code_lines: int
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "file_path": self.file_path,
            "function_name": self.function_name,
            "event_pattern": self.event_pattern,
            "line_range": f"{self.line_start}-{self.line_end}",
            "pattern_type": self.pattern_type.value,
            "complexity_score": self.complexity_score,
            "emit_events": self.emit_events,
            "emit_count": self.emit_count,
            "characteristics": {
                "has_conditions": self.has_conditions,
                "has_loops": self.has_loops,
                "has_external_calls": self.has_external_calls,
                "has_database_ops": self.has_database_ops
            },
            "migration": {
                "priority": self.migration_priority,
                "suggested_transformer": self.suggested_transformer,
                "code_lines": self.code_lines
            }
        }


class HandlerAnalyzer:
    """Analyzes Python files to find and categorize event handlers."""
    
    def __init__(self, ksi_root: str):
        self.ksi_root = Path(ksi_root)
        self.handler_pattern = re.compile(r'@event_handler\s*\(\s*["\']([^"\']+)["\']\s*\)')
        self.emit_pattern = re.compile(r'emit_event\s*\(\s*["\']([^"\']+)["\']')
        
        # Patterns indicating complexity
        self.db_patterns = [
            'await.*execute', 'cursor.', 'connection.', 'session.',
            'commit()', 'rollback()', 'query(', 'select ', 'insert ',
            'update ', 'delete ', 'SQLAlchemy', 'sqlite3'
        ]
        
        self.external_patterns = [
            'requests.', 'httpx.', 'aiohttp.', 'urllib.',
            'subprocess.', 'os.system', 'os.popen'
        ]
        
        self.file_patterns = [
            'open(', 'with open', 'file.', 'Path(',
            'os.path.', 'shutil.', 'json.load', 'yaml.load'
        ]

    def analyze_ksi_handlers(self) -> Dict[str, List[HandlerAnalysis]]:
        """Analyze all Python files in KSI for event handlers."""
        results = {}
        
        # Find all Python files in ksi_daemon
        daemon_dir = self.ksi_root / "ksi_daemon"
        if not daemon_dir.exists():
            raise FileNotFoundError(f"KSI daemon directory not found: {daemon_dir}")
        
        python_files = list(daemon_dir.rglob("*.py"))
        
        for file_path in python_files:
            try:
                handlers = self.analyze_file(file_path)
                if handlers:
                    relative_path = str(file_path.relative_to(self.ksi_root))
                    results[relative_path] = handlers
            except Exception as e:
                print(f"Error analyzing {file_path}: {e}")
        
        return results

    def analyze_file(self, file_path: Path) -> List[HandlerAnalysis]:
        """Analyze a single Python file for event handlers."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (UnicodeDecodeError, PermissionError):
            return []
        
        # Find all @event_handler decorators
        handler_matches = []
        for match in self.handler_pattern.finditer(content):
            event_pattern = match.group(1)
            start_pos = match.start()
            
            # Find the function definition
            func_start = content.find('def ', start_pos)
            if func_start == -1:
                continue
                
            func_end = content.find('\n@', func_start)
            if func_end == -1:
                func_end = content.find('\ndef ', func_start + 4)
            if func_end == -1:
                func_end = len(content)
            
            handler_matches.append((event_pattern, func_start, func_end))
        
        # Analyze each handler
        handlers = []
        lines = content.split('\n')
        
        for event_pattern, func_start, func_end in handler_matches:
            handler_code = content[func_start:func_end]
            analysis = self.analyze_handler_code(
                file_path, event_pattern, handler_code, lines, func_start
            )
            if analysis:
                handlers.append(analysis)
        
        return handlers

    def analyze_handler_code(self, file_path: Path, event_pattern: str, 
                           code: str, all_lines: List[str], start_pos: int) -> Optional[HandlerAnalysis]:
        """Analyze a single handler's code."""
        
        # Extract function name
        func_match = re.search(r'def\s+(\w+)', code)
        if not func_match:
            return None
        func_name = func_match.group(1)
        
        # Calculate line numbers
        line_start = len(code[:start_pos].split('\n'))
        line_end = line_start + len(code.split('\n')) - 1
        code_lines = line_end - line_start
        
        # Find emit_event calls
        emit_events = self.emit_pattern.findall(code)
        emit_count = len(emit_events)
        
        # Analyze characteristics
        has_conditions = self._has_conditions(code)
        has_loops = self._has_loops(code)
        has_external_calls = self._has_external_calls(code)
        has_database_ops = self._has_database_ops(code)
        
        # Calculate complexity score
        complexity_score = self._calculate_complexity(
            code, emit_count, has_conditions, has_loops, 
            has_external_calls, has_database_ops
        )
        
        # Determine pattern type
        pattern_type = self._determine_pattern_type(
            emit_count, has_conditions, has_loops, 
            has_external_calls, has_database_ops, complexity_score
        )
        
        # Determine migration priority and suggested transformer
        priority, transformer = self._suggest_migration(
            pattern_type, complexity_score, emit_count
        )
        
        return HandlerAnalysis(
            file_path=str(file_path.relative_to(self.ksi_root.parent)),
            function_name=func_name,
            event_pattern=event_pattern,
            line_start=line_start,
            line_end=line_end,
            pattern_type=pattern_type,
            complexity_score=complexity_score,
            emit_events=emit_events,
            emit_count=emit_count,
            has_conditions=has_conditions,
            has_loops=has_loops,
            has_external_calls=has_external_calls,
            has_database_ops=has_database_ops,
            migration_priority=priority,
            suggested_transformer=transformer,
            code_lines=code_lines
        )

    def _has_conditions(self, code: str) -> bool:
        """Check if handler has conditional logic."""
        return bool(re.search(r'\bif\b|\belif\b|\belse\b', code))

    def _has_loops(self, code: str) -> bool:
        """Check if handler has loops."""
        return bool(re.search(r'\bfor\b|\bwhile\b', code))

    def _has_external_calls(self, code: str) -> bool:
        """Check if handler makes external calls."""
        return any(pattern in code for pattern in self.external_patterns)

    def _has_database_ops(self, code: str) -> bool:
        """Check if handler has database operations."""
        return any(pattern in code.lower() for pattern in self.db_patterns)

    def _calculate_complexity(self, code: str, emit_count: int, 
                            has_conditions: bool, has_loops: bool,
                            has_external_calls: bool, has_database_ops: bool) -> int:
        """Calculate complexity score (1-10)."""
        score = 1
        
        # Base complexity from emit count
        score += min(emit_count, 3)
        
        # Add for control structures
        if has_conditions:
            score += 2
        if has_loops:
            score += 3
        if has_external_calls:
            score += 4
        if has_database_ops:
            score += 4
        
        # Add for code length
        lines = len(code.split('\n'))
        if lines > 50:
            score += 2
        elif lines > 20:
            score += 1
        
        return min(score, 10)

    def _determine_pattern_type(self, emit_count: int, has_conditions: bool,
                               has_loops: bool, has_external_calls: bool,
                               has_database_ops: bool, complexity_score: int) -> HandlerPattern:
        """Determine the pattern type of the handler."""
        
        # Complex logic - not suitable for migration
        if has_external_calls or has_database_ops or has_loops or complexity_score >= 8:
            return HandlerPattern.COMPLEX_LOGIC
        
        # Simple forwarder - just emits events
        if emit_count <= 2 and not has_conditions and complexity_score <= 3:
            return HandlerPattern.SIMPLE_FORWARDER
        
        # Multi-target - emits to multiple events
        if emit_count >= 3 and not has_conditions:
            return HandlerPattern.MULTI_TARGET
        
        # Conditional router - has if/else logic
        if has_conditions and emit_count >= 1:
            return HandlerPattern.CONDITIONAL_ROUTER
        
        # Field mapper - transforms data
        if emit_count >= 1 and complexity_score <= 5:
            return HandlerPattern.FIELD_MAPPER
        
        return HandlerPattern.COMPLEX_LOGIC

    def _suggest_migration(self, pattern_type: HandlerPattern, 
                          complexity_score: int, emit_count: int) -> Tuple[str, Optional[str]]:
        """Suggest migration priority and transformer type."""
        
        if pattern_type == HandlerPattern.COMPLEX_LOGIC:
            return "not_suitable", None
        
        if pattern_type == HandlerPattern.SIMPLE_FORWARDER:
            return "high", "simple_forwarder.yaml"
        
        if pattern_type == HandlerPattern.MULTI_TARGET:
            return "high", "multi_target.yaml"
        
        if pattern_type == HandlerPattern.CONDITIONAL_ROUTER:
            if complexity_score <= 4:
                return "medium", "conditional_router.yaml"
            else:
                return "low", "conditional_router.yaml"
        
        if pattern_type == HandlerPattern.FIELD_MAPPER:
            if complexity_score <= 3:
                return "medium", "field_mapper.yaml"
            else:
                return "low", "field_mapper.yaml"
        
        return "not_suitable", None

    def generate_migration_report(self, analyses: Dict[str, List[HandlerAnalysis]]) -> Dict:
        """Generate a comprehensive migration report."""
        
        # Collect statistics
        total_handlers = sum(len(handlers) for handlers in analyses.values())
        pattern_counts = {}
        priority_counts = {}
        total_code_lines = 0
        
        all_handlers = []
        for handlers in analyses.values():
            all_handlers.extend(handlers)
        
        for handler in all_handlers:
            pattern_counts[handler.pattern_type.value] = pattern_counts.get(handler.pattern_type.value, 0) + 1
            priority_counts[handler.migration_priority] = priority_counts.get(handler.migration_priority, 0) + 1
            total_code_lines += handler.code_lines
        
        # Calculate migration potential
        suitable_handlers = sum(1 for h in all_handlers if h.migration_priority != "not_suitable")
        migration_percentage = (suitable_handlers / total_handlers * 100) if total_handlers > 0 else 0
        
        return {
            "summary": {
                "total_handlers": total_handlers,
                "total_files": len(analyses),
                "total_code_lines": total_code_lines,
                "suitable_for_migration": suitable_handlers,
                "migration_percentage": round(migration_percentage, 1)
            },
            "pattern_distribution": pattern_counts,
            "priority_distribution": priority_counts,
            "migration_phases": self._suggest_phases(all_handlers),
            "detailed_analysis": {
                file_path: [handler.to_dict() for handler in handlers]
                for file_path, handlers in analyses.items()
            }
        }

    def _suggest_phases(self, handlers: List[HandlerAnalysis]) -> Dict:
        """Suggest migration phases based on analysis."""
        
        phase1 = [h for h in handlers if h.migration_priority == "high" and 
                 h.pattern_type in [HandlerPattern.SIMPLE_FORWARDER, HandlerPattern.MULTI_TARGET]]
        
        phase2 = [h for h in handlers if h.migration_priority in ["high", "medium"] and
                 h.pattern_type == HandlerPattern.FIELD_MAPPER]
        
        phase3 = [h for h in handlers if h.migration_priority in ["medium", "low"] and
                 h.pattern_type == HandlerPattern.CONDITIONAL_ROUTER]
        
        return {
            "phase_1_easy_wins": {
                "count": len(phase1),
                "estimated_code_reduction": sum(h.code_lines for h in phase1),
                "handlers": [f"{h.file_path}:{h.function_name}" for h in phase1[:10]]  # Top 10
            },
            "phase_2_field_mapping": {
                "count": len(phase2),
                "estimated_code_reduction": sum(h.code_lines for h in phase2),
                "handlers": [f"{h.file_path}:{h.function_name}" for h in phase2[:10]]
            },
            "phase_3_conditional": {
                "count": len(phase3),
                "estimated_code_reduction": sum(h.code_lines for h in phase3),
                "handlers": [f"{h.file_path}:{h.function_name}" for h in phase3[:10]]
            }
        }


def main():
    """Main entry point for the handler analyzer."""
    import sys
    
    if len(sys.argv) < 2:
        ksi_root = os.getcwd()
    else:
        ksi_root = sys.argv[1]
    
    analyzer = HandlerAnalyzer(ksi_root)
    
    try:
        print("Analyzing KSI event handlers...")
        analyses = analyzer.analyze_ksi_handlers()
        
        print(f"Found {sum(len(h) for h in analyses.values())} handlers in {len(analyses)} files")
        
        # Generate report
        report = analyzer.generate_migration_report(analyses)
        
        # Write report to file
        report_path = Path(ksi_root) / "migration_analysis_report.json"
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Migration analysis report written to: {report_path}")
        
        # Print summary
        summary = report["summary"]
        print(f"\nSummary:")
        print(f"  Total handlers: {summary['total_handlers']}")
        print(f"  Suitable for migration: {summary['suitable_for_migration']} ({summary['migration_percentage']}%)")
        print(f"  Total code lines: {summary['total_code_lines']}")
        
        print(f"\nPattern distribution:")
        for pattern, count in report["pattern_distribution"].items():
            print(f"  {pattern}: {count}")
        
        print(f"\nMigration phases:")
        phases = report["migration_phases"]
        print(f"  Phase 1 (easy wins): {phases['phase_1_easy_wins']['count']} handlers")
        print(f"  Phase 2 (field mapping): {phases['phase_2_field_mapping']['count']} handlers")
        print(f"  Phase 3 (conditional): {phases['phase_3_conditional']['count']} handlers")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()