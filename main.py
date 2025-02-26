import sys
import open3d as o3d
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QPushButton, 
    QVBoxLayout, QWidget, QColorDialog, QLabel, QComboBox
)
from PyQt6.QtGui import QColor
from PyQt6.QtCore import Qt

class PointCloudVisualizer(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Point Cloud Viewer")
        self.setGeometry(100, 100, 400, 300)

        self.initUI()
        self.pcd = None  # Placeholder for the point cloud object
        self.bg_color = [1.0, 1.0, 1.0]  # Default white background
        self.render_mode = "Lit"


    def initUI(self):
        layout = QVBoxLayout()

        # Buttons
        self.load_btn = QPushButton("Load Point Cloud")
        self.load_btn.clicked.connect(self.load_point_cloud)
        layout.addWidget(self.load_btn)

        self.color_btn = QPushButton("Change Background Color")
        self.color_btn.clicked.connect(self.change_bg_color)
        layout.addWidget(self.color_btn)

        self.render_mode_label = QLabel("Render Mode:")
        layout.addWidget(self.render_mode_label)

        self.render_mode_combo = QComboBox()
        self.render_mode_combo.addItems(["Lit", "Unlit", "Wireframe"])
        self.render_mode_combo.currentIndexChanged.connect(self.change_render_mode)
        layout.addWidget(self.render_mode_combo)

        self.status_label = QLabel("Status: No file loaded", alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        # Set up main widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_point_cloud(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Point Cloud File", "", "Point Cloud Files (*.ply *.pcd *.xyz)")
        if file_path:
            self.status_label.setText(f"Loaded: {file_path}")
            self.pcd = o3d.io.read_point_cloud(file_path)
            self.visualize_point_cloud()

    def visualize_point_cloud(self):
        if self.pcd is None:
            return

        vis = o3d.visualization.Visualizer()
        vis.create_window()

        # Apply background color
        opt = vis.get_render_option()
        opt.background_color = np.array(self.bg_color)

        # Render Mode Handling
        if self.render_mode == "Lit":
            vis.add_geometry(self.pcd)
        elif self.render_mode == "Unlit":
            # Set the material to unlit by removing normals
            self.pcd.normals = o3d.utility.Vector3dVector(np.zeros((len(self.pcd.points), 3)))  
            vis.add_geometry(self.pcd)
        elif self.render_mode == "Wireframe":
            # Convert to wireframe
            lines = [[i, i+1] for i in range(len(self.pcd.points)-1)]
            line_set = o3d.geometry.LineSet()
            line_set.points = self.pcd.points
            line_set.lines = o3d.utility.Vector2iVector(lines)
            vis.add_geometry(line_set)

        vis.run()
        vis.destroy_window()

    def change_bg_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            r, g, b, _ = color.getRgb()
            self.bg_color = [r / 255.0, g / 255.0, b / 255.0]  # Normalize color values
            print(f"Background color set to: ({r}, {g}, {b})")

    def change_render_mode(self, index):
        modes = ["Lit", "Unlit", "Wireframe"]
        selected_mode = modes[index]
        print(f"Render mode changed to: {selected_mode}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PointCloudVisualizer()
    window.show()
    sys.exit(app.exec())
