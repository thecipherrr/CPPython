import lex 

class Number:
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f"{self.token}"


