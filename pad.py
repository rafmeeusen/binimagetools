#!/usr/bin/env python

'''
Pad tool.
pad a file by padding 0xff bytes
'''

import argparse
import os
import sys
import tempfile

    
'''
pad function
pad input stream to output stream, by copying input, then adding 0xff bytes
newsize = or give new size
'''
def pad(infile, padsize, outfile):
    # copy stream
    while (data := infile.read()):
        outfile.write(data)
    bytesleft = padsize
    bufsize=2048
    while(bytesleft):
        if bytesleft > bufsize:
            outfile.write(bytearray([255] * bufsize))
            bytesleft -= bufsize
        else:
            outfile.write(bytearray([255] * bytesleft))
            bytesleft = 0

def main():
    parser = argparse.ArgumentParser(description='Binary image padding tool')
    parser.add_argument('infile', nargs=1, help='input file')
    parser.add_argument('nrbytes', nargs=1, type=int, help='number of bytes')
    parser.add_argument('-s', '--filesize', default=False, required=False, action='store_true', help='interpret number as new size of file after padding (DEFAULT)')
    parser.add_argument('-p', '--padsize', default=False, required=False, action='store_true', help='interpret number as number of bytes to pad')
    parser.add_argument('-f', '--outputfile', required=False, help='output file name')
    args = parser.parse_args()

    fn1=args.infile[0]
    nrbytes=args.nrbytes[0]
    infilesize = os.path.getsize(fn1)

    if args.filesize and args.padsize:
        errmsg = 'FATAL ERROR. Cannot give both options padding size and full final size'
        sys.exit(errmsg)
    elif args.padsize:
        padsize = nrbytes
    else:
        # final size given or nothing given
        padsize = nrbytes - infilesize
        if padsize < 0:
            errmsg = 'FATAL ERROR. Calculated padding size negative. Cannot reach final file size of ' + str(nrbytes)
            sys.exit(errmsg)
            
    infile = open(fn1, 'rb')
    if args.outputfile:
        outfile = open(args.outputfile, 'wb')
    else:
        outfile = tempfile.NamedTemporaryFile(delete=False)
    print('padding', infile.name, 'with a padding size of', padsize, 'into', outfile.name, 'with a final size of', (infilesize+padsize))
    pad(infile, padsize, outfile)
    infile.close()
    outfile.close()
    # doublecheck file size:
    outfilesize = os.path.getsize(outfile.name)
    expected_outfilesize = infilesize + padsize
    if outfilesize != expected_outfilesize:
        print('WARNING: size of output file ' + outfile.name + ' is not as expected') 

if __name__ == '__main__':
    main()


