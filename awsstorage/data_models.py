class AwsFileToUpload(object):

    def __init__(self, stream, name, size):
        self.stream = stream
        self.name = name
        self.size = size

    def chunks(self):
        return self.stream
