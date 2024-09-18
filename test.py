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
    
    def gen_yellow_range(self,yellow_char: str):
        chr_num = ord(yellow_char)
        
        if chr_num == 97: #a
            return 'b-z'
        if chr_num == 98: #b
            return 'ac-z'
        if chr_num == 121: #y
            return 'a-xz'
        if chr_num == 122: #z
            return 'a-y'
        
        
        return f'a-{chr(chr_num-1)}{chr(chr_num+1)}-z'
    
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

            cur_range = self.gen_yellow_range(char)
            
            # o[a-np-z]*
            # Lookeahead needs to be adjusted to allow for geq cnt
            #   Note: Max amount of duplicate chars in a word is 3
            #   Lol all it took was removing the '$' at the end
            cur_lookahead = fr'(?=^[{cur_range}]*{f"{char}[{cur_range}]*"*cnt})'
            pattern = cur_lookahead + pattern
            
        print(pattern)
        return pattern
    
    def search(self, pattern):
        matches = re.findall(pattern, self.words, re.MULTILINE)
        if not matches:
            print("Not found")
            return None
        return [''.join(match) for match in matches]
    
    def add_guess(self, guess: str, colors: str):
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
    
    
solver = Solver(word_file='words.txt')


inp = ''
colors = ''
while True:

    while True:
        inp = input("Input Guess: ")
        if re.match(r'^[a-z]{5}$', inp) is not None:
            break
        if inp == '0':
            break
        print("Invalid guess. Must be 5 lowercase letters")
    guess = inp
    while True:
        inp = input("Input Guess: ")
        if re.match(r'^[gby]{5}$', inp) is not None:
            break
        if inp == '0':
            break
        print("Invalid guess. Must be 5 instances of [bgy]")
    solver.add_guess(guess, inp)
    print(solver.get_solutions())