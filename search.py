import re


class Symbol(object):

    def __init__(self, element):
        self.value = element

    def __hash__(self):
        return hash(self.value)


class InvalidPatternElement(Exception):
    pass


class SymbolEncoder(object):

    def __init__(self):
        self._symbol_hashes = []
        self._hash_to_hash_index = {}

    def encode(self, symbol):
        hash_index = self._hash_to_hash_index.get(hash(symbol), None)

        if hash_index is None:
            self._hash_to_hash_index[hash(symbol)] = len(self._symbol_hashes)
            self._symbol_hashes.append(hash(symbol))

        return chr(self._hash_to_hash_index[hash(symbol)])


class Match(object):

    def __init__(self, match, start, end):
        self.match = match
        self.span = (start, end)

    def __repr__(self):
        return "<pygregex.Match object; span={0}, match='{1}'>".format(self.span, self.match)


def _encode_pattern(pattern, encoder):
    encoded_pattern = []

    for element_idx, element in enumerate(pattern):
        if isinstance(element, Symbol):
            encoded_pattern.append(encoder.encode(element))
        elif isinstance(element, str):
            if len(element) > 1:
                raise InvalidPatternElement('Pattern element at index {0} is a string longer than one character. Maybe you meant it to be an instance of Symbol?'.format(element_idx))
            else:
                encoded_pattern.append(element)
        else:
            raise InvalidPatternElement('Pattern element at index {0} is not an instance of Symbol.'.format(element_idx))

    return ''.join(encoded_pattern)


def _encode_sequence(sequence, encoder):
    encoded_sequence = []

    for element in sequence:
        encoded_sequence.append(encoder.encode(element))

    return ''.join(encoded_sequence)


def search(pattern, sequence):
    encoder = SymbolEncoder()

    encoded_pattern = _encode_pattern(pattern, encoder)
    encoded_sequence = _encode_sequence(sequence, encoder)

    for match in re.finditer(encoded_pattern, encoded_sequence):
        yield Match(match=sequence[match.start(): match.end()], start=match.start(), end=match.end())


print([match for match in search(
    pattern=[Symbol('aa'), '.', '*', Symbol('aa')],
    sequence=['aa', 'bb', 'cc', 'aa']
)])