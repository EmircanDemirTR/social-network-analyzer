"""
Node class representing a user/vertex in the social network graph.
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
import random


@dataclass
class Node:
    """
    Represents a node (user) in the social network graph.
    
    Attributes:
        id: Unique identifier for the node
        name: Display name of the node/user
        x, y: Position coordinates for visualization
        vx, vy: Velocity components for physics simulation
        activity: Activity level (0.0 - 1.0)
        interaction: Interaction count
        connection_count: Number of connections
        color: RGB color tuple for visualization
        is_selected: Whether the node is currently selected
        is_highlighted: Whether the node is highlighted (e.g., in algorithm visualization)
    """
    id: int
    name: str = ""
    x: float = field(default_factory=lambda: random.uniform(100, 700))
    y: float = field(default_factory=lambda: random.uniform(100, 500))
    vx: float = 0.0
    vy: float = 0.0
    activity: float = field(default_factory=lambda: random.uniform(0.1, 1.0))
    interaction: float = field(default_factory=lambda: random.uniform(1, 20))
    connection_count: int = 0
    color: tuple = (0, 217, 255)  # Neon blue default
    is_selected: bool = False
    is_highlighted: bool = False
    highlight_color: Optional[tuple] = None
    
    def __post_init__(self):
        """Initialize default name if not provided."""
        if not self.name:
            self.name = f"User_{self.id}"
    
    def get_properties(self) -> Dict[str, Any]:
        """
        Get node properties as a dictionary.
        
        Returns:
            Dictionary containing all node properties
        """
        return {
            'id': self.id,
            'name': self.name,
            'x': self.x,
            'y': self.y,
            'activity': round(self.activity, 2),
            'interaction': round(self.interaction, 2),
            'connection_count': self.connection_count,
            'color': self.color
        }
    
    def update_position(self, dx: float, dy: float) -> None:
        """
        Update node position by delta values.
        
        Args:
            dx: Change in x coordinate
            dy: Change in y coordinate
        """
        self.x += dx
        self.y += dy
    
    def set_position(self, x: float, y: float) -> None:
        """
        Set node position to specific coordinates.
        
        Args:
            x: New x coordinate
            y: New y coordinate
        """
        self.x = x
        self.y = y
    
    def apply_force(self, fx: float, fy: float) -> None:
        """
        Apply force to the node (updates velocity).
        
        Args:
            fx: Force in x direction
            fy: Force in y direction
        """
        self.vx += fx
        self.vy += fy
    
    def update_physics(self, damping: float = 0.85) -> None:
        """
        Update position based on velocity and apply damping.
        
        Args:
            damping: Velocity damping factor (0-1)
        """
        self.x += self.vx
        self.y += self.vy
        self.vx *= damping
        self.vy *= damping
    
    def reset_velocity(self) -> None:
        """Reset velocity to zero."""
        self.vx = 0.0
        self.vy = 0.0
    
    def distance_to(self, other: 'Node') -> float:
        """
        Calculate Euclidean distance to another node.
        
        Args:
            other: Another Node instance
            
        Returns:
            Euclidean distance between the nodes
        """
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
    
    def set_highlight(self, highlighted: bool, color: Optional[tuple] = None) -> None:
        """
        Set highlight state and optional highlight color.
        
        Args:
            highlighted: Whether to highlight the node
            color: Optional RGB color tuple for highlight
        """
        self.is_highlighted = highlighted
        self.highlight_color = color if highlighted else None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize node to dictionary for JSON export.
        
        Returns:
            Dictionary representation of the node
        """
        return {
            'id': self.id,
            'name': self.name,
            'x': self.x,
            'y': self.y,
            'activity': self.activity,
            'interaction': self.interaction,
            'connection_count': self.connection_count
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Node':
        """
        Create Node from dictionary.
        
        Args:
            data: Dictionary containing node data
            
        Returns:
            New Node instance
        """
        return cls(
            id=data['id'],
            name=data.get('name', ''),
            x=data.get('x', random.uniform(100, 700)),
            y=data.get('y', random.uniform(100, 500)),
            activity=data.get('activity', random.uniform(0.1, 1.0)),
            interaction=data.get('interaction', random.uniform(1, 20)),
            connection_count=data.get('connection_count', 0)
        )
    
    def __hash__(self):
        """Make Node hashable by its id."""
        return hash(self.id)
    
    def __eq__(self, other):
        """Compare nodes by id."""
        if isinstance(other, Node):
            return self.id == other.id
        return False
    
    def __repr__(self):
        return f"Node(id={self.id}, name='{self.name}')"


