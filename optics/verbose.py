"""
辅助调试用
"""
class Verbose:
    def __init__(self, verbose):
        self.set_printer(verbose)

    def set_printer(self, verbose):
        if verbose:
            self.printer = print
        else:
            self.printer = lambda x: None