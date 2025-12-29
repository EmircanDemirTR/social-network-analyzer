"""
Algorithm panel for running and visualizing graph algorithms.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel,
    QPushButton, QComboBox, QTableWidget, QTableWidgetItem,
    QHeaderView, QSpinBox, QFrame, QSplitter
)
from PyQt6.QtCore import Qt, pyqtSignal, QTimer
from PyQt6.QtGui import QColor

from ..models.graph import Graph
from ..algorithms import (
    BFS, DFS, Dijkstra, AStar,
    ConnectedComponents, DegreeCentrality, WelshPowell,
    AlgorithmResult
)
from .styles import DarkTheme


class AlgorithmPanel(QWidget):
    """
    Panel for running algorithms and displaying results.
    """
    
    algorithm_completed = pyqtSignal(object)  # AlgorithmResult
    legend_updated = pyqtSignal(str)  # Legend text
    
    def __init__(self, graph: Graph, canvas):
        super().__init__()
        self.graph = graph
        self.canvas = canvas
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)
        
        # Top section: buttons and parameters
        top_widget = QWidget()
        top_layout = QHBoxLayout(top_widget)
        top_layout.setContentsMargins(0, 0, 0, 0)
        
        # Algorithm buttons group
        buttons_group = QGroupBox("ALGORİTMALAR")
        buttons_layout = QVBoxLayout(buttons_group)
        
        # Row 1: Traversal and shortest path
        row1 = QHBoxLayout()
        
        self.bfs_btn = QPushButton("BFS")
        self.bfs_btn.setObjectName("algorithmButton")
        self.bfs_btn.clicked.connect(self._run_bfs)
        row1.addWidget(self.bfs_btn)
        
        self.dfs_btn = QPushButton("DFS")
        self.dfs_btn.setObjectName("algorithmButton")
        self.dfs_btn.clicked.connect(self._run_dfs)
        row1.addWidget(self.dfs_btn)
        
        self.dijkstra_btn = QPushButton("Dijkstra")
        self.dijkstra_btn.setObjectName("algorithmButton")
        self.dijkstra_btn.clicked.connect(self._run_dijkstra)
        row1.addWidget(self.dijkstra_btn)
        
        self.astar_btn = QPushButton("A*")
        self.astar_btn.setObjectName("algorithmButton")
        self.astar_btn.clicked.connect(self._run_astar)
        row1.addWidget(self.astar_btn)
        
        buttons_layout.addLayout(row1)
        
        # Row 2: Other algorithms
        row2 = QHBoxLayout()
        
        self.components_btn = QPushButton("Bileşenler")
        self.components_btn.setObjectName("algorithmButton")
        self.components_btn.clicked.connect(self._run_components)
        row2.addWidget(self.components_btn)
        
        self.centrality_btn = QPushButton("Merkezilik")
        self.centrality_btn.setObjectName("algorithmButton")
        self.centrality_btn.clicked.connect(self._run_centrality)
        row2.addWidget(self.centrality_btn)
        
        self.coloring_btn = QPushButton("Renklendirme")
        self.coloring_btn.setObjectName("algorithmButton")
        self.coloring_btn.clicked.connect(self._run_coloring)
        row2.addWidget(self.coloring_btn)
        
        self.reset_colors_btn = QPushButton("Renkleri Sıfırla")
        self.reset_colors_btn.clicked.connect(self._reset_colors)
        row2.addWidget(self.reset_colors_btn)
        
        self.clear_btn = QPushButton("Temizle")
        self.clear_btn.clicked.connect(self._clear_results)
        row2.addWidget(self.clear_btn)
        
        buttons_layout.addLayout(row2)
        
        top_layout.addWidget(buttons_group)
        
        # Parameters group
        params_group = QGroupBox("PARAMETRELER")
        params_layout = QVBoxLayout(params_group)
        
        # Start node selector
        start_layout = QHBoxLayout()
        start_layout.addWidget(QLabel("Başlangıç:"))
        self.start_combo = QComboBox()
        self.start_combo.setMinimumWidth(120)
        start_layout.addWidget(self.start_combo)
        params_layout.addLayout(start_layout)
        
        # End node selector
        end_layout = QHBoxLayout()
        end_layout.addWidget(QLabel("Hedef:"))
        self.end_combo = QComboBox()
        self.end_combo.setMinimumWidth(120)
        end_layout.addWidget(self.end_combo)
        params_layout.addLayout(end_layout)
        
        # Top K selector
        topk_layout = QHBoxLayout()
        topk_layout.addWidget(QLabel("Top K:"))
        self.topk_spin = QSpinBox()
        self.topk_spin.setRange(1, 20)
        self.topk_spin.setValue(5)
        topk_layout.addWidget(self.topk_spin)
        params_layout.addLayout(topk_layout)
        
        # Refresh button
        refresh_btn = QPushButton("Listeyi Yenile")
        refresh_btn.clicked.connect(self._refresh_combos)
        params_layout.addWidget(refresh_btn)
        
        top_layout.addWidget(params_group)
        
        # Result info
        result_group = QGroupBox("SONUÇ")
        result_layout = QVBoxLayout(result_group)
        
        self.result_label = QLabel("Algoritma seçin ve çalıştırın")
        self.result_label.setWordWrap(True)
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        result_layout.addWidget(self.result_label)
        
        self.time_label = QLabel("Süre: -")
        self.time_label.setStyleSheet(f"color: {DarkTheme.COLORS['neon_green']};")
        result_layout.addWidget(self.time_label)
        
        top_layout.addWidget(result_group)
        
        layout.addWidget(top_widget)
        
        # Bottom section: result table (larger)
        self.result_table = QTableWidget()
        self.result_table.setColumnCount(5)
        self.result_table.setHorizontalHeaderLabels(
            ["Sıra", "Düğüm ID", "Düğüm Adı", "Değer", "Ek Bilgi"]
        )
        self.result_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )
        self.result_table.setMinimumHeight(250)
        layout.addWidget(self.result_table, stretch=2)
    
    def _refresh_combos(self):
        """Refresh node selection combo boxes."""
        self.start_combo.clear()
        self.end_combo.clear()
        
        for node in self.graph.nodes.values():
            item_text = f"{node.id} - {node.name}"
            self.start_combo.addItem(item_text)
            self.end_combo.addItem(item_text)
    
    def _get_selected_start_id(self) -> int:
        """Get selected start node ID."""
        text = self.start_combo.currentText()
        if text:
            try:
                return int(text.split(" ")[0])
            except (ValueError, IndexError):
                pass
        
        # Default to first node
        if self.graph.nodes:
            return list(self.graph.nodes.keys())[0]
        return -1
    
    def _get_selected_end_id(self) -> int:
        """Get selected end node ID."""
        text = self.end_combo.currentText()
        if text:
            try:
                return int(text.split(" ")[0])
            except (ValueError, IndexError):
                pass
        
        # Default to last node
        if self.graph.nodes:
            return list(self.graph.nodes.keys())[-1]
        return -1
    
    def _display_result(self, result: AlgorithmResult):
        """Display algorithm result."""
        self.result_label.setText(result.message)
        self.time_label.setText(f"Süre: {result.execution_time * 1000:.3f} ms")
        self.algorithm_completed.emit(result)
    
    def _populate_table(self, headers: list, rows: list):
        """Populate the result table."""
        self.result_table.clear()
        self.result_table.setColumnCount(len(headers))
        self.result_table.setHorizontalHeaderLabels(headers)
        self.result_table.setRowCount(len(rows))
        
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.result_table.setItem(i, j, item)
    
    def _run_bfs(self):
        """Run BFS algorithm."""
        if not self.graph.nodes:
            self.result_label.setText("Graf boş!")
            return
        
        start_id = self._get_selected_start_id()
        if start_id < 0:
            return
        
        self.canvas._clear_all_highlights()
        
        algo = BFS(self.graph)
        result = algo.execute(start_node_id=start_id)
        
        if result.success:
            # Color by level - gradient from cyan to purple
            levels = result.data['levels']
            max_level = max(levels.values()) if levels else 0
            
            level_colors = [
                (0, 217, 255),    # Cyan - level 0
                (0, 255, 136),    # Green
                (255, 215, 0),    # Gold
                (255, 107, 107),  # Coral
                (180, 41, 249),   # Purple
                (255, 46, 151),   # Pink
            ]
            
            for node_id, level in levels.items():
                color_idx = level % len(level_colors)
                color = level_colors[color_idx]
                self.graph.nodes[node_id].set_highlight(True, color)
                if node_id in self.canvas._node_items:
                    self.canvas._node_items[node_id].update_appearance()
            
            # Populate table
            headers = ["Sıra", "Düğüm ID", "Düğüm Adı", "Seviye", ""]
            rows = []
            visit_order = result.data['visit_order']
            for i, node_id in enumerate(visit_order):
                node = self.graph.nodes[node_id]
                level = levels.get(node_id, 0)
                rows.append([i + 1, node_id, node.name, level, ""])
            self._populate_table(headers, rows)
            
            # Update legend
            self.legend_updated.emit(
                "BFS Renkleri (Seviyeye Göre):\n"
                "• Cyan: Seviye 0 (Başlangıç)\n"
                "• Yeşil: Seviye 1\n"
                "• Altın: Seviye 2\n"
                "• Mercan: Seviye 3\n"
                "• Mor: Seviye 4\n"
                "• Pembe: Seviye 5+"
            )
        
        self._display_result(result)
    
    def _run_dfs(self):
        """Run DFS algorithm."""
        if not self.graph.nodes:
            self.result_label.setText("Graf boş!")
            return
        
        start_id = self._get_selected_start_id()
        if start_id < 0:
            return
        
        self.canvas._clear_all_highlights()
        
        algo = DFS(self.graph)
        result = algo.execute(start_node_id=start_id)
        
        if result.success:
            visit_order = result.data['visit_order']
            discovery_times = result.data['discovery_time']
            max_disc = max(discovery_times.values()) if discovery_times else 1
            
            # Color by discovery time - gradient
            for node_id in visit_order:
                disc = discovery_times.get(node_id, 0)
                # Interpolate from green to purple based on discovery time
                ratio = disc / max_disc if max_disc > 0 else 0
                r = int(0 + ratio * 180)
                g = int(255 - ratio * 214)
                b = int(136 + ratio * 113)
                self.graph.nodes[node_id].set_highlight(True, (r, g, b))
                if node_id in self.canvas._node_items:
                    self.canvas._node_items[node_id].update_appearance()
            
            headers = ["Sıra", "Düğüm ID", "Düğüm Adı", "Keşif", "Bitiş"]
            rows = []
            for i, node_id in enumerate(visit_order):
                node = self.graph.nodes[node_id]
                disc = discovery_times.get(node_id, 0)
                fin = result.data['finish_time'].get(node_id, 0)
                rows.append([i + 1, node_id, node.name, disc, fin])
            self._populate_table(headers, rows)
            
            # Update legend
            self.legend_updated.emit(
                "DFS Renkleri (Keşif Zamanına Göre):\n"
                "• Yeşil: İlk keşfedilen\n"
                "• Gradient → Mor: Son keşfedilen\n"
                "Erken keşif = Yeşil\n"
                "Geç keşif = Mor"
            )
        
        self._display_result(result)
    
    def _run_dijkstra(self):
        """Run Dijkstra's algorithm."""
        if not self.graph.nodes:
            self.result_label.setText("Graf boş!")
            return
        
        start_id = self._get_selected_start_id()
        end_id = self._get_selected_end_id()
        
        if start_id < 0 or end_id < 0:
            return
        
        self.canvas._clear_all_highlights()
        
        algo = Dijkstra(self.graph)
        result = algo.execute(start_node_id=start_id, end_node_id=end_id)
        
        if result.success:
            path = result.data['path']
            self.canvas.highlight_path(path, (180, 41, 249))
            
            headers = ["Sıra", "Düğüm ID", "Düğüm Adı", "Mesafe", ""]
            rows = []
            for i, node_id in enumerate(path):
                node = self.graph.nodes[node_id]
                dist = result.data['distances'].get(node_id, 0)
                rows.append([i + 1, node_id, node.name, f"{dist:.3f}", ""])
            self._populate_table(headers, rows)
            
            # Update legend
            self.legend_updated.emit(
                "Dijkstra En Kısa Yol:\n"
                "• Mor: Bulunan yol üzerindeki\n"
                "  düğümler ve kenarlar\n"
                f"• Toplam maliyet: {result.data['total_cost']:.3f}"
            )
        
        self._display_result(result)
    
    def _run_astar(self):
        """Run A* algorithm."""
        if not self.graph.nodes:
            self.result_label.setText("Graf boş!")
            return
        
        start_id = self._get_selected_start_id()
        end_id = self._get_selected_end_id()
        
        if start_id < 0 or end_id < 0:
            return
        
        self.canvas._clear_all_highlights()
        
        algo = AStar(self.graph)
        result = algo.execute(start_node_id=start_id, end_node_id=end_id)
        
        if result.success:
            path = result.data['path']
            self.canvas.highlight_path(path, (255, 46, 151))
            
            headers = ["Sıra", "Düğüm ID", "Düğüm Adı", "Maliyet", ""]
            rows = []
            for i, node_id in enumerate(path):
                node = self.graph.nodes[node_id]
                rows.append([i + 1, node_id, node.name, f"{result.data['total_cost']:.3f}" if i == len(path)-1 else "-", ""])
            self._populate_table(headers, rows)
            
            # Update legend
            self.legend_updated.emit(
                "A* En Kısa Yol:\n"
                "• Pembe: Bulunan yol üzerindeki\n"
                "  düğümler ve kenarlar\n"
                f"• Toplam maliyet: {result.data['total_cost']:.3f}\n"
                f"• Keşfedilen: {result.data['nodes_explored']} düğüm"
            )
        
        self._display_result(result)
    
    def _run_components(self):
        """Run connected components algorithm."""
        if not self.graph.nodes:
            self.result_label.setText("Graf boş!")
            return
        
        self.canvas._clear_all_highlights()
        
        algo = ConnectedComponents(self.graph)
        result = algo.execute()
        
        if result.success:
            # Color each component differently
            for comp_detail in result.data['component_details']:
                color = comp_detail['color']
                for node_id in comp_detail['nodes']:
                    self.graph.nodes[node_id].set_highlight(True, color)
            
            self.canvas.refresh()
            
            headers = ["Bileşen", "Boyut", "Düğümler", "", ""]
            rows = []
            for comp in result.data['component_details']:
                node_names = [self.graph.nodes[nid].name for nid in comp['nodes'][:3]]
                more = "..." if len(comp['nodes']) > 3 else ""
                rows.append([comp['index'] + 1, comp['size'], 
                           ", ".join(node_names) + more, "", ""])
            self._populate_table(headers, rows)
            
            # Update legend
            legend = f"Bağlı Bileşenler ({result.data['component_count']} adet):\n"
            for comp in result.data['component_details'][:5]:
                legend += f"• Bileşen {comp['index']+1}: {comp['size']} düğüm\n"
            if result.data['component_count'] > 5:
                legend += f"... ve {result.data['component_count']-5} bileşen daha"
            self.legend_updated.emit(legend)
        
        self._display_result(result)
    
    def _run_centrality(self):
        """Run degree centrality algorithm."""
        if not self.graph.nodes:
            self.result_label.setText("Graf boş!")
            return
        
        self.canvas._clear_all_highlights()
        
        top_k = self.topk_spin.value()
        algo = DegreeCentrality(self.graph)
        result = algo.execute(top_k=top_k)
        
        if result.success:
            centrality = result.data['centrality']
            max_cent = max(centrality.values()) if centrality else 1
            min_cent = min(centrality.values()) if centrality else 0
            
            # Color all nodes by centrality - red (high) to blue (low)
            for node_id, cent in centrality.items():
                if max_cent > min_cent:
                    ratio = (cent - min_cent) / (max_cent - min_cent)
                else:
                    ratio = 0.5
                # Low centrality = blue, high centrality = gold/red
                r = int(0 + ratio * 255)
                g = int(217 - ratio * 2)
                b = int(255 - ratio * 200)
                self.graph.nodes[node_id].set_highlight(True, (r, g, b))
                if node_id in self.canvas._node_items:
                    self.canvas._node_items[node_id].update_appearance()
            
            # Scale nodes by centrality
            self.canvas.scale_nodes_by_centrality(centrality)
            
            headers = ["Sıra", "Düğüm ID", "Düğüm Adı", "Derece", "Merkezilik"]
            rows = []
            for item in result.data['top_k']:
                rows.append([item['rank'], item['node_id'], item['name'],
                           item['degree'], f"{item['centrality']:.4f}"])
            self._populate_table(headers, rows)
            
            # Update legend
            self.legend_updated.emit(
                "Derece Merkeziliği:\n"
                "• Mavi: Düşük merkezilik\n"
                "• Altın/Turuncu: Yüksek merkezilik\n"
                "Düğüm boyutu = Bağlantı sayısı\n"
                f"Max derece: {result.data['statistics']['max_degree']}"
            )
        
        self._display_result(result)
    
    def _run_coloring(self):
        """Run Welsh-Powell coloring algorithm."""
        if not self.graph.nodes:
            self.result_label.setText("Graf boş!")
            return
        
        self.canvas._clear_all_highlights()
        
        algo = WelshPowell(self.graph)
        result = algo.execute()
        
        if result.success:
            # Apply colors to nodes
            self.canvas.apply_coloring(
                result.data['coloring'],
                algo.COLORS
            )
            
            headers = ["Renk", "Renk Adı", "Düğüm Sayısı", "Düğümler", ""]
            rows = []
            for color_info in result.data['color_table']:
                node_names = color_info['node_names'][:3]
                more = "..." if len(color_info['node_names']) > 3 else ""
                rows.append([
                    color_info['color_index'] + 1,
                    color_info['color_name'],
                    color_info['count'],
                    ", ".join(node_names) + more,
                    ""
                ])
            self._populate_table(headers, rows)
            
            # Update chromatic number in result message
            result.message = f"Graf {result.data['chromatic_number']} renk ile boyandı (Kromatik Sayı: {result.data['chromatic_number']})"
            
            # Update legend
            legend = f"Welsh-Powell Renklendirme:\n"
            legend += f"Kromatik Sayı: {result.data['chromatic_number']}\n"
            for color_info in result.data['color_table'][:6]:
                legend += f"• {color_info['color_name']}: {color_info['count']} düğüm\n"
            self.legend_updated.emit(legend)
        
        self._display_result(result)
    
    def _reset_colors(self):
        """Reset all node colors to default."""
        default_color = (0, 217, 255)  # Neon blue
        for node in self.graph.nodes.values():
            node.color = default_color
            node.set_highlight(False)
        self.canvas.refresh()
        self.result_label.setText("Renkler sıfırlandı")
        self.legend_updated.emit("Renkler sıfırlandı.\nAlgoritma çalıştırıldığında\nrenk açıklaması burada görünür.")
    
    def _clear_results(self):
        """Clear all results and highlights."""
        self.canvas._clear_all_highlights()
        self.canvas.refresh()
        self.result_table.setRowCount(0)
        self.result_label.setText("Sonuçlar temizlendi")
        self.time_label.setText("Süre: -")
        self.legend_updated.emit("Sonuçlar temizlendi.\nAlgoritma çalıştırıldığında\nrenk açıklaması burada görünür.")

