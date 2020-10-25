class Token:
    def __init__(self, token_class="", lexeme="", line=0, token_id=0):
        self.token_class = token_class
        self.lexeme = lexeme
        self.line = line
        self.token_id = token_id
