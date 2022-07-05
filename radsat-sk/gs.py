import struct

class GenericMessage(object):
	preamble = bytes(69)          # preamble is hard-coded and doesn't change.
	def __init__(self,
				 data,            # contains the raw data to be unpacked 
				 timestamp=None,  # time (in seconds) since Unix Epoch that the message was created
				 size=None,       # size of the message in bytes (NOT including header)
				 type=None,       # type of message
				 frameNum=0,      # frame number of message
				 imageID=0,       # image ID if applicable
				 body=None        # the body of the message. Doesn't include the header (preamble, CRC, size, timestamp)
				 ):
		
        # if the data given can make up a message, strip off the header
		if isinstance(data, bytes):
            # see page 58 of the software design document
			_, self.crc, self.size, self.timestamp, *self.body = struct.unpack('HHBI' + 'I' * len(data) - 9, data)
            
            # at this point, the data contained in self.body is still encoded by protobuf. Need to decode.
            a, b, c, d, e = protobuf_decode(self.body)
		
        # otherwise, create a message with the given attributes
		else:
			self.timestamp = timestamp
			self.size = size
			self.type = type
			self.frameNum = frameNum
			self.imageID = imageID
			self.body = body
			self.data = None # no raw message given
            
    # pack the data back into a string of bytes
	def __generateRaw(self):
		return struct.pack('HHBI' + 'I' * len(data) - 9, GenericMessage.preamble, self.crc, self.size, self.timestamp)
		
    # convert the data into a csv format with appropriate values included
	def convertToCsv(self):
		return f'{self.timestamp},{self.size},{self.type},{self.frameNum},{self.body}'
		
	"""-----------------------------
	Public
	-----------------------------"""
	
	def generateLog(self):
        return self.convertToCsv()
        
    """-----------------------------
	Dunders
	-----------------------------"""
    
    def __bytes__(self):
        if not data:
            self.data = self.generateRaw()
        return self.data
        
    def __str__(self):
        return str(self.data)
        
    def __repr__(self):
        return self.__str__()
        
 
 
class TelemetryMessage(GenericMessage):

    def __generateRaw(self):
        return struct.pack('some_string_here', GenericMessage.preamble, self.crc, self.size, self.timestamp)
    

    # this function is where the bulk of the work will be. We need to determine what data is contained in
    # the message and what data we want to save to a log.
    def generateLog(self):
        stringOut = self.convertToCsv()
        file.writeLine(stringOut)
        file.flush()
        return self.convertToCsv()


def rawToMsg(rawData):
    if rawData[64] == bytes(1):
        return GenericMessage(rawData)
    elif rawData[64] == bytes(1):
        return TelemetryMessage(rawData)
        
        


raw = getSatMessage()
msg = rawToMsg(raw)

logger = Logger()

if isinstance(msg, GenericMessage):
    logger.generic(msg)
elif isinstance(msg, TelemetryMessage):
    logger.telemetry(msg)