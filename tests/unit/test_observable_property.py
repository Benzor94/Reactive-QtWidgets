from PySide6.QtCore import QObject, Signal
from pytest import mark

from reactive_qtwidgets import ObservableProperty


@mark.usefixtures('qapp')
def test_observable_property_basic_functionality() -> None:
    p1 = ObservableProperty(2.3)
    p2 = ObservableProperty(p1.value)
    
    p1.bind(lambda x: setattr(p2, 'value', x), p2.value_changed)

    p1.value = 9.1
    assert p2.value == 9.1
    p2.value = 18.2
    assert p1.value == 18.2

@mark.usefixtures('qapp')
def test_observable_property_stability() -> None:
    
    class DummyObject(QObject):

        value_changed = Signal(float)

        def __init__(self, initial_value: float) -> None:
            super().__init__()
            self._value = round(initial_value, 2)
        
        @property
        def value(self) -> float:
            return self._value
        
        @value.setter
        def value(self, value: float) -> None:
            trunc = round(value, 2)
            if trunc != self._value:
                self._value = trunc
                self.value_changed.emit(trunc)
    
    dummy_obj = DummyObject(0.0)

    p = ObservableProperty(9.999999)
    p.bind(lambda x: setattr(dummy_obj, 'value', x), dummy_obj.value_changed)

    assert p.value == 10.0

@mark.usefixtures('qapp')
def test_observable_property_unbind() -> None:
    p = ObservableProperty('herp derp')
    q = ObservableProperty('hurr durr')

    callback = lambda x: setattr(q, 'value', x)

    p.bind(callback, q.value_changed)
    q.value = 'the quick brown fox etc.'
    assert p.value == 'the quick brown fox etc.'

    p.unbind(callback, q.value_changed)
    p.value = 'my name is bob'
    assert q.value == 'the quick brown fox etc.'
    q.value = 'ni'
    assert p.value == 'my name is bob'

@mark.usefixtures('qapp')
def test_observable_property_multiple_binding() -> None:
    p = ObservableProperty('hello world')
    q1 = ObservableProperty('')
    q2 = ObservableProperty('my name is bob')
    q3 = ObservableProperty('sudoku')

    p.bind(lambda x: setattr(q1, 'value', x), q1.value_changed)
    p.bind(lambda x: setattr(q2, 'value', x), q2.value_changed)
    p.bind(lambda x: setattr(q3, 'value', x), q3.value_changed)

    p.value = 'spam'

    assert q1.value == 'spam'
    assert q2.value == 'spam'
    assert q3.value == 'spam'

    q3.value = 'eggs'

    assert p.value == 'eggs'
    assert q1.value == 'eggs'
    assert q2.value == 'eggs'

    p.unbind_all()

    p.value = 'shrubbery'

    assert q1.value == 'eggs'
    assert q2.value == 'eggs'
    assert q3.value == 'eggs'

    q3.value = 'ni'

    assert p.value == 'shrubbery'
    assert q1.value == 'eggs'
    assert q2.value == 'eggs'

@mark.usefixtures('qapp')
def test_observable_property_unidirectional_binding_target_listens() -> None:
    p = ObservableProperty('hello world')
    q = ObservableProperty('')

    p.bind(lambda x: setattr(q, 'value', x))

    assert q.value == 'hello world'

    p.value = 'spam'

    assert q.value == 'spam'

    q.value = 'eggs'

    assert p.value == 'spam'

@mark.usefixtures('qapp')
def test_observable_property_unidirectional_binding_property_listens() -> None:
    p = ObservableProperty('hello world')
    q = ObservableProperty('')

    p.bind(None, q.value_changed)
    
    assert p.value == 'hello world' # there is no immediate effect here !!!

    p.value = 'spam'

    assert not q.value

    q.value = 'eggs'

    assert p.value == 'eggs'