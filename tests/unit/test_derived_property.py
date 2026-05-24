
from reactive_qtwidgets._derived_property import DerivedProperty
from reactive_qtwidgets._observable_property import ObservableProperty


def test_derived_property_basic_functionality() -> None:
    p1 = ObservableProperty(5)
    p2 = ObservableProperty(2)
    p3 = ObservableProperty(4)
    d = DerivedProperty(lambda: p1.value * p2.value + p3.value, p1, p2, p3)

    assert d.value == 14

    p2.value = 3

    assert d.value == 19

def test_derived_property_binding() -> None:
    p1 = ObservableProperty('John')
    p2 = ObservableProperty('Smith')
    q = ObservableProperty('')

    d = DerivedProperty(lambda: f'{p1.value} {p2.value}', p1, p2)

    assert d.value == 'John Smith'

    d.bind(lambda s: setattr(q, 'value', s))

    assert q.value == 'John Smith'

    p1.value = 'Lara'

    assert q.value == 'Lara Smith'

def test_derived_property_unbinding() -> None:
    text = ObservableProperty('Hello, World')
    length = ObservableProperty(12)

    verdict = False

    text_has_that_length = DerivedProperty(lambda: len(text.value) == length.value, text, length)

    def callback(value: bool) -> None:
        nonlocal verdict
        verdict = value
    
    text_has_that_length.bind(callback)

    assert verdict

    text.value = 'spam'
    
    assert not verdict

    text_has_that_length.unbind(callback)

    length.value = 4

    assert not verdict

def test_derived_property_multiple_binding() -> None:
    base = ObservableProperty(2)
    exponent = ObservableProperty(3)

    exped = DerivedProperty(lambda: base.value ** exponent.value, base, exponent)

    assert exped.value == 8

    exped_value = 0
    exped_property = ObservableProperty(0)

    def callback_value(x: int) -> None:
        nonlocal exped_value
        exped_value = x
    
    def callback_property(x: int) -> None:
        exped_property.value = x
    
    exped.bind(callback_value)
    exped.bind(callback_property)

    assert exped_value == 8
    assert exped_property.value == 8

    base.value = 3

    assert exped_value == 27
    assert exped_property.value == 27

    exped.unbind_all()

    exponent.value = 2

    assert exped.value == 9
    assert exped_value == 27
    assert exped_property.value == 27

def test_derived_property_dispose() -> None:
    text = ObservableProperty('the quick brown fox')
    uppercased = ObservableProperty(True)

    trans_text = DerivedProperty(lambda: text.value.upper() if uppercased.value else text.value.lower(), text, uppercased)

    assert trans_text.value == 'THE QUICK BROWN FOX'

    trans_text_value = ''

    def callback(txt: str) -> None:
        nonlocal trans_text_value
        trans_text_value = txt
    
    trans_text.bind(callback)

    text.value = 'HeLLo, wOrLd'

    assert trans_text.value == 'HELLO, WORLD'
    assert trans_text_value == 'HELLO, WORLD'

    trans_text.dispose()

    uppercased.value = False

    assert trans_text.value == 'HELLO, WORLD'
    assert trans_text_value == 'HELLO, WORLD'