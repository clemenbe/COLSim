import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QLabel, QHBoxLayout)
from PyQt5.QtCore import Qt, QProcess

class SimulationLauncher(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("COLSIM Launcher")
        self.setFixedSize(600, 400)
        
        # Main widget and layout
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        self.layout = QVBoxLayout()
        self.main_widget.setLayout(self.layout)
        
        # Title label
        self.title_label = QLabel("COLSIM - Collision Avoidance Simulation")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 20px;")
        self.layout.addWidget(self.title_label)
        
        # Button layout
        self.button_layout = QHBoxLayout()
        
        # Launch button
        self.launch_button = QPushButton("Launch Simulation")
        self.launch_button.setFixedHeight(50)
        self.launch_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)

        # Button Interactions
        self.launch_button.clicked.connect(self.launch_simulation)
        self.button_layout.addWidget(self.launch_button)

        # OLd Launch button
        self.old_launch_button = QPushButton("Launch Old Simulation")
        self.old_launch_button.setFixedHeight(50)
        self.old_launch_button.setStyleSheet("""
            QPushButton {
                background-color: #d96a0f;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #d1772e;
            }
        """)

        # Button Interactions
        self.old_launch_button.clicked.connect(self.launch_old_simulation)
        self.button_layout.addWidget(self.old_launch_button)
        
        # Close button
        self.close_button = QPushButton("Exit")
        self.close_button.setFixedHeight(50)
        self.close_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
        """)
        
        #Close Button Interaction
        self.close_button.clicked.connect(self.close)
        self.button_layout.addWidget(self.close_button)
        
        self.layout.addLayout(self.button_layout)
        
        # Status label
        self.status_label = QLabel("Ready to launch simulation")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 14px; margin-top: 20px; color: #555;")
        self.layout.addWidget(self.status_label)
        
        # Process handle
        self.process = None

    def launch_simulation(self):
        """Launch the Pygame simulation as a separate process"""
        if self.process is None or self.process.state() == QProcess.NotRunning:
            self.status_label.setText("Starting simulation...")
            QApplication.processEvents()  # Update the UI immediately
            
            self.process = QProcess()
            self.process.setProcessChannelMode(QProcess.MergedChannels)
            
            # Start the simulation script
            self.process.start(sys.executable, ["COLSim/main_program/PyGame_COLSim.py"])
            
            self.launch_button.setText("Stop Simulation")
            self.status_label.setText("Simulation running...")
        else:
            self.process.terminate()
            self.process.waitForFinished()
            self.process = None
            self.launch_button.setText("Launch Simulation")
            self.status_label.setText("Simulation stopped")

    def launch_old_simulation(self):
        """Launch the old simulation as a separate process"""
        if self.process is None or self.process.state() == QProcess.NotRunning:
            self.status_label.setText("Starting simulation...")
            QApplication.processEvents()  # Update the UI
            
            self.process = QProcess()
            self.process.setProcessChannelMode(QProcess.MergedChannels)
            
            # Start the simulation script
            self.process.start(sys.executable, ["COLSim/main_program/main.py"])
            
            self.old_launch_button.setText("Stop Simulation")
            self.status_label.setText("Simulation running...")
        else:
            self.process.terminate()
            self.process.waitForFinished()
            self.process = None
            self.old_launch_button.setText("Launch Simulation")
            self.status_label.setText("Simulation stopped")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = SimulationLauncher()
    launcher.show()
    sys.exit(app.exec_())