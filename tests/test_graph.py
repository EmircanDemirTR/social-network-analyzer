"""
Test module for Graph model operations.
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.graph import Graph
from src.models.node import Node
from src.models.edge import Edge


def test_node_creation():
    """Test node creation and properties."""
    print("\n" + "=" * 50)
    print("TEST: Node Creation")
    print("=" * 50)
    
    node = Node(id=1, name="Test User", activity=0.8, interaction=15)
    
    assert node.id == 1
    assert node.name == "Test User"
    assert node.activity == 0.8
    assert node.interaction == 15
    
    print(f"Node created: {node}")
    print(f"Properties: {node.get_properties()}")
    print("[OK] Node creation test passed")


def test_graph_add_node():
    """Test adding nodes to graph."""
    print("\n" + "=" * 50)
    print("TEST: Graph Add Node")
    print("=" * 50)
    
    graph = Graph()
    
    node1 = graph.add_node(name="User1", activity=0.5)
    node2 = graph.add_node(name="User2", activity=0.7)
    
    assert graph.get_node_count() == 2
    assert node1.id in graph.nodes
    assert node2.id in graph.nodes
    
    print(f"Added nodes: {list(graph.nodes.values())}")
    print(f"Node count: {graph.get_node_count()}")
    print("[OK] Add node test passed")


def test_graph_add_edge():
    """Test adding edges to graph."""
    print("\n" + "=" * 50)
    print("TEST: Graph Add Edge")
    print("=" * 50)
    
    graph = Graph()
    node1 = graph.add_node(name="User1")
    node2 = graph.add_node(name="User2")
    node3 = graph.add_node(name="User3")
    
    edge1 = graph.add_edge(node1.id, node2.id)
    edge2 = graph.add_edge(node2.id, node3.id)
    
    assert graph.get_edge_count() == 2
    assert graph.has_edge(node1.id, node2.id)
    assert graph.has_edge(node2.id, node1.id)  # Undirected
    
    print(f"Added edges: {graph.edges}")
    print(f"Edge count: {graph.get_edge_count()}")
    print(f"Edge weight: {edge1.weight:.4f}")
    print("[OK] Add edge test passed")


def test_self_loop_prevention():
    """Test that self-loops are prevented."""
    print("\n" + "=" * 50)
    print("TEST: Self-Loop Prevention")
    print("=" * 50)
    
    graph = Graph()
    node = graph.add_node(name="User1")
    
    edge = graph.add_edge(node.id, node.id)
    
    assert edge is None
    assert graph.get_edge_count() == 0
    
    print("Self-loop correctly prevented")
    print("[OK] Self-loop prevention test passed")


def test_duplicate_edge_prevention():
    """Test that duplicate edges are prevented."""
    print("\n" + "=" * 50)
    print("TEST: Duplicate Edge Prevention")
    print("=" * 50)
    
    graph = Graph()
    node1 = graph.add_node(name="User1")
    node2 = graph.add_node(name="User2")
    
    edge1 = graph.add_edge(node1.id, node2.id)
    edge2 = graph.add_edge(node1.id, node2.id)
    edge3 = graph.add_edge(node2.id, node1.id)  # Same edge, different direction
    
    assert edge1 is not None
    assert edge2 is None
    assert edge3 is None
    assert graph.get_edge_count() == 1
    
    print("Duplicate edges correctly prevented")
    print("[OK] Duplicate edge prevention test passed")


def test_node_removal():
    """Test node removal and edge cleanup."""
    print("\n" + "=" * 50)
    print("TEST: Node Removal")
    print("=" * 50)
    
    graph = Graph()
    node1 = graph.add_node(name="User1")
    node2 = graph.add_node(name="User2")
    node3 = graph.add_node(name="User3")
    
    graph.add_edge(node1.id, node2.id)
    graph.add_edge(node2.id, node3.id)
    
    print(f"Before removal: {graph.get_node_count()} nodes, {graph.get_edge_count()} edges")
    
    graph.remove_node(node2.id)
    
    assert graph.get_node_count() == 2
    assert graph.get_edge_count() == 0  # Both edges removed
    assert node2.id not in graph.nodes
    
    print(f"After removal: {graph.get_node_count()} nodes, {graph.get_edge_count()} edges")
    print("[OK] Node removal test passed")


def test_adjacency_list():
    """Test adjacency list generation."""
    print("\n" + "=" * 50)
    print("TEST: Adjacency List")
    print("=" * 50)
    
    graph = Graph()
    n1 = graph.add_node(name="A")
    n2 = graph.add_node(name="B")
    n3 = graph.add_node(name="C")
    
    graph.add_edge(n1.id, n2.id)
    graph.add_edge(n1.id, n3.id)
    graph.add_edge(n2.id, n3.id)
    
    adj_list = graph.get_adjacency_list()
    
    assert n2.id in adj_list[n1.id]
    assert n3.id in adj_list[n1.id]
    assert n1.id in adj_list[n2.id]
    
    print(f"Adjacency list: {adj_list}")
    print("[OK] Adjacency list test passed")


def test_adjacency_matrix():
    """Test adjacency matrix generation."""
    print("\n" + "=" * 50)
    print("TEST: Adjacency Matrix")
    print("=" * 50)
    
    graph = Graph()
    n1 = graph.add_node(name="A")
    n2 = graph.add_node(name="B")
    n3 = graph.add_node(name="C")
    
    graph.add_edge(n1.id, n2.id)
    graph.add_edge(n2.id, n3.id)
    
    matrix, node_ids = graph.get_adjacency_matrix()
    
    print(f"Node IDs: {node_ids}")
    print("Matrix:")
    for row in matrix:
        print(f"  {[f'{v:.2f}' for v in row]}")
    
    # Check symmetry (undirected)
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            assert matrix[i][j] == matrix[j][i]
    
    print("[OK] Adjacency matrix test passed")


def test_graph_statistics():
    """Test graph statistics calculation."""
    print("\n" + "=" * 50)
    print("TEST: Graph Statistics")
    print("=" * 50)
    
    graph = Graph()
    for i in range(5):
        graph.add_node(name=f"User{i+1}")
    
    graph.add_edge(1, 2)
    graph.add_edge(2, 3)
    graph.add_edge(3, 4)
    graph.add_edge(4, 5)
    graph.add_edge(1, 5)  # Create a cycle
    
    stats = graph.get_statistics()
    
    print(f"Statistics: {stats}")
    
    assert stats['node_count'] == 5
    assert stats['edge_count'] == 5
    assert stats['density'] > 0
    assert stats['average_degree'] == 2.0  # Each node has 2 edges
    
    print("[OK] Graph statistics test passed")


def test_edge_weight_calculation():
    """Test dynamic edge weight calculation."""
    print("\n" + "=" * 50)
    print("TEST: Edge Weight Calculation")
    print("=" * 50)
    
    graph = Graph()
    
    # Similar nodes should have higher weight
    n1 = graph.add_node(name="Similar1", activity=0.5, interaction=10)
    n2 = graph.add_node(name="Similar2", activity=0.5, interaction=10)
    
    # Different nodes should have lower weight
    n3 = graph.add_node(name="Different", activity=0.9, interaction=50)
    
    edge_similar = graph.add_edge(n1.id, n2.id)
    edge_different = graph.add_edge(n1.id, n3.id)
    
    print(f"Similar nodes weight: {edge_similar.weight:.4f}")
    print(f"Different nodes weight: {edge_different.weight:.4f}")
    
    assert edge_similar.weight > edge_different.weight
    
    print("[OK] Edge weight calculation test passed")


def main():
    """Run all tests."""
    print("=" * 60)
    print("SOSYAL AĞ ANALİZİ - GRAF MODEL TESTLERİ")
    print("=" * 60)
    
    test_node_creation()
    test_graph_add_node()
    test_graph_add_edge()
    test_self_loop_prevention()
    test_duplicate_edge_prevention()
    test_node_removal()
    test_adjacency_list()
    test_adjacency_matrix()
    test_graph_statistics()
    test_edge_weight_calculation()
    
    print("\n" + "=" * 60)
    print("TÜM TESTLER BAŞARILI")
    print("=" * 60)


if __name__ == "__main__":
    main()

