# MoveDrawable
A Python script to automatically move, rename and compress (webP) the assets given to you by your designers.

Usually when you receive the assets from your designers, if they work with Sketch, the files are all in the same folder and named like fillname@1x.png, fillname@2x.png, etc.
This script take those files and rename them, move them to the right Android source folder (mdpi, hdpi, ...) and even compress them to the webP format.

## How to use it
In your terminal, run the following command and follow the instructions:

    python mv_drawable.py <SRC_DIRECTORY> <ANDROID_RESOURCES_DIRECTORY>

## WebP compression
If you want to be able to compress your files to webP, just download cwebp utility from [the official site](https://developers.google.com/speed/webp/docs/using) and move it to the script folder.
Then you will be able to compress assets.

## TODO
- Right now the script only take PNGs as input, should change it to take also at least JPGs.
