from PIL import Image, ImageFilter, ImageDraw, ImageOps
from imager2 import Imager

def ptest1(fid1='images/kdfinger.jpeg', fid2="images/einstein.jpeg",steps=5,newsize=250):
    im1 = Imager(fid1); im2 = Imager(fid2)
    im1 = im1.resize(newsize,newsize); im2 = im2.resize(newsize,newsize)
    roll = im1.morphroll(im2,steps=steps)
    roll.display()
    return roll

def ptest2(fid1='images/einstein.jpeg',outfid='images/tunnel.jpeg',levels=3,newsize=250,scale=0.8):
    im1 = Imager(fid1);
    im1 = im1.resize(newsize,newsize);
    im2 = im1.tunnel(levels=levels,scale=scale)
    im2.display()
    im2.dump_image(outfid)
    return im2

def ptest3(fid1='images/kdfinger.jpeg', fid2="images/einstein.jpeg",newsize=250,levels=4,scale=0.75):
    im1 = Imager(fid1); im2 = Imager(fid2)
    im1 = im1.resize(newsize,newsize); im2 = im2.resize(newsize,newsize)
    box = im1.mortun(im2,levels=levels,scale=scale)
    box.display()
    return box

def reformat(in_fid, out_ext='jpeg',scalex=1.0,scaley=1.0):
    base, extension = in_fid.split('.')
    im = Imager(in_fid)
    im = im.scale(scalex,scaley)
    im.dump_image(base,out_ext)



def test(fid1, fid2):
    im1 = Imager(fid1)
    im2 = Imager(fid2)
    im1.get_image_dims()
    im2.resize(im1.xmax, im2.ymax)
    im3 = im1.morph(im2, 0.5)
    im3.display()


class Image_art():
    def __init__(self, fid1, fid2, fid3):
        self.im1 = Imager(fid1)
        self.im2 = Imager(fid2)
        self.im3 = Imager(fid3)
        self.art = Imager()

    def images_art(self, alpha = 0.5):
        self.im2.image = self.im2.image.filter(ImageFilter.CONTOUR)
        self.im1.get_image_dims()
        self.im2 = self.im2.resize(self.im1.xmax, self.im1.ymax)
        self.im3 = self.im3.resize(self.im1.xmax, self.im1.ymax)
        temp = self.im1.morph(self.im2, alpha)
        morphed = temp.morph(self.im3, alpha)
        morphed.image = ImageOps.solarize(morphed.image,threshold=200)
        morphed.get_image_dims()
        draw = ImageDraw.Draw(morphed.image)
        draw.text((morphed.xmax/2, morphed.ymax/2),"art or not??", fill=(255,0,0,255))
        self.art = morphed

    def filter_blur(self):
        self.art.image = self.art.image.filter(ImageFilter.DETAIL)



    def display(self):
        self.art.display()


def main():
    art = Image_art("images/campus.jpeg", "images/fibonacci.jpeg", "images/brain.jpeg")
    art.images_art()
    art.filter_blur()
    art.display()

if __name__ == '__main__':
    main()
