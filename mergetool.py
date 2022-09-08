#!/usr/bin/env python

'''
Merge tool.
Meant to merge binary blobs that are parts of an image, where empty parts are 0xff, so typically a flash image.
Extra functions: offset a file by prepending 0xff bytes / pad a file by padding 0xff bytes
'''

import argparse
import os
import sys
import tempfile

'''
merge function
arguments: 3 file-like objects
file1/file2: two file-like objects that can be read from
outfile: file-like object where merge result is written to
merging: equal bytes are just copied, 0xff is considered EMPTY (so other file is taken), and a non-0xff difference is a fatal error

assumption: inputs are equal size streams
'''
def merge(file1, file2, outfile):
    print('merging', file1.name, 'and', file2.name, 'into', outfile.name)
    cnt = 0
    b1 = file1.read(1)
    while b1:
        bout = None
        b2 = file2.read(1)
        cnt += 1
        if b1 == b2:
            bout = b1
        else: 
            if b1 == b'\xff':
                bout = b2
            elif b2 == b'\xff':
                bout = b1
            else:
                print('b1:', b1)
                print('b2:', b2)
                print('type:', type(b2))
                excmsg = 'FATAL ERROR. Merging failed due to difference at offset ' + str(cnt) + ' (' + hex(cnt) + ')'
                raise Exception(excmsg)
        outfile.write(bout)
        b1 = file1.read(1)
    
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
    parser = argparse.ArgumentParser(description='Binary image merger tool')
    parser.add_argument('cmd', metavar='CMD', nargs=1, help='command: merge, pad or offset (or abbreviations like m,p,o)')
    parser.add_argument('-i', '--input', required=True, action='append', help='input file, use multiple -i for multiple input files')
    parser.add_argument('-o', '--offset', required=False, type=int, help='offset in number of bytes')
    parser.add_argument('-p', '--padsize', required=False, type=int, help='number of bytes to pad')
    parser.add_argument('-s', '--size', required=False, type=int, help='new size of file after padding or offsetting')
    args = parser.parse_args()
    if len(args.cmd) > 1:
        raise Exception('too many cmds dont know what to do')
    cmd = args.cmd[0]
    if 'merge'.startswith(cmd):
        if len(args.input) != 2:
            errmsg = 'FATAL ERROR. Merging requires two file arguments' 
            sys.exit(errmsg)
        fn1=args.input[0]
        fn2=args.input[1]
        s1 = os.path.getsize(fn1)
        s2 = os.path.getsize(fn2)
        if s1 != s2:
            errmsg = 'FATAL ERROR. For merging both files need to be same size. Size are: ' + str(s1) + ' and ' + str(s2)
            sys.exit(errmsg)
        f1 = open(fn1, 'rb')
        f2 = open(fn2, 'rb')
        outfile = tempfile.NamedTemporaryFile(delete=False)
        merge(f1, f2, outfile)
        f1.close()
        f2.close()
        outfile.close()
        # doublecheck file size:
        if os.path.getsize(outfile.name) != s1:
            print('WARNING: size of output file ' + outfile.name + ' is not same as input file size') 
    elif 'pad'.startswith(cmd):
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
    elif 'offset'.startswith(cmd):
        if len(args.input) != 1:
            errmsg = 'FATAL ERROR. Offseting requires one file argument'
            sys.exit(errmsg)
        if not args.offset:
            errmsg = 'FATAL ERROR. Need offset option when offsetting'
            sys.exit(errmsg)
        fn1=args.input[0]
        byteoffset=args.offset
        outfile = tempfile.NamedTemporaryFile(delete=False)
        infile = open(fn1, 'rb')
        offset(infile, byteoffset, outfile)
        infile.close()
        outfile.close()
    else:
        print('error unknown cmd:', cmd)

if __name__ == '__main__':
    main()


