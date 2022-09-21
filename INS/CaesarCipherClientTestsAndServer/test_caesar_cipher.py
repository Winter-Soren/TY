import pytest
from caesar_cipher import GenerateCaesarCipher

def test_GenerateCaesarCipher_CalledWithNonIntegerShift_RaisesValueError():
    with pytest.raises(ValueError):
        GenerateCaesarCipher('message', 'not_an_integer_shift')

def test_GenerateCaesarCipher_CalledWithNonStringMessage_RaisesValueError():
    with pytest.raises(ValueError):
        GenerateCaesarCipher(['not', 'a', 'string', 'message'], 10)

def test_GenerateCaesarCipher_CalledWithStringMessageAndIntegerShift_NoExceptionsRaised():
    shift_integer = 10
    message_string = 'message'
    try:
        GenerateCaesarCipher(message_string, shift_integer)
    except Exception:
        pytest.fail('An exception was not supposed to be raised when passed the correct argument types.')

def test_GenerateCaesarCipher_ShiftOfZero_ReturnsMessageUnchanged():
    assert GenerateCaesarCipher('message', 0) == 'message'

def test_GenerateCaesarCipher_ShiftOfOne_ReturnsMessageWithLettersShiftedOne():
    assert GenerateCaesarCipher('abc', 1) == 'bcd'

def test_GenerateCaesarCipher_ShiftOfNegativeOne_ReturnsMessageWithLettersShiftedNegativeOne():
    assert GenerateCaesarCipher('bcd', -1) == 'abc'

def test_GenerateCaesarCipher_ShiftOfAsciiRange_ReturnsMessageUnchanged():
    assert GenerateCaesarCipher('abc', 128) == 'abc'

def test_GenerateCaesarCipher_ShiftOfNegativeAsciiRange_ReturnsMessageUnchanged():
    assert GenerateCaesarCipher('abc', -128) == 'abc'

def test_GenerateCaesarCipher_ShiftOfAsciiRangePlusThree_ReturnsMessageShiftedThree():
    assert GenerateCaesarCipher('abc', 131) == 'def'

def test_GenerateCaesarCipher_ShiftOfNegativeAsciiRangeMinusThree_ReturnsMessageShiftedNegativeThree():
    assert GenerateCaesarCipher('def', -131) == 'abc'

def test_GenerateCaesarCipher_LargerRandomMessageAndShift_ReturnsCorrectMessage():
    assert GenerateCaesarCipher('GHIJKLMNOP', 7) == 'NOPQRSTUVW'

def test_GenerateCaesarCipher_ExtremelyLargeShift_ReturnsCorrectMessage():
    large_shift_thats_equivalent_to_zero = 128 * 10
    assert GenerateCaesarCipher('abcd', large_shift_thats_equivalent_to_zero) == 'abcd'

def test_GenerateCaesarCipher_ExtremelyLargeNegativeOneShift_ReturnsCorrectMessage():
    large_shift_thats_equivalent_to_zero = -((128 * 10) + 1)
    assert GenerateCaesarCipher('bcd', large_shift_thats_equivalent_to_zero) == 'abc'
