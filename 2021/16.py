#!/usr/bin/python3.8

from aoc import Env

e = Env(16)
e.T("D2FE28", 6, None)
e.T("8A004A801A8002F478", 16, None)
e.T("620080001611562C8802118E34", 12, None)
e.T("C0015000016115A2E0802F182340", 23, None)
e.T("A0016C880162017C3686B18A3D4780", 31, None)
e.T('C200B40A82', None, 3)
e.T('04005AC33890', None, 54)
e.T('880086C3E88112', None, 7)
e.T('CE00C43D881120', None, 9)
e.T('D8005AC2A8F0', None, 1)
e.T('F600BC2D8F', None, 0)
e.T('9C005AC2F8F0', None, 0)
e.T('9C0141080250320F1802104A08', None, 1)


class Stream():
    def __init__(self, string):
        self.digits = [int(x, 16) for x in string]
        self.nibble = 0
        self.bit = 3
        self.pos = 0
    
    def get_bit(self):
        v = (self.digits[self.nibble] >> self.bit) & 1
        self.bit -= 1
        if self.bit < 0:
            self.bit = 3
            self.nibble += 1
        self.pos += 1
        return v

    def get_bits(self, n):
        v = 0
        for x in range(n):
            v = v * 2 + self.get_bit()
        return v


class Packet():
    def __init__(self, ver):
        self.ver = ver
    
    def sum_versions(self):
        return self.ver


class LiteralPacket(Packet):
    def __init__(self, ver, value):
        super().__init__(ver)
        self.value = value
    
    def eval(self):
        return self.value


class OperatorPacket(Packet):
    def __init__(self, ver, type_id, sub_packets):
        super().__init__(ver)
        self.sub_packets = sub_packets
        self.type_id = type_id

    def sum_versions(self):
        return self.ver + sum(x.sum_versions() for x in self.sub_packets)

    def eval(self):
        t = self.type_id
        if t == 0:
            # sum
            return sum(x.eval() for x in self.sub_packets)
        elif t == 1:
            # product
            v = 1
            for x in self.sub_packets:
                v *= x.eval()
            return v
        elif t == 2:
            # minimum
            return min(x.eval() for x in self.sub_packets)
        elif t == 3:
            # maximum
            return max(x.eval() for x in self.sub_packets)
        elif t == 5:
            # greater
            assert len(self.sub_packets) == 2
            return 1 if self.sub_packets[0].eval() > self.sub_packets[1].eval() else 0
        elif t == 6:
            # less
            assert len(self.sub_packets) == 2
            return 1 if self.sub_packets[0].eval() < self.sub_packets[1].eval() else 0
        elif t == 7:
            # equal
            assert len(self.sub_packets) == 2
            return 1 if self.sub_packets[0].eval() == self.sub_packets[1].eval() else 0
        else:
            assert False


def parse_packet(stream):
    ver = stream.get_bits(3)
    type_id = stream.get_bits(3)
    if type_id == 4:
        # literal packet
        lit_v = 0
        while True:
            x = stream.get_bits(5)
            lit_v = lit_v * 16 + x % 16
            if x < 16:
                break
        return LiteralPacket(ver, lit_v)
    else:
        # operator packet
        sub_packets = []
        length_type_id = stream.get_bit()
        if length_type_id == 0:
            # 15 bits total length
            sub_length = stream.get_bits(15)
            start = stream.pos
            while stream.pos - start < sub_length:
                sub_packets.append(parse_packet(stream))
        else:
            # 11 bits number of subpackets
            sub_packets_n = stream.get_bits(11)
            for x in range(sub_packets_n):
                sub_packets.append(parse_packet(stream))
        return OperatorPacket(ver, type_id, sub_packets)


def part1(input):
    stream = Stream(input.get_valid_lines()[0])
    packet = parse_packet(stream)
    return packet.sum_versions()


e.run_tests(1, part1)
e.run_main(1, part1)


def part2(input):
    stream = Stream(input.get_valid_lines()[0])
    packet = parse_packet(stream)
    return packet.eval()


e.run_tests(2, part2)
e.run_main(2, part2)
