"""
Centrality measures for graph analysis.
"""
from typing import Dict, List, Tuple
from .base import Algorithm, AlgorithmResult


class DegreeCentrality(Algorithm):
    """
    Degree Centrality algorithm.
    
    Measures the importance of nodes based on their number of connections.
    Higher degree = more influential/connected user.
    """
    
    @property
    def name(self) -> str:
        return "Derece Merkeziliği"
    
    @property
    def description(self) -> str:
        return "Düğümlerin bağlantı sayılarına göre önem derecelerini hesaplar."
    
    def execute(self, top_k: int = 5, **kwargs) -> AlgorithmResult:
        """
        Calculate degree centrality for all nodes.
        
        Args:
            top_k: Number of top nodes to highlight (default: 5)
            
        Returns:
            AlgorithmResult with centrality scores
        """
        self._clear_steps()
        self._start_timer()
        
        if not self.graph.nodes:
            return self._create_result(
                success=True,
                data={'centrality': {}, 'top_k': []},
                message="Graf boş"
            )
        
        n = len(self.graph.nodes)
        centrality: Dict[int, float] = {}
        degrees: Dict[int, int] = {}
        
        # Calculate degree for each node
        for node_id in self.graph.nodes:
            degree = self.graph.get_degree(node_id)
            degrees[node_id] = degree
            
            # Normalized centrality: degree / (n - 1)
            # For n > 1, otherwise 0
            if n > 1:
                centrality[node_id] = degree / (n - 1)
            else:
                centrality[node_id] = 0.0
            
            self._add_step(
                'calculate',
                node_id=node_id,
                degree=degree,
                centrality=centrality[node_id]
            )
        
        # Sort by centrality (descending)
        sorted_nodes = sorted(
            centrality.items(),
            key=lambda x: (x[1], degrees[x[0]]),  # Sort by centrality, then degree
            reverse=True
        )
        
        # Get top k nodes
        top_k_nodes: List[Dict] = []
        for rank, (node_id, cent) in enumerate(sorted_nodes[:top_k], 1):
            node = self.graph.nodes[node_id]
            top_k_nodes.append({
                'rank': rank,
                'node_id': node_id,
                'name': node.name,
                'degree': degrees[node_id],
                'centrality': round(cent, 4)
            })
            
            self._add_step(
                'top_k',
                rank=rank,
                node_id=node_id,
                centrality=cent
            )
        
        # Statistics
        centrality_values = list(centrality.values())
        avg_centrality = sum(centrality_values) / len(centrality_values) if centrality_values else 0
        max_centrality = max(centrality_values) if centrality_values else 0
        min_centrality = min(centrality_values) if centrality_values else 0
        
        result_data = {
            'centrality': centrality,
            'degrees': degrees,
            'top_k': top_k_nodes,
            'statistics': {
                'average_centrality': round(avg_centrality, 4),
                'max_centrality': round(max_centrality, 4),
                'min_centrality': round(min_centrality, 4),
                'average_degree': round(sum(degrees.values()) / len(degrees), 2) if degrees else 0,
                'max_degree': max(degrees.values()) if degrees else 0
            }
        }
        
        return self._create_result(
            success=True,
            data=result_data,
            message=f"En etkili düğüm: {top_k_nodes[0]['name'] if top_k_nodes else 'Yok'} (derece: {top_k_nodes[0]['degree'] if top_k_nodes else 0})"
        )
    
    def get_top_k(self, k: int = 5) -> List[Tuple[int, int, float]]:
        """
        Quick method to get top k nodes by degree.
        
        Args:
            k: Number of top nodes
            
        Returns:
            List of (node_id, degree, centrality) tuples
        """
        result = self.execute(top_k=k)
        if not result.success:
            return []
        
        return [
            (item['node_id'], item['degree'], item['centrality'])
            for item in result.data.get('top_k', [])
        ]




