__author__ = 'Jatin'

import requests, urllib2, BeautifulSoup, os.path as fcheck, gzip, binascii
from PIL import Image
#
# churl = "http://www.pythonchallenge.com/pc/return/balloons.html"
#
# if fcheck.isfile("balloons.jpg"):
#     print "Balloons.jpg already exists. \nSkipping download..."
#
# else:
#     chimgurl = "http://www.pythonchallenge.com/pc/return/balloons.jpg"
#     response = requests.get(chimgurl, auth=("huge", "file"))
#     chimg = open("balloons.jpg", "wb")
#     chimg.write(response.content)
#     chimg.close()
#
# chimg = Image.open("balloons.jpg")
# ox, oy = chimg.size
# print ox, oy
#
# img1 = Image.new("RGB", (ox / 2, oy), "Red")
# # img1.show()
# img2 = Image.new("RGB", (ox / 2, oy), "Green")
# # img2.show()
#
# # pxlval = open("level18","w")
#
#
# for _oy in range(0, oy):
#     for _ox in range(0, ox):
#         if _ox < ox / 2:
#             img1.putpixel((_ox, _oy), chimg.getpixel((_ox, _oy)))
#         else:
#             img2.putpixel((_ox - ox / 2, _oy), chimg.getpixel((_ox, _oy)))
#
# # img1.show()
# # img2.show()
#
# r1, g1, b1 = img1.split()
# r2, g2, b2 = img2.split()
#
# # img1.save("img1.jpg", "JPEG")
# # img2.save("img2.jpg", "JPEG")
# # nwim1 = Image.merge("RGB",(r1,g2,b1))
# # nwim1.show()
#
# diffImg = Image.new("RGB", (ox / 2, oy), "Black")
# for _oy in range(0, oy):
#     for _ox in range(0, ox / 2):
#         r1, g1, b1 = img1.getpixel((_ox, _oy))
#         r2, g2, b2 = img2.getpixel((_ox, _oy))
#         # print r2 - r1, g2 - g1, b2 - b1
#         # diffImg.putpixel((_ox, _oy), (r2 - r1, g2 - g1, b2 - b1))
#         diffImg.putpixel((_ox, _oy), (r1 - r2, g1 - g2, b1 - b2))
# diffImg.show()

# Nope, this is all useless! As comment said it may be obvious. The difference here is basically of "brightness"

churl = "http://www.pythonchallenge.com/pc/return/brightness.html"
response = requests.get(churl, auth=("huge", "file"))
print response.content

# Maybe consider deltas.gz! Hmmm

# response = requests.get("http://www.pythonchallenge.com/pc/return/deltas.gz", auth=("huge","file"))
# f = open("deltas.gz", "w")
# f.write(response.content)
# f.close()

# No matter what I do, If I save deltas.gz using code above, it corrupts the file, anyway manually downloaded the file and extracting now.
# Will include this delta file in git


with gzip.open('deltas.gz', 'rb') as f:
    file_content = f.readlines()

l18 = open("level18", "w")
l18.writelines(file_content)
l18.close()

# Now we have 2 images hexcode in the level18 file. Let's break it into 2 files

l18 = open("level18", "r")
l18_1 = open("level18_1", "r+")
l18_2 = open("level18_2", "r+")

fcon = l18.read()
fconlst = fcon.split("\n")

# Bad approach, lets look for alternatives
# for i in range(len(fconlst)):
#     nwlst = fconlst[i].split("   ")
#     l18_1.write(nwlst[0])
#     l18_2.write(nwlst[1])

# A bit cheating as first file is till 53, and second starts from 56
pairs = [(line[:53], line[56:]) for line in fconlst]
columns = ['\n'.join([p[i] for p in pairs]) for i in range(2)]

l18_1.write(columns[0])
l18_2.write(columns[1])
l18.close()
# l18_1.close()
# l18_2.close()

# OK I cheated here. Just couldn't find how to convert hex to image in Python. I was able to do that using HxD editor in Windows. :)
import codecs, re


def unhex(s): return codecs.getdecoder('hex')(re.sub('[^0-9a-fA-F]', '', s))[0]


for i in range(2): open('de lta%d.png' % i, 'wb').write(unhex(columns[i]))
# Images are garbled up here.



f1_lines = columns[0].splitlines()
f2_lines = columns[1].splitlines()

import difflib

d = difflib.Differ()
diff = d.compare(f1_lines, f2_lines)
diffstr = '\n'.join(diff)
print diffstr
img1 = open("level18_img1", "w")
img2 = open("level18_img2", "w")
img3 = open("level18_img3", "w")

for line in diffstr.splitlines():
    if line[0] == " ":
        img1.write(line[2:] + "\n")

    elif line[0] == "+":
        img2.write(line[2:] + "\n")

    elif line[0] == "-":
        img3.write(line[2:] + "\n")

for i in range(3): open('newdelta%d.png' % i, 'wb').write(unhex("img" + str(i)))
