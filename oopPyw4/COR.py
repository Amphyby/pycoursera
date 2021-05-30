# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
class SomeObject:
    def __init__(self):
        self.integer_field = 0
        self.float_field = 0.0
        self.string_field = ""

class EventGet:
    def __init__(self, kind):
        self.kind = kind

class EventSet:
    def __init__(self, value):
        self.value = value

class NullHandler:
    def __init__(self, previous):
        self.preceeding = previous

    def handle(self, obj, event):
        if self.preceeding is not None:
            return self.preceeding.handle(obj, event)

class IntHandler(NullHandler):
    def handle(self, obj, event):
        if isinstance(event, EventGet) and event.kind == int:
            return obj.integer_field
        elif isinstance(event, EventSet) and type(event.value) == int:
            obj.integer_field = event.value
            return
        else:
            return super().handle(obj, event)

class FloatHandler(NullHandler):
    def handle(self, obj, event):
        if isinstance(event, EventGet) and event.kind == float:
            return obj.float_field
        elif isinstance(event, EventSet) and type(event.value) == float:
            obj.float_field = event.value
            return
        else:
            return super().handle(obj, event)

class StrHandler(NullHandler):
    def handle(self, obj, event):
        if isinstance(event, EventGet) and event.kind == str:
            return obj.string_field
        elif isinstance(event, EventSet) and type(event.value) == str:
            obj.string_field = event.value
            return
        else:
            return super().handle(obj, event)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    chain = IntHandler(FloatHandler(StrHandler(NullHandler)))
    obj = SomeObject()
    obj.integer_field = 42
    obj.float_field = 3.14
    obj.string_field = "some text"
    chain = IntHandler(FloatHandler(StrHandler(NullHandler)))
    print(chain.handle(obj, EventGet(int)))
    print(chain.handle(obj, EventGet(float)))
    print(chain.handle(obj, EventGet(str)))
    chain.handle(obj, EventSet(100))
    print(chain.handle(obj, EventGet(int)))
    chain.handle(obj, EventSet(0.5))
    print(chain.handle(obj, EventGet(float)))
    chain.handle(obj, EventSet('new text'))
    print(chain.handle(obj, EventGet(str)))

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
