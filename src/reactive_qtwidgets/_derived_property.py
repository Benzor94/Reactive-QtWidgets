from collections.abc import Iterable
from typing import override

from PySide6.QtCore import QObject

from reactive_qtwidgets._observable_property import ObservableProperty
from reactive_qtwidgets._types import Consumer, ReadableProperty, Supplier


class DerivedProperty[T](ReadableProperty[T]):

    def __init__(self, supplier: Supplier[T], properties: Iterable[ObservableProperty], *, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._supplier = supplier
        self._properties = set(properties)
        self._bindings: set[Consumer[T]] = set()
        self._value = supplier()
        for prop in self._properties:
            prop.bind(self._on_connected_property_value_change)

    @property
    @override
    def value(self) -> T:
        return self._value

    @override
    def bind(self, callback: Consumer[T]) -> None:
        if callback in self._bindings:
            return
        self.value_changed.connect(callback)
        callback(self._value)
        self._bindings.add(callback)
    
    @override
    def unbind(self, callback: Consumer[T]) -> None:
        if callback not in self._bindings:
            return
        self.value_changed.disconnect(callback)
        self._bindings.remove(callback)
    
    @override
    def unbind_all(self) -> None:
        for callback in set(self._bindings):
            self.unbind(callback)
    
    def dispose(self) -> None:
        for prop in self._properties:
            prop.unbind(self._on_connected_property_value_change)
        self._properties.clear()
        self.unbind_all()

    def _on_connected_property_value_change(self, _: T) -> None:
        self._value = self._supplier()
        self.value_changed.emit(self._value)
