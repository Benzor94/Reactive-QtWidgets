from PySide6.QtWidgets import QApplication, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget

from reactive_qtwidgets import Command, DerivedProperty, ObservableProperty


def test_command() -> None:
    app = QApplication([])
    mw = QMainWindow()

    label = QLabel()
    text_box = QLineEdit()
    pause_btn = QPushButton('Pause')
    generate_btn = QPushButton('Generate')

    pause_btn.setCheckable(True)

    is_paused = ObservableProperty(False)
    is_paused.bind(lambda b: pause_btn.setChecked(b), pause_btn.toggled)

    is_unpaused = DerivedProperty(lambda: not is_paused.value, is_paused)

    gen_command = Command(lambda: label.setText(text_box.text()), is_unpaused)
    gen_command.bind(generate_btn.clicked)

    root = QWidget()
    layout = QVBoxLayout(root)
    layout.addWidget(label)
    layout.addWidget(text_box)

    inner_layout = QHBoxLayout()
    inner_layout.addWidget(pause_btn)
    inner_layout.addWidget(generate_btn)
    layout.addLayout(inner_layout)

    mw.setCentralWidget(root)

    mw.resize(600, 300)
    mw.show()
    app.exec()