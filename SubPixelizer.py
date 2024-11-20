import os, sys
import imageio.v2 as imageio
import numpy as np


# Constants
CMD_USAGE = "Usage: SubPixelizer.py -i <input_file> -o <output_file> [-2px]"


# TODO: Comment
def is_null_or_whitespace(s: str) -> bool:
    return (s is None or not s.strip())

# TODO: Comment
# TODO: Recomment
def retrieve_args():
    input_file = ""
    output_file = ""
    is_subpixel_conversion = True

    # Print help message
    if (len(sys.argv) == 2):
        if (sys.argv[1] in ["--help", "-h"]):
            help_msg = [
                CMD_USAGE,
                "",
                "Options:",
                "  -i,   --input           Input file (required)",
                "  -o,   --output          Output file (required)",
                "  -2px, --to-pixel        Convert to normal pixel format (optional, default converts to subpixel)",
                "  -h,   --help            Display this help message"
            ]
            print("\n".join(help_msg)) # TODO: implment

            sys.exit(0)

    if (len(sys.argv) >= 5 and len(sys.argv) <= 6):
        # Get arguments
        i = 1
        while (i < len(sys.argv)):
            arg = sys.argv[i]
            i += 1 # Increment count
            known_arg = False

            # Conversion operation
            if (arg.lower() in ["--to-pixel", "-2px"]):
                known_arg = True
                is_subpixel_conversion = False

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

            if (not known_arg):
                print(f"Error: File not found! (\"{input_file}\")")
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
        print("Error: Invalid usage! (Use the '--help' argument if you are stuck)")
        print(CMD_USAGE)
        sys.exit(1)

    return input_file, output_file, is_subpixel_conversion

# TODO: Comment
def convert_to_subpixel(input_file: str, output_file: str):
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
                
                out_img[y, subpixel] = intensity
    
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
def convert_to_pixel(input_file: str, output_file: str):
    pass

# TODO: Comment
def main():
    input_file, output_file, is_subpixel_conversion   = retrieve_args()

    # Transfrom (sub)pixels
    if is_subpixel_conversion:
        convert_to_subpixel(input_file, output_file)
    else:
        convert_to_pixel(input_file, output_file)

if __name__ == "__main__":
    main()