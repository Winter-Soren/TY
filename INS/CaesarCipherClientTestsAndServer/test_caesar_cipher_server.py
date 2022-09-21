import socket
import select
import time
import pytest
import string
import os
from timeit import default_timer as timer
from multiprocessing import Process, Manager

_host = '127.0.0.1'
_server_port = 55555
# generate really large message and expected response once for all tests in module
really_large_msg, really_large_msg_response = '', ''
for idx in range(10000):
    really_large_msg +=  '129 ' + string.ascii_lowercase + ' '
    really_large_msg_response += string.ascii_lowercase[1:] + '{ '

@pytest.fixture
def CaesarCipherServerFixture(request):
    class TestInfo:
        _sock = None

        def __init__(self):
            self._sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                self._sock.connect((_host, _server_port))
            except Exception as e:
                assert False, 'Unable to connect to server on port ' + \
                    str(_server_port) + ', exception: ' + str(e)

        def get_large_message_and_expected_response(self):
            return (really_large_msg, really_large_msg_response)

    t = TestInfo()

    def Uninitialize():
        t._sock.shutdown(socket.SHUT_RDWR)
        t._sock.close()
        t._sock = None

    request.addfinalizer(Uninitialize)
    return t


def test_ClientsFirstMessageHasNoTrailingSpace_ServerWillWaitForAdditionalMessages(CaesarCipherServerFixture):
    sock = CaesarCipherServerFixture._sock
    one_second_timeout = 1
    timed_out = False

    sock.sendall(b'text_without_a_trailing_space')
    sock.setblocking(0)
    ready = select.select([sock], [], [], one_second_timeout)
    if not ready[0]:
        timed_out = True

    assert timed_out


def test_ClientsFirstWordIsNotANumber_ServerClosesConnection(CaesarCipherServerFixture):
    sock = CaesarCipherServerFixture._sock
    response = None

    try:
        sock.sendall(b'Not_A_Number message')
        response = sock.recv(1024)
    except socket.error, e:
        pass

    assert response == ''


def test_ClientsFirstWordIsANumberAndSecondHasTrailingSpace_ServerRespondsWithMessage(CaesarCipherServerFixture):
    sock = CaesarCipherServerFixture._sock
    response = None

    try:
        sock.sendall(b'123 message ')
        response = sock.recv(1024)
    except socket.error, e:
        pass

    assert response


def test_ShiftOfZero_ServerRespondsWithSecondWordUnchanged(CaesarCipherServerFixture):
    sock = CaesarCipherServerFixture._sock
    response = None

    try:
        sock.sendall(b'0 unchanged_message ')
        response = sock.recv(1024)
    except socket.error, e:
        pass

    assert response == 'unchanged_message '

def test_ShiftOfOneSingleCharMessage_ServerRespondsWithCharShiftedOne(CaesarCipherServerFixture):
    sock = CaesarCipherServerFixture._sock
    response = None

    try:
        sock.sendall(b'1 a ')
        response = sock.recv(1024)
    except socket.error, e:
        pass

    assert response == 'b '

def test_ShiftOfOneMultipleCharsMessage_ServerRespondsWithSecondWordsCharsShiftedOne(CaesarCipherServerFixture):
    sock = CaesarCipherServerFixture._sock
    response = None

    try:
        sock.sendall(b'1 abc ')
        response = sock.recv(1024)
    except socket.error, e:
        pass

    assert response == 'bcd '


def test_ShiftOfTwoMultipleCharsMessage_ServerRespondsWithSecondWordsCharsShiftedTwo(CaesarCipherServerFixture):
    sock = CaesarCipherServerFixture._sock
    response = None

    try:
        sock.sendall(b'2 abc ')
        response = sock.recv(1024)
    except socket.error, e:
        pass

    assert response == 'cde '

def test_MultipleShiftOfOneCharMessages_RespondsWithCharsShiftedOneWithTrailingSpaces(CaesarCipherServerFixture):
    sock = CaesarCipherServerFixture._sock
    response = None

    try:
        sock.sendall(b'1 a 1 b ')
        response = sock.recv(1024)
    except socket.error, e:
        pass

    assert response == 'b c '

def test_ShiftOfOneWithLastAsciiCharMessage_RespondsWithFirstAsciiChar(CaesarCipherServerFixture):
    sock = CaesarCipherServerFixture._sock
    response = None

    try:
        sock.sendall(b'1 \x7f ')
        response = sock.recv(1024)
    except socket.error, e:
        pass

    assert response == '\x00 '

def test_ShiftOfNegativeOneSingleCharMessage_ServerRespondsWithCharShiftedNegativeOne(CaesarCipherServerFixture):
    sock = CaesarCipherServerFixture._sock
    response = None

    try:
        sock.sendall(b'-1 b ')
        response = sock.recv(1024)
    except socket.error, e:
        pass

    assert response == 'a '

def test_NegativeShiftWhichGoesBelowFirstAsciiChar_ShiftLoopsAroundAndContinuesFromTheLastAsciiChar(CaesarCipherServerFixture):
    sock = CaesarCipherServerFixture._sock
    response = None

    try:
        sock.sendall(b'-128 abc123 ')
        response = sock.recv(1024)
    except socket.error, e:
        pass

    assert response == 'abc123 '

def test_ShiftOfAsciiRange_RespondsWithSameMessage(CaesarCipherServerFixture):
    sock = CaesarCipherServerFixture._sock
    response = None

    try:
        sock.sendall(b'128 ' + string.ascii_lowercase + ' ')
        response = sock.recv(1024)
    except socket.error, e:
        pass

    assert response == string.ascii_lowercase + ' '

def test_ShiftOfAsciiRangePlusOne_RespondsWithTheMessagePlusOne(CaesarCipherServerFixture):
    sock = CaesarCipherServerFixture._sock
    response = None

    try:
        sock.sendall(b'129 ' + string.ascii_lowercase + ' ')
        response = sock.recv(1024)
    except socket.error, e:
        pass

    assert response == 'bcdefghijklmnopqrstuvwxyz{ '

def test_ShiftAndMessageSentOneCharAtATime_RespondsCorrectly(CaesarCipherServerFixture):
    sock = CaesarCipherServerFixture._sock
    response = None
    message = 'abcd'
    shift = str((128 * 3) + 1) # shift 1

    try:
        for digit in shift:
            sock.sendall(digit.encode())
            time.sleep(1)
        sock.sendall(' '.encode())

        for char in message:
            sock.sendall(char.encode())
            time.sleep(1)
        sock.sendall(' '.encode())

        response = sock.recv(1024)
    except socket.error, e:
        pass

    assert response == 'bcde '

def test_ExtremelyLargeMessageContainingMultipleRequests_RespondsCorrectlyAndQuickly(CaesarCipherServerFixture):
    sock = CaesarCipherServerFixture._sock
    message, expected_response = CaesarCipherServerFixture.get_large_message_and_expected_response()
    response = ''
    start_time, end_time = 0, 0

    start_time = timer()
    try:
        sock.sendall(message.encode())
        while True:
            partial_response = sock.recv(1024)
            if not partial_response:
                break
            response += partial_response
    except socket.error, e:
        pass
    end_time = timer()
    response_time = end_time - start_time

    assert response == expected_response, 'Extremely large message response was not correct!'
    assert response_time < 2, 'Extremely large message response was not fast enough!'

def test_TenClientsConcurrently_RespondsToAllCorrectlyAndQuickly(CaesarCipherServerFixture):
    manager = Manager()
    shared_dict = manager.dict()
    total_clients = 10
    clients = []
    message, expected_response = CaesarCipherServerFixture.get_large_message_and_expected_response()

    for i in range(total_clients):
        clients.append(Process(target=NewProcessCipherRequester, args=(message, shared_dict,)))

    for client in clients:
        client.start()

    for client in clients:
        client.join(30)
        if client.is_alive():
            client.terminate()

    assert len(shared_dict) == total_clients, 'Did not get an answer from all concurrent clients in the allotted time.'
    avg_response_time = 0
    for pid, pids_result in shared_dict.items():
        response, response_time = pids_result
        avg_response_time += response_time
        assert response == expected_response, 'Process ' + str(pid) + '\'s ciphered message was incorrect.'

    avg_response_time /= total_clients
    assert avg_response_time < 2, 'Average response time from ' + str(total_clients) + ' concurrent clients was not fast enough!'

def NewProcessCipherRequester(request_message, result):
    """Function to be run in a new process that
       connects to server and sends request_message
       storing the pid -> (answer, response_time) in result. """
    sock = None

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((_host, _server_port))

        start_time = timer()
        sock.sendall(request_message.encode())

        response, partial_response = '', ''
        while True:
            partial_response = sock.recv(1024)
            if not partial_response:
                result[os.getpid()] = (response, (timer() - start_time))
                break
            response += partial_response

    except Exception:
        pass
    sock.shutdown(socket.SHUT_RDWR)
    sock.close()
