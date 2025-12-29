"""
Dialog for editing node properties.
"""
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QDoubleSpinBox, QPushButton,
    QGroupBox
)
from PyQt6.QtCore import Qt

from ..models.node import Node
from .styles import DarkTheme


class NodeDialog(QDialog):
    """
    Dialog for viewing and editing node properties.
    """
    
    def __init__(self, node: Node, parent=None):
        super().__init__(parent)
        self.node = node
        self._init_ui()
    
    def _init_ui(self):
        """Initialize the dialog UI."""
        self.setWindowTitle(f"Düğüm Düzenle - {self.node.name}")
        self.setMinimumWidth(300)
        self.setStyleSheet(DarkTheme.get_stylesheet())
        
        layout = QVBoxLayout(self)
        
        # Basic info group
        basic_group = QGroupBox("Temel Bilgiler")
        basic_layout = QFormLayout(basic_group)
        
        self.id_label = QLabel(str(self.node.id))
        basic_layout.addRow("ID:", self.id_label)
        
        self.name_input = QLineEdit(self.node.name)
        basic_layout.addRow("İsim:", self.name_input)
        
        layout.addWidget(basic_group)
        
        # Properties group
        props_group = QGroupBox("Özellikler")
        props_layout = QFormLayout(props_group)
        
        self.activity_input = QDoubleSpinBox()
        self.activity_input.setRange(0.0, 1.0)
        self.activity_input.setSingleStep(0.1)
        self.activity_input.setDecimals(2)
        self.activity_input.setValue(self.node.activity)
        props_layout.addRow("Aktivite:", self.activity_input)
        
        self.interaction_input = QDoubleSpinBox()
        self.interaction_input.setRange(0, 1000)
        self.interaction_input.setSingleStep(1)
        self.interaction_input.setDecimals(2)
        self.interaction_input.setValue(self.node.interaction)
        props_layout.addRow("Etkileşim:", self.interaction_input)
        
        self.connection_label = QLabel(str(self.node.connection_count))
        props_layout.addRow("Bağlantı Sayısı:", self.connection_label)
        
        layout.addWidget(props_group)
        
        # Position group
        pos_group = QGroupBox("Konum")
        pos_layout = QFormLayout(pos_group)
        
        self.x_input = QDoubleSpinBox()
        self.x_input.setRange(-10000, 10000)
        self.x_input.setValue(self.node.x)
        pos_layout.addRow("X:", self.x_input)
        
        self.y_input = QDoubleSpinBox()
        self.y_input.setRange(-10000, 10000)
        self.y_input.setValue(self.node.y)
        pos_layout.addRow("Y:", self.y_input)
        
        layout.addWidget(pos_group)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        cancel_btn = QPushButton("İptal")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        save_btn = QPushButton("Kaydet")
        save_btn.setObjectName("primaryButton")
        save_btn.clicked.connect(self.accept)
        buttons_layout.addWidget(save_btn)
        
        layout.addLayout(buttons_layout)
    
    def get_data(self) -> dict:
        """
        Get the edited data from the dialog.
        
        Returns:
            Dictionary of updated properties
        """
        return {
            'name': self.name_input.text(),
            'activity': self.activity_input.value(),
            'interaction': self.interaction_input.value(),
            'x': self.x_input.value(),
            'y': self.y_input.value()
        }


