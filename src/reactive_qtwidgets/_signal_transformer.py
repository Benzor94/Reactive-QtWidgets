"""Qt signal adapter that transforms signal arguments before re-emitting them."""

from collections.abc import Callable
from typing import Any, Self

from PySide6.QtCore import QObject, Signal, SignalInstance


class SignalTransformer[T](QObject):
    """Connects to a Qt signal, transforms its arguments, and re-emits the result.
 
    The transformation function is applied each time the source fires,
    and the result is emitted as :attr:`transformed_signal`.
 
    Args:
        signal: The Qt signal to subscribe to.
        transformation: A callable applied to the signal's arguments to
            produce the transformed value that is emitted on
            :attr:`transformed_signal`.
    
    Examples:
        Decorator-style usage:

        ```python
        @SignalTransformer.transform(slider.valueChanged)
        def as_fraction(raw: int) -> float:
            return raw / slider.maximum()

        as_fraction.transformed_signal.connect(progress_label.update)
        ```

        Direct construction:

        ```python
        transformer = SignalTransformer(line_edit.textChanged, str.strip)
        transformer.transformed_signal.connect(search_model.set_query)
        ```
    """


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
