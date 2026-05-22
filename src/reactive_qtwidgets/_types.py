from abc import ABC, ABCMeta, abstractmethod
from collections.abc import Callable
from typing import override

from PySide6.QtCore import QObject, SignalInstance
from shiboken6.Shiboken import Object

type Supplier[T] = Callable[[],T]
type Consumer[T] = Callable[[T], None]

class QObjectABCMeta(Object, ABCMeta): ...

class ReadableProperty[T](QObject, ABC, metaclass=QObjectABCMeta):

    @property
    @abstractmethod
    def value(self) -> T: ...

    @abstractmethod
    def bind(self, callback: Consumer[T]) -> None: ...

    @abstractmethod
    def unbind(self, callback: Consumer[T]) -> None: ...

    @abstractmethod
    def unbind_all(self) -> None: ...

class ReadWriteProperty[T](ReadableProperty[T]):

    @ReadableProperty.value.setter
    @abstractmethod
    def value(self, value: T) -> None: ...

    @abstractmethod
    @override
    def bind(self, callback: Consumer[T] | None, signal: SignalInstance | None = None) -> None: ...

    @abstractmethod
    @override
    def unbind(self, callback: Consumer[T] | None, signal: SignalInstance | None = None) -> None: ...