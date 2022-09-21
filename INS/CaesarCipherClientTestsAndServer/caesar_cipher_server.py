import socket
import select
import enum
import argparse
from caesar_cipher import GenerateCaesarCipher

class CaesarCipherServer:
    '''Caesar cipher socket server. Handles incoming requests to
    encode ASCII messages using a user specified shift.
    Returns an encoded caesar cipher to the user.
    '''

    class AwaitingState(enum.Enum):
        '''Used to track state of how the server will interpret current(or next) incoming contiguous segment of text.'''
        ShiftAmount = 1
        Message = 2

    def __init__(self, port):
        self._port = port

    def run(self):
        '''Starts the server on the port specified in the constructor.'''
        self._sock = self._create_port_listener()
        while True:
            (conn, addr) = self._sock.accept()
            conn.setblocking(0)
            self._handle_incoming_connection(conn, addr)

    def _create_port_listener(self):
        '''Creates a listening socket bound to localhost.'''
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        HOST = ''
        s.bind((HOST, self._port))
        s.listen(5)
        return s

    def _handle_incoming_connection(self, conn, addr):
        '''High level entry point to parsing and responding to a connection's incoming caesar cipher encodings requests.

            Expected Incoming Message Format:
                "shift message "
            A space signifies completion of a shift or message word. Spaces are not allowed in messages.

            Expected Outgoing Message Format:
                "encoded_message "
            A trailing space is sent with the encoded_message.
        '''

        try:
            print('connection from ', addr)
            waiting_state = self.AwaitingState(self.AwaitingState.ShiftAmount)
            unprocessed_remainder = ''
            while True:
                new_unprocessed_data = self._wait_for_data_string(conn)
                (complete_requests, unprocessed_remainder, waiting_state) = self._parse_complete_requests(waiting_state, unprocessed_remainder, new_unprocessed_data)
                ciphers = self._perform_cipher(complete_requests)
                self._send_completed_ciphers(ciphers, conn)
        except TimeoutError as e:
            print(e) # No data from client in X seconds
        except ConnectionAbortedError as e:
            print(e) # Client closed connection
        except ValueError as e:
            print(e) # Given an invalid shift(Not an integer)
        except Exception as e:
            print(e)
        finally:
            if conn:
                conn.close()
                print('closed connection')

    def _wait_for_data_string(self, conn):
        '''Waits for data from a connection, returning any received data as a string.
        Throws TimeoutError after 2 seconds.
        Throws ConnectionAbortedError upon disconnection
        '''
        inputs = [conn]
        for read_attempt in range(0, 2):
            readable, writable, exceptional = select.select(inputs, [], [], 1)
            if not readable:
                if read_attempt >= 1:
                    raise TimeoutError('No messages for 2 seconds.')
            else:
                data = conn.recv(1024)
                if not data:
                    # no such thing as empty message peer disconnected
                    raise ConnectionAbortedError('Peer disconnected.')

                return data.decode()
        return ''

    def _parse_complete_requests(self, waiting_state, old_unprocessed_data, new_unprocessed_data):
        '''Iterates through words of incoming data parsing them into complete requests(shift, message).
            Expected Complete request format:
                "shift message "
            A space signifies completion of a shift or message word. Spaces are not allowed in messages.

            Receives:   (AwaitingState) - how to interpret current word
                        (string) - old unprocessed data, i.e. an incomplete request
                        (string) - new unprocessed data, fresh data which should hopefully complete the request + more

            Returns: (dictionary) - completed requests, idx(maintains ordering) -> (shift, message)
                     (string) - unprocessed data, incomplete request that should get passed back into this on next call
                     (AwaitingState) - how to interpret current word after iterating through the new data
        '''
        old_split_words = old_unprocessed_data.split(' ') if old_unprocessed_data else []
        new_split_words = new_unprocessed_data.split(' ') if new_unprocessed_data else []

        print('old data ', old_unprocessed_data, '\n')
        print('new data ', new_unprocessed_data, '\n')
        print('split message ', new_split_words, '\n')

        # Unpack old unprocessed shift and message
        complete_ciphers = {}
        shift, message = '', ''
        for idx, word in enumerate(old_split_words):
            if idx == 0:
                shift = word
            elif idx == 1:
                message = word

        # Interpret the new words recording complete requests in the process
        last_word_idx = len(new_split_words) - 1
        for idx, word in enumerate(new_split_words):
            if waiting_state == self.AwaitingState.ShiftAmount:
                shift += word
            elif waiting_state == self.AwaitingState.Message:
                message += word

            # Complete word are those followed by a space
            complete_word = idx < last_word_idx
            if complete_word:
                if waiting_state == self.AwaitingState.ShiftAmount:
                    waiting_state = self.AwaitingState.Message
                elif waiting_state == self.AwaitingState.Message:
                    waiting_state = self.AwaitingState.ShiftAmount
                    # Current request is now complete as we have both shift + message
                    complete_ciphers[idx] = (shift, message)
                    print('completed request ', complete_ciphers)
                    shift, message = '', ''

        # Record what hasn't been processed yet so we can take it into account during the next
        # flow of incoming data
        unprocessed_remainder = ''
        if shift:
            unprocessed_remainder += shift
            if waiting_state == self.AwaitingState.Message:
                unprocessed_remainder += ' '

        if message:
            unprocessed_remainder += message

        print('unprocessed remainder ', unprocessed_remainder)

        return (complete_ciphers, unprocessed_remainder, waiting_state)


    def _perform_cipher(self, complete_requests):
        '''Given a dictionary of complete requests, i.e. idx -> (shift, message) 
           Validates the request, makes sure shift is an integer, throws ValueError otherwise.
           Then performs the requested caesar cipher returning a list of the ciphers.
        '''
        ciphers = []

        for idx, request in complete_requests.items():
            (shift, message) = request

            unvalidated_shift = shift
            is_negative = unvalidated_shift.startswith('-')
            if is_negative:
                unvalidated_shift = unvalidated_shift[1:]

            if not unvalidated_shift.isnumeric():
                raise ValueError('Given an invalid shift to apply to message. ' + shift + ' ' + message)

            if is_negative:
                shift = -int(unvalidated_shift)
            else:
                shift = int(unvalidated_shift)

            ciphers.append(GenerateCaesarCipher(message, shift))

        return ciphers

    def _send_completed_ciphers(self, ciphers, conn):
        '''Constructs a string response message containing the given ciphers separated by spaces,
           and sends it to the given connection.
        '''
        full_response_message = ''
        for cipher in ciphers:
            full_response_message += cipher + ' '
            print('appended to full message string, total', full_response_message)

        if full_response_message:
            print('sending full message')
            conn.sendall(full_response_message.encode())

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('port')
    args = parser.parse_args()

    server = CaesarCipherServer(int(args.port))
    server.run()
