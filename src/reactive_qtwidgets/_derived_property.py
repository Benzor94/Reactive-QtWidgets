from collections.abc import Iterable
from typing import override

from PySide6.QtCore import QObject, Signal

from reactive_qtwidgets._observable_property import ObservableProperty
from reactive_qtwidgets._types import Consumer, ReadableProperty, Supplier


class DerivedProperty[T](ReadableProperty[T]):
    _value_changed = Signal(object)

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
        callback(self._value)
        self._value_changed.connect(callback)
        self._bindings.add(callback)
    
    @override
    def unbind(self, callback: Consumer[T]) -> None:
        if callback not in self._bindings:
            return
        self._value_changed.disconnect(callback)
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
        self._value_changed.emit(self._value)
