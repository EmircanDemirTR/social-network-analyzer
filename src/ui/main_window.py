"""
Main application window for Social Network Analyzer.
"""
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QMenuBar, QMenu, QStatusBar, QLabel,
    QFileDialog, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QIcon
import json
import os

from .styles import DarkTheme
from .graph_canvas import GraphCanvas
from .control_panel import ControlPanel
from .stats_panel import StatsPanel
from .algorithm_panel import AlgorithmPanel
from ..models.graph import Graph


class MainWindow(QMainWindow):
    """
    Main application window containing all UI components.
    """
    
    def __init__(self):
        super().__init__()
        
        self.graph = Graph()
        self.setWindowTitle("Sosyal Ağ Analizi - Social Network Analyzer")
        self.setMinimumSize(1400, 900)
        self.resize(1600, 1000)
        
        # Apply dark theme
        self.setStyleSheet(DarkTheme.get_stylesheet())
        
        # Initialize UI
        self._init_ui()
        self._init_menu()
        self._init_status_bar()
        self._init_connections()
        
        # Start stats update timer
        self._stats_timer = QTimer(self)
        self._stats_timer.timeout.connect(self._update_stats)
        self._stats_timer.start(500)  # Update every 500ms
    
    def _init_ui(self):
        """Initialize the main UI layout."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Left panel - Control panel
        self.control_panel = ControlPanel(self.graph)
        self.control_panel.setFixedWidth(260)
        
        # Center - Graph canvas and algorithm panel
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setContentsMargins(0, 0, 0, 0)
        center_layout.setSpacing(10)
        
        self.graph_canvas = GraphCanvas(self.graph)
        self.algorithm_panel = AlgorithmPanel(self.graph, self.graph_canvas)
        self.algorithm_panel.setMinimumHeight(400)
        
        center_layout.addWidget(self.graph_canvas, stretch=2)
        center_layout.addWidget(self.algorithm_panel, stretch=2)
        
        # Right panel - Stats panel
        self.stats_panel = StatsPanel(self.graph)
        self.stats_panel.setFixedWidth(220)
        
        # Add to main layout
        main_layout.addWidget(self.control_panel)
        main_layout.addWidget(center_widget, stretch=1)
        main_layout.addWidget(self.stats_panel)
    
    def _init_menu(self):
        """Initialize the menu bar."""
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("Dosya")
        
        new_action = QAction("Yeni Graf", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self._new_graph)
        file_menu.addAction(new_action)
        
        file_menu.addSeparator()
        
        import_json_action = QAction("JSON İçe Aktar...", self)
        import_json_action.setShortcut("Ctrl+O")
        import_json_action.triggered.connect(self._import_json)
        file_menu.addAction(import_json_action)
        
        import_csv_action = QAction("CSV İçe Aktar...", self)
        import_csv_action.triggered.connect(self._import_csv)
        file_menu.addAction(import_csv_action)
        
        file_menu.addSeparator()
        
        export_json_action = QAction("JSON Dışa Aktar...", self)
        export_json_action.setShortcut("Ctrl+S")
        export_json_action.triggered.connect(self._export_json)
        file_menu.addAction(export_json_action)
        
        export_csv_action = QAction("CSV Dışa Aktar...", self)
        export_csv_action.triggered.connect(self._export_csv)
        file_menu.addAction(export_csv_action)
        
        export_adj_list_action = QAction("Komşuluk Listesi Aktar...", self)
        export_adj_list_action.triggered.connect(self._export_adjacency_list)
        file_menu.addAction(export_adj_list_action)
        
        export_adj_matrix_action = QAction("Komşuluk Matrisi Aktar...", self)
        export_adj_matrix_action.triggered.connect(self._export_adjacency_matrix)
        file_menu.addAction(export_adj_matrix_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Çıkış", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit Menu
        edit_menu = menubar.addMenu("Düzenle")
        
        clear_action = QAction("Seçimleri Temizle", self)
        clear_action.setShortcut("Escape")
        clear_action.triggered.connect(self._clear_selections)
        edit_menu.addAction(clear_action)
        
        clear_highlights_action = QAction("Vurguları Temizle", self)
        clear_highlights_action.triggered.connect(self._clear_highlights)
        edit_menu.addAction(clear_highlights_action)
        
        # View Menu
        view_menu = menubar.addMenu("Görünüm")
        
        fit_action = QAction("Sığdır", self)
        fit_action.setShortcut("Ctrl+0")
        fit_action.triggered.connect(self.graph_canvas.fit_in_view)
        view_menu.addAction(fit_action)
        
        zoom_in_action = QAction("Yakınlaştır", self)
        zoom_in_action.setShortcut("Ctrl++")
        zoom_in_action.triggered.connect(lambda: self.graph_canvas.zoom(1.2))
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction("Uzaklaştır", self)
        zoom_out_action.setShortcut("Ctrl+-")
        zoom_out_action.triggered.connect(lambda: self.graph_canvas.zoom(0.8))
        view_menu.addAction(zoom_out_action)
        
        # Help Menu
        help_menu = menubar.addMenu("Yardım")
        
        about_action = QAction("Hakkında", self)
        about_action.triggered.connect(self._show_about)
        help_menu.addAction(about_action)
    
    def _init_status_bar(self):
        """Initialize the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        self.status_label = QLabel("Hazır")
        self.status_bar.addWidget(self.status_label)
        
        self.node_status = QLabel("Düğüm: -")
        self.status_bar.addPermanentWidget(self.node_status)
    
    def _init_connections(self):
        """Initialize signal connections between components."""
        # Control panel connections
        self.control_panel.node_added.connect(self._on_node_added)
        self.control_panel.edge_added.connect(self._on_edge_added)
        self.control_panel.auto_layout_requested.connect(self.graph_canvas.auto_layout)
        
        # Canvas connections
        self.graph_canvas.node_selected.connect(self._on_node_selected)
        self.graph_canvas.node_deleted.connect(self._on_node_deleted)
        self.graph_canvas.edge_deleted.connect(self._on_edge_deleted)
        self.graph_canvas.status_message.connect(self._show_status)
        
        # Algorithm panel connections
        self.algorithm_panel.algorithm_completed.connect(self._on_algorithm_completed)
        self.algorithm_panel.legend_updated.connect(self.control_panel.set_legend)
    
    def _on_node_added(self, node):
        """Handle node addition from control panel."""
        self.graph_canvas.refresh()
        self._update_stats()
        self._show_status(f"Düğüm eklendi: {node.name}")
    
    def _on_edge_added(self, edge):
        """Handle edge addition from control panel."""
        self.graph_canvas.refresh()
        self._update_stats()
        self._show_status(f"Bağlantı eklendi: {edge.source.name} - {edge.target.name}")
    
    def _on_node_selected(self, node_id):
        """Handle node selection on canvas."""
        if node_id >= 0:
            node = self.graph.nodes.get(node_id)
            if node:
                self.node_status.setText(f"Seçili: {node.name} (ID: {node_id})")
                self.control_panel.set_selected_node(node)
        else:
            self.node_status.setText("Düğüm: -")
            self.control_panel.set_selected_node(None)
    
    def _on_node_deleted(self, node_id):
        """Handle node deletion."""
        self._update_stats()
        self._show_status(f"Düğüm silindi: ID {node_id}")
    
    def _on_edge_deleted(self, source_id, target_id):
        """Handle edge deletion."""
        self._update_stats()
        self._show_status(f"Bağlantı silindi: {source_id} - {target_id}")
    
    def _on_algorithm_completed(self, result):
        """Handle algorithm completion."""
        self._show_status(f"{result.name}: {result.message}")
    
    def _update_stats(self):
        """Update statistics panel."""
        self.stats_panel.update_stats()
    
    def _show_status(self, message):
        """Show message in status bar."""
        self.status_label.setText(message)
    
    def _new_graph(self):
        """Create a new empty graph."""
        reply = QMessageBox.question(
            self, "Yeni Graf",
            "Mevcut graf silinecek. Devam etmek istiyor musunuz?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.graph.clear()
            self.graph_canvas.refresh()
            self._update_stats()
            self._show_status("Yeni graf oluşturuldu")
    
    def _import_json(self):
        """Import graph from JSON file."""
        filename, _ = QFileDialog.getOpenFileName(
            self, "JSON Dosyası Seç", "", "JSON Files (*.json)"
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                self.graph = Graph.from_dict(data)
                self.graph_canvas.set_graph(self.graph)
                self.control_panel.graph = self.graph
                self.stats_panel.graph = self.graph
                self.algorithm_panel.graph = self.graph
                
                self._update_stats()
                self._show_status(f"Graf yüklendi: {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Dosya yüklenemedi:\n{str(e)}")
    
    def _import_csv(self):
        """Import graph from CSV file."""
        filename, _ = QFileDialog.getOpenFileName(
            self, "CSV Dosyası Seç", "", "CSV Files (*.csv)"
        )
        
        if filename:
            try:
                from ..utils.data_handler import DataHandler
                self.graph = DataHandler.import_csv(filename)
                self.graph_canvas.set_graph(self.graph)
                self.control_panel.graph = self.graph
                self.stats_panel.graph = self.graph
                self.algorithm_panel.graph = self.graph
                
                self._update_stats()
                self._show_status(f"Graf yüklendi: {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Dosya yüklenemedi:\n{str(e)}")
    
    def _export_json(self):
        """Export graph to JSON file."""
        filename, _ = QFileDialog.getSaveFileName(
            self, "JSON Olarak Kaydet", "graph.json", "JSON Files (*.json)"
        )
        
        if filename:
            try:
                data = self.graph.to_dict()
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                self._show_status(f"Graf kaydedildi: {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Dosya kaydedilemedi:\n{str(e)}")
    
    def _export_csv(self):
        """Export graph to CSV file."""
        filename, _ = QFileDialog.getSaveFileName(
            self, "CSV Olarak Kaydet", "graph.csv", "CSV Files (*.csv)"
        )
        
        if filename:
            try:
                from ..utils.data_handler import DataHandler
                DataHandler.export_csv(self.graph, filename)
                self._show_status(f"Graf kaydedildi: {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Dosya kaydedilemedi:\n{str(e)}")
    
    def _export_adjacency_list(self):
        """Export adjacency list to file."""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Komşuluk Listesi Kaydet", "adjacency_list.txt", "Text Files (*.txt)"
        )
        
        if filename:
            try:
                adj_list = self.graph.get_adjacency_list()
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("# Komşuluk Listesi\n")
                    f.write("# Format: DüğümID: [Komşu1, Komşu2, ...]\n\n")
                    for node_id, neighbors in sorted(adj_list.items()):
                        node_name = self.graph.nodes[node_id].name
                        neighbor_names = [self.graph.nodes[n].name for n in neighbors]
                        f.write(f"{node_id} ({node_name}): {neighbors}\n")
                        f.write(f"  İsimler: {neighbor_names}\n")
                self._show_status(f"Komşuluk listesi kaydedildi: {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Dosya kaydedilemedi:\n{str(e)}")
    
    def _export_adjacency_matrix(self):
        """Export adjacency matrix to file."""
        filename, _ = QFileDialog.getSaveFileName(
            self, "Komşuluk Matrisi Kaydet", "adjacency_matrix.txt", "Text Files (*.txt)"
        )
        
        if filename:
            try:
                matrix, node_ids = self.graph.get_adjacency_matrix()
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write("# Komşuluk Matrisi\n")
                    f.write(f"# Düğüm sırası: {node_ids}\n\n")
                    
                    # Header
                    f.write("     " + " ".join(f"{nid:5}" for nid in node_ids) + "\n")
                    f.write("-" * (6 + 6 * len(node_ids)) + "\n")
                    
                    # Matrix rows
                    for i, row in enumerate(matrix):
                        f.write(f"{node_ids[i]:4}|")
                        f.write(" ".join(f"{val:5.2f}" for val in row) + "\n")
                
                self._show_status(f"Komşuluk matrisi kaydedildi: {filename}")
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Dosya kaydedilemedi:\n{str(e)}")
    
    def _clear_selections(self):
        """Clear all selections on canvas."""
        self.graph_canvas.clear_selection()
        self._on_node_selected(-1)
    
    def _clear_highlights(self):
        """Clear all highlights."""
        self.graph.clear_highlights()
        self.graph_canvas.refresh()
        self._show_status("Vurgular temizlendi")
    
    def _show_about(self):
        """Show about dialog."""
        QMessageBox.about(
            self,
            "Hakkında",
            """<h2>Sosyal Ağ Analizi</h2>
            <p>Versiyon 1.0.0</p>
            <p>Kocaeli Üniversitesi<br>
            Teknoloji Fakültesi<br>
            Bilişim Sistemleri Mühendisliği</p>
            <p>Yazılım Geliştirme Laboratuvarı-I<br>
            Proje 2</p>
            <hr>
            <p>Graf algoritmalarını görselleştiren ve<br>
            sosyal ağ analizleri yapan bir uygulama.</p>"""
        )
    
    def closeEvent(self, event):
        """Handle window close event."""
        reply = QMessageBox.question(
            self, "Çıkış",
            "Uygulamadan çıkmak istiyor musunuz?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            event.accept()
        else:
            event.ignore()

