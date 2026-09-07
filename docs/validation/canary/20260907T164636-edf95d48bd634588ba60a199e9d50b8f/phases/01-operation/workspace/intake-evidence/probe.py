from labels import label


class UpperInt:
    def upper(self):
        return 7


class UpperList:
    def upper(self):
        return ['UPPER']


class Prefix(str):
    pass


class Reflected:
    def __radd__(self, other):
        return ('reflected', other)


class UpperReflected:
    def upper(self):
        return Reflected()


cases = [
    ('ordinary omitted', lambda: label('hello')),
    ('mixed-case prefix', lambda: label('hello', 'pre:')),
    ('keyword prefix', lambda: label('hello', prefix='pre:')),
    ('omitted None value', lambda: label(None)),
    ('omitted bytes value', lambda: label(b'hello')),
    ('omitted custom integer upper', lambda: label(UpperInt())),
    ('omitted custom reflected upper', lambda: label(UpperReflected())),
    ('invalid integer prefix', lambda: label('hello', 7)),
    ('invalid prefix and value', lambda: label(None, 7)),
    ('bytes prefix and value', lambda: label(b'hello', b'pre:')),
    ('list prefix and custom upper', lambda: label(UpperList(), ['pre:'])),
    ('string subclass prefix', lambda: label('hello', Prefix('pre:'))),
]
for name, call in cases:
    try:
        print(f'{name}: return {call()!r}')
    except Exception as exc:
        print(f'{name}: {type(exc).__name__}: {exc}')
print('probe completed')
