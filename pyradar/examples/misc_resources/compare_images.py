# -*- coding: utf-8 -*-
from sys import argv
import Image

FILENAME1 = "image_filtered.png"
FILENAME2 = "image_original.png"


def load_images(filename1=None, filename2=None):
    """
    Open two images with Image module and return their Image objects.
    """
    img1 = None
    img2 = None

    if filename1 or filename2:
        try:
            img1_obj = Image.open(filename1)
            try:
                img2_obj = Image.open(filename2)

                img1 = list(img1_obj.getdata())
                img2 = list(img2_obj.getdata())
            except IOError:
                print "ERROR:Can't open '%s'\n" % filename2
                img2 = None
        except IOError:
            print "ERROR:Can't open '%s'\n" % filename1
            img1 = None
    else:
        try:
            img1_obj = Image.open(FILENAME1)
            try:
                img2_obj = Image.open(FILENAME2)

                img1 = list(img1_obj.getdata())
                img2 = list(img2_obj.getdata())
            except IOError:
                print "ERROR:Can't open '%s'\n" % FILENAME2
                img2 = None
        except IOError:
            print "ERROR:Can't open '%s'\n" % FILENAME1
            img1 = None

    return img1, img2


if __name__ == "__main__":
    print "#" * 79
    print "Comparing files..."

    if len(argv) == 3:
        filename1 = argv[1]
        filename2 = argv[2]
        print "Using filenames '%s', '%s'" % (filename1, filename2)
        img1, img2 = load_images(filename1, filename2)

    elif len(argv) == 2:
        print "Using defaults filenames '%s', '%s'" % (FILENAME1, FILENAME2)
        img1, img2 = load_images()

    if img1 and img2 and (img1 == img2):
        print "The images are the same."
    elif img1 and img2:
        print "The images are differents."
    else:
        pass
