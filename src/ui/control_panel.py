"""
Control panel for graph manipulation.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel,
    QPushButton, QLineEdit, QDoubleSpinBox,
    QComboBox, QFormLayout
)
from PyQt6.QtCore import Qt, pyqtSignal

from ..models.graph import Graph
from ..models.node import Node
from .styles import DarkTheme


class ControlPanel(QWidget):
    """
    Control panel for adding/editing nodes and edges.
    """
    
    # Signals
    node_added = pyqtSignal(object)  # Node
    edge_added = pyqtSignal(object)  # Edge
    auto_layout_requested = pyqtSignal()
    
    def __init__(self, graph: Graph):
        super().__init__()
        self.graph = graph
        self._selected_node = None
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        
        # Title
        title = QLabel("KONTROL PANELİ")
        title.setObjectName("titleLabel")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # Node controls
        layout.addWidget(self._create_node_group())
        
        # Edge controls
        layout.addWidget(self._create_edge_group())
        
        # Layout controls
        layout.addWidget(self._create_layout_group())
        
        # Selected node info
        layout.addWidget(self._create_info_group())
        
        # Color legend
        layout.addWidget(self._create_legend_group())
        
        layout.addStretch()
    
    def _create_node_group(self) -> QGroupBox:
        """Create node controls group."""
        group = QGroupBox("Düğüm İşlemleri")
        layout = QVBoxLayout(group)
        
        # Node name input
        name_layout = QHBoxLayout()
        name_layout.addWidget(QLabel("İsim:"))
        self.node_name_input = QLineEdit()
        self.node_name_input.setPlaceholderText("Kullanıcı adı")
        name_layout.addWidget(self.node_name_input)
        layout.addLayout(name_layout)
        
        # Properties
        props_layout = QFormLayout()
        
        self.activity_input = QDoubleSpinBox()
        self.activity_input.setRange(0.0, 1.0)
        self.activity_input.setSingleStep(0.1)
        self.activity_input.setValue(0.5)
        props_layout.addRow("Aktivite:", self.activity_input)
        
        self.interaction_input = QDoubleSpinBox()
        self.interaction_input.setRange(0, 100)
        self.interaction_input.setSingleStep(1)
        self.interaction_input.setValue(10)
        props_layout.addRow("Etkileşim:", self.interaction_input)
        
        layout.addLayout(props_layout)
        
        # Add button
        add_node_btn = QPushButton("+ Düğüm Ekle")
        add_node_btn.setObjectName("primaryButton")
        add_node_btn.clicked.connect(self._add_node)
        layout.addWidget(add_node_btn)
        
        return group
    
    def _create_edge_group(self) -> QGroupBox:
        """Create edge controls group."""
        group = QGroupBox("Bağlantı İşlemleri")
        layout = QVBoxLayout(group)
        
        # Source and target selection
        source_layout = QHBoxLayout()
        source_layout.addWidget(QLabel("Kaynak:"))
        self.source_combo = QComboBox()
        self.source_combo.setMinimumWidth(100)
        source_layout.addWidget(self.source_combo)
        layout.addLayout(source_layout)
        
        target_layout = QHBoxLayout()
        target_layout.addWidget(QLabel("Hedef:"))
        self.target_combo = QComboBox()
        self.target_combo.setMinimumWidth(100)
        target_layout.addWidget(self.target_combo)
        layout.addLayout(target_layout)
        
        # Add edge button
        add_edge_btn = QPushButton("+ Bağlantı Ekle")
        add_edge_btn.clicked.connect(self._add_edge)
        layout.addWidget(add_edge_btn)
        
        # Refresh combos button
        refresh_btn = QPushButton("Listeyi Yenile")
        refresh_btn.clicked.connect(self._refresh_combos)
        layout.addWidget(refresh_btn)
        
        return group
    
    def _create_layout_group(self) -> QGroupBox:
        """Create layout controls group."""
        group = QGroupBox("Yerleşim")
        layout = QVBoxLayout(group)
        
        # Auto layout button
        auto_btn = QPushButton("Otomatik Yerleşim")
        auto_btn.setObjectName("primaryButton")
        auto_btn.clicked.connect(self.auto_layout_requested.emit)
        layout.addWidget(auto_btn)
        
        # Help text
        help_label = QLabel("Graf yapısına göre düğümleri\notomatik olarak konumlandırır")
        help_label.setStyleSheet("color: #6c7a89; font-size: 10px;")
        help_label.setWordWrap(True)
        layout.addWidget(help_label)
        
        return group
    
    def _create_info_group(self) -> QGroupBox:
        """Create selected node info group."""
        group = QGroupBox("Seçili Düğüm")
        layout = QFormLayout(group)
        
        self.info_name = QLabel("-")
        layout.addRow("İsim:", self.info_name)
        
        self.info_id = QLabel("-")
        layout.addRow("ID:", self.info_id)
        
        self.info_degree = QLabel("-")
        layout.addRow("Derece:", self.info_degree)
        
        self.info_activity = QLabel("-")
        layout.addRow("Aktivite:", self.info_activity)
        
        self.info_interaction = QLabel("-")
        layout.addRow("Etkileşim:", self.info_interaction)
        
        return group
    
    def _add_node(self):
        """Add a new node to the graph."""
        name = self.node_name_input.text().strip()
        activity = self.activity_input.value()
        interaction = self.interaction_input.value()
        
        try:
            node = self.graph.add_node(
                name=name if name else None,
                activity=activity,
                interaction=interaction
            )
            
            self.node_name_input.clear()
            self._refresh_combos()
            self.node_added.emit(node)
        except ValueError as e:
            pass  # Node already exists
    
    def _add_edge(self):
        """Add a new edge to the graph."""
        source_text = self.source_combo.currentText()
        target_text = self.target_combo.currentText()
        
        if not source_text or not target_text:
            return
        
        try:
            source_id = int(source_text.split(" ")[0])
            target_id = int(target_text.split(" ")[0])
            
            edge = self.graph.add_edge(source_id, target_id)
            if edge:
                self.edge_added.emit(edge)
        except (ValueError, IndexError):
            pass
    
    def _refresh_combos(self):
        """Refresh the node selection combo boxes."""
        self.source_combo.clear()
        self.target_combo.clear()
        
        for node in self.graph.nodes.values():
            item_text = f"{node.id} - {node.name}"
            self.source_combo.addItem(item_text)
            self.target_combo.addItem(item_text)
    
    def set_selected_node(self, node):
        """Update the selected node info display."""
        self._selected_node = node
        
        if node:
            self.info_name.setText(node.name)
            self.info_id.setText(str(node.id))
            self.info_degree.setText(str(self.graph.get_degree(node.id)))
            self.info_activity.setText(f"{node.activity:.2f}")
            self.info_interaction.setText(f"{node.interaction:.2f}")
        else:
            self.info_name.setText("-")
            self.info_id.setText("-")
            self.info_degree.setText("-")
            self.info_activity.setText("-")
            self.info_interaction.setText("-")
    
    def _create_legend_group(self) -> QGroupBox:
        """Create color legend group."""
        group = QGroupBox("Renk Açıklaması")
        layout = QVBoxLayout(group)
        
        self.legend_label = QLabel("Algoritma çalıştırıldığında\nrenk açıklaması burada görünür")
        self.legend_label.setStyleSheet("color: #6c7a89; font-size: 10px;")
        self.legend_label.setWordWrap(True)
        layout.addWidget(self.legend_label)
        
        return group
    
    def set_legend(self, legend_text: str):
        """Update the color legend text."""
        self.legend_label.setText(legend_text)
        self.legend_label.setStyleSheet("color: #eaeaea; font-size: 11px;")

