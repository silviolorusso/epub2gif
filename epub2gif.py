## epub2gif

import sys, os, glob, shutil

import ebooklib
from ebooklib import epub
from PIL import Image, ImageFont, ImageDraw
from images2gif import writeGif

# args
if len(sys.argv) == 2:
    bookname = os.path.splitext(sys.argv[1])[0]
    book = epub.read_epub(sys.argv[1])
else:
    print '\nNo EPUB file provided.\nUsage: python epub2gif.py filename.epub\n'
    quit()

# parameters
speed = 0.1
W = 500
H = 400
bgColor = (255,255,255)

# save content of pic to file
def savetofile(img):
    # get name and extension
    img_name = os.path.basename(img.file_name)
    img_type = img.media_type
    ext = img_type.split('/')[1]
    # write to file
    img_file = open(img_name, 'w')
    img_file.write(img.get_content())

# create temporary dir and enter it
temp_dir = "temp"
if not os.path.exists(temp_dir):
    os.makedirs(temp_dir)
os.chdir(temp_dir)

# print all pictures in the book
for image in book.get_items_of_type(ebooklib.ITEM_IMAGE):
    savetofile(image)

# resize all pics
for picture in glob.glob("*.*"):
    background = Image.new("RGBA", (W,H), bgColor)
    image = Image.open(picture)
    image.thumbnail((W, H), Image.NEAREST)
    (w, h) = image.size
    background.paste(image, ((W-w)/2,(H-h)/2))
    background.save(os.path.splitext(picture)[0]+'.jpg')

# make gif!
images = [Image.open(image) for image in glob.glob("*.jpg")]
filename = '../' + bookname + '.gif'
writeGif(filename, images, duration=speed)

# clean up 
os.chdir('..')
shutil.rmtree(temp_dir)