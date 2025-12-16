"""
Graph traversal algorithms: BFS and DFS.
"""
from collections import deque
from typing import List, Set, Dict, Any, Optional
from .base import Algorithm, AlgorithmResult


class BFS(Algorithm):
    """
    Breadth-First Search algorithm.
    
    Explores all neighbors at current depth before moving to nodes at next depth.
    """
    
    @property
    def name(self) -> str:
        return "BFS (Genişlik Öncelikli Arama)"
    
    @property
    def description(self) -> str:
        return "Bir düğümden başlayarak tüm erişilebilir düğümleri seviye seviye keşfeder."
    
    def execute(self, start_node_id: int, **kwargs) -> AlgorithmResult:
        """
        Execute BFS from a starting node.
        
        Args:
            start_node_id: ID of the starting node
            
        Returns:
            AlgorithmResult with visited nodes in order
        """
        self._clear_steps()
        self._start_timer()
        
        if start_node_id not in self.graph.nodes:
            return self._create_result(
                success=False,
                message=f"Düğüm {start_node_id} bulunamadı"
            )
        
        visited: Set[int] = set()
        visit_order: List[int] = []
        levels: Dict[int, int] = {}  # node_id -> level
        queue: deque = deque([(start_node_id, 0)])
        
        visited.add(start_node_id)
        
        while queue:
            node_id, level = queue.popleft()
            visit_order.append(node_id)
            levels[node_id] = level
            
            # Record step for animation
            self._add_step(
                'visit',
                node_id=node_id,
                level=level,
                visited=list(visited)
            )
            
            # Explore neighbors
            for neighbor_id in self.graph.get_neighbor_ids(node_id):
                if neighbor_id not in visited:
                    visited.add(neighbor_id)
                    queue.append((neighbor_id, level + 1))
                    
                    self._add_step(
                        'discover',
                        node_id=neighbor_id,
                        from_node=node_id,
                        level=level + 1
                    )
        
        result_data = {
            'visit_order': visit_order,
            'levels': levels,
            'visited_count': len(visit_order),
            'start_node': start_node_id
        }
        
        return self._create_result(
            success=True,
            data=result_data,
            message=f"{len(visit_order)} düğüm ziyaret edildi"
        )


class DFS(Algorithm):
    """
    Depth-First Search algorithm.
    
    Explores as far as possible along each branch before backtracking.
    """
    
    @property
    def name(self) -> str:
        return "DFS (Derinlik Öncelikli Arama)"
    
    @property
    def description(self) -> str:
        return "Bir düğümden başlayarak mümkün olduğunca derine iner, sonra geri döner."
    
    def execute(self, start_node_id: int, **kwargs) -> AlgorithmResult:
        """
        Execute DFS from a starting node.
        
        Args:
            start_node_id: ID of the starting node
            
        Returns:
            AlgorithmResult with visited nodes in order
        """
        self._clear_steps()
        self._start_timer()
        
        if start_node_id not in self.graph.nodes:
            return self._create_result(
                success=False,
                message=f"Düğüm {start_node_id} bulunamadı"
            )
        
        visited: Set[int] = set()
        visit_order: List[int] = []
        discovery_time: Dict[int, int] = {}
        finish_time: Dict[int, int] = {}
        time_counter = [0]  # Use list for mutable reference
        
        def dfs_visit(node_id: int, depth: int = 0):
            visited.add(node_id)
            time_counter[0] += 1
            discovery_time[node_id] = time_counter[0]
            visit_order.append(node_id)
            
            self._add_step(
                'visit',
                node_id=node_id,
                depth=depth,
                discovery_time=discovery_time[node_id]
            )
            
            for neighbor_id in self.graph.get_neighbor_ids(node_id):
                if neighbor_id not in visited:
                    self._add_step(
                        'explore_edge',
                        from_node=node_id,
                        to_node=neighbor_id,
                        depth=depth + 1
                    )
                    dfs_visit(neighbor_id, depth + 1)
            
            time_counter[0] += 1
            finish_time[node_id] = time_counter[0]
            
            self._add_step(
                'finish',
                node_id=node_id,
                finish_time=finish_time[node_id]
            )
        
        dfs_visit(start_node_id)
        
        result_data = {
            'visit_order': visit_order,
            'discovery_time': discovery_time,
            'finish_time': finish_time,
            'visited_count': len(visit_order),
            'start_node': start_node_id
        }
        
        return self._create_result(
            success=True,
            data=result_data,
            message=f"{len(visit_order)} düğüm ziyaret edildi"
        )




