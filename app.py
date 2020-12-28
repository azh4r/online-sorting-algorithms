import sys

# This module should read in the parameters
# or ask for parameters to be entered.
# TODO
def read_file(file_location):
    print("read file")
    file_dict = {}
    with open(file_location, "r") as in_file:
        in_file.seek(500)
        for line in in_file:
            (key, val) = line.split()
            file_dict[key] = int(val)
    in_file.close
    return file_dict


def sort_file(file_dict):
    print("sort file")
    sorted_dict = dict(sorted(file_dict.items(), key = lambda item: item[1], reverse=True))
    return sorted_dict

def write_file(sorted_dict):
    print("write file")
    with open('out_file.txt', 'w') as f:
        for key,value in sorted_dict.items():
            f.write("%s %s\n" % (key,value))


# read in the file name from command line
# parameters must be X, location of file.   (these 2 are required)
# initially I can use local file later on I will change it to remote file. 


DEFAULT_FILE_LOCATION = '/home/azhar/projects/triad-challenge/triad-challenge/spacemaps_technical_challenge.txt'

file_location = ''

def main():
    file_location = sys.argv[1] if len(sys.argv) >=2 else DEFAULT_FILE_LOCATION
    print(file_location)
    file_dict = read_file(file_location)
    sorted_dict = sort_file(file_dict)
    write_file(sorted_dict)


if __name__ == '__main__':
    main()