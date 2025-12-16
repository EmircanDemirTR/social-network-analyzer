"""
Connected Components detection algorithm.
"""
from typing import Dict, List, Set
from .base import Algorithm, AlgorithmResult


class ConnectedComponents(Algorithm):
    """
    Algorithm to find connected components in an undirected graph.
    
    A connected component is a maximal set of vertices such that
    there is a path between every pair of vertices.
    """
    
    @property
    def name(self) -> str:
        return "Bağlı Bileşenler"
    
    @property
    def description(self) -> str:
        return "Graftaki birbirine bağlı düğüm gruplarını (ayrık toplulukları) tespit eder."
    
    def execute(self, **kwargs) -> AlgorithmResult:
        """
        Find all connected components in the graph.
        
        Returns:
            AlgorithmResult with list of components
        """
        self._clear_steps()
        self._start_timer()
        
        if not self.graph.nodes:
            return self._create_result(
                success=True,
                data={'components': [], 'component_count': 0},
                message="Graf boş"
            )
        
        visited: Set[int] = set()
        components: List[List[int]] = []
        component_map: Dict[int, int] = {}  # node_id -> component_index
        
        # Colors for components
        component_colors = [
            (0, 217, 255),    # Neon blue
            (0, 255, 136),    # Neon green
            (180, 41, 249),   # Neon purple
            (255, 107, 107),  # Coral red
            (255, 215, 0),    # Gold
            (0, 255, 255),    # Cyan
            (255, 105, 180),  # Hot pink
            (50, 205, 50),    # Lime green
            (255, 165, 0),    # Orange
            (138, 43, 226),   # Blue violet
        ]
        
        def bfs_component(start_id: int) -> List[int]:
            """Find all nodes in the component containing start_id."""
            component = []
            queue = [start_id]
            visited.add(start_id)
            
            while queue:
                node_id = queue.pop(0)
                component.append(node_id)
                
                self._add_step(
                    'visit',
                    node_id=node_id,
                    component_index=len(components)
                )
                
                for neighbor_id in self.graph.get_neighbor_ids(node_id):
                    if neighbor_id not in visited:
                        visited.add(neighbor_id)
                        queue.append(neighbor_id)
            
            return component
        
        # Find all components
        for node_id in self.graph.nodes:
            if node_id not in visited:
                component = bfs_component(node_id)
                component_index = len(components)
                
                # Map nodes to their component
                for nid in component:
                    component_map[nid] = component_index
                
                components.append(component)
                
                self._add_step(
                    'component_complete',
                    component_index=component_index,
                    component_nodes=component,
                    color=component_colors[component_index % len(component_colors)]
                )
        
        # Sort components by size (largest first)
        components.sort(key=len, reverse=True)
        
        # Prepare result data
        component_details = []
        for i, comp in enumerate(components):
            color = component_colors[i % len(component_colors)]
            component_details.append({
                'index': i,
                'nodes': comp,
                'size': len(comp),
                'color': color
            })
        
        result_data = {
            'components': components,
            'component_details': component_details,
            'component_count': len(components),
            'component_map': component_map,
            'largest_component_size': len(components[0]) if components else 0,
            'isolated_nodes': [c[0] for c in components if len(c) == 1]
        }
        
        return self._create_result(
            success=True,
            data=result_data,
            message=f"{len(components)} bağlı bileşen bulundu"
        )




