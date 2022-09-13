#!/usr/bin/env python

'''
Offset tool.
offset a file by prepending 0xff bytes
'''

import argparse
import os
import sys
import tempfile


'''
offset function
(aka prepend) : add 0xff in beginning of file, and then copy the original behind it. 
opposite of padding (first write 0xff, then copy stream)
'''
def offset(infile, nrbytes, outfile):
    bytesleft = nrbytes
    while(bytesleft):
        outfile.write(b'\xff')
        bytesleft -= 1
    while (data := infile.read()):
        outfile.write(data)


def main():
    parser = argparse.ArgumentParser(description='Binary image offset tool')
    parser.add_argument('infile', nargs=1, help='input file')
    parser.add_argument('offset', nargs=1, type=int, help='offset in number of bytes')
    parser.add_argument('-f', '--outputfile', required=False, help='output file name')
    args = parser.parse_args()

    fn1=args.infile[0]
    byteoffset=args.offset[0]
    infile = open(fn1, 'rb')
    if args.outputfile:
        outfile = open(args.outputfile, 'wb')
    else:
        outfile = tempfile.NamedTemporaryFile(delete=False)

    print('offsetting', infile.name, 'with offset', byteoffset, 'into', outfile.name)
    offset(infile, byteoffset, outfile)
    infile.close()
    outfile.close()

if __name__ == '__main__':
    main()


