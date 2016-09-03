# -*- coding: utf-8 -*-

class Validovat:
    def __init__(self,arrayName):
        self.arrayName = arrayName

    def overeniPole(self):
        try:
            self.arrayName
            return True
        except NameError:
            return False

    def isEmpty(self):
            if Validovat(self.arrayName).overeniPole():
                    if len(self.arrayName) == 0:
                            return True
                    else:
                            return False


