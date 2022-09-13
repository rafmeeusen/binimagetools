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
    print('offsetting', infile.name, 'with offset', nrbytes, 'into', outfile.name)
    bytesleft = nrbytes
    while(bytesleft):
        outfile.write(b'\xff')
        bytesleft -= 1
    while (data := infile.read()):
        outfile.write(data)


def main():
    parser = argparse.ArgumentParser(description='Binary image offset tool')
    parser.add_argument('-i', '--input', required=True, action='append', help='input file, use multiple -i for multiple input files')
    parser.add_argument('-o', '--offset', required=False, type=int, help='offset in number of bytes')
    args = parser.parse_args()

    if len(args.input) != 1:
        errmsg = 'FATAL ERROR. Offseting requires one file argument'
        sys.exit(errmsg)
    fn1=args.input[0]
    if not args.offset:
        byteoffset=0
    else:
        byteoffset=args.offset
    outfile = tempfile.NamedTemporaryFile(delete=False)
    infile = open(fn1, 'rb')
    offset(infile, byteoffset, outfile)
    infile.close()
    outfile.close()

if __name__ == '__main__':
    main()


