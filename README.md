# labelboy
Code for generating labels using our label printer

## PROPRIETARY DRIVERS

The two filters named `rastertotspl` must be placed at `/usr/lib/cups/filters/rastertotspl` with permission slug 755. Work is ongoing to replace these with open source versions. They seem loosely based on the rastertolabel filter which is already present. Perhaps a dissasembly could allow an open source filter to be written?
