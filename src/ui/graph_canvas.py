"""
Graph visualization canvas using QGraphicsView.
"""
from PyQt6.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsEllipseItem,
    QGraphicsLineItem, QGraphicsTextItem, QMenu, QGraphicsItem
)
from PyQt6.QtCore import Qt, QTimer, QPointF, QRectF, pyqtSignal
from PyQt6.QtGui import (
    QPen, QBrush, QColor, QPainter, QFont,
    QRadialGradient, QWheelEvent, QMouseEvent, QContextMenuEvent, QKeyEvent
)
import math
import time
from typing import Dict, Optional, List, Tuple

from ..models.graph import Graph
from ..models.node import Node
from ..physics.force_directed import ForceDirectedLayout
from .styles import DarkTheme


class NodeItem(QGraphicsEllipseItem):
    """
    Visual representation of a node in the graph.
    """
    
    BASE_RADIUS = 25
    
    def __init__(self, node: Node, canvas: 'GraphCanvas'):
        self.node = node
        self.canvas = canvas
        self.radius = self.BASE_RADIUS
        
        super().__init__(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)
        
        self.setPos(node.x, node.y)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)
        self.setAcceptHoverEvents(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setZValue(10)  # Above edges
        
        # Label
        self.label = QGraphicsTextItem(node.name, self)
        self.label.setDefaultTextColor(QColor(DarkTheme.COLORS['text_primary']))
        font = QFont("Segoe UI", 12, QFont.Weight.ExtraBold)
        self.label.setFont(font)
        self._center_label()
        
        # Initial appearance
        self._is_hovered = False
        self.update_appearance()
    
    def _center_label(self):
        """Center the label below the node."""
        rect = self.label.boundingRect()
        self.label.setPos(-rect.width() / 2, self.radius + 5)
    
    def update_appearance(self):
        """Update node visual appearance based on state."""
        node = self.node
        
        # Determine color
        if node.is_highlighted and node.highlight_color:
            r, g, b = node.highlight_color
        else:
            r, g, b = node.color
        
        color = QColor(r, g, b)
        
        # Create gradient
        gradient = QRadialGradient(0, 0, self.radius)
        
        if self.isSelected() or node.is_selected:
            # Selected state - bright glow
            gradient.setColorAt(0, color.lighter(150))
            gradient.setColorAt(0.7, color)
            gradient.setColorAt(1, color.darker(120))
            pen_width = 4
            pen_color = QColor(DarkTheme.COLORS['neon_green'])
        elif self._is_hovered:
            # Hovered state
            gradient.setColorAt(0, color.lighter(140))
            gradient.setColorAt(0.7, color)
            gradient.setColorAt(1, color.darker(110))
            pen_width = 3
            pen_color = QColor(DarkTheme.COLORS['neon_blue'])
        elif node.is_highlighted:
            # Highlighted state (algorithm visualization)
            gradient.setColorAt(0, color.lighter(160))
            gradient.setColorAt(0.7, color.lighter(120))
            gradient.setColorAt(1, color)
            pen_width = 3
            pen_color = color.lighter(150)
        else:
            # Normal state
            gradient.setColorAt(0, color.lighter(120))
            gradient.setColorAt(0.7, color)
            gradient.setColorAt(1, color.darker(130))
            pen_width = 2
            pen_color = color.darker(150)
        
        self.setBrush(QBrush(gradient))
        self.setPen(QPen(pen_color, pen_width))
        
        # Update label
        self.label.setPlainText(node.name)
        self._center_label()
    
    def set_size_by_degree(self, degree: int, max_degree: int):
        """Scale node size based on degree centrality."""
        if max_degree > 0:
            scale = 0.7 + 0.6 * (degree / max_degree)
        else:
            scale = 1.0
        
        self.radius = self.BASE_RADIUS * scale
        self.setRect(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius)
        self._center_label()
        self.update_appearance()
    
    def itemChange(self, change, value):
        """Handle item changes like position."""
        if change == QGraphicsItem.GraphicsItemChange.ItemPositionHasChanged:
            # Update node model position
            pos = value
            self.node.x = pos.x()
            self.node.y = pos.y()
            # Stop velocity when dragging
            self.node.reset_velocity()
            # Update connected edges
            self.canvas.update_edges_for_node(self.node.id)
        
        return super().itemChange(change, value)
    
    def hoverEnterEvent(self, event):
        """Handle hover enter."""
        self._is_hovered = True
        self.update_appearance()
        self.canvas.show_node_tooltip(self.node)
        super().hoverEnterEvent(event)
    
    def hoverLeaveEvent(self, event):
        """Handle hover leave."""
        self._is_hovered = False
        self.update_appearance()
        self.canvas.hide_tooltip()
        super().hoverLeaveEvent(event)
    
    def mouseDoubleClickEvent(self, event):
        """Handle double click to edit node."""
        self.canvas.edit_node(self.node)
        super().mouseDoubleClickEvent(event)


class EdgeItem(QGraphicsLineItem):
    """
    Visual representation of an edge in the graph.
    """
    
    def __init__(self, edge, canvas: 'GraphCanvas'):
        self.edge = edge
        self.canvas = canvas
        
        super().__init__()
        
        self.setZValue(1)  # Below nodes
        self.update_position()
        self.update_appearance()
    
    def update_position(self):
        """Update edge line position based on node positions."""
        x1, y1 = self.edge.source.x, self.edge.source.y
        x2, y2 = self.edge.target.x, self.edge.target.y
        self.setLine(x1, y1, x2, y2)
    
    def update_appearance(self):
        """Update edge visual appearance."""
        if self.edge.is_highlighted:
            if self.edge.highlight_color:
                r, g, b = self.edge.highlight_color
                color = QColor(r, g, b)
            else:
                color = QColor(DarkTheme.COLORS['neon_purple'])
            width = 4
        else:
            color = QColor(DarkTheme.COLORS['border_light'])
            width = 2
        
        # Vary opacity based on weight
        alpha = int(100 + 155 * self.edge.weight)
        color.setAlpha(min(255, alpha))
        
        self.setPen(QPen(color, width, Qt.PenStyle.SolidLine, 
                        Qt.PenCapStyle.RoundCap))


class GraphCanvas(QGraphicsView):
    """
    Main canvas for graph visualization with interactivity.
    """
    
    # Signals
    node_selected = pyqtSignal(int)  # node_id, -1 for deselect
    node_deleted = pyqtSignal(int)
    edge_deleted = pyqtSignal(int, int)  # source_id, target_id
    status_message = pyqtSignal(str)
    
    def __init__(self, graph: Graph):
        super().__init__()
        
        self.graph = graph
        self._scene = QGraphicsScene()
        self.setScene(self._scene)
        
        # Visual elements tracking
        self._node_items: Dict[int, NodeItem] = {}
        self._edge_items: List[EdgeItem] = []
        
        # Physics (disabled by default)
        self._physics = ForceDirectedLayout()
        self._physics_enabled = False
        
        # Performance tracking
        self._frame_times: List[float] = []
        self._last_frame_time = time.time()
        
        # Interaction state
        self._selected_node_id: Optional[int] = None
        self._edge_creation_mode = False
        self._edge_source_id: Optional[int] = None
        
        # Setup view
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        self.setViewportUpdateMode(QGraphicsView.ViewportUpdateMode.FullViewportUpdate)
        self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        
        # Scene setup
        self._scene.setSceneRect(-2000, -2000, 4000, 4000)
        self._scene.setBackgroundBrush(QBrush(QColor(DarkTheme.COLORS['background_dark'])))
        
        # Draw grid
        self._draw_grid()
    
    def _draw_grid(self):
        """Draw background grid."""
        grid_color = QColor(DarkTheme.COLORS['border'])
        grid_color.setAlpha(30)
        pen = QPen(grid_color, 1)
        
        grid_size = 50
        for x in range(-2000, 2000, grid_size):
            self._scene.addLine(x, -2000, x, 2000, pen)
        for y in range(-2000, 2000, grid_size):
            self._scene.addLine(-2000, y, 2000, y, pen)
    
    def set_graph(self, graph: Graph):
        """Set a new graph and refresh display."""
        self.graph = graph
        self._physics.graph = graph
        self.refresh()
    
    def refresh(self):
        """Refresh the entire canvas."""
        # Clear existing items (except grid)
        for item in self._node_items.values():
            self._scene.removeItem(item)
        for item in self._edge_items:
            self._scene.removeItem(item)
        
        self._node_items.clear()
        self._edge_items.clear()
        
        # Create edge items first (so they're behind nodes)
        for edge in self.graph.edges:
            edge_item = EdgeItem(edge, self)
            self._edge_items.append(edge_item)
            self._scene.addItem(edge_item)
        
        # Create node items
        for node in self.graph.nodes.values():
            node_item = NodeItem(node, self)
            self._node_items[node.id] = node_item
            self._scene.addItem(node_item)
        
        # Update physics
        self._physics.graph = self.graph
    
    def update_edges_for_node(self, node_id: int):
        """Update edges connected to a specific node."""
        for edge_item in self._edge_items:
            if edge_item.edge.contains_node(node_id):
                edge_item.update_position()
    
    def _physics_step(self):
        """Perform one physics simulation step."""
        if not self._physics_enabled or not self.graph.nodes:
            return
        
        # Check if any node is being dragged
        dragging = any(item.isSelected() for item in self._node_items.values())
        
        if not dragging:
            self._physics.step(self.graph)
            
            # Update visual positions
            for node_id, node_item in self._node_items.items():
                node = self.graph.nodes.get(node_id)
                if node:
                    node_item.setPos(node.x, node.y)
            
            # Update edges
            for edge_item in self._edge_items:
                edge_item.update_position()
        
        # Track FPS
        current_time = time.time()
        self._frame_times.append(current_time - self._last_frame_time)
        self._last_frame_time = current_time
        
        # Keep only last 60 frames
        if len(self._frame_times) > 60:
            self._frame_times.pop(0)
    
    def get_fps(self) -> float:
        """Get current FPS."""
        if not self._frame_times:
            return 60.0
        avg_frame_time = sum(self._frame_times) / len(self._frame_times)
        return 1.0 / avg_frame_time if avg_frame_time > 0 else 60.0
    
    def toggle_physics(self, enabled: bool):
        """Toggle physics simulation."""
        self._physics_enabled = enabled
    
    def update_physics_params(self, repulsion: float, attraction: float, damping: float):
        """Update physics parameters."""
        self._physics.repulsion = repulsion
        self._physics.attraction = attraction
        self._physics.damping = damping
    
    def zoom(self, factor: float):
        """Zoom the view."""
        self.scale(factor, factor)
    
    def fit_in_view(self):
        """Fit all content in view."""
        if self.graph.nodes:
            # Calculate bounding rect of all nodes
            min_x = min(n.x for n in self.graph.nodes.values()) - 100
            max_x = max(n.x for n in self.graph.nodes.values()) + 100
            min_y = min(n.y for n in self.graph.nodes.values()) - 100
            max_y = max(n.y for n in self.graph.nodes.values()) + 100
            
            rect = QRectF(min_x, min_y, max_x - min_x, max_y - min_y)
            self.fitInView(rect, Qt.AspectRatioMode.KeepAspectRatio)
    
    def clear_selection(self):
        """Clear all selections."""
        self._scene.clearSelection()
        self._selected_node_id = None
        
        for node in self.graph.nodes.values():
            node.is_selected = False
        
        for item in self._node_items.values():
            item.update_appearance()
    
    def select_node(self, node_id: int):
        """Programmatically select a node."""
        self.clear_selection()
        
        if node_id in self._node_items:
            self._node_items[node_id].setSelected(True)
            self._selected_node_id = node_id
            self.graph.nodes[node_id].is_selected = True
            self._node_items[node_id].update_appearance()
            self.node_selected.emit(node_id)
    
    def highlight_nodes(self, node_ids: List[int], color: Tuple[int, int, int] = None):
        """Highlight multiple nodes."""
        for node_id in node_ids:
            if node_id in self.graph.nodes:
                self.graph.nodes[node_id].set_highlight(True, color)
                if node_id in self._node_items:
                    self._node_items[node_id].update_appearance()
    
    def highlight_edges(self, edges: List[Tuple[int, int]], color: Tuple[int, int, int] = None):
        """Highlight specific edges."""
        for source_id, target_id in edges:
            for edge_item in self._edge_items:
                if ((edge_item.edge.source.id == source_id and edge_item.edge.target.id == target_id) or
                    (edge_item.edge.source.id == target_id and edge_item.edge.target.id == source_id)):
                    edge_item.edge.set_highlight(True, color)
                    edge_item.update_appearance()
    
    def highlight_path(self, path: List[int], color: Tuple[int, int, int] = None):
        """Highlight a path (nodes and edges)."""
        if not color:
            color = (180, 41, 249)  # Neon purple
        
        self.highlight_nodes(path, color)
        
        edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
        self.highlight_edges(edges, color)
    
    def apply_coloring(self, coloring: Dict[int, int], colors: List[Tuple[int, int, int]]):
        """Apply coloring result to nodes."""
        for node_id, color_idx in coloring.items():
            if node_id in self.graph.nodes:
                color = colors[color_idx % len(colors)]
                self.graph.nodes[node_id].color = color
                if node_id in self._node_items:
                    self._node_items[node_id].update_appearance()
    
    def scale_nodes_by_centrality(self, centrality: Dict[int, float]):
        """Scale node sizes based on centrality values."""
        if not centrality:
            return
        
        max_cent = max(centrality.values())
        for node_id, cent in centrality.items():
            if node_id in self._node_items:
                # Map centrality to degree for sizing
                degree = self.graph.get_degree(node_id)
                max_degree = max(self.graph.get_degree(nid) for nid in self.graph.nodes)
                self._node_items[node_id].set_size_by_degree(degree, max_degree)
    
    def show_node_tooltip(self, node: Node):
        """Show tooltip for a node."""
        props = node.get_properties()
        tip = (f"<b>{node.name}</b><br>"
               f"ID: {node.id}<br>"
               f"Aktivite: {props['activity']}<br>"
               f"Etkileşim: {props['interaction']}<br>"
               f"Bağlantı: {props['connection_count']}")
        self.setToolTip(tip)
    
    def hide_tooltip(self):
        """Hide tooltip."""
        self.setToolTip("")
    
    def edit_node(self, node: Node):
        """Open edit dialog for a node."""
        from .node_dialog import NodeDialog
        dialog = NodeDialog(node, self)
        if dialog.exec():
            updated_data = dialog.get_data()
            self.graph.update_node(node.id, **updated_data)
            if node.id in self._node_items:
                self._node_items[node.id].update_appearance()
            self.status_message.emit(f"Düğüm güncellendi: {node.name}")
    
    def delete_node(self, node_id: int):
        """Delete a node."""
        if node_id in self.graph.nodes:
            self.graph.remove_node(node_id)
            self.refresh()
            self.node_deleted.emit(node_id)
    
    def delete_edge(self, source_id: int, target_id: int):
        """Delete an edge."""
        if self.graph.remove_edge(source_id, target_id):
            self.refresh()
            self.edge_deleted.emit(source_id, target_id)
    
    def start_edge_creation(self, source_id: int):
        """Start edge creation mode."""
        self._edge_creation_mode = True
        self._edge_source_id = source_id
        self.setCursor(Qt.CursorShape.CrossCursor)
        self.status_message.emit("Hedef düğümü seçin...")
    
    def cancel_edge_creation(self):
        """Cancel edge creation mode."""
        self._edge_creation_mode = False
        self._edge_source_id = None
        self.setCursor(Qt.CursorShape.ArrowCursor)
    
    # Event handlers
    def wheelEvent(self, event: QWheelEvent):
        """Handle mouse wheel - Ctrl+wheel for zoom, normal wheel for scroll."""
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            # Zoom with Ctrl + wheel
            factor = 1.15 if event.angleDelta().y() > 0 else 1 / 1.15
            self.zoom(factor)
        else:
            # Scroll vertically
            delta = event.angleDelta().y()
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() - delta
            )
    
    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press."""
        if event.button() == Qt.MouseButton.LeftButton:
            item = self.itemAt(event.pos())
            
            if self._edge_creation_mode:
                if isinstance(item, NodeItem):
                    target_id = item.node.id
                    if target_id != self._edge_source_id:
                        edge = self.graph.add_edge(self._edge_source_id, target_id)
                        if edge:
                            self.refresh()
                            self.status_message.emit(
                                f"Bağlantı oluşturuldu: {self._edge_source_id} - {target_id}"
                            )
                        else:
                            self.status_message.emit("Bağlantı oluşturulamadı")
                self.cancel_edge_creation()
                return
            
            if isinstance(item, NodeItem):
                self._selected_node_id = item.node.id
                item.node.is_selected = True
                item.update_appearance()
                self.node_selected.emit(item.node.id)
            else:
                self.clear_selection()
                self.node_selected.emit(-1)
        
        elif event.button() == Qt.MouseButton.MiddleButton:
            self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        
        super().mousePressEvent(event)
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """Handle mouse release."""
        if event.button() == Qt.MouseButton.MiddleButton:
            self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
        super().mouseReleaseEvent(event)
    
    def contextMenuEvent(self, event: QContextMenuEvent):
        """Handle right-click context menu."""
        item = self.itemAt(event.pos())
        menu = QMenu(self)
        
        if isinstance(item, NodeItem):
            node = item.node
            
            edit_action = menu.addAction("Düzenle")
            edit_action.triggered.connect(lambda: self.edit_node(node))
            
            menu.addSeparator()
            
            add_edge_action = menu.addAction("Bağlantı Ekle")
            add_edge_action.triggered.connect(lambda: self.start_edge_creation(node.id))
            
            highlight_neighbors_action = menu.addAction("Komşuları Vurgula")
            highlight_neighbors_action.triggered.connect(
                lambda: self.highlight_nodes(self.graph.get_neighbor_ids(node.id), (255, 215, 0))
            )
            
            menu.addSeparator()
            
            delete_action = menu.addAction("Sil")
            delete_action.triggered.connect(lambda: self.delete_node(node.id))
        
        else:
            # Click on empty space
            scene_pos = self.mapToScene(event.pos())
            
            add_node_action = menu.addAction("Düğüm Ekle")
            add_node_action.triggered.connect(
                lambda: self._add_node_at_position(scene_pos.x(), scene_pos.y())
            )
            
            menu.addSeparator()
            
            clear_selection_action = menu.addAction("Seçimi Temizle")
            clear_selection_action.triggered.connect(self.clear_selection)
            
            clear_highlights_action = menu.addAction("Vurguları Temizle")
            clear_highlights_action.triggered.connect(self._clear_all_highlights)
        
        menu.exec(event.globalPos())
    
    def _add_node_at_position(self, x: float, y: float):
        """Add a new node at the given position."""
        node = self.graph.add_node(x=x, y=y)
        self.refresh()
        self.status_message.emit(f"Düğüm eklendi: {node.name}")
    
    def auto_layout(self):
        """
        Automatically arrange nodes using physics engine simulation.
        Runs physics for a duration then stops.
        """
        if not self.graph.nodes:
            return
        
        import random
        
        nodes = list(self.graph.nodes.values())
        n = len(nodes)
        
        # Initialize positions in a circle to start
        center_x, center_y = 400, 300
        initial_radius = min(350, 80 + n * 15)
        
        for i, node in enumerate(nodes):
            angle = 2 * math.pi * i / n
            node.x = center_x + initial_radius * math.cos(angle) + random.uniform(-20, 20)
            node.y = center_y + initial_radius * math.sin(angle) + random.uniform(-20, 20)
            node.vx = 0
            node.vy = 0
        
        # Reset and configure physics engine - increased repulsion for more spacing
        self._physics.repulsion = 15000.0
        self._physics.attraction = 0.04
        self._physics.damping = 0.85
        self._physics.min_distance = 80
        self._physics.temperature = 1.0
        self._physics.graph = self.graph
        
        # Run physics simulation for fixed iterations
        iterations = 150
        
        for i in range(iterations):
            self._physics.step(self.graph)
            
            # Update visual positions every 10 iterations for performance
            if i % 10 == 0:
                for node_id, node_item in self._node_items.items():
                    node = self.graph.nodes.get(node_id)
                    if node:
                        node_item.setPos(node.x, node.y)
                for edge_item in self._edge_items:
                    edge_item.update_position()
                # Process events to keep UI responsive
                from PyQt6.QtWidgets import QApplication
                QApplication.processEvents()
        
        # Reset velocities
        for node in nodes:
            node.vx = 0
            node.vy = 0
        
        self.refresh()
        self.fit_in_view()
        self.status_message.emit("Düğümler fizik motoruyla düzenlendi")
    
    def keyPressEvent(self, event: QKeyEvent):
        """Handle keyboard events."""
        if event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            if event.key() == Qt.Key.Key_0:
                self.fit_in_view()
        super().keyPressEvent(event)
    
    def _clear_all_highlights(self):
        """Clear all highlights from nodes and edges."""
        self.graph.clear_highlights()
        
        for item in self._node_items.values():
            item.update_appearance()
        
        for item in self._edge_items:
            item.update_appearance()

