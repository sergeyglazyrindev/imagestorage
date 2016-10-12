class AwsFileToUpload(object):

    def __init__(self, stream, name, size):
        self.stream = stream
        self.name = name
        self.size = size

    def read(self):
        return self.stream.read()

    def get_file(self):
        return self.stream
