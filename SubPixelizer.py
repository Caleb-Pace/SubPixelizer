import os, sys, math
import imageio.v2 as imageio
import numpy as np


# Constants
CMD_USAGE = "Usage: SubPixelizer.py -i <input_file> -o <output_file> [-2px | --to-pixel] [--show-colors]"


# TODO: Comment
def is_null_or_whitespace(s: str) -> bool:
    return (s is None or not s.strip())

# TODO: Comment
# TODO: Recomment
def retrieve_args():
    input_file = ""
    output_file = ""
    should_decode = True # Should decode subpixels
    is_grayscale = True  # Don't show subpixel color

    # Print help message
    if (len(sys.argv) == 2):
        if (sys.argv[1] in ["--help", "-h"]):
            help_msg = [
                CMD_USAGE,
                "",
                "Options:",
                "  -i,   --input              Input file (required)",
                "  -o,   --output             Output file (required)",
                "  -2px, --to-pixel           Treats input as subpixel data, converting 3 pixels into 1 (optional; defaults to decoding subpixels back into pixels)",
                "        --show-colors        Show subpixel colors in output (optional, defaults to grayscale, only applies to decode)",
                "  -h,   --help               Display this help message"
            ]
            print("\n".join(help_msg))

            sys.exit(0)

    if (len(sys.argv) >= 5 and len(sys.argv) <= 7):
        # Get arguments
        i = 1
        while (i < len(sys.argv)):
            arg = sys.argv[i]
            i += 1 # Increment count
            known_arg = False

            # Input file
            if (arg.lower() in ["--input", "-i"]):
                known_arg = True

                input_file = f"{sys.argv[i]}" # Get next arg
                i += 1 # Increment count

                # Validate path
                if (not os.path.exists(input_file)):
                    print(f"Error: File not found! (\"{input_file}\")")
                    sys.exit(1)
            
            # Output file
            if (arg.lower() in ["--output", "-o"]):
                known_arg = True

                output_file = sys.argv[i] # Get next arg
                i += 1 # Increment count

            # Conversion operation
            if (arg.lower() in ["--to-pixel", "-2px"]):
                known_arg = True
                should_decode = False

            # Grayscale output
            if (arg.lower() == "--show-colors"):
                known_arg = True
                is_grayscale = False

            if (not known_arg):
                print(f"Error: Unknown argument, '{arg}'!")
                sys.exit(1)
        
        # Check for missing arguments
        if is_null_or_whitespace(input_file):
            print("Error: Missing (or invalid) argument for 'input file'!")
            print(CMD_USAGE)
            sys.exit(1)
        if is_null_or_whitespace(output_file):
            print("Error: Missing (or invalid) argument for 'output file'!")
            print(CMD_USAGE)
            sys.exit(1)
    else:
        print(CMD_USAGE)
        print("\nError: Invalid usage! (Use the '--help' argument if you are stuck)")
        sys.exit(1)

    return input_file, output_file, should_decode, is_grayscale

# TODO: Comment
def get_luminosity_value(pixel: list[int]) -> int:
    if len(pixel) != 3:
        raise ValueError("Pixel must be a list of exactly three integers.")

    r = pixel[0]
    g = pixel[1]
    b = pixel[2]

    return ((0.2126 * r) + (0.7152 * g) + (0.0722 * b))

# TODO: Comment
def decode_subpixels(input_file: str, output_file: str, is_grayscale: bool):
    # Read in input image
    in_img = imageio.imread(input_file)

    # Get image size
    height, width = in_img.shape[:2]
    out_width = (width * 3)

    # Create image
    out_img = np.zeros((height, out_width, 3), dtype=np.uint8)

    # Generate output
    for y in range(height):
        for x in range(width):
            for c in range(3):
                subpixel = ((x * 3) + c)
                intensity = in_img[y, x][c] # [row, column][rgb color]
                
                if is_grayscale:
                    out_img[y, subpixel] = intensity
                else:
                    out_img[y, subpixel][c] = intensity # Show subpixel color
    
    # Write output to file
    try:
        imageio.imwrite(output_file, out_img)
    except ValueError:
        # Get file extension
        extension = output_file.split(".")[-1]

        print(f"Error: Unsupported image type! (\"{extension}\")")
        sys.exit(1)

    print(f"Decoded subpixel image!\n  \"{input_file}\" -> \"{output_file}\"")

# TODO: Comment
# TODO: Implement
def encode_pixels(input_file: str, output_file: str):
    # Read in input image
    in_img = imageio.imread(input_file)

    # Get image size
    height, width = in_img.shape[:2]
    out_width = math.ceil(width / 3)

    # Create image
    out_img = np.zeros((height, out_width, 3), dtype=np.uint8)

    # Generate output
    for y in range(height):
        for x in range(out_width):
            for c in range(3):
                pixel = ((x * 3) + c)
                if (pixel >= width):
                    continue # No pixel
                
                # Use luminosity grayscale method
                rgb = in_img[y, pixel] 
                luminosity = get_luminosity_value(rgb)
                
                out_img[y, x][c] = luminosity # [row, column][rgb color]
    
    # Write output to file
    try:
        imageio.imwrite(output_file, out_img)
    except ValueError:
        # Get file extension
        extension = output_file.split(".")[-1]

        print(f"Error: Unsupported image type! (\"{extension}\")")
        sys.exit(1)

    print(f"Encoded pixel image!\n  \"{input_file}\" -> \"{output_file}\"") 

# TODO: Comment
def main():
    input_file, output_file, should_decode, is_grayscale  = retrieve_args()

    # Transfrom (sub)pixels
    if should_decode:
        decode_subpixels(input_file, output_file, is_grayscale)
    else:
        encode_pixels(input_file, output_file)

if __name__ == "__main__":
    main()