
from reactive_qtwidgets import ObservableProperty, SignalTransformer


def test_signal_transformer_basic_functionality() -> None:
    text = ObservableProperty('Hello World')
    text_length = ObservableProperty(0)

    def transformer(length: int) -> str:
        return text.value[0:length]
    
    signal_transformer = SignalTransformer(text_length.value_changed, transformer)
    text.bind(lambda txt: setattr(text_length, 'value', len(txt)), signal_transformer.transformed_signal)

    assert text.value == 'Hello World'
    assert text_length.value == 11

    text_length.value = 5

    assert text.value == 'Hello'
    assert text_length.value == 5

    signal_transformer.dispose()

    text.value = 'spam'
    
    assert text_length.value == 4

    text_length.value = 2

    assert text.value == 'spam'

def test_signal_transformer_decorator() -> None:
    text = ObservableProperty('Hello World')
    text_length = ObservableProperty(0)

    @SignalTransformer.transform(text_length.value_changed)
    def signal_transformer(length: int) -> str:
        return text.value[0:length]
    
    text.bind(lambda txt: setattr(text_length, 'value', len(txt)), signal_transformer.transformed_signal)

    assert text.value == 'Hello World'
    assert text_length.value == 11

    text_length.value = 5

    assert text.value == 'Hello'
    assert text_length.value == 5