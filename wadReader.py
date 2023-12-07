import struct
from pygame.math import Vector2
from data_types import *

class WADReader:
    def __init__(self, wad_path):
        self.wad_path = wad_path
        self.wad_file = open(self.wad_path, "rb")
        self.header = self.read_header()
        self.directory = self.read_directory()

    def read_linedef(self, offset):
        # 14 bytes = 2H * 7
        read_2_bytes = self.read_2_bytes
        linedef = LineDef()
        linedef.start_vertex_id = read_2_bytes(offset, 'H')
        linedef.end_vertex_id = read_2_bytes(offset + 2, 'H')
        linedef.flags = read_2_bytes(offset + 4, 'H')
        linedef.line_type = read_2_bytes(offset + 6, 'H')
        linedef.sector_tag = read_2_bytes(offset + 8, 'H')
        linedef.front_sidedef_id = read_2_bytes(offset + 10, 'H')
        linedef.back_sidedef_id = read_2_bytes(offset + 12, 'H')
        return linedef

    def read_vertex(self, offset):
        # 4 bytes = 2h + 2h
        x = self.read_2_bytes(offset, 'h')
        y = self.read_2_bytes(offset + 2, 'h')
        return Vector2(x, y)

    def read_directory(self):
        directory = []
        for i in range(self.header["lump_count"]):
            offset = self.header["init_offset"] + i * 16
            lump_info = {
                "lump_offset": self.read_4_bytes(offset),
                "lump_size": self.read_4_bytes(offset + 4),
                "lump_name": self.read_string(offset + 8, 8)
            }
            directory.append(lump_info)

        return directory
    
    def read_header(self):
        return {
            'wad_type': self.read_string(0, 4),  # TYPE OF WAD
            'lump_count': self.read_4_bytes(4),  # NUMBER OF ASSETS
            'init_offset': self.read_4_bytes(8), # START POINTER FOR ASSETS
        }
    

    def read_1_byte(self, offset, byte_format = 'B'):
        '''
        byte_format = "b": signed_char, "B": unsigned_char
        '''
        return self.read_bytes(offset, 1, byte_format)[0]

    def read_2_bytes(self, offset, byte_format):
        '''
        byte_format = "h": int32, "H": uint32
        '''
        return self.read_bytes(offset, 2, byte_format)[0]

    def read_4_bytes(self, offset, byte_format = 'i'):
        '''
        byte_format = "i": int32, "I": uint32
        '''
        return self.read_bytes(offset, 4, byte_format)[0]
    
    def read_string(self, offset, num_bytes):
        return "".join(b.decode('ascii') for b in 
                       self.read_bytes(offset, num_bytes, "c" * num_bytes)
                       if ord(b) != 0).upper()

    def read_bytes(self, offset, num_bytes, byte_format):
        self.wad_file.seek(offset)
        buffer = self.wad_file.read(num_bytes)
        return struct.unpack(byte_format, buffer)
    
    def close(self):
        self.wad_file.close()