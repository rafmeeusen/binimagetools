#!/usr/bin/env python

'''
Merge tool.
Merge binary blobs that are parts of an image, where empty parts are 0xff, so typically a flash image.
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

def main():
    parser = argparse.ArgumentParser(description='Binary image merger tool')
    parser.add_argument('-i', '--input', required=True, action='append', help='input file, use multiple -i for multiple input files')
    args = parser.parse_args()

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

if __name__ == '__main__':
    main()

