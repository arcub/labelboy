#!/usr/bin/env python3
# coding: utf-8

import cups
from datetime import datetime
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from tempfile import mktemp
from time import sleep
import segno
import sys

arguments = sys.argv

code = None

if (len(arguments) > 1):
    code = arguments[1]
else:
    print("Missing code!")
    exit()
#code = "JAFSMGEFB/775/CRS"

path = arguments[0].split("/")
path.pop()
path = "/".join(path) + "/"
#print(path)
#exit()

code = code.upper()
codebits = code.split("/")

gpcrs = False

gperms = int(codebits[1][2])

modify = (gperms & 4) > 0
takehome = (gperms & 2) > 0
reconf = (gperms & 1) > 0

qrcode = segno.make_qr("https://crs.indent.one/id/" + code)
qrcode.save("qrcode.png", scale=4, border=0)

# Set up CUPS
conn = cups.Connection()
printers = conn.getPrinters()
printer_name = list(printers.keys())[0]
cups.setUser('crs')

# Image (code taken from boothcam.py)
im = Image.new('RGBA', (90*8, 162*8))
#im.paste(Image.open('logo.png').resize((162, 90)), ( 0, 0, 162, 90))
im.paste(Image.open("qrcode.png").resize((74*8, 74*8)), (8*8, 8*8))
imd = ImageDraw.Draw(im)


ibm_mono_s_big = ImageFont.truetype(path + "IBMPlexMono-Bold.ttf", 145)
ibm_sans_s_med = ImageFont.truetype(path + "IBMPlexSans-Medium.ttf", 72)

ibm_mono_s_med = ImageFont.truetype(path + "IBMPlexMono-Bold.ttf", 96)

ibm_sans_s_med_b = ImageFont.truetype(path + "IBMPlexSans-Bold.ttf", 72)
ibm_sans_s_sml = ImageFont.truetype(path + "IBMPlexSans-Medium.ttf", 50)
ibm_mono_s_sml = ImageFont.truetype(path + "IBMPlexMono-Bold.ttf", 48)
ibm_sans_s_sml_b = ImageFont.truetype(path + "IBMPlexSans-Bold.ttf", 48)
 
# Add Text to an image
#imd.fontmode = "1" # Disable antialiasing


imd.text((60, 86*8), "https://crs.indent.one/id/", font=ibm_sans_s_sml, fill=(0, 0, 0))
width = int(((74/3) + 2.5)*8)
imd.text(((7*8), 92*8), codebits[0][0:3], font=ibm_mono_s_med, fill=(0, 0, 0))
imd.text(((7*8) + (width), 92*8), codebits[0][3:6], font=ibm_mono_s_med, fill=(0, 0, 0))
imd.text(((7*8) + (width * 2), 92*8), codebits[0][6:9], font=ibm_mono_s_med, fill=(0, 0, 0))

imd.text((7*8, (92*8) + (9*8)), codebits[1] + " " + codebits[2], font=ibm_mono_s_big, fill=(0, 0, 0))

if (len(codebits) > 3):
    _, _, w, h = imd.textbbox((0,0), codebits[3], font=ibm_mono_s_sml)
    imd.text((((90*8)-w)/2, (92*8) + (28*8)), codebits[3], font=ibm_mono_s_sml, fill=(0, 0, 0))

imd.text((7*8, (96*8) + (32*8)), "Modify or hack", font=ibm_sans_s_med_b, fill=(0, 0, 0))
imd.text((7*8, (96*8) + (40*8)), "Take home", font=ibm_sans_s_med_b, fill=(0, 0, 0))
imd.text((7*8, (96*8) + (48*8)), "Reconfigure", font=ibm_sans_s_med_b, fill=(0, 0, 0))

if (modify):
    im.paste(Image.open("yes.png").resize((10*8, 10*8)), (74*8, (96*8) + (33*8)))
else:
    im.paste(Image.open("no.png").resize((10*8, 10*8)), (74*8, (96*8) + (33*8)))
    
if (takehome):
    im.paste(Image.open("yes.png").resize((10*8, 10*8)), (74*8, (96*8) + (41*8)))
else:
    im.paste(Image.open("no.png").resize((10*8, 10*8)), (74*8, (96*8) + (41*8)))
    
if (reconf):
    im.paste(Image.open("yes.png").resize((10*8, 10*8)), (74*8, (96*8) + (49*8)))
else:
    im.paste(Image.open("no.png").resize((10*8, 10*8)), (74*8, (96*8) + (49*8)))

#imd.text((7*8, (84*8) + (32*8)), "Modify", font=ibm_sans_s_med, fill=(0, 0, 0))
#imd.text((7*8, (84*8) + (42*8)), "Build with", font=ibm_sans_s_med, fill=(0, 0, 0))
#imd.text((7*8, (84*8) + (52*8)), "Reconfigure", font=ibm_sans_s_med, fill=(0, 0, 0))
#imd.text((7*8, (84*8) + (65*8)), "crs.indent.one/id", font=ibm_sans_s_med_b, fill=(0, 0, 0))

im.rotate(90)

# Save data to a temporary file
output = mktemp(prefix="png")
#im.save("label.png", format='png')
im.save(output, format="png")

# Send the picture to the printer
#print_id = conn.printFile(printer_name, "label.png", "label", {})
print_id = conn.printFile(printer_name, output, "label", {})
sleep(1)
# Wait until the job finishes
#print(conn.getJobs())
#while print_id in conn.getJobs():
#    sleep(1)


