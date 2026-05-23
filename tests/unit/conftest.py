from collections.abc import Generator

from PySide6.QtCore import QCoreApplication
from pytest import fixture


@fixture(scope='session')
def qapp() -> Generator[QCoreApplication, None, None]:
    app = QCoreApplication([])
    yield app