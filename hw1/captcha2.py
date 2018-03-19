from PIL import Image

im = Image.open("captcha.png")
im = im.convert("L")
im2 = Image.new("L",im.size,255)

im = im.convert("L")

temp = {}

for x in range(im.size[1]):
  for y in range(im.size[0]):
    pix = im.getpixel((y,x))
    temp[pix] = pix
    if pix == 220 or pix == 227: # these are the numbers to get
      im2.putpixel((y,x),0)

im2.show()