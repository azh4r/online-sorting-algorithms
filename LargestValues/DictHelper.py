
# Function to convert a line iterable into a dict
def dict_lines(lines):
    dict_segment = {}
    for line in lines:
        key, val = line.split()
        dict_segment[key] = int(val)
    return dict_segment


# Function will sort a dict object to return a sorted dict
def sort_dict(file_dict):
    # print("sort dict")
    sorted_dict = dict(sorted(file_dict.items(), key = lambda item: item[1], reverse=True))
    return sorted_dict
