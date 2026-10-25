"""Exercise real packet parsing with synthetic serial bytes; no hardware."""
import unittest

from scservo_sdk import (
    COMM_RX_CORRUPT,
    COMM_RX_TIMEOUT,
    COMM_SUCCESS,
    GroupSyncRead,
    PacketHandler,
)


def status_packet(payload, motor_id=3, error=0):
    packet = [0xff, 0xff, motor_id, len(payload) + 2, error] + list(payload)
    return bytes(packet + [~sum(packet[2:]) & 0xff])


class BytePort:
    def __init__(self, replies):
        self.incoming = bytearray(replies)
        self.is_using = False
        self.writes = []

    def readPort(self, count):
        chunk = self.incoming[:count]
        del self.incoming[:count]
        return chunk

    def writePort(self, packet):
        self.writes.append(bytes(packet))
        return len(packet)

    def clearPort(self):
        pass

    def setPacketTimeout(self, count):
        pass

    def isPacketTimeout(self):
        return not self.incoming


class ReadResponseLengthTests(unittest.TestCase):
    def read(self, method, payload, requested_length, error=0):
        packet = PacketHandler(0)
        port = BytePort(status_packet(payload, error=error))
        if method == 'readRx':
            return packet.readRx(port, 3, requested_length)
        return packet.readTxRx(port, 3, 63, requested_length)

    def test_position_reply_is_not_returned_as_temperature(self):
        for method in ('readRx', 'readTxRx'):
            with self.subTest(method=method):
                # 2890 would otherwise become a plausible 74-degree reading.
                self.assertEqual(self.read(method, [0x4a, 0x0b], 1),
                                 ([], COMM_RX_CORRUPT, 0))

    def test_empty_acknowledgement_does_not_expose_checksum_as_data(self):
        for method in ('readRx', 'readTxRx'):
            with self.subTest(method=method):
                self.assertEqual(self.read(method, [], 1),
                                 ([], COMM_RX_CORRUPT, 0))

    def test_short_payload_is_rejected(self):
        for method in ('readRx', 'readTxRx'):
            for payload, length in (([32], 2), ([1, 2], 4), ([1, 2, 3], 4)):
                with self.subTest(method=method, payload=payload, length=length):
                    self.assertEqual(self.read(method, payload, length),
                                     ([], COMM_RX_CORRUPT, 0))

    def test_exact_one_two_and_four_byte_payloads_are_unchanged(self):
        for method in ('readRx', 'readTxRx'):
            for payload in ([32], [0x4a, 0x0b], [1, 2, 3, 4]):
                with self.subTest(method=method, payload=payload):
                    self.assertEqual(self.read(method, payload, len(payload)),
                                     (payload, COMM_SUCCESS, 0))

    def test_valid_hot_reading_and_servo_error_flag_are_preserved(self):
        for method in ('readRx', 'readTxRx'):
            for error in (0, 4):
                with self.subTest(method=method, error=error):
                    self.assertEqual(self.read(method, [74], 1, error=error),
                                     ([74], COMM_SUCCESS, error))

    def test_bad_checksum_is_still_rejected(self):
        response = bytearray(status_packet([32])); response[-1] ^= 1
        for method in ('readRx', 'readTxRx'):
            with self.subTest(method=method):
                packet = PacketHandler(0); port = BytePort(response)
                result = (packet.readRx(port, 3, 1) if method == 'readRx' else
                          packet.readTxRx(port, 3, 63, 1))
                self.assertEqual(result, ([], COMM_RX_CORRUPT, 0))

    def test_reply_for_another_motor_does_not_satisfy_read(self):
        for method in ('readRx', 'readTxRx'):
            with self.subTest(method=method):
                packet = PacketHandler(0)
                port = BytePort(status_packet([74], motor_id=2))
                result = (packet.readRx(port, 3, 1) if method == 'readRx' else
                          packet.readTxRx(port, 3, 63, 1))
                self.assertEqual(result, ([], COMM_RX_TIMEOUT, 0))

    def test_one_byte_wrappers_report_failure_instead_of_false_temperature(self):
        packet = PacketHandler(0)
        response = status_packet([0x4a, 0x0b])
        self.assertEqual(packet.read1ByteRx(BytePort(response), 3),
                         (0, COMM_RX_CORRUPT, 0))
        self.assertEqual(packet.read1ByteTxRx(BytePort(response), 3, 63),
                         (0, COMM_RX_CORRUPT, 0))

    def test_group_sync_read_propagates_mismatched_length(self):
        response = status_packet([32], motor_id=1) + status_packet([0x4a, 0x0b])
        group = GroupSyncRead(BytePort(response), PacketHandler(0), 63, 1)
        group.addParam(1); group.addParam(3)
        self.assertEqual(group.txRxPacket(), COMM_RX_CORRUPT)
        self.assertFalse(group.last_result)
        self.assertEqual(group.getData(3, 63, 1), 0)


if __name__ == '__main__':
    unittest.main()
