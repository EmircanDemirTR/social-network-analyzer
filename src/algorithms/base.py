"""
Base classes and interfaces for graph algorithms.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, TYPE_CHECKING
import time

if TYPE_CHECKING:
    from ..models.graph import Graph


@dataclass
class AlgorithmResult:
    """
    Container for algorithm execution results.
    
    Attributes:
        name: Algorithm name
        success: Whether execution was successful
        execution_time: Time taken in seconds
        data: Result data (varies by algorithm)
        steps: List of intermediate steps for animation
        message: Optional status message
    """
    name: str
    success: bool = True
    execution_time: float = 0.0
    data: Any = None
    steps: List[Dict[str, Any]] = field(default_factory=list)
    message: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary for display."""
        return {
            'algorithm': self.name,
            'success': self.success,
            'execution_time_ms': round(self.execution_time * 1000, 3),
            'message': self.message,
            'data': self.data
        }


class Algorithm(ABC):
    """
    Abstract base class for all graph algorithms.
    
    All algorithm implementations should inherit from this class
    and implement the execute method.
    """
    
    def __init__(self, graph: 'Graph'):
        """
        Initialize algorithm with a graph.
        
        Args:
            graph: Graph object to run algorithm on
        """
        self.graph = graph
        self._steps: List[Dict[str, Any]] = []
        self._start_time: float = 0.0
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Return the algorithm name."""
        pass
    
    @property
    def description(self) -> str:
        """Return algorithm description."""
        return ""
    
    @abstractmethod
    def execute(self, **kwargs) -> AlgorithmResult:
        """
        Execute the algorithm.
        
        Args:
            **kwargs: Algorithm-specific parameters
            
        Returns:
            AlgorithmResult containing execution results
        """
        pass
    
    def _start_timer(self) -> None:
        """Start the execution timer."""
        self._start_time = time.perf_counter()
    
    def _get_elapsed_time(self) -> float:
        """Get elapsed time since timer started."""
        return time.perf_counter() - self._start_time
    
    def _add_step(self, step_type: str, **kwargs) -> None:
        """
        Add an animation step.
        
        Args:
            step_type: Type of step (visit, highlight, etc.)
            **kwargs: Step-specific data
        """
        self._steps.append({
            'type': step_type,
            'time': self._get_elapsed_time(),
            **kwargs
        })
    
    def _clear_steps(self) -> None:
        """Clear all recorded steps."""
        self._steps.clear()
    
    def get_steps(self) -> List[Dict[str, Any]]:
        """Get recorded animation steps."""
        return self._steps.copy()
    
    def _create_result(self, success: bool = True, data: Any = None, 
                       message: str = "") -> AlgorithmResult:
        """
        Create an AlgorithmResult with timing information.
        
        Args:
            success: Whether algorithm succeeded
            data: Result data
            message: Status message
            
        Returns:
            AlgorithmResult instance
        """
        return AlgorithmResult(
            name=self.name,
            success=success,
            execution_time=self._get_elapsed_time(),
            data=data,
            steps=self._steps.copy(),
            message=message
        )




