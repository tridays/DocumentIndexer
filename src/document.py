__author__ = 'xp'


class Document(object):
    def __init__(self, number: str, title: str, body: str):
        self.number = number
        self.title = title
        self.body = body
        self.token_nums = 0  # type: int
        self.term_nums = 0  # type: int
