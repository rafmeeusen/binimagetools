# binimagetools
Various tools to handle binary images like firmware flash images

## Overview 

- uart2flashdump.py: use nand dump on uboot via serial port to make flash image
- offset.py: shift image by inserting 0xff bytes before
- pad.py: pad file with 0xff bytes
- merge.py: merge binary images with 0xff as "erased" or "empty" (flash images)

## Example use case

Example below shows how to 
- create multiple flash image dumps at different offsets, each of different size, 
- then offsetting each dump (0xff bytes for the unknown beginning), 
- then padding each dump (0xff bytes at the end) such that all file sizes are equal to final image size, 
- and finally merging them all into one image file

The merging step would throw an error if there was a conflict between the partial images. 

This method allows to create a a full flash image or a more complete partial image from different partial images, with overlaps allowed. 

```
./uart2flashdump.py dump0.bin 0 13
./offset.py dump0.bin 0 -f dump0.bin.o
./pad.py dump0.bin.o -s 268435456 -f dump0.bin.o.p

./uart2flashdump.py dump1000.bin 1000 19
./offset.py dump1000.bin 2048000 -f dump1000.bin.o
./pad.py dump1000.bin.o -s 268435456 -f dump1000.bin.o.p

./uart2flashdump.py dump6000.bin 6000 16
./offset.py dump6000.bin 12288000 -f dump6000.bin.o
./pad.py dump6000.bin.o -s 268435456 -f dump6000.bin.o.p

./uart2flashdump.py dump15000.bin 15000 32
./offset.py dump15000.bin 30720000 -f dump15000.bin.o
./pad.py dump15000.bin.o -s 268435456 -f dump15000.bin.o.p

./uart2flashdump.py dump30000.bin 30000 3
./offset.py dump30000.bin 61440000 -f dump30000.bin.o
./pad.py dump30000.bin.o -s 268435456 -f dump30000.bin.o.p

./uart2flashdump.py dump50000.bin 50000 35
./offset.py dump50000.bin 102400000 -f dump50000.bin.o
./pad.py dump50000.bin.o -s 268435456 -f dump50000.bin.o.p

../merge.py  dump*bin.o.p -f merged.bin`
```
