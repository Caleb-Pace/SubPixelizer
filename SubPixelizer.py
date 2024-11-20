# Import necessary libraries
import os, sys, math
import imageio.v2 as imageio
import numpy as np

# Command-line usage message
CMD_USAGE = "Usage: SubPixelizer.py -i <input_file> -o <output_file> [-2px | --to-pixel] [--show-colors]"

def is_null_or_whitespace(s: str) -> bool:
    """
    Check if string is null or contains only whitespace
    """
    return (s is None or not s.strip())

def retrieve_args():
    """
    Retrieve command-line arguments and process them
    """
    input_file = ""
    output_file = ""
    should_decode = True # Default to decoding subpixels
    is_grayscale = True  # Default to grayscale output

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

    # Process command-line arguments
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

def get_luminosity_value(pixel: list[int]) -> int:
    """
    Calculate the luminosity value of a pixel (using the standard formula)
    """
    if len(pixel) != 3:
        raise ValueError("Pixel must be a list of exactly three integers.")

    r, g, b = pixel[0], pixel[1], pixel[2]
    return ((0.2126 * r) + (0.7152 * g) + (0.0722 * b)) # Luminosity formula    

def decode_subpixels(input_file: str, output_file: str, is_grayscale: bool):
    """
    Decode subpixel data
    """
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

def encode_pixels(input_file: str, output_file: str):
    """
    Encode pixels by averaging their luminosity into a single pixel
    """
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

def main():
    """
    Program entry point
    """
    input_file, output_file, should_decode, is_grayscale  = retrieve_args()

    # Transfrom (sub)pixels
    if should_decode:
        decode_subpixels(input_file, output_file, is_grayscale)
    else:
        encode_pixels(input_file, output_file)

if __name__ == "__main__":
    main()