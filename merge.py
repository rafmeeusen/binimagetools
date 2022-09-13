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

    parser.add_argument('infiles', nargs='*', help='input files, minimum two')
    parser.add_argument('-f', '--outputfile', required=False, help='output file name')
    args = parser.parse_args()

    if len(args.infiles) < 2:
        excmsg = 'FATAL ERROR. Need at least two input files'
        raise Exception(excmsg)

    # check file sizes are equal
    print('comparing file sizes')
    size0 = os.path.getsize(args.infiles[0])
    for fn in args.infiles[1:]:
        if os.path.getsize(fn) != size0:
            errmsg = 'FATAL ERROR. For merging both files need to be same size. Different: ' + args.infiles[0] + ' and ' + fn
            sys.exit(errmsg)

    # open all input files
    ifs = [open(fn,'rb') for fn in args.infiles]

    # create tmp files (input/output)
    nr_tmpfiles = len(args.infiles) - 2
    tmpfs = [tempfile.NamedTemporaryFile(delete=False) for i in range(nr_tmpfiles)]

    # now merge per two files
    nextin = ifs[0]
    for (infile,tmpout) in zip(ifs[1:-1], tmpfs):
        print('merging', nextin.name, 'and', infile.name, 'into', tmpout.name)
        merge(nextin, infile, tmpout)
        nextin = tmpout
    # last merge into final output:
    if args.outputfile:
        finalout = open(args.outputfile, 'wb')
    else:
        finalout = tempfile.NamedTemporaryFile(delete=False)
    print('merging', nextin.name, 'and', ifs[-1].name, 'into', finalout.name)
    merge(nextin, ifs[-1], finalout)

    # close all files
    for f in ifs:
        f.close()
    for t in tmpfs:
        t.close()
    finalout.close()

if __name__ == '__main__':
    main()


