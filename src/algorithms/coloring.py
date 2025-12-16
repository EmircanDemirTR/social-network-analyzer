"""
Welsh-Powell graph coloring algorithm.
"""
from typing import Dict, List, Set, Tuple
from .base import Algorithm, AlgorithmResult


class WelshPowell(Algorithm):
    """
    Welsh-Powell graph coloring algorithm.
    
    Colors graph vertices such that no two adjacent vertices share the same color,
    using a greedy approach based on vertex degrees.
    """
    
    # Predefined color palette for coloring
    COLORS = [
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
        (255, 99, 71),    # Tomato
        (0, 191, 255),    # Deep sky blue
        (255, 20, 147),   # Deep pink
        (124, 252, 0),    # Lawn green
        (255, 140, 0),    # Dark orange
    ]
    
    COLOR_NAMES = [
        "Neon Mavi", "Neon Yeşil", "Neon Mor", "Mercan Kırmızı", "Altın",
        "Camgöbeği", "Sıcak Pembe", "Limon Yeşili", "Turuncu", "Mavi Menekşe",
        "Domates", "Derin Gök Mavisi", "Derin Pembe", "Çimen Yeşili", "Koyu Turuncu"
    ]
    
    @property
    def name(self) -> str:
        return "Welsh-Powell Renklendirme"
    
    @property
    def description(self) -> str:
        return "Komşu düğümleri farklı renklere boyar (minimum renk sayısı ile)."
    
    def execute(self, **kwargs) -> AlgorithmResult:
        """
        Execute Welsh-Powell coloring algorithm.
        
        Returns:
            AlgorithmResult with node colors and chromatic number
        """
        self._clear_steps()
        self._start_timer()
        
        if not self.graph.nodes:
            return self._create_result(
                success=True,
                data={'coloring': {}, 'chromatic_number': 0},
                message="Graf boş"
            )
        
        # Step 1: Sort nodes by degree (descending)
        node_degrees: List[Tuple[int, int]] = [
            (node_id, self.graph.get_degree(node_id))
            for node_id in self.graph.nodes
        ]
        node_degrees.sort(key=lambda x: x[1], reverse=True)
        
        self._add_step(
            'sorted',
            order=[(nid, deg) for nid, deg in node_degrees]
        )
        
        # Step 2: Color nodes greedily
        coloring: Dict[int, int] = {}  # node_id -> color_index
        colored_nodes: Set[int] = set()
        
        current_color = 0
        
        while len(colored_nodes) < len(self.graph.nodes):
            # Go through uncolored nodes in degree order
            for node_id, degree in node_degrees:
                if node_id in colored_nodes:
                    continue
                
                # Check if this node can be colored with current color
                neighbors = self.graph.get_neighbor_ids(node_id)
                neighbor_colors = {coloring.get(n) for n in neighbors if n in coloring}
                
                if current_color not in neighbor_colors:
                    # Assign current color to this node
                    coloring[node_id] = current_color
                    colored_nodes.add(node_id)
                    
                    self._add_step(
                        'color',
                        node_id=node_id,
                        color_index=current_color,
                        color_rgb=self.COLORS[current_color % len(self.COLORS)],
                        color_name=self.COLOR_NAMES[current_color % len(self.COLOR_NAMES)]
                    )
            
            current_color += 1
        
        chromatic_number = current_color
        
        # Prepare color table
        color_groups: Dict[int, List[int]] = {}
        for node_id, color in coloring.items():
            if color not in color_groups:
                color_groups[color] = []
            color_groups[color].append(node_id)
        
        color_table = []
        for color_idx in sorted(color_groups.keys()):
            nodes_in_color = color_groups[color_idx]
            color_table.append({
                'color_index': color_idx,
                'color_name': self.COLOR_NAMES[color_idx % len(self.COLOR_NAMES)],
                'color_rgb': self.COLORS[color_idx % len(self.COLORS)],
                'nodes': nodes_in_color,
                'node_names': [self.graph.nodes[nid].name for nid in nodes_in_color],
                'count': len(nodes_in_color)
            })
        
        result_data = {
            'coloring': coloring,
            'chromatic_number': chromatic_number,
            'color_table': color_table,
            'color_groups': color_groups,
            'node_order': [nid for nid, _ in node_degrees]
        }
        
        return self._create_result(
            success=True,
            data=result_data,
            message=f"Graf {chromatic_number} renk ile boyandı (kromatik sayı)"
        )
    
    def get_chromatic_number(self) -> int:
        """
        Get the chromatic number of the graph.
        
        Returns:
            Minimum number of colors needed
        """
        result = self.execute()
        return result.data.get('chromatic_number', 0) if result.success else 0
    
    def get_node_color(self, node_id: int) -> Tuple[int, int, int]:
        """
        Get the color assigned to a specific node.
        
        Args:
            node_id: ID of the node
            
        Returns:
            RGB color tuple
        """
        result = self.execute()
        if not result.success:
            return self.COLORS[0]
        
        color_idx = result.data.get('coloring', {}).get(node_id, 0)
        return self.COLORS[color_idx % len(self.COLORS)]




