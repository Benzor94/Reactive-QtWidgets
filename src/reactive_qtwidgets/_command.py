from collections.abc import Callable
from typing import Self

from PySide6.QtCore import QObject, SignalInstance, Slot

from reactive_qtwidgets import ObservableProperty
from reactive_qtwidgets._types import ReadableProperty


class Command(QObject):

    @classmethod
    def action(cls, is_enabled: ReadableProperty[bool] | None = None) -> Callable[[Callable[[], None]], Self]:

        def action_decorator(func: Callable[[], None]) -> Self:
            return cls(func, is_enabled)
        
        return action_decorator

    def __init__(self, action: Callable[[], None], is_enabled: ReadableProperty[bool] | None = None, *, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._action = action
        self._is_enabled = is_enabled if is_enabled is not None else ObservableProperty(True)
        self._bindings: set[SignalInstance] = set()
    
    @property
    def is_enabled(self) -> ReadableProperty[bool]:
        return self._is_enabled
    
    def bind(self, signal: SignalInstance) -> None:
        if signal in self._bindings:
            return
        signal.connect(self._on_incoming_signal)
        self._bindings.add(signal)
    
    def unbind(self, signal: SignalInstance) -> None:
        if signal not in self._bindings:
            return
        signal.disconnect(self._on_incoming_signal)
        self._bindings.remove(signal)
    
    def unbind_all(self) -> None:
        for signal in set(self._bindings):
            self.unbind(signal)
    
    @Slot()
    def _on_incoming_signal(self) -> None:
        if self._is_enabled.value:
            self._action()

