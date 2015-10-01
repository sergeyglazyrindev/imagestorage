def size_string_to_tuple(size_string):
    size = size_string.split('x')
    if len(size) == 1:
        return size[0], None
    return size[0], size[1]
