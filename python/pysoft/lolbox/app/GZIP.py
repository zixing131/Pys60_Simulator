# -*- coding: utf-8 -*- 
#######wap.wapele.cn#######
#######中文名好听########
#######decompile2########


__doc__ = "Functions that read and write gzipped files.\n\nThe user of the file doesn't have to worry about the compression,\nbut random access is not allowed."
import struct
import sys
import time
import zlib
import __builtin__
__all__ = ['GzipFile', 'open']
FTEXT, FHCRC, FEXTRA, FNAME, FCOMMENT = (1, 2, 4, 8, 16)
READ, WRITE = (1, 2)
def U32(i):
    if i < 0 : 
        i += (1 << 32)
    return i




def LOWU32(i):
    return (i & 4294967295)




def write32(output, value):
    output.write(struct.pack('<l', value))




def write32u(output, value):
    output.write(struct.pack('<L', value))




def read32(input):
    return struct.unpack('<l', input.read(4))[0]




def open(filename, mode = 'rb', compresslevel = 9):
    return GzipFile(filename, mode, compresslevel)




class GzipFile :


    __module__ = __name__
    __doc__ = 'The GzipFile class simulates most of the methods of a file object with\n    the exception of the readinto() and truncate() methods.\n\n    '
    myfileobj = None
    max_read_chunk = ((10 * 1024) * 1024)
    def __init__(self, filename = None, mode = None, compresslevel = 9, fileobj = None):
        if mode and 'b' not in mode : 
            mode += 'b'
        if fileobj is None : 
            self.myfileobj = fileobj = __builtin__.open(filename, mode or 'rb')
        if filename is None : 
            if hasattr(fileobj, 'name') : 
                filename = fileobj.name
            else : 
                filename = ''
            pass
        if mode is None : 
            if hasattr(fileobj, 'mode') : 
                mode = fileobj.mode
            else : 
                mode = 'rb'
            pass
        if mode[0 : 1] == 'r' : 
            self.mode = READ
            self._new_member = True
            self.extrabuf = ''
            self.extrasize = 0
            self.filename = filename
            self.min_readsize = 100
        elif mode[0 : 1] == 'w' or mode[0 : 1] == 'a' : 
            self.mode = WRITE
            self._init_write(filename)
            self.compress = zlib.compressobj(compresslevel, zlib.DEFLATED,  - zlib.MAX_WBITS, zlib.DEF_MEM_LEVEL, 0)
        else : 
            raise IOError,'Mode ' + mode + ' not supported'
        self.fileobj = fileobj
        self.offset = 0
        if self.mode == WRITE : 
            self._write_gzip_header()




    def __repr__(self):
        s = repr(self.fileobj)
        return '<gzip ' + s[1 : -1] + ' ' + hex(id(self)) + '>'




    def _init_write(self, filename):
        if filename[-3 : ] != '.gz' : 
            filename = filename + '.gz'
        self.filename = filename
        self.crc = zlib.crc32('')
        self.size = 0
        self.writebuf = []
        self.bufsize = 0




    def _write_gzip_header(self):
        self.fileobj.write('\x1f\x8b')
        self.fileobj.write('')
        fname = self.filename[ : -3]
        flags = 0
        if fname : 
            flags = FNAME
        self.fileobj.write(chr(flags))
        write32u(self.fileobj, long(time.time()))
        self.fileobj.write('')
        self.fileobj.write('\xff')
        if fname : 
            self.fileobj.write(fname + ' ')




    def _init_read(self):
        self.crc = zlib.crc32('')
        self.size = 0




    def _read_gzip_header(self):
        magic = self.fileobj.read(2)
        if magic != '\x1f\x8b' : 
            raise IOError,'Not a gzipped file'
        method = ord(self.fileobj.read(1))
        if method != 8 : 
            raise IOError,'Unknown compression method'
        flag = ord(self.fileobj.read(1))
        self.fileobj.read(6)
        if (flag & FEXTRA) : 
            xlen = ord(self.fileobj.read(1))
            xlen = xlen + (256 * ord(self.fileobj.read(1)))
            self.fileobj.read(xlen)
        if (flag & FNAME) : 
            while True : 
                s = self.fileobj.read(1)
                if  not (s) or s == ' ' : 
                    break
            pass
        if (flag & FCOMMENT) : 
            while True : 
                s = self.fileobj.read(1)
                if  not (s) or s == ' ' : 
                    break
            pass
        if (flag & FHCRC) : 
            self.fileobj.read(2)




    def write(self, data):
        if self.mode != WRITE : 
            import errno
            raise IOError(errno.EBADF, 'write() on read-only GzipFile object')
        if self.fileobj is None : 
            raise ValueError,'write() on closed GzipFile object'
        if len(data) > 0 : 
            self.size = self.size + len(data)
            self.crc = zlib.crc32(data, self.crc)
            self.fileobj.write(self.compress.compress(data))
            self.offset += len(data)




    def read(self, size = -1):
        if self.mode != READ : 
            import errno
            raise IOError(errno.EBADF, 'read() on write-only GzipFile object')
        if self.extrasize <= 0 and self.fileobj is None : 
            return ''
        readsize = 1024
        if size < 0 : 
            try :
                while True : 
                    self._read(readsize)
                    readsize = min(self.max_read_chunk, (readsize * 2))
            except EOFError : 
                size = self.extrasize
            pass
        else : 
            try :
                while size > self.extrasize : 
                    self._read(readsize)
                    readsize = min(self.max_read_chunk, (readsize * 2))
            except EOFError : 
                if size > self.extrasize : 
                    size = self.extrasize
                pass
            pass
        chunk = self.extrabuf[ : size]
        self.extrabuf = self.extrabuf[size : ]
        self.extrasize = (self.extrasize - size)
        self.offset += size
        return chunk




    def _unread(self, buf):
        self.extrabuf = buf + self.extrabuf
        self.extrasize = len(buf) + self.extrasize
        self.offset -= len(buf)




    def _read(self, size = 1024):
        if self.fileobj is None : 
            raise EOFError,'Reached EOF'
        if self._new_member : 
            pos = self.fileobj.tell()
            self.fileobj.seek(0, 2)
            if pos == self.fileobj.tell() : 
                raise EOFError,'Reached EOF'
            else : 
                self.fileobj.seek(pos)
            self._init_read()
            self._read_gzip_header()
            self.decompress = zlib.decompressobj( - zlib.MAX_WBITS)
            self._new_member = False
        buf = self.fileobj.read(size)
        if buf == '' : 
            uncompress = self.decompress.flush()
            self._read_eof()
            self._add_read_data(uncompress)
            raise EOFError,'Reached EOF'
        uncompress = self.decompress.decompress(buf)
        self._add_read_data(uncompress)
        if self.decompress.unused_data != '' : 
            self.fileobj.seek(( - len(self.decompress.unused_data) + 8), 1)
            self._read_eof()
            self._new_member = True




    def _add_read_data(self, data):
        self.crc = zlib.crc32(data, self.crc)
        self.extrabuf = self.extrabuf + data
        self.extrasize = self.extrasize + len(data)
        self.size = self.size + len(data)




    def _read_eof(self):
        self.fileobj.seek(-8, 1)
        crc32 = read32(self.fileobj)
        isize = U32(read32(self.fileobj))
        if U32(crc32) != U32(self.crc) : 
            raise IOError,'CRC check failed'
        elif isize != LOWU32(self.size) : 
            raise IOError,'Incorrect length of data produced'




    def close(self):
        if self.mode == WRITE : 
            self.fileobj.write(self.compress.flush())
            write32u(self.fileobj, LOWU32(self.crc))
            write32u(self.fileobj, LOWU32(self.size))
            self.fileobj = None
        elif self.mode == READ : 
            self.fileobj = None
        if self.myfileobj : 
            self.myfileobj.close()
            self.myfileobj = None




    def __del__(self):
        try :
            if self.myfileobj is None and self.fileobj is None : 
                return None
        except AttributeError : 
            return None
        self.close()




    def flush(self, zlib_mode = zlib.Z_SYNC_FLUSH):
        if self.mode == WRITE : 
            self.fileobj.write(self.compress.flush(zlib_mode))
        self.fileobj.flush()




    def fileno(self):
        return self.fileobj.fileno()




    def isatty(self):
        return False




    def tell(self):
        return self.offset




    def rewind(self):
        if self.mode != READ : 
            raise IOError("Can't rewind in write mode")
        self.fileobj.seek(0)
        self._new_member = True
        self.extrabuf = ''
        self.extrasize = 0
        self.offset = 0




    def seek(self, offset):
        if self.mode == WRITE : 
            if offset < self.offset : 
                raise IOError('Negative seek in write mode')
            count = (offset - self.offset)
            for i in range((count // 1024)):
                self.write((1024 * ' '))
            self.write(((count % 1024) * ' '))
        elif self.mode == READ : 
            if offset < self.offset : 
                self.rewind()
            count = (offset - self.offset)
            for i in range((count // 1024)):
                self.read(1024)
            self.read((count % 1024))




    def readline(self, size = -1):
        if size < 0 : 
            size = sys.maxint
            readsize = self.min_readsize
        else : 
            readsize = size
        bufs = []
        while size != 0 : 
            c = self.read(readsize)
            i = c.find('\n')
            if size <= i or i == -1 and len(c) > size : 
                i = (size - 1)
            if i >= 0 or c == '' : 
                bufs.append(c[ : (i + 1)])
                self._unread(c[(i + 1) : ])
                break
            bufs.append(c)
            size = (size - len(c))
            readsize = min(size, (readsize * 2))
        if readsize > self.min_readsize : 
            self.min_readsize = min(readsize, (self.min_readsize * 2), 512)
        return ''.join(bufs)




    def readlines(self, sizehint = 0):
        if sizehint <= 0 : 
            sizehint = sys.maxint
        L = []
        while sizehint > 0 : 
            line = self.readline()
            if line == '' : 
                break
            L.append(line)
            sizehint = (sizehint - len(line))
        return L




    def writelines(self, L):
        for line in L:
            self.write(line)




    def __iter__(self):
        return self




    def next(self):
        line = self.readline()
        if line : 
            return line
        else : 
            raise StopIteration






def _test():
    args = sys.argv[1 : ]
    decompress = args and args[0] == '-d'
    if decompress : 
        args = args[1 : ]
    if  not (args) : 
        args = ['-']
    for arg in args:
        if decompress : 
            if arg == '-' : 
                f = GzipFile(filename = '', mode = 'rb', fileobj = sys.stdin)
                g = sys.stdout
            else : 
                if arg[-3 : ] != '.gz' : 
                    print "filename doesn't end in .gz:",
                    print repr(arg),
                    print
                    continue
                f = open(arg, 'rb')
                g = __builtin__.open(arg[ : -3], 'wb')
            pass
        elif arg == '-' : 
            f = sys.stdin
            g = GzipFile(filename = '', mode = 'wb', fileobj = sys.stdout)
        else : 
            f = __builtin__.open(arg, 'rb')
            g = open(arg + '.gz', 'wb')
        while True : 
            chunk = f.read(1024)
            if  not (chunk) : 
                break
            g.write(chunk)
        if g is not sys.stdout : 
            g.close()
        if f is not sys.stdin : 
            f.close()


if __name__ == '__main__' : 
    _test()