from PIL import Image
from skimage import data
import tesserocr, pytesseract
from random import randint


num = randint(1, 66)

def removeSault(img):
    pixel = img.load()
    w, h = img.size

    dirx = [0, 1, 1, 1, 0, -1, -1, -1]
    diry = [-1, -1, 0, 1, 1, 1, 0, -1]

    for y in range(1, h - 2):
        string = ''
        for x in range(1, w - 2):
            count = 0
            # for i in range(0, 8):
            #     if pixel[x + dirx[i], y + diry[i]] > 254:
            #         count += 1

            # if count >= 7:
            #     pixel[x, y] = 255

            if pixel[x,y] > 140:
                pixel[x, y] = 255;
                string += '0'
            else:
                pixel[x, y] = 0;
                string += '1'

        print(string)
    return img


def move(img):
    for x in range(1, 10):
        pass


# def Binarization():


img = Image.open('captch' + str(68) + '.png').convert('L')

img = removeSault(img)

img.show()
code = tesserocr.image_to_text(img)
code = code.replace('\n', '')

print(code)

