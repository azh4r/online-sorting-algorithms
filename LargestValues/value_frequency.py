# open the challenge text file.

# read the data into a dict, in_dict

# create another dict

# read the in_dict 
    # for each value in in_dict enter it in frequency_dict if it does not already exist and add 1 to frequency column
        # if it does exist then increment the value in the frequence column 

# write the frequency dict to a file. 

DEFAULT_FILE_LOCATION = '/home/azhar/projects/triad-challenge/triad-challenge/spacemaps_technical_challenge.txt'

def main():
    file_dict = {}
    frequency_dict = {}

    with open(DEFAULT_FILE_LOCATION, 'r') as file_handle:
        file_handle.seek(500)
        for line in file_handle:
            key, val = line.split()
            file_dict[key] = val
    
    for k, v in file_dict.items():
        if not frequency_dict.get(v):
            frequency_dict[v]=1
        else:
            frequency_dict[v] += 1
    
    #sorted_dict = sorted(frequency_dict)
    sorted_dict = dict(sorted(frequency_dict.items(), key = lambda x:int(x[0])))
    #sorted_dict = dict(sorted(file_dict.items(), key = lambda item: item[1], reverse=True))

    with open('frequency_file.txt', 'w') as f:
        for k, v in sorted_dict.items():
            f.write("%s %s\n" % (k,v))


if __name__ == '__main__':
    main()
