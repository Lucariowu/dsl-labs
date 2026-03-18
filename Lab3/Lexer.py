from Token import Token, TokenType, KEYWORDS

class Lexer:
    def __init__(self, source_code: str):
        self.source_code = source_code
        self.position = 0      # Current character reading position
        self.read_position = 0 # Next character reading position
        self.current_char = ''
        
        # Tracking lines and columns for friendly errors
        self.line = 1
        self.column = 0

        self.read_char() # Initialize first char

    def read_char(self):
        """Reads the next character and advances the position pointers."""
        if self.read_position >= len(self.source_code):
            self.current_char = '\0'  # EOF
        else:
            self.current_char = self.source_code[self.read_position]
        
        self.position = self.read_position
        self.read_position += 1
        self.column += 1

    def peek_char(self):
        """Looks at the next character without advancing the pointer."""
        if self.read_position >= len(self.source_code):
            return '\0'
        return self.source_code[self.read_position]

    def skip_whitespace(self):
        """Advances pointer past any spaces, tabs, or newlines."""
        while self.current_char in [' ', '\t', '\n', '\r']:
            if self.current_char == '\n':
                self.line += 1
                self.column = 0
            self.read_char()

    def get_next_token(self) -> Token:
        """Core lexer method. Reads the current char and constructs a Token."""
        self.skip_whitespace()

        tok = None
        current_col = self.column # Capture start column for the token

        if self.current_char == '=':
            if self.peek_char() == '=':
                ch = self.current_char
                self.read_char()
                tok = Token(TokenType.EQUALS, ch + self.current_char, self.line, current_col)
            else:
                tok = Token(TokenType.ASSIGN, self.current_char, self.line, current_col)
        elif self.current_char == '+':
            tok = Token(TokenType.PLUS, self.current_char, self.line, current_col)
        elif self.current_char == '-':
            tok = Token(TokenType.MINUS, self.current_char, self.line, current_col)
        elif self.current_char == '*':
            tok = Token(TokenType.MULTIPLY, self.current_char, self.line, current_col)
        elif self.current_char == '/':
            tok = Token(TokenType.DIVIDE, self.current_char, self.line, current_col)
        elif self.current_char == '(':
            tok = Token(TokenType.LPAREN, self.current_char, self.line, current_col)
        elif self.current_char == ')':
            tok = Token(TokenType.RPAREN, self.current_char, self.line, current_col)
        elif self.current_char == '{':
            tok = Token(TokenType.LBRACE, self.current_char, self.line, current_col)
        elif self.current_char == '}':
            tok = Token(TokenType.RBRACE, self.current_char, self.line, current_col)
        elif self.current_char == ';':
            tok = Token(TokenType.SEMICOLON, self.current_char, self.line, current_col)
        elif self.current_char == ',':
            tok = Token(TokenType.COMMA, self.current_char, self.line, current_col)
        elif self.current_char == '"':
            tok = Token(TokenType.STRING, self.read_string(), self.line, current_col)
            return tok # return early because read_string advances the pointers appropriately
        elif self.current_char == '\0':
            tok = Token(TokenType.EOF, "", self.line, current_col)
        else:
            if self.is_letter(self.current_char):
                literal = self.read_identifier()
                token_type = KEYWORDS.get(literal, TokenType.IDENTIFIER)
                return Token(token_type, literal, self.line, current_col)
            elif self.is_digit(self.current_char):
                return self.read_number(current_col)
            else:
                tok = Token(TokenType.ILLEGAL, self.current_char, self.line, current_col)

        self.read_char()
        return tok

    def read_identifier(self) -> str:
        """Reads a continuously formed identifier or keyword."""
        position = self.position
        while self.is_letter(self.current_char) or self.is_digit(self.current_char):
            self.read_char()
        return self.source_code[position:self.position]

    def read_number(self, start_col: int) -> Token:
        """Reads integers and floats."""
        position = self.position
        is_float = False

        while self.is_digit(self.current_char) or self.current_char == '.':
            if self.current_char == '.':
                if is_float:
                    break # Two dots means illegal or a new token sequence
                is_float = True
            self.read_char()

        value = self.source_code[position:self.position]
        tok_type = TokenType.FLOAT if is_float else TokenType.INTEGER
        return Token(tok_type, value, self.line, start_col)

    def read_string(self) -> str:
        """Reads characters inside quotes `"` until the closing quote."""
        position = self.position + 1
        while True:
            self.read_char()
            if self.current_char == '"' or self.current_char == '\0':
                break
        
        # Capture string value without the quotes
        result = self.source_code[position:self.position]
        if self.current_char == '"':
            self.read_char() # Skip the closing quote
        return result

    @staticmethod
    def is_letter(ch: str) -> bool:
        return ('a' <= ch <= 'z') or ('A' <= ch <= 'Z') or ch == '_'

    @staticmethod
    def is_digit(ch: str) -> bool:
        return '0' <= ch <= '9'

    def tokenize(self):
        """Utility method to tokenize the entire string at once."""
        tokens = []
        while True:
            tok = self.get_next_token()
            tokens.append(tok)
            if tok.type == TokenType.EOF:
                break
        return tokens
