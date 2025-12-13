"""
Edge class representing a connection between two nodes in the social network graph.
"""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, TYPE_CHECKING

if TYPE_CHECKING:
    from .node import Node


@dataclass
class Edge:
    """
    Represents an undirected, weighted edge (connection) between two nodes.
    
    Attributes:
        source: Source node
        target: Target node  
        weight: Edge weight (calculated based on node properties)
        is_highlighted: Whether the edge is highlighted in visualization
        highlight_color: Color for highlighting
    """
    source: 'Node'
    target: 'Node'
    weight: float = 0.0
    is_highlighted: bool = False
    highlight_color: Optional[tuple] = None
    
    def __post_init__(self):
        """Calculate weight after initialization if not set."""
        if self.weight == 0.0:
            self.weight = self.calculate_weight()
    
    def calculate_weight(self) -> float:
        """
        Calculate edge weight using the project formula:
        
        Weight(i,j) = 1 / (1 + sqrt((Activity_i - Activity_j)^2 + 
                                     (Interaction_i - Interaction_j)^2 + 
                                     (Connection_i - Connection_j)^2))
        
        Returns:
            Calculated weight value (higher = more similar nodes)
        """
        activity_diff = self.source.activity - self.target.activity
        interaction_diff = self.source.interaction - self.target.interaction
        connection_diff = self.source.connection_count - self.target.connection_count
        
        euclidean_distance = (
            activity_diff ** 2 + 
            interaction_diff ** 2 + 
            connection_diff ** 2
        ) ** 0.5
        
        # Weight formula: similar nodes have higher weight
        weight = 1.0 / (1.0 + euclidean_distance)
        return weight
    
    def recalculate_weight(self) -> None:
        """Recalculate and update the edge weight."""
        self.weight = self.calculate_weight()
    
    def get_cost(self) -> float:
        """
        Get edge cost for pathfinding algorithms.
        Lower weight (dissimilar nodes) = higher cost
        
        Returns:
            Cost value (inverse of weight for pathfinding)
        """
        # For shortest path, we want dissimilar nodes to have higher cost
        # So cost = 1/weight or we can use (1 - weight) scaled
        return 1.0 / self.weight if self.weight > 0 else float('inf')
    
    def get_other_node(self, node: 'Node') -> Optional['Node']:
        """
        Get the other node in this edge given one node.
        
        Args:
            node: One of the nodes in this edge
            
        Returns:
            The other node, or None if given node is not in this edge
        """
        if node.id == self.source.id:
            return self.target
        elif node.id == self.target.id:
            return self.source
        return None
    
    def contains_node(self, node_id: int) -> bool:
        """
        Check if this edge contains a node with the given id.
        
        Args:
            node_id: Node ID to check
            
        Returns:
            True if the node is part of this edge
        """
        return self.source.id == node_id or self.target.id == node_id
    
    def set_highlight(self, highlighted: bool, color: Optional[tuple] = None) -> None:
        """
        Set highlight state and optional highlight color.
        
        Args:
            highlighted: Whether to highlight the edge
            color: Optional RGB color tuple for highlight
        """
        self.is_highlighted = highlighted
        self.highlight_color = color if highlighted else None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize edge to dictionary for JSON export.
        
        Returns:
            Dictionary representation of the edge
        """
        return {
            'source_id': self.source.id,
            'target_id': self.target.id,
            'weight': self.weight
        }
    
    def __hash__(self):
        """Make Edge hashable by source and target ids (undirected)."""
        return hash(frozenset([self.source.id, self.target.id]))
    
    def __eq__(self, other):
        """Compare edges (undirected comparison)."""
        if isinstance(other, Edge):
            return (
                (self.source.id == other.source.id and self.target.id == other.target.id) or
                (self.source.id == other.target.id and self.target.id == other.source.id)
            )
        return False
    
    def __repr__(self):
        return f"Edge({self.source.id} <-> {self.target.id}, weight={self.weight:.3f})"


