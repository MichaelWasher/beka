import struct

class Chopper(object):
    BGP_MARKER = b"\xFF" * 16
    HEADER_LENGTH = 19

    def __init__(self, input_stream):
        self.input_stream = input_stream

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        header, length, message_type = self.load_header()
        extra_data_length = length - self.HEADER_LENGTH
        if extra_data_length > 0:
            serialised_body = self.input_stream.read(extra_data_length)
        elif extra_data_length < 0:
            raise ValueError("Invalid BGP length field")
        else:
            serialised_body = None

        return message_type, serialised_body

    def load_header(self):
        # TODO handle when stream runs out
        header = self.input_stream.read(19)

        marker, length, message_type = struct.unpack("!16sHB", header)

        if marker == self.BGP_MARKER:
            return header, length, message_type
        else:
            raise ValueError("BGP marker missing")