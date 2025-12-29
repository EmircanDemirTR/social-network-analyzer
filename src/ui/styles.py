"""
Dark theme styles for the Social Network Analyzer application.
"""


class DarkTheme:
    """
    Dark theme color palette and QSS styles.
    """
    
    # Color Palette
    COLORS = {
        'background': '#1a1a2e',
        'background_dark': '#0f0f1a',
        'panel': '#16213e',
        'panel_light': '#1f2b47',
        'accent': '#0f3460',
        'accent_highlight': '#e94560',
        'neon_blue': '#00d9ff',
        'neon_green': '#00ff88',
        'neon_purple': '#b429f9',
        'neon_pink': '#ff2e97',
        'text_primary': '#eaeaea',
        'text_secondary': '#6c7a89',
        'text_muted': '#4a5568',
        'border': '#2d3748',
        'border_light': '#4a5568',
        'success': '#00ff88',
        'warning': '#ffc107',
        'error': '#ff4757',
        'info': '#00d9ff',
    }
    
    # Node colors for visualization
    NODE_COLORS = [
        (0, 217, 255),    # Neon blue
        (0, 255, 136),    # Neon green
        (180, 41, 249),   # Neon purple
        (255, 46, 151),   # Neon pink
        (255, 107, 107),  # Coral
        (255, 215, 0),    # Gold
        (0, 255, 255),    # Cyan
        (255, 105, 180),  # Hot pink
    ]
    
    @classmethod
    def get_stylesheet(cls) -> str:
        """
        Get the complete QSS stylesheet for the application.
        
        Returns:
            QSS stylesheet string
        """
        return f"""
        /* Main Window */
        QMainWindow {{
            background-color: {cls.COLORS['background']};
        }}
        
        /* Central Widget */
        QWidget {{
            background-color: {cls.COLORS['background']};
            color: {cls.COLORS['text_primary']};
            font-family: 'Segoe UI', 'Arial', sans-serif;
            font-size: 13px;
        }}
        
        /* Menu Bar */
        QMenuBar {{
            background-color: {cls.COLORS['panel']};
            color: {cls.COLORS['text_primary']};
            padding: 4px 8px;
            border-bottom: 1px solid {cls.COLORS['border']};
        }}
        
        QMenuBar::item {{
            padding: 6px 12px;
            border-radius: 4px;
        }}
        
        QMenuBar::item:selected {{
            background-color: {cls.COLORS['accent']};
        }}
        
        QMenu {{
            background-color: {cls.COLORS['panel']};
            color: {cls.COLORS['text_primary']};
            border: 1px solid {cls.COLORS['border']};
            border-radius: 4px;
            padding: 4px;
        }}
        
        QMenu::item {{
            padding: 8px 24px;
            border-radius: 4px;
        }}
        
        QMenu::item:selected {{
            background-color: {cls.COLORS['accent']};
        }}
        
        QMenu::separator {{
            height: 1px;
            background-color: {cls.COLORS['border']};
            margin: 4px 8px;
        }}
        
        /* Panels and Frames */
        QFrame {{
            background-color: {cls.COLORS['panel']};
            border: 1px solid {cls.COLORS['border']};
            border-radius: 8px;
        }}
        
        QGroupBox {{
            background-color: {cls.COLORS['panel']};
            border: 1px solid {cls.COLORS['border']};
            border-radius: 8px;
            margin-top: 12px;
            padding-top: 12px;
            font-weight: bold;
        }}
        
        QGroupBox::title {{
            subcontrol-origin: margin;
            subcontrol-position: top left;
            left: 12px;
            padding: 0 8px;
            color: {cls.COLORS['neon_blue']};
        }}
        
        /* Buttons */
        QPushButton {{
            background-color: {cls.COLORS['accent']};
            color: {cls.COLORS['text_primary']};
            border: none;
            border-radius: 6px;
            padding: 8px 16px;
            font-weight: bold;
            min-width: 80px;
        }}
        
        QPushButton:hover {{
            background-color: {cls.COLORS['accent_highlight']};
        }}
        
        QPushButton:pressed {{
            background-color: {cls.COLORS['neon_pink']};
        }}
        
        QPushButton:disabled {{
            background-color: {cls.COLORS['border']};
            color: {cls.COLORS['text_muted']};
        }}
        
        QPushButton#algorithmButton {{
            background-color: {cls.COLORS['panel_light']};
            border: 2px solid {cls.COLORS['neon_blue']};
            min-width: 100px;
        }}
        
        QPushButton#algorithmButton:hover {{
            background-color: {cls.COLORS['accent']};
            border-color: {cls.COLORS['neon_green']};
        }}
        
        QPushButton#primaryButton {{
            background-color: {cls.COLORS['accent_highlight']};
        }}
        
        QPushButton#primaryButton:hover {{
            background-color: {cls.COLORS['neon_pink']};
        }}
        
        /* Input Fields */
        QLineEdit {{
            background-color: {cls.COLORS['background_dark']};
            color: {cls.COLORS['text_primary']};
            border: 2px solid {cls.COLORS['border']};
            border-radius: 6px;
            padding: 8px 12px;
            selection-background-color: {cls.COLORS['accent']};
        }}
        
        QLineEdit:focus {{
            border-color: {cls.COLORS['neon_blue']};
        }}
        
        QSpinBox, QDoubleSpinBox {{
            background-color: {cls.COLORS['background_dark']};
            color: {cls.COLORS['text_primary']};
            border: 2px solid {cls.COLORS['border']};
            border-radius: 6px;
            padding: 6px 10px;
        }}
        
        QSpinBox:focus, QDoubleSpinBox:focus {{
            border-color: {cls.COLORS['neon_blue']};
        }}
        
        QSpinBox::up-button, QDoubleSpinBox::up-button,
        QSpinBox::down-button, QDoubleSpinBox::down-button {{
            background-color: {cls.COLORS['accent']};
            border: none;
            width: 20px;
        }}
        
        QComboBox {{
            background-color: {cls.COLORS['background_dark']};
            color: {cls.COLORS['text_primary']};
            border: 2px solid {cls.COLORS['border']};
            border-radius: 6px;
            padding: 8px 12px;
            min-width: 100px;
        }}
        
        QComboBox:focus {{
            border-color: {cls.COLORS['neon_blue']};
        }}
        
        QComboBox::drop-down {{
            border: none;
            width: 30px;
        }}
        
        QComboBox QAbstractItemView {{
            background-color: {cls.COLORS['panel']};
            color: {cls.COLORS['text_primary']};
            border: 1px solid {cls.COLORS['border']};
            selection-background-color: {cls.COLORS['accent']};
        }}
        
        /* Sliders */
        QSlider::groove:horizontal {{
            background-color: {cls.COLORS['border']};
            height: 6px;
            border-radius: 3px;
        }}
        
        QSlider::handle:horizontal {{
            background-color: {cls.COLORS['neon_blue']};
            width: 16px;
            height: 16px;
            margin: -5px 0;
            border-radius: 8px;
        }}
        
        QSlider::handle:horizontal:hover {{
            background-color: {cls.COLORS['neon_green']};
        }}
        
        QSlider::sub-page:horizontal {{
            background-color: {cls.COLORS['neon_blue']};
            border-radius: 3px;
        }}
        
        /* Checkboxes */
        QCheckBox {{
            spacing: 8px;
        }}
        
        QCheckBox::indicator {{
            width: 20px;
            height: 20px;
            border-radius: 4px;
            border: 2px solid {cls.COLORS['border']};
            background-color: {cls.COLORS['background_dark']};
        }}
        
        QCheckBox::indicator:checked {{
            background-color: {cls.COLORS['neon_blue']};
            border-color: {cls.COLORS['neon_blue']};
        }}
        
        QCheckBox::indicator:hover {{
            border-color: {cls.COLORS['neon_blue']};
        }}
        
        /* Tables */
        QTableWidget {{
            background-color: {cls.COLORS['background_dark']};
            color: {cls.COLORS['text_primary']};
            border: 1px solid {cls.COLORS['border']};
            border-radius: 6px;
            gridline-color: {cls.COLORS['border']};
        }}
        
        QTableWidget::item {{
            padding: 8px;
        }}
        
        QTableWidget::item:selected {{
            background-color: {cls.COLORS['accent']};
        }}
        
        QHeaderView::section {{
            background-color: {cls.COLORS['panel']};
            color: {cls.COLORS['neon_blue']};
            padding: 10px;
            border: none;
            border-bottom: 2px solid {cls.COLORS['neon_blue']};
            font-weight: bold;
        }}
        
        /* Scroll Bars */
        QScrollBar:vertical {{
            background-color: {cls.COLORS['background_dark']};
            width: 12px;
            border-radius: 6px;
            margin: 0;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {cls.COLORS['border']};
            border-radius: 6px;
            min-height: 30px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {cls.COLORS['neon_blue']};
        }}
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0;
        }}
        
        QScrollBar:horizontal {{
            background-color: {cls.COLORS['background_dark']};
            height: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:horizontal {{
            background-color: {cls.COLORS['border']};
            border-radius: 6px;
            min-width: 30px;
        }}
        
        QScrollBar::handle:horizontal:hover {{
            background-color: {cls.COLORS['neon_blue']};
        }}
        
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0;
        }}
        
        /* Labels */
        QLabel {{
            color: {cls.COLORS['text_primary']};
            background-color: transparent;
            border: none;
        }}
        
        QLabel#titleLabel {{
            font-size: 18px;
            font-weight: bold;
            color: {cls.COLORS['neon_blue']};
        }}
        
        QLabel#statLabel {{
            font-size: 24px;
            font-weight: bold;
            color: {cls.COLORS['neon_green']};
        }}
        
        QLabel#statTitleLabel {{
            font-size: 11px;
            color: {cls.COLORS['text_secondary']};
            text-transform: uppercase;
        }}
        
        /* Status Bar */
        QStatusBar {{
            background-color: {cls.COLORS['panel']};
            color: {cls.COLORS['text_secondary']};
            border-top: 1px solid {cls.COLORS['border']};
            padding: 4px;
        }}
        
        QStatusBar::item {{
            border: none;
        }}
        
        /* Tool Tips */
        QToolTip {{
            background-color: {cls.COLORS['panel']};
            color: {cls.COLORS['text_primary']};
            border: 1px solid {cls.COLORS['neon_blue']};
            border-radius: 4px;
            padding: 8px;
        }}
        
        /* Splitter */
        QSplitter::handle {{
            background-color: {cls.COLORS['border']};
        }}
        
        QSplitter::handle:horizontal {{
            width: 2px;
        }}
        
        QSplitter::handle:vertical {{
            height: 2px;
        }}
        
        /* Tab Widget */
        QTabWidget::pane {{
            background-color: {cls.COLORS['panel']};
            border: 1px solid {cls.COLORS['border']};
            border-radius: 6px;
            padding: 4px;
        }}
        
        QTabBar::tab {{
            background-color: {cls.COLORS['background_dark']};
            color: {cls.COLORS['text_secondary']};
            padding: 10px 20px;
            border-top-left-radius: 6px;
            border-top-right-radius: 6px;
            margin-right: 2px;
        }}
        
        QTabBar::tab:selected {{
            background-color: {cls.COLORS['panel']};
            color: {cls.COLORS['neon_blue']};
            border-bottom: 2px solid {cls.COLORS['neon_blue']};
        }}
        
        QTabBar::tab:hover:!selected {{
            background-color: {cls.COLORS['accent']};
        }}
        
        /* Progress Bar */
        QProgressBar {{
            background-color: {cls.COLORS['background_dark']};
            border: none;
            border-radius: 4px;
            height: 8px;
            text-align: center;
        }}
        
        QProgressBar::chunk {{
            background-color: {cls.COLORS['neon_blue']};
            border-radius: 4px;
        }}
        
        /* Dialog */
        QDialog {{
            background-color: {cls.COLORS['background']};
        }}
        
        /* Graphics View (for graph canvas) */
        QGraphicsView {{
            background-color: {cls.COLORS['background_dark']};
            border: 2px solid {cls.COLORS['border']};
            border-radius: 8px;
        }}
        """
    
    @classmethod
    def get_accent_button_style(cls) -> str:
        """Get style for accent/primary buttons."""
        return f"""
        QPushButton {{
            background-color: {cls.COLORS['accent_highlight']};
            color: {cls.COLORS['text_primary']};
            border: none;
            border-radius: 6px;
            padding: 10px 20px;
            font-weight: bold;
        }}
        QPushButton:hover {{
            background-color: {cls.COLORS['neon_pink']};
        }}
        """
    
    @classmethod
    def get_glow_effect_style(cls, color: str) -> str:
        """Get CSS for glow effect (used in canvas items)."""
        return f"0 0 10px {color}, 0 0 20px {color}, 0 0 30px {color}"


