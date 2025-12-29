"""
Statistics panel showing real-time graph metrics.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, QGroupBox
)
from PyQt6.QtCore import Qt

from ..models.graph import Graph
from .styles import DarkTheme


class StatCard(QFrame):
    """A card displaying a single statistic."""
    
    def __init__(self, title: str, value: str = "0"):
        super().__init__()
        self.setFrameStyle(QFrame.Shape.StyledPanel)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 8, 10, 8)
        layout.setSpacing(4)
        
        self.title_label = QLabel(title)
        self.title_label.setObjectName("statTitleLabel")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.title_label)
        
        self.value_label = QLabel(value)
        self.value_label.setObjectName("statLabel")
        self.value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.value_label)
    
    def set_value(self, value: str):
        """Update the displayed value."""
        self.value_label.setText(value)


class StatsPanel(QWidget):
    """
    Panel displaying real-time graph statistics.
    """
    
    def __init__(self, graph: Graph):
        super().__init__()
        self.graph = graph
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # Title
        title = QLabel("İSTATİSTİKLER")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Main stats cards
        self.node_card = StatCard("DÜĞÜM SAYISI", "0")
        layout.addWidget(self.node_card)
        
        self.edge_card = StatCard("KENAR SAYISI", "0")
        layout.addWidget(self.edge_card)
        
        self.k_card = StatCard("k DEĞERİ", "0.00")
        layout.addWidget(self.k_card)
        
        self.density_card = StatCard("YOĞUNLUK", "0.0000")
        layout.addWidget(self.density_card)
        
        self.avg_degree_card = StatCard("ORT. DERECE", "0.00")
        layout.addWidget(self.avg_degree_card)
        
        self.component_card = StatCard("BAĞLI BİLEŞEN", "0")
        layout.addWidget(self.component_card)
        
        # Degree stats group
        degree_group = QGroupBox("Derece İstatistikleri")
        degree_layout = QVBoxLayout(degree_group)
        
        self.max_degree_card = StatCard("MAX DERECE", "0")
        degree_layout.addWidget(self.max_degree_card)
        
        self.min_degree_card = StatCard("MIN DERECE", "0")
        degree_layout.addWidget(self.min_degree_card)
        
        layout.addWidget(degree_group)
        
        layout.addStretch()
    
    def update_stats(self):
        """Update all statistics from the graph."""
        if not self.graph:
            return
        
        stats = self.graph.get_statistics()
        
        self.node_card.set_value(str(stats['node_count']))
        self.edge_card.set_value(str(stats['edge_count']))
        self.density_card.set_value(f"{stats['density']:.4f}")
        self.avg_degree_card.set_value(f"{stats['average_degree']:.2f}")
        self.max_degree_card.set_value(str(stats['max_degree']))
        self.min_degree_card.set_value(str(stats['min_degree']))
        
        # Calculate k value (average degree)
        k = stats['average_degree']
        self.k_card.set_value(f"{k:.2f}")
        
        # Calculate connected components
        self._update_components()
    
    def _update_components(self):
        """Update connected components count."""
        if not self.graph.nodes:
            self.component_card.set_value("0")
            return
        
        # Simple component counting using BFS
        visited = set()
        components = 0
        
        for node_id in self.graph.nodes:
            if node_id not in visited:
                components += 1
                # BFS
                queue = [node_id]
                while queue:
                    current = queue.pop(0)
                    if current in visited:
                        continue
                    visited.add(current)
                    for neighbor in self.graph.get_neighbor_ids(current):
                        if neighbor not in visited:
                            queue.append(neighbor)
        
        self.component_card.set_value(str(components))

