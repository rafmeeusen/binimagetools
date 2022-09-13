# binimagetools
Various tools to handle binary images like firmware flash images

- uart2flashdump.py: use nand dump on uboot via serial port to make flash image
- pad.py: pad file with 0xff bytes
- offset.py: shift image by inserting 0xff bytes before
- merge.py: merge binary images with 0xff as "erased" or "empty" (flash images)
