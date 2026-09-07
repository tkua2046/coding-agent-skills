import sys
import unicodedata
from labels import label

print('Python:', sys.version)
print('Unicode data:', unicodedata.unidata_version)
for args, kwargs in [
    (('abc',), {}), (('ß',), {}), (('ﬃ',), {}),
    (('ı',), {}), (('é',), {}), (('aß',), {}),
    (('e\u0301',), {}), (('',), {}),
    (('ß',), {'prefix': 'id:'}), (('abc', 'id:'), {}),
    ((None,), {}), ((123,), {}), ((b'abc',), {}),
    (('abc',), {'prefix': None}),
]:
    try:
        result = label(*args, **kwargs)
        print(f'label{args!r}, kwargs={kwargs!r} -> {result!r}; length={len(result)}')
    except Exception as exc:
        print(f'label{args!r}, kwargs={kwargs!r} -> {type(exc).__name__}: {exc}')
