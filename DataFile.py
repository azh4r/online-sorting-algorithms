# Class with functions to get handle to a file and
# to read in a file.
# Update: This should also take in number of lines to read
# and return also that file has ended. 
class DataFile:
    
    def get_handle(file_location):
        in_file = open(file_location, "r")
        return in_file
    
    # method to convert a segment of txt file into dict 
    # returning the segment in dict and the position in the file
    # and whether it reached the end of file or not. 
    def read_file(file_handle, lines_to_read, offset):
        end_of_file = False
        file_dict = {}
        count = 0
        file_handle.seek(offset)
        while count < lines_to_read and not end_of_file: 
            line = file_handle.readline().strip()
            if line == '':
                end_of_file = True
                break
            (key, val) = line.split()
            file_dict[key] = int(val)
            count +=1

        offset = file_handle.tell()
        if end_of_file:
            file_handle.close()
        return (file_dict, offset, end_of_file)
