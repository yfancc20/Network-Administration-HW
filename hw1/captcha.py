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
        for x in range(offsetx - 20, offsetx - 16 - 1):
            for y in range(0, 50 - 16 - 1):
                count = 0
                for m in range(0, 16):
                    for n in range(0, 16):
                        if  pixel[m + x, n + y] == 0:
                            count += 1

                if count > max:
                     max = count
                     posx, posy = x, y

        # print(posx, posy)

        # offset = posy - 0
        # for x in range(posx, posx + 20):
        #     for y in range(posy, posy + 16):
        #         pixel[x, y - offset] = pixel[x, y]
        #         pixel[x, y] = 255

        if posy + 8 <= 25:
            offset = 25 - (posy + 8)
            # print('offset:' + str(offset))
            for x in range(posx, posx + 16):
                for y in range(posy + 16 - 1, posy - 1, -1):
                    pixel[x, y + offset] = pixel[x, y]
                    pixel[x, y] = 255
        else:
            offset = (posy + 8) - 25
            for x in range(posx, posx + 16):
                for y in range(posy, posy + 16):
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



img = Image.open('captcha' + str(39) + '.png').convert('L')
print(num)
img = removeSault(img)
img.show()
img = move(img)
img.show()
code = decode(img)

print(code)






# img = removeSault(img)
# img.show()
# decode(img)





