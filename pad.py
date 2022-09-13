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
    print('padding', infile.name, 'with a padding size of', padsize, 'into', outfile.name)
    # copy stream
    while (data := infile.read()):
        outfile.write(data)
    bytesleft = padsize
    while(bytesleft):
        outfile.write(b'\xff')
        bytesleft -= 1


def main():
    parser = argparse.ArgumentParser(description='Binary image padding tool')
    parser.add_argument('-i', '--input', required=True, action='append', help='input file, use multiple -i for multiple input files')
    parser.add_argument('-p', '--padsize', required=False, type=int, help='number of bytes to pad')
    parser.add_argument('-s', '--size', required=False, type=int, help='new size of file after padding or offsetting')
    args = parser.parse_args()

    if len(args.input) != 1:
        errmsg = 'FATAL ERROR. Padding requires one file argument'
        sys.exit(errmsg)
    if args.padsize and args.size:
        errmsg = 'FATAL ERROR. Cannot give both options padding size and full final size'
        sys.exit(errmsg)
    fn1=args.input[0]
    infilesize = os.path.getsize(fn1)
    if args.padsize:
        padsize = args.padsize
    elif args.size:
        padsize = args.size - infilesize
    else:
        errmsg = 'FATAL ERROR. Need padding size option or full size option when padding'
        sys.exit(errmsg)
    infile = open(fn1, 'rb')
    outfile = tempfile.NamedTemporaryFile(delete=False)
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


