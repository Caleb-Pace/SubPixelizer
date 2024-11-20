# SubPixelizer
The **SubPixelizer** is a Python command-line tool that encodes pixel data into subpixel components (red, green, blue) and decodes subpixel data back into a single luminosity value.

### Inspiration
This tool was created based on ideas from [Japhy Riddle](https://www.youtube.com/@japhyriddle) video that demonstrates encoding pixel art. <br/>
You can watch it here: [Smaller Than Pixel Art: Sub-Pixel Art!](https://www.youtube.com/watch?v=SlS3FOmKUbE)


## How it works
### Decoding (Pixels → Subpixels)
The program breaks down each pixel into its color intensity values (red, green, blue). It then assigns each intensity value to a separate pixel. By default, this process results in grayscale output, but you can preserve the original subpixel colors by using the `--show-colors` flag.

### Encoding (Compresses Subpixels → Pixels)
(Use the `-2px` or `--to-pixel` flag)

The program calculates a luminosity value for each pixel using the [Rec. 709 Luma coefficients](https://en.wikipedia.org/wiki/Rec._709#Luma_coefficients). It then groups three luminosity values and combines them into a single pixel, effectively compressing three subpixels into one.


## Setup
You will need [Python 3.x](https://www.python.org/downloads/) installed (I was using version 3.10)

1. Download the [`SubPixelizer.py`](./SubPixelizer.py) file and the [`requirements.txt`](./requirements.txt) file.

2. Install the required dependencies by running:
```bash
pip install -r requirements.txt
```


## Usage
```
Usage: SubPixelizer.py -i <input_file> -o <output_file> [-2px | --to-pixel] [--show-colors]

Options:
  -i,   --input              Input file (required)
  -o,   --output             Output file (required)
  -2px, --to-pixel           Treats input as subpixel data, converting 3 pixels into 1 (optional; defaults to decoding subpixels back into pixels)
        --show-colors        Show subpixel colors in output (optional, defaults to grayscale, only applies to decode)
  -h,   --help               Display this help message
```
*`python SubPixelizer.py --help` to see this message*

### Examples
- Encode pixel data into subpixel components:
```bash
python SubPixelizer.py -i "Pixel art pomeranian.png" -o "Encoded Pomeranian.png" -2px
```

- Decode subpixel data back into pixel data:
```bash
python SubPixelizer.py -i "Encoded Pomeranian.png" -o "Decoded Pomeranian.png"
```

- Decode subpixel data (while maintaining subpixel colors):
```bash
python SubPixelizer.py -i "Decode me.png" -o message.png --show-colors
```


## Images
- ![Pixel art pomeranian.png](./Pixel%20art%20pomeranian.png)<br/>
Modified from [Freepik (AI generated)](https://www.freepik.com/free-ai-image/pixel-art-style-scene-with-adorable-pet-dog_186697850.htm)

- ![Flower.png](./Flower.png)<br/>
Modified from [Freepik](https://www.freepik.com/free-vector/flat-design-flower-pixel-art-illustration_22631544.htm)

- ![Message from Japhy Riddle.png](./Message%20from%20Japhy%20Riddle.png)<br/>
Copied manually from [YouTube: Smaller Than Pixel Art: Sub-Pixel Art!](https://www.youtube.com/watch?v=SlS3FOmKUbE&t=368s)

- ![Decode me.png](/Decode%20me.png)<br/>
Made by me (the project author)
