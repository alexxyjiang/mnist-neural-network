#!/usr/bin/python
from struct import unpack

class IdxFileHeader(object):
  def __init__(self):
    self._magic1        = 0x00
    self._magic2        = 0x00
    self._datatype      = 0x00
    self._datatype_desc = ''
    self._datatype_len  = -1
    self._dim_count     = 0x00
    self._dims_list     = []
    self._header_size   = 0x00

  def __str__(self):
    return 'Magic: %02X%02X\tDatatype: %02X(%s, %d)\tDims: %d(%s)\tHeader: %d bytes'%(self._magic1, self._magic2, self._datatype, self._datatype_desc, self._datatype_len, self._dim_count, self._dims_list, self._header_size)

  def datatype_desc(self):
    return self._datatype_desc

  def datatype_len(self):
    return self._datatype_len

  def dims_count(self):
    return self._dim_count

  def dims_list(self):
    return self._dims_list

  def header_size(self):
    return self._header_size

  # index file-type flag
  #   0x08: unsigned byte
  #   0x09: signed byte
  #   0x0B: short (2 bytes)
  #   0x0C: int (4 bytes)
  #   0x0D: float (4 bytes)
  #   0x0E: double (8 bytes)
  def decode_data_type(self):
    if self._datatype == 0x08:
      self._datatype_desc = 'B'
      self._datatype_len  = 1
    elif self._datatype == 0x09:
      self._datatype_desc = 'b'
      self._datatype_len  = 1
    elif self._datatype == 0x0B:
      self._datatype_desc = '>h'
      self._datatype_len  = 2
    elif self._datatype == 0x0C:
      self._datatype_desc = '>i'
      self._datatype_len  = 4
    elif self._datatype == 0x0D:
      self._datatype_desc = '>f'
      self._datatype_len  = 4
    elif self._datatype == 0x0E:
      self._datatype_desc = '>d'
      self._datatype_len  = 8
    else:
      self._datatype_desc = ''
      self._datatype_len  = -1

  def load_header_from_file(self, file_handle):
    if type(file_handle) is file:
      file_handle.seek(0)
      (self._magic1, self._magic2, self._datatype, self._dim_count) = unpack('BBBB', file_handle.read(4))
      self.decode_data_type()
      for i in range(self._dim_count):
        dim_length  = unpack('>i', file_handle.read(4))
        self._dims_list.append(dim_length[0])
      self._header_size = file_handle.tell()
    else:
      raise TypeError('try to load from invalid file')

class IdxFile(object):
  def __init__(self):
    self._file_header = IdxFileHeader()
    self._payload     = {}

  def __str__(self):
    return '%s\n%s'%(str(self._file_header), str(self._payload))

  def file_header(self):
    return self._file_header

  def payload(self):
    return self._payload

  def load_idx_file(self, filename_idx):
    if type(filename_idx) is str:
      handle  = open(filename_idx, 'rb')
      self._file_header.load_header_from_file(handle)
      self.load_payload(handle)
    else:
      raise TypeError('invalid file name')

  def load_payload(self, file_handle):
    if type(file_handle) is file:
      datatype_desc = self._file_header.datatype_desc()
      datatype_len  = self._file_header.datatype_len()
      dims_count    = self._file_header.dims_count()
      dims_list     = self._file_header.dims_list()
      dims_loaded   = [0 for i in range(dims_count)]
      file_handle.seek(self._file_header.header_size())
      while dims_loaded[0] < dims_list[0]:
        data  = unpack(datatype_desc, file_handle.read(datatype_len))[0]
        if dims_count == 1:
          self._payload[dims_loaded[0]] = data
          dims_loaded[0]  += 1
        else:
          if not dims_loaded[0] in self._payload:
            self._payload[dims_loaded[0]] = [dims_list[1:], [data]]
          else:
            self._payload[dims_loaded[0]][1].append(data)
          dims_loaded[-1] += 1
          for i in range(dims_count-1, 0, -1):
            if dims_loaded[i] == dims_list[i]:
              dims_loaded[i]    = 0
              dims_loaded[i-1]  += 1
    else:
      raise TypeError('try to load from invalid file')
