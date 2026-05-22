from abc import ABC, ABCMeta, abstractmethod
from collections.abc import Callable

from PySide6.QtCore import QObject
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
