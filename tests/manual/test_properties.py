from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QDoubleSpinBox, QGroupBox, QHBoxLayout, QLabel, QMainWindow, QSlider, QVBoxLayout, QWidget

from reactive_qtwidgets import DerivedProperty, ObservableProperty


def test_properties() -> None:
    app = QApplication([])
    mw = MainWindow()
    mw.resize(600, 300)
    mw.show()
    app.exec()



class UnidirectionalBindingBox(QGroupBox):
    def __init__(self) -> None:
        super().__init__('Unidirectional binding')
        self._layout = QHBoxLayout(self)

        slider = QSlider(Qt.Orientation.Horizontal)
        slider.setRange(0, 100)
        slider.setValue(42)

        label = QLabel()
        label.setMinimumWidth(60)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._uni_prop = ObservableProperty(slider.value())
        self._uni_prop.bind(
            callback=lambda v: label.setText(str(v)),
            signal=slider.valueChanged,
        )

        self._layout.addWidget(QLabel('Slider:'))
        self._layout.addWidget(slider, stretch=1)
        self._layout.addWidget(QLabel('Value:'))
        self._layout.addWidget(label)


class BidirectionalBindingBox(QGroupBox):
    def __init__(self) -> None:
        super().__init__('Bidirectional binding')
        self._layout = QHBoxLayout(self)

        spin_a = QDoubleSpinBox()
        spin_a.setRange(-1000.0, 1000.0)
        spin_a.setDecimals(4)
        spin_a.setValue(3.1415)

        spin_b = QDoubleSpinBox()
        spin_b.setRange(-1000.0, 1000.0)
        spin_b.setDecimals(2)
        spin_b.setValue(3.1415)

        self._bi_prop = ObservableProperty[float](spin_a.value())
        self._bi_prop.bind(spin_a.setValue, spin_a.valueChanged)
        self._bi_prop.bind(spin_b.setValue, spin_b.valueChanged)

        self._layout.addWidget(QLabel('Spinbox A (4dp):'))
        self._layout.addWidget(spin_a)
        self._layout.addWidget(QLabel('◄──►'))
        self._layout.addWidget(QLabel('Spinbox B (2dp):'))
        self._layout.addWidget(spin_b)


class DerivedPropertyGroupBox(QGroupBox):
    def __init__(self) -> None:
        super().__init__('Derived property')
        self._layout = QVBoxLayout(self)

        sliders_row = QHBoxLayout()
        result_row = QHBoxLayout()
 
        slider_a = QSlider(Qt.Orientation.Horizontal)
        slider_a.setRange(0, 100)
        slider_a.setValue(23)
 
        slider_b = QSlider(Qt.Orientation.Horizontal)
        slider_b.setRange(0, 100)
        slider_b.setValue(47)
 
        label_a = QLabel(str(slider_a.value()))
        label_a.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_b = QLabel(str(slider_b.value()))
        label_b.setAlignment(Qt.AlignmentFlag.AlignCenter)
        result_label = QLabel()
        result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
 
        self._prop_a = ObservableProperty[int](slider_a.value())
        self._prop_b = ObservableProperty[int](slider_b.value())
 
        self._prop_a.bind(lambda v: label_a.setText(str(v)), slider_a.valueChanged)
        self._prop_b.bind(lambda v: label_b.setText(str(v)), slider_b.valueChanged)
 
        self._derived = DerivedProperty(
            lambda: f"{self._prop_a.value} + {self._prop_b.value} = {self._prop_a.value + self._prop_b.value}",
            self._prop_a, self._prop_b
        )
        self._derived.bind(result_label.setText)
 
        sliders_row.addWidget(QLabel("A:"))
        sliders_row.addWidget(slider_a, stretch=1)
        sliders_row.addWidget(label_a)
        sliders_row.addSpacing(16)
        sliders_row.addWidget(QLabel("B:"))
        sliders_row.addWidget(slider_b, stretch=1)
        sliders_row.addWidget(label_b)
 
        result_row.addWidget(QLabel("Result:"))
        result_row.addWidget(result_label, stretch=1)
 
        self._layout.addLayout(sliders_row)
        self._layout.addLayout(result_row)

class MainWindow(QMainWindow):

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Reactive Properties Demo")
 
        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)
        layout.setSpacing(16)
        layout.setContentsMargins(16, 16, 16, 16)
 
        layout.addWidget(UnidirectionalBindingBox())
        layout.addWidget(BidirectionalBindingBox())
        layout.addWidget(DerivedPropertyGroupBox())




