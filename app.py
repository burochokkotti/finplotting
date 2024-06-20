import sys
import pandas as pd
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
import finplot as fplt

# Read data from CSV file
data = pd.read_csv('test_data.csv')
data['date'] = pd.to_datetime(data['date'], errors='coerce')
data['value'] = data['return_d30_stock']
data = data[['date', 'value']]

df = data

# Convert date to ordinal for polyfit
df['date_ordinal'] = df['date'].apply(lambda date: date.toordinal())

class FinplotCanvas(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setParent(parent)
        layout = QVBoxLayout(self)
        self.setLayout(layout)
        
        # Create finplot window
        self.plot_item = fplt.create_plot('Trendline Example', init_zoom_periods=100, maximize=False)
        
        layout.addWidget(self.plot_item.vb.win)
        
        # Plot data
        fplt.plot(df['date'], df['value'], ax=self.plot_item, legend='Data')
        
        # Calculate trendline
        z = np.polyfit(df['date_ordinal'], df['value'], 1)
        p = np.poly1d(z)
        trendline_values = p(df['date_ordinal'])
        
        # Plot trendline
        # fplt.plot(df['date'], trendline_values, ax=self.plot_item, legend='Trendline', color='r')

        # Set initial view range to the first 30 days
        initial_dates = df['date']
        initial_values = df['value']
        self.plot_item.vb.setXRange(initial_dates.min().timestamp(), initial_dates.max().timestamp(), padding=0)
        self.plot_item.vb.setYRange(initial_values.min(), initial_values.max(), padding=0)
        
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("PyQt5 Finplot Trendline Example")

        # Create finplot canvas
        finplot_canvas = FinplotCanvas(self)

        # Set central widget
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(finplot_canvas)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
