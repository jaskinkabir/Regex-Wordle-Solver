import re

class Solver:
    
    def __init__(
        self,
        words = '',
        word_file = 'words.txt',
        greens: list[str]=['','','','',''], 
        yellows: dict[str,int]={}, 
        blacks: str = '', 
        forbidden_yellow_pos: list[str]=['','','','','']
    ):
        

        self.greens = greens
        self.yellows = yellows
        self.blacks = blacks
        self.forbidden_yellow_pos = forbidden_yellow_pos
        self.solutions: list[str] = []
        self.words = words
        with open(file=word_file) as f:
            self.words += f.read()
    
    def gen_pattern(self):  
        
        pattern = ''
        for i in range(5):
            if self.greens[i] != '':
                pattern += self.greens[i]
                continue
            cur_block = '[^'
            
            if self.blacks:
                cur_block += self.blacks
            
            if self.forbidden_yellow_pos[i]:
                cur_block += self.forbidden_yellow_pos[i]
            cur_block += ']'
            pattern += cur_block
        pattern = fr'^{pattern}$'
        
        for char, cnt in self.yellows.items():
            if cnt == 0:
                continue
            if char in self.greens and self.greens.count(char) == cnt:
                continue
            
            cur_lookahead = rf'(?=[a-z]*{rf"{char}[a-z]*"*cnt})'
            pattern = cur_lookahead + pattern
            
        self.pattern = pattern
        return pattern
    
    def search(self, pattern):
        matches = re.findall(pattern, self.words, re.MULTILINE)
        if not matches:
            print("Not found")
            return None
        return [''.join(match) for match in matches]
    
    def guess(self, guess: str, colors: str):
            self.yellows = {}
            if len(guess) != 5 or len(colors) != 5:
                raise ValueError("Guess and colors must be len 5")
            # Yellow dict will be reset upon each guess
            for i, (char, color) in enumerate(zip(guess, colors)):
                match(color):
                    case'b':
                        self.blacks += char
                        continue
                    case'g':
                        self.greens[i] = char
                        self.yellows[char] = self.yellows.get(char,0) + 1
                        continue
                    case 'y':
                        self.forbidden_yellow_pos[i] += char
                        self.yellows[char] = self.yellows.get(char,0) + 1

            self.solutions = self.search(self.gen_pattern())
    def get_solutions(self):
        return self.solutions