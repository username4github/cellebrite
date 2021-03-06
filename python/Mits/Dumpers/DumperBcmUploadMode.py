from Mits.Dumpers.IDumper import IDumper
from Mits.Utils.General import timed_xrange, get_dump_path


import time


FIRST_CHUNK = 0x8b44 # 35652


CHUNK_SIZE = 0x40000
SPARE_SIZE = 0x2000


class DumperBcmUploadMode(IDumper):
    name = "BcmUploadMode"
    
    def dump(self, start_address , end_address, name = ""):
        self.protocol.before_read(start_address, end_address)
        
        self.open_output(name, "BcmUploadMode", start_address, end_address)
        try:
            self.protocol.dump_get_chunk(0,FIRST_CHUNK, 0) # These first 35652 bytes is just a header of the dump (not needed)
            
            self.protocol.dump_get_chunk(0,CHUNK_SIZE, SPARE_SIZE) # According to the Decoding team, the first chunk of the dump is not needed
            offset = 0
            for i in timed_xrange(start_address + FIRST_CHUNK + CHUNK_SIZE + SPARE_SIZE, end_address, CHUNK_SIZE + SPARE_SIZE):
                buffer = self.protocol.dump_get_chunk(i,CHUNK_SIZE, SPARE_SIZE)
                self.write_to_output(buffer, offset)
                offset = offset + len(buffer)
			
            self.protocol.after_read()


        except KeyboardInterrupt:
            print "User canceled the dump"
            self.protocol.abort_dump()
            
        finally:
            self.close_output()
            
