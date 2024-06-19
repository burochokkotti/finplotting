import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

# Read data from CSV file for no reason
data = pd.read_csv('test_data.csv')
data['date'] = pd.to_datetime(data['date'], errors='coerce').dt.date
data['value'] = data['return_d30_stock']
data = data[['date', 'value']]

df = data

# Convert date to ordinal for polyfit
df['date_ordinal'] = pd.to_datetime(df['date']).apply(lambda date: date.toordinal())

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)
        
        self.setParent(parent)

        FigureCanvas.updateGeometry(self)

        # Plot data
        self.axes.plot(df['date'], df['value'], label='Growth')

        # Calculate trendline
        z = np.polyfit(df['date_ordinal'], df['value'], 1)
        p = np.poly1d(z)

        # trendline_values = p(df['date_ordinal'])
        # # Plot trendline
        # self.axes.plot(df['date'], trendline_values, label='Trendline', color='r')

        # Add legend
        self.axes.legend()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt5 Matplotlib Trendline Example")

        # Create Matplotlib canvas
        mpl_canvas = MplCanvas(self, width=5, height=4, dpi=100)

        # Set central widget
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(mpl_canvas)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
