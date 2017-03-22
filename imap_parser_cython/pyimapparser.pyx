# -*- coding: utf-8 -*-
"""
"""
from __future__ import generator_stop

from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp cimport bool, int

from cython.operator cimport dereference, postincrement, preincrement,\
                             predecrement


from . import constants

cdef extern from "ctype.h":
    int isblank ( int c )
    int isalnum ( int c )
    int atoi (const char * str)

cdef Py_UCS4 LIST_START = '('
cdef Py_UCS4 LIST_END = ')'
cdef Py_UCS4 LITERAL_START = '{'
cdef Py_UCS4 LITERAL_END = '}'
cdef Py_UCS4 DOUBLE_QUOTE = '"'
cdef Py_UCS4 SINGLE_QUOTE = '\''
cdef Py_UCS4 WHITESPACE = ' '
cdef Py_UCS4 SQUARE_BRACKETS_START = '['
cdef Py_UCS4 SQUARE_BRACKETS_END = ']'
cdef Py_UCS4 ESCAPING_CHAR = '\\'
cdef Py_UCS4 END_OF_LINE = '\0'
cdef Py_UCS4 LESS_SIGN_LINE = '<'
cdef Py_UCS4 ESCAPEDSLASH = '\\'
cdef Py_UCS4 DOLLAR = '$'


cdef class ResponseTokenizer:
    cdef string line
    cdef list literals
    cdef size_t list_count
    cdef size_t pos

    def __init__(self, const string & line, list  literals):
        self.literals = literals
        self.list_count = 0
        self.pos = 0
        self.line = line

    def __iter__(self):
        return self

    def __next__(self):
        if not self.has_next():
            raise StopIteration()

        self.skipWhiteSpaces()

        if not self.has_next():
            raise StopIteration()

        cdef char current = self.line.at(postincrement(self.pos))

        if current == LIST_START:
            preincrement(self.list_count)
            return [item for item in self]
        elif current == LIST_END or current == END_OF_LINE:
            predecrement(self.list_count)
            raise StopIteration()
        elif current == DOUBLE_QUOTE or current == SINGLE_QUOTE:
            return self.read_until(current)
        elif current == LITERAL_START:
            return self.get_literal_value(self.read_until(LITERAL_END))
        elif self.is_atom(current):
            return self.parse_value(<bytes>current + self.read_until(WHITESPACE))

        raise KeyError(<bytes>current)

    cdef object get_literal_value(self, const string & size):
        assert self.literals, 'Literal list is empty'
        value = self.literals.pop(0)
        if len(value) != atoi(size.c_str()):
            msg = 'Expected {} octets but got {} . ' \
                  'Value: {}'.format(size, len(value), value)
            raise Exception(msg)
        return value

    cdef object parse_value(self, bytes val):
        """Parse value from IMAP response

        :param val:
        :return:
        """
        if val.lower() == b'nil' or not val:
            return None
        if val.isdigit():
            return int(val)
        return val

    cdef bool has_next(self):
        return self.pos < self.line.size()

    cdef void skipWhiteSpaces(self):
        while self.has_next():
            if not isblank(self.line.at(self.pos)):
                break
            preincrement(self.pos)

    cdef bool is_atom(self, const char & char_):
        return isalnum(char_) or char_ == ESCAPEDSLASH or char_ == DOLLAR

    cdef string read_until(self, const char & delim, bool append_delim=False):
        cdef string res
        if not self.has_next():
            return res
        cdef char char_ = self.line.at(self.pos)
        cdef char prev
        while self.has_next() or char_ != END_OF_LINE:
            if delim == WHITESPACE:
                if self.list_count > 0 and char_ == LIST_END:
                    break
                if char_ == SQUARE_BRACKETS_START:
                    preincrement(self.pos)
                    res.push_back(char_)
                    res.append(self.read_until(SQUARE_BRACKETS_END, True))
                    break
            if char_ == delim and prev != ESCAPING_CHAR:
                if append_delim:
                    res.push_back(char_)
                preincrement(self.pos)
                break
            res.push_back(char_)
            prev = char_
            preincrement(self.pos)
            if not self.has_next():
                break
            char_ = self.line.at(self.pos)
        return res


class AtomTokenizer(object):
    """Tokenize imap fetch response

    """
    __default_atom_parser = constants.FETCH_ITEMS.get(b'X-')

    __slots__ = ('__tokenizer', 'name', 'value')

    def __init__(self, line=b'', literals=[]):
        self.tokenize(line, literals)

    def tokenize(self, line, literals):
        self.__tokenizer = ResponseTokenizer(line, literals)
        self.name = None
        self.value = None
        return self

    def __iter__(self):
        self.name = 'SEQ'
        self.value = self.__tokenizer.__next__()
        yield self

        rest_items = iter(self.__tokenizer.__next__())

        for item in rest_items:
            name, atom_data = parse_atom_name(item)
            atom = constants.FETCH_ITEMS.get(name, self.__default_atom_parser)
            self.name = name.decode()
            self.value = atom.parse(atom_data, rest_items.__next__())
            yield self

    def items(self):
        yield from [(item.name, item.value) for item in self]

class ListTokenizer(ResponseTokenizer):
    __slots__ = ()

#cdef size_t NOT_FOUND = string.npos

cdef bool is_range_valid(const size_t & pos,const size_t & pos2, const size_t & size):
    if pos < 0 or pos2 < 0:
        return False
    if not pos >=0 and pos <= size:
        return False
    return pos2 >=0 and pos2 <= size and pos2 > pos



cdef tuple _get_transferred(const string & line):
    cdef size_t pos = line.find_last_of(b'<')
    cdef size_t part_end = line.find_last_of(b'>')
    if is_range_valid(pos, part_end, line.size()):
        return pos, line.substr(pos+1,part_end-pos-1)
    return pos, b''

def get_transferred(line: bytes):
    return _get_transferred(<string>line)[-1]

cdef tuple _get_part(const string & line):
    cdef size_t pos = line.find_first_of(b'[')
    cdef size_t part_end = line.find_last_of(b']')
    if is_range_valid(pos, part_end, line.size()):
        return pos, line.substr(pos + 1, part_end - pos - 1)
    return pos, b''

def get_part(line: bytes):
    return _get_part(<string>line)[-1]

cdef tuple parse_atom_name(const string & name):

    part_pos, part = _get_part(name)
    transferred_pos, transferred = _get_transferred(name)

    if part_pos == -1 and transferred_pos == -1:
        return name, {}

    tuncate_pos = min(part_pos, transferred_pos)
    if tuncate_pos <= 0:
        raise Exception('??????')
    return name.substr(0, tuncate_pos), {'part': part,
                                         'transferred': transferred}

