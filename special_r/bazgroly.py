class ParamFun:

    def __call__(self, *args, **kwargs):
        t = args[0]
        return t


p = ParamFun()
print(p(1))