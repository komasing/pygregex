# pygregex
Python library for regular expressions over arbitrary iterable data
structures with hashable elements.

### Motivation

Have you ever had sequential ordered data which you wanted to test
against patterns? If that's the case, then you must have come across
regular expressions.

However, Python's brilliant builtin regular expression library _re_
falls short when we want to detect multisymbol or custom object
sequences.

### Solution

Current library utilizes Python's builtin _re_ library and the large
range of unicode characters (1 114 112) to encode custom hashable elements
to unicode characters, run regular expression matching on encoded
sequence, and decode the results back to the custom elements.

### Issues

Due to the limited unicode characters, the patterns and sequences can
only contain 1 114 112 different custom elements. It can be a problem,
if it's desirable to match for example events with many attributes, some
of which are numerical, and there are many events.

A workaround is to limit the number of attributes and avoid continuous
features, whenever expecting long sequences.
