import sys
import requests

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QFileDialog,
    QGridLayout,
)
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt

from charts import create_equipment_chart


API_UPLOAD_URL = "http://127.0.0.1:8000/api/upload/"


def upload_csv(file_path):
    with open(file_path, "rb") as f:
        response = requests.post(
            API_UPLOAD_URL,
            files={"file": f},
        )
    response.raise_for_status()
    return response.json()


class EquipmentApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Chemical Equipment Visualizer")
        self.resize(900, 700)

        # MAIN LAYOUT
        self.layout = QVBoxLayout()
        self.layout.setSpacing(20)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.layout)

        # TITLE
        title = QLabel("Chemical Equipment Visualizer")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("""
            QLabel {
                font-size: 22px;
                font-weight: 600;
            }
        """)
        self.layout.addWidget(title)

        # UPLOAD BUTTON
        self.upload_btn = QPushButton("Upload CSV File")
        self.upload_btn.clicked.connect(self.select_file)
        self.upload_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                padding: 10px 18px;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #1e40af;
            }
        """)
        self.layout.addWidget(self.upload_btn, alignment=Qt.AlignCenter)

        # STATUS LABEL
        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.status_label)

        # SUMMARY GRID
        self.summary_layout = QGridLayout()
        self.summary_layout.setSpacing(15)

        self.total_label = QLabel("Total Equipment: -")
        self.flow_label = QLabel("Avg Flowrate: -")
        self.pressure_label = QLabel("Avg Pressure: -")
        self.temp_label = QLabel("Avg Temperature: -")

        label_style = """
        QLabel {
            font-size: 14px;
            padding: 6px;
        }
        """

        for lbl in [
            self.total_label,
            self.flow_label,
            self.pressure_label,
            self.temp_label,
        ]:
            lbl.setStyleSheet(label_style)

        self.summary_layout.addWidget(self.total_label, 0, 0)
        self.summary_layout.addWidget(self.flow_label, 0, 1)
        self.summary_layout.addWidget(self.pressure_label, 1, 0)
        self.summary_layout.addWidget(self.temp_label, 1, 1)

        # SUMMARY CARD
        self.summary_widget = QWidget()
        self.summary_widget.setLayout(self.summary_layout)
        self.summary_widget.setStyleSheet("""
            QWidget {
                background-color: #2a2a2a;
                border-radius: 10px;
                padding: 12px;
            }
        """)
        self.layout.addWidget(self.summary_widget)

        # CHART CONTAINER
        self.chart_container = QVBoxLayout()
        self.layout.addLayout(self.chart_container)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv)",
        )

        if not file_path:
            return

        self.status_label.setText("Uploading and analyzing file...")

        try:
            result = upload_csv(file_path)
            summary = result["summary"]

            # UPDATE SUMMARY
            self.total_label.setText(
                f"Total Equipment: {summary['total_equipment']}"
            )
            self.flow_label.setText(
                f"Avg Flowrate: {summary['avg_flowrate']:.2f}"
            )
            self.pressure_label.setText(
                f"Avg Pressure: {summary['avg_pressure']:.2f}"
            )
            self.temp_label.setText(
                f"Avg Temperature: {summary['avg_temperature']:.2f}"
            )

            # CLEAR OLD CHART
            while self.chart_container.count():
                child = self.chart_container.takeAt(0)
                if child.widget():
                    child.widget().deleteLater()

            # ADD NEW CHART
            chart = create_equipment_chart(
                summary["equipment_type_distribution"]
            )
            self.chart_container.addWidget(chart)

            self.status_label.setText("Analysis completed successfully")

        except Exception as e:
            self.status_label.setText(f"Error: {str(e)}")


def main():
    app = QApplication(sys.argv)

    # DARK THEME
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(24, 24, 24))
    palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
    palette.setColor(QPalette.Base, QColor(35, 35, 35))
    palette.setColor(QPalette.Text, QColor(255, 255, 255))
    palette.setColor(QPalette.Button, QColor(45, 45, 45))
    palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    app.setPalette(palette)

    window = EquipmentApp()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
