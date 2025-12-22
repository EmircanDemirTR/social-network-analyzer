"""
Data import/export handler for JSON and CSV formats.
"""
import json
import csv
from typing import TYPE_CHECKING
import os

if TYPE_CHECKING:
    from ..models.graph import Graph


class DataHandler:
    """
    Handles import/export of graph data in JSON and CSV formats.
    """
    
    @staticmethod
    def export_json(graph: 'Graph', filename: str) -> None:
        """
        Export graph to JSON file.
        
        Args:
            graph: Graph to export
            filename: Output filename
        """
        data = graph.to_dict()
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def import_json(filename: str) -> 'Graph':
        """
        Import graph from JSON file.
        
        Args:
            filename: Input filename
            
        Returns:
            Loaded Graph instance
        """
        from ..models.graph import Graph
        
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return Graph.from_dict(data)
    
    @staticmethod
    def export_csv(graph: 'Graph', filename: str) -> None:
        """
        Export graph to CSV file.
        
        Format follows project specification:
        DugumId, Ozellik_I (Aktiflik), Ozellik_II (Etkileşim), Ozellik_III (Bağl. Sayısı), Komsular
        
        Args:
            graph: Graph to export
            filename: Output filename
        """
        with open(filename, 'w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'DugumId', 'Isim', 'Ozellik_I (Aktiflik)', 
                'Ozellik_II (Etkilesim)', 'Ozellik_III (Bagl. Sayisi)',
                'X', 'Y', 'Komsular'
            ])
            
            # Data rows
            for node in graph.nodes.values():
                neighbors = graph.get_neighbor_ids(node.id)
                neighbors_str = ','.join(map(str, neighbors)) if neighbors else ''
                
                writer.writerow([
                    node.id,
                    node.name,
                    round(node.activity, 2),
                    round(node.interaction, 2),
                    node.connection_count,
                    round(node.x, 2),
                    round(node.y, 2),
                    neighbors_str
                ])
    
    @staticmethod
    def import_csv(filename: str) -> 'Graph':
        """
        Import graph from CSV file.
        
        Args:
            filename: Input filename
            
        Returns:
            Loaded Graph instance
        """
        from ..models.graph import Graph
        from ..models.node import Node
        
        graph = Graph()
        edges_to_add = []
        
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                # Parse node data
                node_id = int(row.get('DugumId', row.get('id', 0)))
                name = row.get('Isim', row.get('name', f'User_{node_id}'))
                activity = float(row.get('Ozellik_I (Aktiflik)', row.get('activity', 0.5)))
                interaction = float(row.get('Ozellik_II (Etkilesim)', row.get('interaction', 10)))
                x = float(row.get('X', row.get('x', 0)))
                y = float(row.get('Y', row.get('y', 0)))
                
                # Create node
                node = Node(
                    id=node_id,
                    name=name,
                    activity=activity,
                    interaction=interaction,
                    x=x if x != 0 else None,
                    y=y if y != 0 else None
                )
                
                try:
                    graph.add_node(node)
                except ValueError:
                    pass  # Node already exists
                
                # Store neighbors for edge creation
                neighbors_str = row.get('Komsular', row.get('neighbors', ''))
                if neighbors_str:
                    neighbor_ids = [int(n.strip()) for n in neighbors_str.split(',') if n.strip()]
                    for neighbor_id in neighbor_ids:
                        edges_to_add.append((node_id, neighbor_id))
        
        # Add edges (avoid duplicates)
        added_edges = set()
        for source_id, target_id in edges_to_add:
            edge_key = frozenset([source_id, target_id])
            if edge_key not in added_edges:
                if source_id in graph.nodes and target_id in graph.nodes:
                    graph.add_edge(source_id, target_id)
                    added_edges.add(edge_key)
        
        return graph
    
    @staticmethod
    def export_adjacency_list(graph: 'Graph', filename: str) -> None:
        """
        Export adjacency list to text file.
        
        Args:
            graph: Graph to export
            filename: Output filename
        """
        adj_list = graph.get_adjacency_list()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# Komşuluk Listesi\n")
            f.write("# Format: DüğümID (İsim): [Komşu1, Komşu2, ...]\n\n")
            
            for node_id in sorted(adj_list.keys()):
                node = graph.nodes[node_id]
                neighbors = adj_list[node_id]
                neighbor_names = [graph.nodes[n].name for n in neighbors]
                
                f.write(f"{node_id} ({node.name}): {neighbors}\n")
                f.write(f"  -> İsimler: {neighbor_names}\n")
    
    @staticmethod
    def export_adjacency_matrix(graph: 'Graph', filename: str) -> None:
        """
        Export adjacency matrix to text file.
        
        Args:
            graph: Graph to export
            filename: Output filename
        """
        matrix, node_ids = graph.get_adjacency_matrix()
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write("# Komşuluk Matrisi (Ağırlık Değerleri)\n")
            f.write(f"# Düğüm sırası: {node_ids}\n")
            f.write(f"# Düğüm sayısı: {len(node_ids)}\n\n")
            
            # Header row with node IDs
            header = "      " + "  ".join(f"{nid:5}" for nid in node_ids)
            f.write(header + "\n")
            f.write("-" * len(header) + "\n")
            
            # Matrix rows
            for i, row in enumerate(matrix):
                row_str = f"{node_ids[i]:5}|"
                row_str += "  ".join(f"{val:5.2f}" for val in row)
                f.write(row_str + "\n")
    
    @staticmethod
    def generate_sample_data(node_count: int, edge_probability: float = 0.3) -> 'Graph':
        """
        Generate sample graph data for testing.
        
        Args:
            node_count: Number of nodes to generate
            edge_probability: Probability of edge between any two nodes
            
        Returns:
            Generated Graph instance
        """
        import random
        from ..models.graph import Graph
        
        graph = Graph()
        
        # Turkish names for sample data
        names = [
            "Ahmet", "Mehmet", "Ayşe", "Fatma", "Ali", "Veli", 
            "Zeynep", "Elif", "Mustafa", "Hüseyin", "Hatice", "Emine",
            "Ömer", "Yusuf", "İbrahim", "Osman", "Aslı", "Selin",
            "Burak", "Emre", "Deniz", "Cem", "Can", "Arda",
            "Berk", "Kaan", "Mert", "Ece", "İrem", "Defne",
            "Yağmur", "Nehir", "Derya", "Sevgi", "Gül", "Çiçek",
            "Barış", "Serkan", "Tolga", "Onur", "Kemal", "Selim",
            "Leyla", "Merve", "Büşra", "Gamze", "Hande", "Seda",
            "Taner", "Volkan", "Sinan", "Erhan", "Gökhan", "Özgür",
            "Pelin", "Nazlı", "Burcu", "Ceren", "Dilara", "Simge"
        ]
        
        # Generate nodes in a circular layout
        import math
        center_x, center_y = 400, 300
        radius = min(300, 50 + node_count * 8)
        
        for i in range(node_count):
            angle = 2 * math.pi * i / node_count
            x = center_x + radius * math.cos(angle)
            y = center_y + radius * math.sin(angle)
            
            name = names[i % len(names)]
            if i >= len(names):
                name = f"{name}_{i // len(names)}"
            
            graph.add_node(
                name=name,
                x=x,
                y=y,
                activity=random.uniform(0.1, 1.0),
                interaction=random.uniform(1, 50)
            )
        
        # Generate edges randomly
        node_ids = list(graph.nodes.keys())
        for i, source_id in enumerate(node_ids):
            for target_id in node_ids[i + 1:]:
                if random.random() < edge_probability:
                    graph.add_edge(source_id, target_id)
        
        return graph


