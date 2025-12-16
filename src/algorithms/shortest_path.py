"""
Shortest path algorithms: Dijkstra and A*.
"""
import heapq
import math
from typing import Dict, List, Optional, Tuple, Set
from .base import Algorithm, AlgorithmResult


class Dijkstra(Algorithm):
    """
    Dijkstra's shortest path algorithm.
    
    Finds the shortest path between two nodes using edge weights (costs).
    """
    
    @property
    def name(self) -> str:
        return "Dijkstra En Kısa Yol"
    
    @property
    def description(self) -> str:
        return "İki düğüm arasındaki en kısa (minimum maliyetli) yolu bulur."
    
    def execute(self, start_node_id: int, end_node_id: int, **kwargs) -> AlgorithmResult:
        """
        Execute Dijkstra's algorithm to find shortest path.
        
        Args:
            start_node_id: ID of the starting node
            end_node_id: ID of the target node
            
        Returns:
            AlgorithmResult with path and distances
        """
        self._clear_steps()
        self._start_timer()
        
        if start_node_id not in self.graph.nodes:
            return self._create_result(
                success=False,
                message=f"Başlangıç düğümü {start_node_id} bulunamadı"
            )
        
        if end_node_id not in self.graph.nodes:
            return self._create_result(
                success=False,
                message=f"Hedef düğümü {end_node_id} bulunamadı"
            )
        
        # Initialize distances
        distances: Dict[int, float] = {nid: float('inf') for nid in self.graph.nodes}
        distances[start_node_id] = 0
        
        # Previous node for path reconstruction
        previous: Dict[int, Optional[int]] = {nid: None for nid in self.graph.nodes}
        
        # Priority queue: (distance, node_id)
        pq: List[Tuple[float, int]] = [(0, start_node_id)]
        visited: Set[int] = set()
        
        while pq:
            current_dist, current_id = heapq.heappop(pq)
            
            if current_id in visited:
                continue
            
            visited.add(current_id)
            
            self._add_step(
                'visit',
                node_id=current_id,
                distance=current_dist,
                visited=list(visited)
            )
            
            # Found target
            if current_id == end_node_id:
                break
            
            # Explore neighbors
            for neighbor_id in self.graph.get_neighbor_ids(current_id):
                if neighbor_id in visited:
                    continue
                
                edge = self.graph.get_edge(current_id, neighbor_id)
                if edge is None:
                    continue
                
                # Cost is inverse of weight (dissimilar = higher cost)
                cost = edge.get_cost()
                new_dist = current_dist + cost
                
                if new_dist < distances[neighbor_id]:
                    distances[neighbor_id] = new_dist
                    previous[neighbor_id] = current_id
                    heapq.heappush(pq, (new_dist, neighbor_id))
                    
                    self._add_step(
                        'update',
                        node_id=neighbor_id,
                        new_distance=new_dist,
                        from_node=current_id
                    )
        
        # Reconstruct path
        path = []
        current = end_node_id
        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()
        
        # Check if path exists
        if distances[end_node_id] == float('inf'):
            return self._create_result(
                success=False,
                data={'distances': distances},
                message=f"{start_node_id} ve {end_node_id} arasında yol yok"
            )
        
        # Get path edges for highlighting
        path_edges = []
        for i in range(len(path) - 1):
            path_edges.append((path[i], path[i + 1]))
        
        result_data = {
            'path': path,
            'path_edges': path_edges,
            'total_cost': distances[end_node_id],
            'distances': {k: v for k, v in distances.items() if v != float('inf')},
            'start_node': start_node_id,
            'end_node': end_node_id
        }
        
        return self._create_result(
            success=True,
            data=result_data,
            message=f"Yol bulundu: {len(path)} düğüm, maliyet: {distances[end_node_id]:.3f}"
        )


class AStar(Algorithm):
    """
    A* shortest path algorithm.
    
    Uses heuristic (Euclidean distance) to guide search towards goal.
    """
    
    @property
    def name(self) -> str:
        return "A* En Kısa Yol"
    
    @property
    def description(self) -> str:
        return "Sezgisel fonksiyon kullanarak en kısa yolu daha hızlı bulur."
    
    def _heuristic(self, node_id: int, goal_id: int) -> float:
        """
        Calculate heuristic (Euclidean distance between node positions).
        
        Args:
            node_id: Current node ID
            goal_id: Goal node ID
            
        Returns:
            Estimated distance to goal
        """
        node = self.graph.nodes.get(node_id)
        goal = self.graph.nodes.get(goal_id)
        
        if node is None or goal is None:
            return float('inf')
        
        # Euclidean distance in visual space
        dx = node.x - goal.x
        dy = node.y - goal.y
        
        # Scale down the heuristic to not overpower the actual cost
        return math.sqrt(dx * dx + dy * dy) * 0.01
    
    def execute(self, start_node_id: int, end_node_id: int, **kwargs) -> AlgorithmResult:
        """
        Execute A* algorithm to find shortest path.
        
        Args:
            start_node_id: ID of the starting node
            end_node_id: ID of the target node
            
        Returns:
            AlgorithmResult with path and distances
        """
        self._clear_steps()
        self._start_timer()
        
        if start_node_id not in self.graph.nodes:
            return self._create_result(
                success=False,
                message=f"Başlangıç düğümü {start_node_id} bulunamadı"
            )
        
        if end_node_id not in self.graph.nodes:
            return self._create_result(
                success=False,
                message=f"Hedef düğümü {end_node_id} bulunamadı"
            )
        
        # g_score: cost from start to current
        g_score: Dict[int, float] = {nid: float('inf') for nid in self.graph.nodes}
        g_score[start_node_id] = 0
        
        # f_score: g_score + heuristic
        f_score: Dict[int, float] = {nid: float('inf') for nid in self.graph.nodes}
        f_score[start_node_id] = self._heuristic(start_node_id, end_node_id)
        
        # Previous node for path reconstruction
        came_from: Dict[int, Optional[int]] = {}
        
        # Priority queue: (f_score, g_score, node_id)
        # Include g_score as tiebreaker
        open_set: List[Tuple[float, float, int]] = [(f_score[start_node_id], 0, start_node_id)]
        open_set_nodes: Set[int] = {start_node_id}
        closed_set: Set[int] = set()
        
        while open_set:
            _, current_g, current_id = heapq.heappop(open_set)
            open_set_nodes.discard(current_id)
            
            self._add_step(
                'visit',
                node_id=current_id,
                g_score=g_score[current_id],
                f_score=f_score[current_id],
                open_set=list(open_set_nodes),
                closed_set=list(closed_set)
            )
            
            if current_id == end_node_id:
                # Reconstruct path
                path = []
                current = end_node_id
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start_node_id)
                path.reverse()
                
                # Get path edges
                path_edges = []
                for i in range(len(path) - 1):
                    path_edges.append((path[i], path[i + 1]))
                
                result_data = {
                    'path': path,
                    'path_edges': path_edges,
                    'total_cost': g_score[end_node_id],
                    'nodes_explored': len(closed_set) + 1,
                    'start_node': start_node_id,
                    'end_node': end_node_id
                }
                
                return self._create_result(
                    success=True,
                    data=result_data,
                    message=f"Yol bulundu: {len(path)} düğüm, maliyet: {g_score[end_node_id]:.3f}"
                )
            
            closed_set.add(current_id)
            
            # Explore neighbors
            for neighbor_id in self.graph.get_neighbor_ids(current_id):
                if neighbor_id in closed_set:
                    continue
                
                edge = self.graph.get_edge(current_id, neighbor_id)
                if edge is None:
                    continue
                
                tentative_g = g_score[current_id] + edge.get_cost()
                
                if tentative_g < g_score[neighbor_id]:
                    came_from[neighbor_id] = current_id
                    g_score[neighbor_id] = tentative_g
                    f_score[neighbor_id] = tentative_g + self._heuristic(neighbor_id, end_node_id)
                    
                    if neighbor_id not in open_set_nodes:
                        heapq.heappush(open_set, (f_score[neighbor_id], tentative_g, neighbor_id))
                        open_set_nodes.add(neighbor_id)
                    
                    self._add_step(
                        'update',
                        node_id=neighbor_id,
                        g_score=tentative_g,
                        f_score=f_score[neighbor_id],
                        from_node=current_id
                    )
        
        return self._create_result(
            success=False,
            message=f"{start_node_id} ve {end_node_id} arasında yol bulunamadı"
        )




