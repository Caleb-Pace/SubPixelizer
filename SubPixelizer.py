import os, sys


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

    print("Arguments passed:", sys.argv) # DEBUG

    # Print help message
    if (len(sys.argv) == 2):
        if (sys.argv[1] in ["--help", "-h"]):
            help_msg = [
                CMD_USAGE,
                "",
                "Options:",
                "  -i, --input            Input file (required)",
                "  -o, --output           Output file (required)",
                "  -2px                    Convert to normal pixel format (optional, default is subpixel)",
                "  --help                  Display this help message"
            ]
            print("\n".join(help_msg)) # TODO: implment

            sys.exit(0)

    if (len(sys.argv) >= 5 and len(sys.argv) <= 6):
        # Get arguments
        i = 1
        while (i < len(sys.argv)):
            arg = sys.argv[i]
            print(f"Argument {i}: {arg}") # DEBUG
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
        print("Error: Invalid usage!")
        print(CMD_USAGE)
        sys.exit(1)

    return input_file, output_file, is_subpixel_conversion

# TODO: Comment
def main():
    input_file, output_file, is_subpixel_conversion   = retrieve_args()

    print(f"In file: \"{input_file}\"")
    print(f"Out file: \"{output_file}\"")
    print(f"Converting to \"{'sub-pixel' if is_subpixel_conversion else 'standard-pixel'}\"")

if __name__ == "__main__":
    main()