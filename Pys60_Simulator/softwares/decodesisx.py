#!/usr/bin/env python
# -*- coding: utf-8 -*-

##############################################################################
# decodesisx.py - Decodes a Symbian OS v9.x SISX file
# Copyright 2006, 2007 Jussi Yl�nen
#
# This program is based on a whitepaper by Symbian's Security team:
# Symbian OS v9.X SIS File Format Specification, Version 1.1, June 2006
# http://developer.symbian.com/main/downloads/papers/SymbianOSv91/softwareinstallsis.pdf
#
# This program is part of Ensymble developer utilities for Symbian OS(TM).
#
# Ensymble is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# Ensymble is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ensymble; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# Version history
# ---------------
#
# v0.09 2006-09-22
# Replaced every possible range(...) with xrange(...) for efficiency
#
# v0.08 2006-09-12
# Implemented a SISController dump option (-c, for use with -d and/or -f)
#
# v0.07 2006-09-05
# Implemented a header hex dump option (-e)
#
# v0.06 2006-08-29
# Fixed errors in uncompressed SISCompressed field handling
#
# v0.05 2006-08-10
# Option --dumptofile (-f) now uses a directory for dumped files
# A temporary directory is generated if none given by the user
# Other small corrections and polishing
#
# v0.04 2006-08-09
# Added command line options using getopt
# Added support for reading the SISX file from stdin
# Made it possible to extract files from SISX
# Improved hexdump ASCII support
#
# v0.03 2006-08-07
# Added some crude debug features: dumping to files, decompressed data dumping
#
# v0.02 2006-08-06
# Changed field type flags to callbacks for flexibility
# Added an UID checking and printing
#
# v0.01 2006-08-04
# Initial version
#
# v0.00 2006-08-03
# Work started
##############################################################################

VERSION = "v0.09 2006-09-22"

import sys
import os
import zlib
import struct
import getopt
import random
import tempfile

# Parameters
MAXSISFILESIZE      = 8 * 1024 * 1024   # Arbitrary maximum size of SISX file

sisfilename = None
tempdir = None
dumpcounter = 0
norecursecompressed = False

class options:
    '''Command line options'''

    hexdump         = True
    headerdump      = False
    dumpcontroller  = False
    dumptofile      = False

def mkdtemp(template):
    '''
    Create a unique temporary directory.

    tempfile.mkdtemp() was introduced in Python v2.3. This is for
    backward compatibility.
    '''

    # Cross-platform way to determine a suitable location for temporary files.
    systemp = tempfile.gettempdir()

    if not template.endswith("XXXXXX"):
        raise ValueError("invalid template for mkdtemp(): %s" % template)

    for n in xrange(10000):
        randchars = []
        for m in xrange(6):
            randchars.append(random.choice("abcdefghijklmnopqrstuvwxyz"))

        tempdir = os.path.join(systemp, template[: -6]) + "".join(randchars)

        try:
            os.mkdir(tempdir, 0700)
            return tempdir
        except OSError:
            pass

def hexdump(data, datalen = None):

    '''Print binary data as a human readable hex dump.'''

    if datalen == None or datalen > len(data):
        datalen = len(data)

    offset = 0
    while offset < datalen:
        line = []
        line.append("%06x:" % offset)
        for n in xrange(16):
            if n & 3 == 0:
                line.append(" ")
            if (offset + n) < datalen:
                c = data[offset + n]
                line.append("%02x " % ord(c))
            else:
                line.append("   ")
        line.append(' "')
        for n in xrange(16):
            if (offset + n) < datalen:
                c = data[offset + n]
                if ord(c) >= 32 and ord(c) < 127:
                    line.append(c)
                else:
                    line.append(".")
            else:
                break
        line.append('"')

        print "".join(line)
        offset += 16

def handlearray(data, datalen, reclevel):
    '''Handle SISArray.'''

    arraytype = data[:4]
    data = data[4:]

    arraypos = 0
    arraylen = datalen - 4
    while arraypos < arraylen:
        # Construct virtual SISFields for each array element.
        arraydata = arraytype + data[arraypos:]
        arraypos += parsesisfield(arraydata,
                                  arraylen - arraypos + 4, reclevel + 1) - 4

    if arraypos != arraylen:
        raise ValueError("SISArray data length mismatch")

def handlecompressed(data, datalen, reclevel):
    '''Handle SISCompressed.'''

    if datalen < 12:
        raise ValueError("SISCompressed contents too short")

    compalgo = struct.unpack("<L", data[:4])[0]
    uncomplen = struct.unpack("<Q", data[4:12])[0]

    print "%s%s  %d bytes uncompressed, algorithm %d" % ("  " * reclevel,
                                                         " " * 13, uncomplen,
                                                         compalgo)

    if compalgo == 0:
        # No compression, strip SISField and SISCompressed headers.
        data = data[12:datalen]
    elif compalgo == 1:
        # RFC1950 (zlib header and checksum) compression, decompress.
        data = zlib.decompress(data[12:datalen])
    else:
        raise ValueError("invalid SISCompressed algorithm %d" % compalgo)

    if uncomplen != len(data):
        raise ValueError("SISCompressed uncompressed data length mismatch")

    if norecursecompressed:
        # Recursive parsing disabled temporarily from handlefiledata().
        # Dump data instead.
        dumpdata(data, uncomplen, reclevel + 1)
    else:
        # Normal recursive parsing, delegate to handlerecursive().
        handlerecursive(data, uncomplen, reclevel)

def handlerecursive(data, datalen, reclevel):
    '''Handle recursive SISFields, i.e. SISFields only containing
    other SISFields.'''

    parselen = parsebuffer(data, datalen, reclevel + 1)
    if datalen != parselen:
        raise ValueError("recursive SISField data length mismatch %d %d" %
                            (datalen, parselen))

def handlefiledata(data, datalen, reclevel):
    '''Handle SISFileData.'''

    global norecursecompressed

    # Temporarily disable recursion for handlecompressed().
    oldnrc = norecursecompressed
    norecursecompressed = True
    handlerecursive(data, datalen, reclevel)
    norecursecompressed = oldnrc

def handlecontroller(data, datalen, reclevel):
    '''Handle SISController SISField. Dump data if required.'''

    if options.dumpcontroller:
        dumpdata(data, datalen, reclevel)

    # Handle contained fields as usual.
    handlerecursive(data, datalen, reclevel)

def dumpdata(data, datalen, reclevel):
    '''Dumps data to a file in a temporary directory.'''
    #print(data)

    global tempdir, dumpcounter

    if options.hexdump:
        hexdump(data, datalen)
        print
    if options.dumptofile:
        if tempdir == None:
            # Create temporary directory for dumped files.
            tempdir = mkdtemp("decodesisx-XXXXXX")
            dumpcounter = 0

        filename = os.path.join(tempdir, "dump%04d" % dumpcounter)
        dumpcounter += 1
        f = file(filename, "wb")
        f.write(data[:datalen])
        f.close()
        print "%sContents written to %s" % ("  " * reclevel, filename)

# SISField types and callbacks
sisfieldtypes = [
    ("Invalid SISField",                None),
    ("SISString",                       dumpdata),
    ("SISArray",                        handlearray),
    ("SISCompressed",                   handlecompressed),
    ("SISVersion",                      dumpdata),
    ("SISVersionRange",                 handlerecursive),
    ("SISDate",                         dumpdata),
    ("SISTime",                         dumpdata),
    ("SISDateTime",                     handlerecursive),
    ("SISUid",                          dumpdata),
    ("Unused",                          None),
    ("SISLanguage",                     dumpdata),
    ("SISContents",                     handlerecursive),
    ("SISController",                   handlecontroller),
    ("SISInfo",                         dumpdata),  # TODO: SISInfo
    ("SISSupportedLanguages",           handlerecursive),
    ("SISSupportedOptions",             handlerecursive),
    ("SISPrerequisites",                handlerecursive),
    ("SISDependency",                   handlerecursive),
    ("SISProperties",                   handlerecursive),
    ("SISProperty",                     dumpdata),
    ("SISSignatures",                   handlerecursive),
    ("SISCertificateChain",             handlerecursive),
    ("SISLogo",                         handlerecursive),
    ("SISFileDescription",              dumpdata),  # TODO: SISFileDescription
    ("SISHash",                         dumpdata),  # TODO: SISHash
    ("SISIf",                           handlerecursive),
    ("SISElseIf",                       handlerecursive),
    ("SISInstallBlock",                 handlerecursive),
    ("SISExpression",                   dumpdata),  # TODO: SISExpression
    ("SISData",                         handlerecursive),
    ("SISDataUnit",                     handlerecursive),
    ("SISFileData",                     handlefiledata),
    ("SISSupportedOption",              handlerecursive),
    ("SISControllerChecksum",           dumpdata),
    ("SISDataChecksum",                 dumpdata),
    ("SISSignature",                    handlerecursive),
    ("SISBlob",                         dumpdata),
    ("SISSignatureAlgorithm",           handlerecursive),
    ("SISSignatureCertificateChain",    handlerecursive),
    ("SISDataIndex",                    dumpdata),
    ("SISCapabilities",                 dumpdata)   # TODO: SISCapabilities
]

def parsesisfieldheader(data):
    datalen = len(data)

    headerlen = 8
    if datalen < headerlen:
        raise ValueError("not enough data for a complete SISField header")

    # Get SISField type.
    fieldtype = struct.unpack("<L", data[:4])[0]

    # Get SISField length, 31-bit or 63-bit.
    fieldlen = struct.unpack("<L", data[4:8])[0]
    fieldlen2 = None
    if fieldlen & 0x8000000L:
        # 63-bit length, read rest of length.
        headerlen = 12
        if datalen < headerlen:
            raise ValueError("not enough data for a complete SISField header")
        fieldlen2 = struct.unpack("<L", data[8:12])[0]
        fieldlen = (fieldlen & 0x7ffffffL) | (fieldlen2 << 31)

    return fieldtype, headerlen, fieldlen

def parsesisfield(data, datalen, reclevel):
    '''Parse one SISField. Call an appropriate callback
    from sisfieldtypes[].'''

    fieldtype, headerlen, fieldlen = parsesisfieldheader(data)

    # Check SISField type.
    fieldcallback = None
    if fieldtype < len(sisfieldtypes):
        fieldname, fieldcallback = sisfieldtypes[fieldtype]

    if fieldcallback == None:
        # Invalid field type, terminate.
        raise ValueError("invalid SISField type %d" % fieldtype)

    print(fieldname)
    # Calculate padding to 32-bit boundary.
    padlen = ((fieldlen + 3) & ~0x3L) - fieldlen

    # Verify length.
    if (headerlen + fieldlen + padlen) > datalen:
        raise ValueError("SISField contents too short")

    #print "%s%s: %d bytes" % ("  " * reclevel, fieldname, fieldlen)

    if options.headerdump:
        hexdump(data[:headerlen])
        print

    # Call field callback.
    sisfieldtypes[fieldtype][1](data[headerlen:], fieldlen, reclevel)

    return headerlen + fieldlen + padlen

def parsebuffer(data, datalen, reclevel):
    '''Parse all successive SISFields.'''

    datapos = 0
    while datapos < datalen:
        fieldlen = parsesisfield(data[datapos:], datalen - datapos, reclevel)
        print(fieldlen)
        datapos += fieldlen

    return datapos

def main():
    global sisfilename, tempdir, dumpcounter, options

    #pgmname     = os.path.basename(sys.argv[0])
    pgmname = r"D:\phpStudy\PHPTutorial\WWW\test.sisx"
    pgmversion  = VERSION

    try:
        try:
            gopt = getopt.gnu_getopt
        except:
            # Python <v2.3, GNU-style parameter ordering not supported.
            gopt = getopt.getopt

        # Parse command line using getopt.
        short_opts = "decft:h"
        long_opts = [
            "hexdump", "headerdump", "dumpcontroller",
            "dumptofile", "dumpdir", "help"
        ]
        args = gopt(sys.argv[1:], short_opts, long_opts)

        opts = dict(args[0])
        pargs = args[1]

        if len(pargs) > 1 or "--help" in opts.keys() or "-h" in opts.keys():
            # Help requested.
            print (
'''
DecodeSISX - Symbian OS v9.x SISX file decoder %(pgmversion)s

usage: %(pgmname)s [--dumptofile] [--hexdump] [--dumpdir=DIR] [sisfile]

        -d, --hexdump        - Show interesting SISFields as hex dumps
        -e, --headerdump     - Show SISField headers as hex dumps
        -c, --dumpcontroller - Dump each SISController SISField separately
        -f, --dumptofile     - Save interesting SISFields to files
        -t, --dumpdir        - Directory to use for dumped files (automatic)
        sisfile              - SIS file to decode (stdin if not given or -)

''' % locals())
            return 0

        if "--hexdump" in opts.keys() or "-d" in opts.keys():
            options.hexdump = True

        if "--headerdump" in opts.keys() or "-e" in opts.keys():
            options.headerdump = True

        if "--dumpcontroller" in opts.keys() or "-c" in opts.keys():
            options.dumpcontroller = True

        if "--dumptofile" in opts.keys() or "-f" in opts.keys():
            options.dumptofile = True

        # A temporary directory is generated by default.
        tempdir = opts.get("--dumpdir", opts.get("-t", None))

        '''
        if len(pargs) == 0 or pargs[0] == '-':
            sisfilename = "stdin"
            sisfile = sys.stdin
        else:
            sisfilename = pargs[0]
            sisfile = file(sisfilename, "rb") '''

        sisfilename = r"D:\phpStudy\PHPTutorial\WWW\test.sisx"
        sisfile = file(sisfilename, "rb")

        try:
            # Load the whole SIS file as a string.
            sisdata = sisfile.read(MAXSISFILESIZE)
            if len(sisdata) == MAXSISFILESIZE:
                raise IOError("%s: file too large" % sisfilename)
        finally:
            if sisfile != sys.stdin:
                sisfile.close()

        if len(sisdata) < 16:
            raise ValueError("%s: file too short" % sisfilename)

        # Check UIDs.
        uid1, uid2, uid3, uidcrc = struct.unpack("<LLLL", sisdata[:16])
        if uid1 != 0x10201a7a:
            if (uid2 in (0x1000006D, 0x10003A12)) and uid3 == 0x10000419:
                raise ValueError("%s: pre-9.1 SIS file" % sisfilename)
            else:
                raise ValueError("%s: not a SIS file" % sisfilename)

        print "UID1: 0x%08x, UID2: 0x%08x, UID3: 0x%08x, UIDCRC: 0x%08x\n" % (
            uid1, uid2, uid3, uidcrc)

        # Recursively parse the SIS file.
        parsebuffer(sisdata[16:], len(sisdata) - 16, 0)
    except (TypeError, ValueError, IOError, OSError), e:
        return "%s: %s" % (pgmname, str(e))
    except KeyboardInterrupt:
        return ""

# Call main if run as stand-alone executable.
if __name__ == '__main__':
    sys.exit(main())
