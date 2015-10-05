def size_string_to_tuple(size_string):
    size = list(filter(None, size_string.split('x')))
    return int(size[0]), int(size[1])
