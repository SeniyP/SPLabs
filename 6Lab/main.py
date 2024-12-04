import sys
import pandas as pd
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QComboBox, QLabel, QWidget, QInputDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class DataVisualizationApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Data Visualization App')
        self.setGeometry(100, 100, 800, 600)

        self.main_widget = QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.layout = QVBoxLayout(self.main_widget)

        self.load_button = QPushButton('Load CSV Data', self)
        self.load_button.clicked.connect(self.load_data)
        self.layout.addWidget(self.load_button)

        self.add_record_button = QPushButton('Add Record', self)
        self.add_record_button.clicked.connect(self.add_record)
        self.layout.addWidget(self.add_record_button)

        self.chart_type_combo = QComboBox(self)
        self.chart_type_combo.addItems(['Line Chart', 'Histogram', 'Pie Chart'])
        self.chart_type_combo.currentIndexChanged.connect(self.update_chart)
        self.layout.addWidget(self.chart_type_combo)

        self.stats_label = QLabel('Statistics will be displayed here', self)
        self.layout.addWidget(self.stats_label)

        self.figure = plt.Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.layout.addWidget(self.canvas)

        self.data = None

    def load_data(self):
        self.data = pd.read_csv('sample_data.csv')

        self.update_statistics()

    def update_statistics(self):
        if self.data is not None:
            num_rows, num_cols = self.data.shape
            min_values = self.data.min()
            max_values = self.data.max()
            stats_text = (f'Rows: {num_rows}, Columns: {num_cols}\n'
                          f'Min Values:\n{min_values}\n'
                          f'Max Values:\n{max_values}')
            self.stats_label.setText(stats_text)

        self.update_chart()

    def update_chart(self):
        self.figure.clear()
        self.ax = self.figure.add_subplot(111)

        chart_type = self.chart_type_combo.currentText()

        if chart_type == 'Line Chart':
            self.ax.plot(pd.to_datetime(self.data['Date']), self.data['Value1'], label='Value1')
            self.ax.set_title('Line Chart: Date vs Value1')
            self.ax.set_xlabel('Date')
            self.ax.set_ylabel('Value1')

        elif chart_type == 'Histogram':
            self.ax.hist(self.data['Value2'], bins=20, edgecolor='black')
            self.ax.set_title('Histogram: Value2 Distribution')
            self.ax.set_xlabel('Value2')
            self.ax.set_ylabel('Frequency')

        elif chart_type == 'Pie Chart':
            category_counts = self.data['Category'].value_counts()
            self.ax.pie(category_counts, labels=category_counts.index, autopct='%1.1f%%')
            self.ax.set_title('Pie Chart: Category Distribution')

        self.canvas.draw()

    def add_record(self):
        text, ok = QInputDialog.getText(self, 'Add New Record', 'Enter new value for Value1:')
        if ok and text:
            new_value1 = float(text)  

            date, ok_date = QInputDialog.getText(self, 'Add New Record', 'Enter date (YYYY-MM-DD):')
            if ok_date and date:
                new_date = date

                text_value2, ok_value2 = QInputDialog.getText(self, 'Add New Record', 'Enter new value for Value2:')
                if ok_value2 and text_value2:
                    new_value2 = float(text_value2)

                    category, ok_category = QInputDialog.getText(self, 'Add New Record', 'Enter category:')
                    if ok_category and category:
                        new_record = pd.DataFrame({
                            'Date': [new_date],
                            'Value1': [new_value1],
                            'Value2': [new_value2],
                            'Category': [category]  
                        })

                        self.data = pd.concat([self.data, new_record], ignore_index=True)

                        self.data.to_csv('sample_data.csv', index=False)

                        self.update_statistics()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = DataVisualizationApp()
    window.show()
    sys.exit(app.exec_())
