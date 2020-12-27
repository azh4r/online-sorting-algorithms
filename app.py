import sys

# This module should read in the parameters
# or ask for parameters to be entered.
def read_file():
    print("read file")


# read in the file from parameter.

DEFAULT_FILE_LOCATION = '/home/azhar/projects/triad-challenge/triad-challenge/spacemaps_technical_challenge.txt'

def main():
    file_location = ''
    print("hello")
    file_location = sys.argv[1] if len(sys.argv) >=2 else DEFAULT_FILE_LOCATION
    print(file_location)


if __name__ == '__main__':
    main()