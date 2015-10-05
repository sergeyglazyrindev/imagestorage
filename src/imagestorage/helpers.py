def size_string_to_tuple(size_string):
    size = list(filter(None, size_string.split('x')))
    if len(size) == 1:
        return int(size[0]), None
    return int(size[0]), int(size[1])
