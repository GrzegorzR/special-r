
class CallableNumerical:

    def __init__(self, val):
        self.val = val

    def __call__(self, *args, **kwargs):
        return self.val
