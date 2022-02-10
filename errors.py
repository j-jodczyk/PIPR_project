class SynonymError(Exception):
    def __init__(self):
        messege = 'Unable to find synonym to any word in given sentence.'
        super().__init__(messege)


class RhymeNotFoudError(Exception):
    pass
