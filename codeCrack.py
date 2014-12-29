from PIL import Image
import sys
import os
import cStringIO


__author__ = 'qmax'

class CrackOcr:
    def __init__(self, mask,threshold=150):
        self.lettermask = Image.open(mask)
        self.ledata = self.lettermask.load()

        for y in xrange(self.lettermask.size[1]):
            for x in xrange(self.lettermask.size[0]):
                if not(self.ledata[x, y][0] > threshold and self.ledata[x, y][1] > threshold and self.ledata[x, y][2] > threshold):
                    self.ledata[x, y] = (255, 255, 255)
                else:
                    self.ledata[x, y] = (0, 0, 0)

    def ocr(self, im, threshold=150, alphabet="0146953782"):
        img = Image.open(im)
        img = img.convert("RGB")
        box = (5, 0, 85, 20)
        img = img.crop(box)
        pixdata = img.load()

        # open the mask


        def test_letter(img, letter):

            A = img.load()
            B = letter.load()
            mx = 1000000
            max_x = 0
            x = 0

            for x in xrange(img.size[0]-letter.size[0]):
                sum = 0
                for i in xrange(letter.size[0]):
                    for j in xrange(letter.size[1]):
                        sum = sum + abs(A[x+i, j][0] - B[i, j][0])
                if sum < mx:
                    mx = sum
                    max_x = x
            return mx, max_x

        # Clean the background noise, if color != black, then set to white.
        for y in xrange(img.size[1]):
            for x in xrange(img.size[0]):
                if not(pixdata[x, y][0] > threshold and pixdata[x, y][1] > threshold and pixdata[x, y][2] > threshold):
                    pixdata[x, y] = (255, 255, 255)
                else:
                    pixdata[x, y] = (0, 0, 0)

    #    img.show()

        letterlist = []

    # here cut the image and mask
        for imgcut in [0, 13, 26, 39, 52, 65]:
                    box = (imgcut, 0, imgcut + 12, 20)
                    imgtemp = img.crop(box)
    #                imgtemp.show()

                    t_max = 99999
                    t_temp = [99999, 99999]
                    counter = -1
                    counter_temp = counter
                    old_x = -1

                    for x in xrange(self.lettermask.size[0]):

                            black = True
                            for y in xrange(self.lettermask.size[1]):
                                    #print (x,y,ledata[x, y][0])
                                    if self.ledata[x, y][0] <> 0 :
                                            black = False
                                            break
                            if black:
                                    counter += 1
                                    if True:
                                            box = (old_x+1, 0, x, 20)
                                            letter = self.lettermask.crop(box)

                                            t = test_letter(imgtemp, letter)
                                            if t[0] < t_max:
                                                    t_max = t[0]
                                                    t_temp = t
                                                    counter_temp = counter

                                    old_x = x

    #                print t_temp,counter_temp
                    letterlist.append((t_temp[0], alphabet[counter_temp], t_temp[1], imgcut))

        t = sorted(letterlist, key=lambda x: x[3])

        answer = ""
        for l in t:
            answer = answer + l[1]
        return answer