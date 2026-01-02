"""
Test module for graph algorithms.
"""
import sys
import os
import time

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.graph import Graph
from src.models.node import Node
from src.algorithms import (
    BFS, DFS, Dijkstra, AStar,
    ConnectedComponents, DegreeCentrality, WelshPowell
)
from src.utils.data_handler import DataHandler


def create_test_graph():
    """Create a simple test graph."""
    graph = Graph()
    
    # Add nodes
    for i in range(1, 11):
        graph.add_node(
            id=i,
            name=f"Node_{i}",
            activity=0.1 * i,
            interaction=i * 5
        )
    
    # Add edges to create an interesting structure
    edges = [
        (1, 2), (1, 3), (2, 3), (2, 4), (3, 5),
        (4, 5), (4, 6), (5, 6), (6, 7),
        (8, 9), (9, 10)  # Separate component
    ]
    
    for source, target in edges:
        graph.add_edge(source, target)
    
    return graph


def test_bfs(graph):
    """Test BFS algorithm."""
    print("\n" + "=" * 50)
    print("TEST: BFS (Breadth-First Search)")
    print("=" * 50)
    
    algo = BFS(graph)
    result = algo.execute(start_node_id=1)
    
    print(f"Başarı: {result.success}")
    print(f"Mesaj: {result.message}")
    print(f"Süre: {result.execution_time * 1000:.3f} ms")
    
    if result.success:
        print(f"Ziyaret sırası: {result.data['visit_order']}")
        print(f"Seviyeler: {result.data['levels']}")
    
    return result


def test_dfs(graph):
    """Test DFS algorithm."""
    print("\n" + "=" * 50)
    print("TEST: DFS (Depth-First Search)")
    print("=" * 50)
    
    algo = DFS(graph)
    result = algo.execute(start_node_id=1)
    
    print(f"Başarı: {result.success}")
    print(f"Mesaj: {result.message}")
    print(f"Süre: {result.execution_time * 1000:.3f} ms")
    
    if result.success:
        print(f"Ziyaret sırası: {result.data['visit_order']}")
        print(f"Keşif zamanları: {result.data['discovery_time']}")
    
    return result


def test_dijkstra(graph):
    """Test Dijkstra's algorithm."""
    print("\n" + "=" * 50)
    print("TEST: Dijkstra En Kısa Yol")
    print("=" * 50)
    
    algo = Dijkstra(graph)
    result = algo.execute(start_node_id=1, end_node_id=7)
    
    print(f"Başarı: {result.success}")
    print(f"Mesaj: {result.message}")
    print(f"Süre: {result.execution_time * 1000:.3f} ms")
    
    if result.success:
        print(f"Yol: {result.data['path']}")
        print(f"Toplam maliyet: {result.data['total_cost']:.4f}")
    
    return result


def test_astar(graph):
    """Test A* algorithm."""
    print("\n" + "=" * 50)
    print("TEST: A* En Kısa Yol")
    print("=" * 50)
    
    algo = AStar(graph)
    result = algo.execute(start_node_id=1, end_node_id=7)
    
    print(f"Başarı: {result.success}")
    print(f"Mesaj: {result.message}")
    print(f"Süre: {result.execution_time * 1000:.3f} ms")
    
    if result.success:
        print(f"Yol: {result.data['path']}")
        print(f"Toplam maliyet: {result.data['total_cost']:.4f}")
        print(f"Keşfedilen düğüm: {result.data['nodes_explored']}")
    
    return result


def test_components(graph):
    """Test Connected Components algorithm."""
    print("\n" + "=" * 50)
    print("TEST: Bağlı Bileşenler")
    print("=" * 50)
    
    algo = ConnectedComponents(graph)
    result = algo.execute()
    
    print(f"Başarı: {result.success}")
    print(f"Mesaj: {result.message}")
    print(f"Süre: {result.execution_time * 1000:.3f} ms")
    
    if result.success:
        print(f"Bileşen sayısı: {result.data['component_count']}")
        for i, comp in enumerate(result.data['components']):
            print(f"  Bileşen {i+1}: {comp}")
    
    return result


def test_centrality(graph):
    """Test Degree Centrality algorithm."""
    print("\n" + "=" * 50)
    print("TEST: Derece Merkeziliği")
    print("=" * 50)
    
    algo = DegreeCentrality(graph)
    result = algo.execute(top_k=5)
    
    print(f"Başarı: {result.success}")
    print(f"Mesaj: {result.message}")
    print(f"Süre: {result.execution_time * 1000:.3f} ms")
    
    if result.success:
        print("\nTop 5 Düğüm:")
        print("-" * 50)
        print(f"{'Sıra':<6}{'ID':<8}{'İsim':<12}{'Derece':<10}{'Merkezilik':<12}")
        print("-" * 50)
        for item in result.data['top_k']:
            print(f"{item['rank']:<6}{item['node_id']:<8}{item['name']:<12}"
                  f"{item['degree']:<10}{item['centrality']:.4f}")
    
    return result


def test_welsh_powell(graph):
    """Test Welsh-Powell Coloring algorithm."""
    print("\n" + "=" * 50)
    print("TEST: Welsh-Powell Renklendirme")
    print("=" * 50)
    
    algo = WelshPowell(graph)
    result = algo.execute()
    
    print(f"Başarı: {result.success}")
    print(f"Mesaj: {result.message}")
    print(f"Süre: {result.execution_time * 1000:.3f} ms")
    
    if result.success:
        print(f"\nKromatik sayı: {result.data['chromatic_number']}")
        print("\nRenk tablosu:")
        print("-" * 50)
        for color_info in result.data['color_table']:
            nodes = ', '.join(map(str, color_info['nodes']))
            print(f"  Renk {color_info['color_index']+1} ({color_info['color_name']}): {nodes}")
    
    return result


def run_performance_tests():
    """Run performance tests with different graph sizes."""
    print("\n" + "=" * 60)
    print("PERFORMANS TESTLERİ")
    print("=" * 60)
    
    sizes = [
        ("Küçük (15 düğüm)", "data/sample_small.csv"),
        ("Orta (50 düğüm)", "data/sample_medium.csv"),
    ]
    
    results = []
    
    for name, filename in sizes:
        print(f"\n--- {name} ---")
        
        filepath = os.path.join(os.path.dirname(os.path.dirname(__file__)), filename)
        
        try:
            graph = DataHandler.import_csv(filepath)
            print(f"Graf yüklendi: {graph.get_node_count()} düğüm, {graph.get_edge_count()} kenar")
        except Exception as e:
            print(f"Dosya yüklenemedi: {e}")
            continue
        
        # Run all algorithms
        algorithms = [
            ("BFS", BFS(graph), {'start_node_id': 1}),
            ("DFS", DFS(graph), {'start_node_id': 1}),
            ("Dijkstra", Dijkstra(graph), {'start_node_id': 1, 'end_node_id': graph.get_node_count()}),
            ("A*", AStar(graph), {'start_node_id': 1, 'end_node_id': graph.get_node_count()}),
            ("Bileşenler", ConnectedComponents(graph), {}),
            ("Merkezilik", DegreeCentrality(graph), {'top_k': 5}),
            ("Welsh-Powell", WelshPowell(graph), {}),
        ]
        
        print(f"\n{'Algoritma':<20}{'Süre (ms)':<15}{'Sonuç':<30}")
        print("-" * 65)
        
        for algo_name, algo, params in algorithms:
            result = algo.execute(**params)
            time_ms = result.execution_time * 1000
            
            # Format result summary
            if algo_name in ["BFS", "DFS"]:
                summary = f"{result.data['visited_count']} düğüm ziyaret edildi"
            elif algo_name in ["Dijkstra", "A*"]:
                if result.success:
                    summary = f"Yol: {len(result.data['path'])} düğüm"
                else:
                    summary = "Yol bulunamadı"
            elif algo_name == "Bileşenler":
                summary = f"{result.data['component_count']} bileşen"
            elif algo_name == "Merkezilik":
                summary = f"Max derece: {result.data['statistics']['max_degree']}"
            elif algo_name == "Welsh-Powell":
                summary = f"Kromatik sayı: {result.data['chromatic_number']}"
            else:
                summary = result.message[:28]
            
            print(f"{algo_name:<20}{time_ms:<15.3f}{summary:<30}")
            
            results.append({
                'graph_size': name,
                'algorithm': algo_name,
                'time_ms': time_ms,
                'success': result.success
            })
    
    return results


def main():
    """Run all tests."""
    print("=" * 60)
    print("SOSYAL AĞ ANALİZİ - ALGORİTMA TESTLERİ")
    print("=" * 60)
    
    # Create test graph
    graph = create_test_graph()
    print(f"\nTest grafı oluşturuldu: {graph.get_node_count()} düğüm, {graph.get_edge_count()} kenar")
    
    # Run individual tests
    test_bfs(graph)
    test_dfs(graph)
    test_dijkstra(graph)
    test_astar(graph)
    test_components(graph)
    test_centrality(graph)
    test_welsh_powell(graph)
    
    # Run performance tests
    run_performance_tests()
    
    print("\n" + "=" * 60)
    print("TÜM TESTLER TAMAMLANDI")
    print("=" * 60)


if __name__ == "__main__":
    main()


