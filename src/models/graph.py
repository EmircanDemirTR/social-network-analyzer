"""
Graph class representing the social network as a whole.
"""
from typing import Dict, List, Optional, Set, Tuple, Any
from .node import Node
from .edge import Edge


class Graph:
    """
    Represents an undirected, weighted graph for social network analysis.
    
    Attributes:
        nodes: Dictionary mapping node IDs to Node objects
        edges: List of Edge objects
        _adjacency_list: Cached adjacency list
    """
    
    def __init__(self):
        """Initialize an empty graph."""
        self.nodes: Dict[int, Node] = {}
        self.edges: List[Edge] = []
        self._adjacency_list: Dict[int, List[int]] = {}
        self._next_id: int = 1
    
    def add_node(self, node: Optional[Node] = None, **kwargs) -> Node:
        """
        Add a node to the graph.
        
        Args:
            node: Optional Node object. If not provided, creates a new node.
            **kwargs: Arguments passed to Node constructor if creating new node.
            
        Returns:
            The added node
            
        Raises:
            ValueError: If node with same ID already exists
        """
        if node is None:
            node_id = kwargs.get('id', self._next_id)
            while node_id in self.nodes:
                node_id += 1
            kwargs['id'] = node_id
            node = Node(**kwargs)
        
        if node.id in self.nodes:
            raise ValueError(f"Node with ID {node.id} already exists")
        
        self.nodes[node.id] = node
        self._adjacency_list[node.id] = []
        
        if node.id >= self._next_id:
            self._next_id = node.id + 1
        
        return node
    
    def remove_node(self, node_id: int) -> bool:
        """
        Remove a node and all its connected edges from the graph.
        
        Args:
            node_id: ID of the node to remove
            
        Returns:
            True if node was removed, False if not found
        """
        if node_id not in self.nodes:
            return False
        
        # Remove all edges connected to this node
        self.edges = [e for e in self.edges if not e.contains_node(node_id)]
        
        # Update adjacency list - remove node and references to it
        del self._adjacency_list[node_id]
        for adj_list in self._adjacency_list.values():
            if node_id in adj_list:
                adj_list.remove(node_id)
        
        # Update connection counts for affected nodes
        for node in self.nodes.values():
            node.connection_count = len(self._adjacency_list.get(node.id, []))
        
        # Remove the node
        del self.nodes[node_id]
        
        return True
    
    def update_node(self, node_id: int, **kwargs) -> bool:
        """
        Update node properties.
        
        Args:
            node_id: ID of the node to update
            **kwargs: Properties to update
            
        Returns:
            True if node was updated, False if not found
        """
        if node_id not in self.nodes:
            return False
        
        node = self.nodes[node_id]
        for key, value in kwargs.items():
            if hasattr(node, key):
                setattr(node, key, value)
        
        # Recalculate edge weights if properties changed
        if any(k in kwargs for k in ['activity', 'interaction', 'connection_count']):
            for edge in self.edges:
                if edge.contains_node(node_id):
                    edge.recalculate_weight()
        
        return True
    
    def add_edge(self, source_id: int, target_id: int) -> Optional[Edge]:
        """
        Add an edge between two nodes.
        
        Args:
            source_id: ID of source node
            target_id: ID of target node
            
        Returns:
            The created edge, or None if invalid
        """
        # Validate nodes exist
        if source_id not in self.nodes or target_id not in self.nodes:
            return None
        
        # Prevent self-loops
        if source_id == target_id:
            return None
        
        # Check if edge already exists
        if self.has_edge(source_id, target_id):
            return None
        
        source = self.nodes[source_id]
        target = self.nodes[target_id]
        
        edge = Edge(source=source, target=target)
        self.edges.append(edge)
        
        # Update adjacency list (undirected)
        self._adjacency_list[source_id].append(target_id)
        self._adjacency_list[target_id].append(source_id)
        
        # Update connection counts
        source.connection_count = len(self._adjacency_list[source_id])
        target.connection_count = len(self._adjacency_list[target_id])
        
        # Recalculate weight with updated connection counts
        edge.recalculate_weight()
        
        return edge
    
    def remove_edge(self, source_id: int, target_id: int) -> bool:
        """
        Remove an edge between two nodes.
        
        Args:
            source_id: ID of source node
            target_id: ID of target node
            
        Returns:
            True if edge was removed, False if not found
        """
        edge_to_remove = None
        for edge in self.edges:
            if ((edge.source.id == source_id and edge.target.id == target_id) or
                (edge.source.id == target_id and edge.target.id == source_id)):
                edge_to_remove = edge
                break
        
        if edge_to_remove is None:
            return False
        
        self.edges.remove(edge_to_remove)
        
        # Update adjacency list
        if target_id in self._adjacency_list.get(source_id, []):
            self._adjacency_list[source_id].remove(target_id)
        if source_id in self._adjacency_list.get(target_id, []):
            self._adjacency_list[target_id].remove(source_id)
        
        # Update connection counts
        if source_id in self.nodes:
            self.nodes[source_id].connection_count = len(self._adjacency_list[source_id])
        if target_id in self.nodes:
            self.nodes[target_id].connection_count = len(self._adjacency_list[target_id])
        
        return True
    
    def has_edge(self, source_id: int, target_id: int) -> bool:
        """
        Check if an edge exists between two nodes.
        
        Args:
            source_id: ID of source node
            target_id: ID of target node
            
        Returns:
            True if edge exists
        """
        return target_id in self._adjacency_list.get(source_id, [])
    
    def get_edge(self, source_id: int, target_id: int) -> Optional[Edge]:
        """
        Get the edge between two nodes.
        
        Args:
            source_id: ID of source node
            target_id: ID of target node
            
        Returns:
            Edge object or None if not found
        """
        for edge in self.edges:
            if ((edge.source.id == source_id and edge.target.id == target_id) or
                (edge.source.id == target_id and edge.target.id == source_id)):
                return edge
        return None
    
    def get_neighbors(self, node_id: int) -> List[Node]:
        """
        Get all neighbors of a node.
        
        Args:
            node_id: ID of the node
            
        Returns:
            List of neighboring Node objects
        """
        neighbor_ids = self._adjacency_list.get(node_id, [])
        return [self.nodes[nid] for nid in neighbor_ids if nid in self.nodes]
    
    def get_neighbor_ids(self, node_id: int) -> List[int]:
        """
        Get IDs of all neighbors of a node.
        
        Args:
            node_id: ID of the node
            
        Returns:
            List of neighboring node IDs
        """
        return self._adjacency_list.get(node_id, []).copy()
    
    def get_degree(self, node_id: int) -> int:
        """
        Get the degree (number of connections) of a node.
        
        Args:
            node_id: ID of the node
            
        Returns:
            Degree of the node
        """
        return len(self._adjacency_list.get(node_id, []))
    
    def get_adjacency_list(self) -> Dict[int, List[int]]:
        """
        Get the adjacency list representation of the graph.
        
        Returns:
            Dictionary mapping node IDs to lists of neighbor IDs
        """
        return {nid: neighbors.copy() for nid, neighbors in self._adjacency_list.items()}
    
    def get_adjacency_matrix(self) -> Tuple[List[List[float]], List[int]]:
        """
        Get the adjacency matrix representation of the graph.
        
        Returns:
            Tuple of (matrix, node_ids) where matrix[i][j] is the edge weight
            between nodes[i] and nodes[j], and node_ids is the list of node IDs
            in order
        """
        node_ids = sorted(self.nodes.keys())
        n = len(node_ids)
        id_to_idx = {nid: i for i, nid in enumerate(node_ids)}
        
        matrix = [[0.0] * n for _ in range(n)]
        
        for edge in self.edges:
            i = id_to_idx[edge.source.id]
            j = id_to_idx[edge.target.id]
            matrix[i][j] = edge.weight
            matrix[j][i] = edge.weight  # Undirected
        
        return matrix, node_ids
    
    def get_node_count(self) -> int:
        """Get the number of nodes in the graph."""
        return len(self.nodes)
    
    def get_edge_count(self) -> int:
        """Get the number of edges in the graph."""
        return len(self.edges)
    
    def get_density(self) -> float:
        """
        Calculate graph density.
        Density = 2 * |E| / (|V| * (|V| - 1))
        
        Returns:
            Graph density (0 to 1)
        """
        n = len(self.nodes)
        if n <= 1:
            return 0.0
        max_edges = n * (n - 1) / 2
        return len(self.edges) / max_edges if max_edges > 0 else 0.0
    
    def get_average_degree(self) -> float:
        """
        Calculate average degree of nodes.
        
        Returns:
            Average degree
        """
        if not self.nodes:
            return 0.0
        total_degree = sum(len(neighbors) for neighbors in self._adjacency_list.values())
        return total_degree / len(self.nodes)
    
    def clear_highlights(self) -> None:
        """Clear all node and edge highlights."""
        for node in self.nodes.values():
            node.set_highlight(False)
        for edge in self.edges:
            edge.set_highlight(False)
    
    def clear(self) -> None:
        """Clear the entire graph."""
        self.nodes.clear()
        self.edges.clear()
        self._adjacency_list.clear()
        self._next_id = 1
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize graph to dictionary for JSON export.
        
        Returns:
            Dictionary representation of the graph
        """
        return {
            'nodes': [node.to_dict() for node in self.nodes.values()],
            'edges': [edge.to_dict() for edge in self.edges]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Graph':
        """
        Create Graph from dictionary.
        
        Args:
            data: Dictionary containing graph data
            
        Returns:
            New Graph instance
        """
        graph = cls()
        
        # Add nodes first
        for node_data in data.get('nodes', []):
            node = Node.from_dict(node_data)
            graph.add_node(node)
        
        # Add edges
        for edge_data in data.get('edges', []):
            graph.add_edge(edge_data['source_id'], edge_data['target_id'])
        
        return graph
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get comprehensive graph statistics.
        
        Returns:
            Dictionary containing various graph metrics
        """
        return {
            'node_count': self.get_node_count(),
            'edge_count': self.get_edge_count(),
            'density': round(self.get_density(), 4),
            'average_degree': round(self.get_average_degree(), 2),
            'max_degree': max((self.get_degree(nid) for nid in self.nodes), default=0),
            'min_degree': min((self.get_degree(nid) for nid in self.nodes), default=0)
        }
    
    def __repr__(self):
        return f"Graph(nodes={len(self.nodes)}, edges={len(self.edges)})"


