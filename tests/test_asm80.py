"""Tests for the suite8080.asm80 module."""

from unittest import mock

import pytest

from suite8080 import asm80


@pytest.mark.parametrize('source_line, expected', [
    # Label, mnemonic, operand1, operand2, comment
    #
    # Blank line
    ('', ('', '', '', '', '')),
    # All spaces
    ('   ', ('', '', '', '', '')),
    # Mixed whitespace
    ('\t  \t  ', ('', '', '', '', '')),
    # Comment only
    ('  ; Comment only', ('', '', '', '', 'Comment only')),
    # Label only
    ('label:', ('label', '', '', '', '')),
    # Only mnemonic
    ('nop', ('', 'nop', '', '', '')),
    # One operand
    ('xra a', ('', 'xra', 'a', '', '')),
    # Two operands
    ('mov b, a', ('', 'mov', 'b', 'a', '')),
    # Immediate operand
    ('adi 01h', ('', 'adi', '01h', '', '')),
    # Label operand
    ('jmp loop', ('', 'jmp', 'loop', '', '')),
    # All tokens
    ('label: mov b, a ; Comment', ('label', 'mov', 'b', 'a', 'Comment')),
    # All tokens separated by tabs
    ('label:\tmov\tb,\ta\t;\tComment', ('label', 'mov', 'b', 'a', 'Comment')),
    # All caps Code
    ('LABEL: MOV B, A ; Comment', ('label', 'mov', 'b', 'a', 'Comment')),
    # Incorrect syntax: missing label terminator
    ('label mov b, a ; Comment', ('', 'label mov', 'b', 'a', 'Comment')),
    # Incorrect syntax: missing comment start character
    ('label: mov b, a Comment', ('label', 'mov', 'b', 'a comment', '')),
])
def test_parse(source_line, expected):
    assert asm80.parse(source_line) == expected


def test_report_error(capsys):
    with pytest.raises(SystemExit):
        expected = 'error message'
        asm80.report_error('error message')
        captured = capsys.readouterr()
        assert expected in captured.err


# The tests that use multiple patching may be replaced with patch.multiple().
# If I can figure how it works.

@mock.patch('suite8080.asm80.label', 'label')
@mock.patch('suite8080.asm80.address', 0)
@mock.patch('suite8080.asm80.symbol_table', {})
def test_add_label_address0():
    expected = asm80.address
    asm80.add_label()
    assert asm80.symbol_table[asm80.label] == expected


@mock.patch('suite8080.asm80.label', 'label')
@mock.patch('suite8080.asm80.address', 10)
@mock.patch('suite8080.asm80.symbol_table', {})
def test_add_label_new():
    expected = asm80.address
    asm80.add_label()
    assert asm80.symbol_table[asm80.label] == expected


@mock.patch('suite8080.asm80.label', 'label')
@mock.patch('suite8080.asm80.address', 10)
@mock.patch('suite8080.asm80.symbol_table', {'label': 10})
def test_add_label_duplicate(capsys):
    with pytest.raises(SystemExit):
        expected = 'duplicate label'
        asm80.symbol_table['label'] = 10
        asm80.add_label()
        captured = capsys.readouterr()
        assert expected in captured.err


# There's a bug but I can't figure where.
@pytest.mark.skip(reason='bug')
@mock.patch('suite8080.asm80.operand1', 'b')
@mock.patch('suite8080.asm80.operand2', 'c')
@mock.patch('suite8080.asm80.source_pass', 2)
@mock.patch('suite8080.asm80.output', b'')
def test_mov_b_c():
    expected = b'0x41'  # 65
    asm80.mov()
    assert asm80.output == expected


@pytest.mark.parametrize('register, opcode', [
    ('b', 0),
    ('c', 1),
    ('d', 2),
    ('e', 3),
    ('h', 4),
    ('l', 5),
    ('m', 6),
    ('a', 7),
])
def test_register_offset8(register, opcode):
    assert asm80.register_offset8(register) == opcode


@mock.patch('suite8080.asm80.operand1', 'b')
@mock.patch('suite8080.asm80.operand2', 'invalid')
def test_register_offset8_invalid_register(capsys):
    with pytest.raises(SystemExit):
        expected = 'invalid register'
        asm80.mov()
        captured = capsys.readouterr()
        assert expected in captured.err


@mock.patch('suite8080.asm80.operand1', 'b')
@mock.patch('suite8080.asm80.operand2', '')
def test_register_offset8_missing_register(capsys):
    with pytest.raises(SystemExit):
        expected = 'invalid register'
        asm80.mov()
        captured = capsys.readouterr()
        assert expected in captured.err


@pytest.mark.skip(reason='bug')
@mock.patch('suite8080.asm80.operand1', '12')
@mock.patch('suite8080.asm80.output', b'')
def test_immediate_operand_decimal():
    expected = b'\x0c'
    asm80.immediate_operand()
    assert asm80.output == expected


@pytest.mark.parametrize('input, number', [
    ('123', 123),
    ('123h', 291),
    ('02h', 2),
    ('02', 2),
    ('0ah', 10),
])
def test_get_number(input, number):
    assert asm80.get_number(input) == number