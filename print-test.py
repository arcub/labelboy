#!/usr/bin/env python3

import cups
from PIL import Image
from tempfile import mktemp
from time import sleep

# Set up CUPS
conn = cups.Connection()
printers = conn.getPrinters()
printer_name = list(printers.keys())[0]
cups.setUser('crs')

im = Image.new('RGBA', (162, 90))
im.paste(Image.open('logo.png').resize((162, 90)), ( 0, 0, 162, 90))

# Save data to a temporary file
output = mktemp(prefix='png')
im.save(output, format='png')

# Send the picture to the printer
print_id = conn.printFile(printer_name, output, "label", {})
# Wait until the job finishes
while conn.getJobs().get(print_id, None):
    sleep(1)
unlink(output)
