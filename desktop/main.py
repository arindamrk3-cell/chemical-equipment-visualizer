import sys
from charts import create_equipment_chart

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,QGridLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QFileDialog,
    QTextEdit,
)
from api_client import upload_csv


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.setGeometry(100, 100, 600, 500)

        self.layout = QVBoxLayout()

        self.title = QLabel("Chemical Equipment Visualizer (Desktop)")
        self.layout.addWidget(self.title)

        self.upload_btn = QPushButton("Upload CSV")
        self.upload_btn.clicked.connect(self.select_file)
        self.layout.addWidget(self.upload_btn)

        self.summary_layout = QGridLayout()

        self.total_label = QLabel("Total Equipment: -")
        self.flow_label = QLabel("Avg Flowrate: -")
        self.pressure_label = QLabel("Avg Pressure: -")
        self.temp_label = QLabel("Avg Temperature: -")

        self.summary_layout.addWidget(self.total_label, 0, 0)
        self.summary_layout.addWidget(self.flow_label, 0, 1)
        self.summary_layout.addWidget(self.pressure_label, 1, 0)
        self.summary_layout.addWidget(self.temp_label, 1, 1)
        self.chart_container = QVBoxLayout()
        self.layout.addLayout(self.chart_container)
        self.layout.addLayout(self.summary_layout)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.layout.addWidget(self.output)

        self.setLayout(self.layout)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            "CSV Files (*.csv)",
        )

        if file_path:
            self.output.setText("Uploading file...")
            try:
                result = upload_csv(file_path)
                #self.output.setText(str(result))
                summary = result["summary"]

                self.total_label.setText(f"Total Equipment: {summary['total_equipment']}")
                self.flow_label.setText(f"Avg Flowrate: {summary['avg_flowrate']:.2f}")
                self.pressure_label.setText(f"Avg Pressure: {summary['avg_pressure']:.2f}")
                self.temp_label.setText(f"Avg Temperature: {summary['avg_temperature']:.2f}")
                while self.chart_container.count():
                    child = self.chart_container.takeAt(0)
                    if child.widget():
                        child.widget().deleteLater()

            
                distribution = summary["equipment_type_distribution"]
                chart = create_equipment_chart(distribution)
                self.chart_container.addWidget(chart)
            except Exception as e:
                self.output.setText(str(e))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
