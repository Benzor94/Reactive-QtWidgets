from reactive_qtwidgets import Command, ObservableProperty


def test_command_basic_functionality() -> None:
    is_enabled_property = ObservableProperty(True)
    value_property = ObservableProperty('Hello world')

    counter = 0

    def action() -> None:
        nonlocal counter
        counter += 1

    command = Command(action, is_enabled_property)
    command.bind(value_property.value_changed)

    value_property.value = 'My name is John'

    assert counter == 1

    is_enabled_property.value = False

    value_property.value = 'Spam'

    assert counter == 1

    is_enabled_property.value = True

    value_property.value = 'Eggs'

    assert counter == 2

def test_command_unbind() -> None:
    value_property = ObservableProperty('Hello, world')
    
    counter = 0

    def action() -> None:
        nonlocal counter
        counter +=1
    
    command = Command(action)
    command.bind(value_property.value_changed)

    value_property.value = 'Spam'

    assert counter == 1

    command.unbind(value_property.value_changed)

    value_property.value = 'Eggs'

    assert counter == 1