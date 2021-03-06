from PIL import Image, ImageEnhance
from skimage import data
import tesserocr, pytesseract
from random import randint


num = randint(1, 60)

def removeSault(img):
    pixel = img.load()
    w, h = img.size

    dirx = [0, 1, 1, 1, 0, -1, -1, -1]
    diry = [-1, -1, 0, 1, 1, 1, 0, -1]

    for y in range(1, h - 2):
        string = ''
        for x in range(1, w - 2):
            count = 0
            for i in range(0, 8):
                if pixel[x + dirx[i], y + diry[i]] > 254:
                    count += 1

            if count >= 7:
                pixel[x, y] = 255

            if pixel[x, y] > 130:
                pixel[x, y] = 255;
                string += '0'
            else:
                pixel[x, y] = 0;
                string += '1'

    for y in range(1, h - 2):
        string = ''
        for x in range(1, w - 2):
            count = 0
            for i in range(0, 8):
                if pixel[x + dirx[i], y + diry[i]] == 0:
                    count += 1

            if count >= 5:
                pixel[x, y] = 0

    for x in range(0, w):
        pixel[x, 0] = 255
        pixel[x, h - 1] = 255
    for y in range(0, h):
        pixel[0, y] = 255
        pixel[w - 1, y] = 255

    return img


def move(img):
    w, h = img.size
    pixel = img.load()

    for i in range(0, 5):
        offsetx = (i + 1) * 20
        max = 0
        for x in range(offsetx - 20, offsetx - 14 - 1):
            for y in range(0, 50 - 14 - 1):
                count = 0
                for m in range(0, 14):
                    for n in range(0, 14):
                        if  pixel[m + x, n + y] == 0:
                            count += 1

                if count > max:
                     max = count
                     posx, posy = x, y

        # print(posx, posy)

        # offset = posy - 0
        # for x in range(posx, posx + 20):
        #     for y in range(posy, posy + 14):
        #         pixel[x, y - offset] = pixel[x, y]
        #         pixel[x, y] = 255

        if posy + 7 <= 25:
            offset = 25 - (posy + 7)

            if offset > 5:
                for x in range(posx, posx + 14):
                    for y in range(posy + 14 - 1, posy - 1, -1):
                        pixel[x, y + offset] = pixel[x, y]
                        pixel[x, y] = 255

        else:
            offset = (posy + 7) - 25
            if offset > 5:
                for x in range(posx, posx + 14):
                    for y in range(posy, posy + 14):
                        pixel[x, y - offset] = pixel[x, y]
                        pixel[x, y] = 255

    return img

def decode(img):
    replace_char = {
        '\n': '',
        ' ': '4',
        '(': '6',
        '%': '8',
        '1': '7',
        '$': '9',
    }
    code = tesserocr.image_to_text(img)
    for (key, val) in replace_char.items():
        code = code.replace(key, val)

    return code



img = Image.open('captcha' + str(num) + '.png')
img = img.convert('L')
img = removeSault(img)
img = move(img)
code = decode(img)

print(code)






# img = removeSault(img)
# img.show()
# decode(img)





