from collections.abc import Callable
from typing import Any, Self

from PySide6.QtCore import QObject, Signal, SignalInstance


class SignalTransformer[T](QObject):

    transformed_signal = Signal(object)

    @classmethod
    def transform(cls, signal: SignalInstance) -> Callable[[Callable[..., T]], Self]:
        
        def transform_decorator(func: Callable[..., T]) -> Self:
            return cls(signal, func)
        
        return transform_decorator

    def __init__(self, signal: SignalInstance, transformation: Callable[..., T]) -> None:
        super().__init__()
        self._signal = signal
        self._transformation = transformation
        self._signal.connect(self._on_incoming_signal)

    def _on_incoming_signal(self, *args: Any) -> None:
        transformed = self._transformation(*args)
        self.transformed_signal.emit(transformed)
    
    def dispose(self) -> None:
        self._signal.disconnect(self._on_incoming_signal)
