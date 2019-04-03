
class DataFeeder(object):
    def __init__(self, valid_prop=0.1):
        self._buffer = []

    def add(self):
        pass

    def get_batch(self, mode='TRAIN'):