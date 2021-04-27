# pwexplode library

Simple implementation of the PKWARE Data Compression Library format (imploding) for byte streams in Python 3 licensed under GPL-3.0. 

# Implementation

This library is mostly based on the description of Ben Rudiak-
Gould in the [comp.compression group](https://groups.google.com/forum/#!msg/comp.compression/M5P064or93o/W1ca1-ad6kgJ) and [zlib's blast.c](https://github.com/madler/zlib/blob/master/contrib/blast/blast.c#L150). 

It should be noted that  there is  a small mistake in Ben's example. He uses `00 04 82 24 25 c7 80 7f` as example, which should decompress to `AIAIAIAIAIAIA`. However, testing this with my implementation failed. When I created it with the official pkware ziptool  (see tests in pwexplode), the sequence turned out to be actually `00 04 82 24 25 8f 80 7f` (notice the difference at byte 6). This will successfully decompress to `AIAIAIAIAIAIA`.

Instead of pure dictionaries, this package uses functions to provide the data of the tables necessary to decompress streams. This approach makes functions 'read-only' and can provide error feedback. However, it creates minimal overhead and slightly longer runtimes. In order to reduce the extra time a little bit, all tables are 'complete', _i.e._ each entry just needs to be extracted but not calculated. The difference is minimal and practical non-existant when accessing a function one time only; but these functions can be called hundred or thousand times per stream.

# Usage

Import pwexplode in your Python 3 programs and call the `explode(...)` function. Note that input and output are byte strings!

```python
import pwexplode
...
# Decompress input byte string 
inputdata = b'\x01\x04\x02\x6F\x5A\x08\xB6\x67\xE8\x86\x6A\xA9\x8A\x6D\x28'
            b'\x5E\x56\x6D\xCD\x5B\x5B\x6C\x47\x73\x18\xB6\x8A\x17\xF0\x0F'
...
outputdata = pwexplode.explode(inputdata) 
...
# prints b'I like consistent user interfaces.'
print(outputdata)
```

Calling pwexplode directly will run some tests:

```bash
$ ./pwexplode.py
```


