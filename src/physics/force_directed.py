"""
Force-directed graph layout algorithm.
"""
import math
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..models.graph import Graph


class ForceDirectedLayout:
    """
    Force-directed layout using Fruchterman-Reingold algorithm.
    
    Nodes repel each other (Coulomb's law) while edges attract
    connected nodes (Hooke's law / spring force).
    """
    
    def __init__(self):
        """Initialize the physics simulation."""
        # Force parameters
        self.repulsion = 15000.0  # Repulsion strength (Coulomb constant)
        self.attraction = 0.04    # Attraction strength (spring constant)
        self.damping = 0.85       # Velocity damping (0-1)
        self.min_distance = 80    # Minimum distance between nodes
        self.max_velocity = 50    # Maximum velocity cap
        
        # Simulation state
        self.is_running = True
        self.temperature = 1.0   # Simulated annealing temperature
        self.cooling_rate = 0.999
        
        # Reference to graph
        self.graph = None
    
    def step(self, graph: 'Graph') -> None:
        """
        Perform one simulation step.
        
        Args:
            graph: Graph to simulate
        """
        if not graph or not graph.nodes:
            return
        
        self.graph = graph
        nodes = list(graph.nodes.values())
        
        # Reset forces
        for node in nodes:
            node.vx = 0
            node.vy = 0
        
        # Calculate repulsion forces (all pairs)
        for i, node1 in enumerate(nodes):
            for node2 in nodes[i + 1:]:
                self._apply_repulsion(node1, node2)
        
        # Calculate attraction forces (connected nodes)
        for edge in graph.edges:
            self._apply_attraction(edge.source, edge.target)
        
        # Apply center gravity (weak force pulling to center)
        center_x = sum(n.x for n in nodes) / len(nodes)
        center_y = sum(n.y for n in nodes) / len(nodes)
        
        for node in nodes:
            dx = center_x - node.x
            dy = center_y - node.y
            dist = math.sqrt(dx * dx + dy * dy)
            if dist > 0:
                gravity = 0.1 * self.temperature
                node.vx += gravity * dx / dist
                node.vy += gravity * dy / dist
        
        # Update positions with damping
        for node in nodes:
            # Cap velocity
            speed = math.sqrt(node.vx ** 2 + node.vy ** 2)
            if speed > self.max_velocity:
                node.vx = (node.vx / speed) * self.max_velocity
                node.vy = (node.vy / speed) * self.max_velocity
            
            # Apply temperature
            node.vx *= self.temperature
            node.vy *= self.temperature
            
            # Update position
            node.x += node.vx * self.damping
            node.y += node.vy * self.damping
        
        # Cool down
        self.temperature = max(0.01, self.temperature * self.cooling_rate)
    
    def _apply_repulsion(self, node1, node2) -> None:
        """
        Apply repulsion force between two nodes (Coulomb's law).
        
        F = k / d^2
        """
        dx = node1.x - node2.x
        dy = node1.y - node2.y
        
        dist_sq = dx * dx + dy * dy
        dist = math.sqrt(dist_sq)
        
        if dist < self.min_distance:
            dist = self.min_distance
            dist_sq = dist * dist
        
        if dist > 0:
            # Repulsion force magnitude
            force = self.repulsion / dist_sq
            
            # Direction
            fx = force * dx / dist
            fy = force * dy / dist
            
            # Apply to both nodes (opposite directions)
            node1.vx += fx
            node1.vy += fy
            node2.vx -= fx
            node2.vy -= fy
    
    def _apply_attraction(self, node1, node2) -> None:
        """
        Apply attraction force between connected nodes (Hooke's law).
        
        F = k * d
        """
        dx = node2.x - node1.x
        dy = node2.y - node1.y
        
        dist = math.sqrt(dx * dx + dy * dy)
        
        if dist > 0:
            # Attraction force magnitude (spring)
            force = self.attraction * dist
            
            # Direction
            fx = force * dx / dist
            fy = force * dy / dist
            
            # Apply to both nodes (towards each other)
            node1.vx += fx
            node1.vy += fy
            node2.vx -= fx
            node2.vy -= fy
    
    def start(self) -> None:
        """Start the simulation."""
        self.is_running = True
        self.temperature = 1.0  # Reset temperature
    
    def stop(self) -> None:
        """Stop the simulation."""
        self.is_running = False
    
    def reset(self) -> None:
        """Reset simulation state."""
        self.temperature = 1.0
        if self.graph:
            for node in self.graph.nodes.values():
                node.reset_velocity()
    
    def reheat(self) -> None:
        """Increase temperature to allow more movement."""
        self.temperature = min(1.0, self.temperature + 0.3)
    
    def set_parameters(self, repulsion: float = None, attraction: float = None,
                       damping: float = None) -> None:
        """
        Update simulation parameters.
        
        Args:
            repulsion: Repulsion force strength
            attraction: Attraction force strength
            damping: Velocity damping factor
        """
        if repulsion is not None:
            self.repulsion = repulsion
        if attraction is not None:
            self.attraction = attraction
        if damping is not None:
            self.damping = damping

