"""
Weight Calculator for dynamic edge weight computation.
"""
import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models.node import Node


class WeightCalculator:
    """
    Calculates edge weights based on node properties using the project formula.
    
    Formula:
    Weight(i,j) = 1 / (1 + sqrt((Activity_i - Activity_j)^2 + 
                                 (Interaction_i - Interaction_j)^2 + 
                                 (Connection_i - Connection_j)^2))
    """
    
    @staticmethod
    def calculate_weight(node1: 'Node', node2: 'Node') -> float:
        """
        Calculate the weight between two nodes.
        
        Higher weight = more similar nodes (shorter distance)
        Lower weight = less similar nodes (longer distance)
        
        Args:
            node1: First node
            node2: Second node
            
        Returns:
            Calculated weight (0 to 1)
        """
        activity_diff = node1.activity - node2.activity
        interaction_diff = node1.interaction - node2.interaction
        connection_diff = node1.connection_count - node2.connection_count
        
        # Euclidean distance in property space
        euclidean_distance = math.sqrt(
            activity_diff ** 2 + 
            interaction_diff ** 2 + 
            connection_diff ** 2
        )
        
        # Weight formula from project specification
        weight = 1.0 / (1.0 + euclidean_distance)
        
        return weight
    
    @staticmethod
    def calculate_cost(node1: 'Node', node2: 'Node') -> float:
        """
        Calculate the cost (inverse of weight) for pathfinding.
        
        Used in Dijkstra and A* algorithms where we want to find
        paths through similar nodes.
        
        Args:
            node1: First node
            node2: Second node
            
        Returns:
            Cost value (higher for dissimilar nodes)
        """
        weight = WeightCalculator.calculate_weight(node1, node2)
        if weight <= 0:
            return float('inf')
        return 1.0 / weight
    
    @staticmethod
    def calculate_similarity_score(node1: 'Node', node2: 'Node') -> float:
        """
        Calculate a normalized similarity score (0 to 100).
        
        Args:
            node1: First node
            node2: Second node
            
        Returns:
            Similarity percentage
        """
        weight = WeightCalculator.calculate_weight(node1, node2)
        return weight * 100
    
    @staticmethod
    def get_property_differences(node1: 'Node', node2: 'Node') -> dict:
        """
        Get detailed property differences between two nodes.
        
        Args:
            node1: First node
            node2: Second node
            
        Returns:
            Dictionary with individual property differences
        """
        return {
            'activity_diff': abs(node1.activity - node2.activity),
            'interaction_diff': abs(node1.interaction - node2.interaction),
            'connection_diff': abs(node1.connection_count - node2.connection_count),
            'total_distance': math.sqrt(
                (node1.activity - node2.activity) ** 2 +
                (node1.interaction - node2.interaction) ** 2 +
                (node1.connection_count - node2.connection_count) ** 2
            )
        }


