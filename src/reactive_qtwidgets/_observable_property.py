from typing import override

from PySide6.QtCore import QObject, SignalInstance, Slot

from reactive_qtwidgets._types import Consumer, ReadWriteProperty


class ObservableProperty[T](ReadWriteProperty[T]):

    def __init__(self, initial_value: T, *, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._value = initial_value
        self._bindings: set[tuple[Consumer[T] | None, SignalInstance | None]] = set()
    
    @override
    def __repr__(self) -> str:
        return f'ObservableProperty({self._value})'

    @property
    @override
    def value(self) -> T:
        return self._value

    @value.setter
    def value(self, value: T) -> None:
        if value != self._value:
            self._value = value
            self._notify_listeners()

    @override
    def bind(self, callback: Consumer[T] | None, signal: SignalInstance | None = None) -> None:
        if (callback, signal) in self._bindings:
            return
        if signal is not None:
            signal.connect(self._on_incoming_value)
        if callback is not None:
            self.value_changed.connect(callback)
            callback(self._value)
        self._bindings.add((callback, signal))

    @override
    def unbind(self, callback: Consumer[T] | None, signal: SignalInstance | None = None) -> None:
        if (callback, signal) not in self._bindings:
            return
        if signal is not None:
            signal.disconnect(self._on_incoming_value)
        if callback is not None:
            self.value_changed.disconnect(callback)
        self._bindings.remove((callback, signal))

    @override
    def unbind_all(self) -> None:
        for callback, signal in set(self._bindings):
            self.unbind(callback, signal)

    def _notify_listeners(self) -> None:
        self.value_changed.emit(self._value)

    @Slot(object)
    def _on_incoming_value(self, value: T) -> None:
        self.value = value
