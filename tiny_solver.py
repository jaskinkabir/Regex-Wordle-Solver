import re
class TinySolver:
    def __init__(self, word_file='words.txt'): self.words = [line.strip() for line in open(word_file).readlines()]
    def apply(self, pattern, negate=True): self.words = [word for word in self.words if bool(re.match(pattern, word)) != negate]
    def guess(self, guess, colors):
        for i, (c, color) in enumerate(zip(guess, colors), start=1):
            match color:
                case 'b' | 'y': self.apply(f".*{c}.*", negate=color=='b')
                case 'g': self.apply(f"^{'.'*(i-1)}{c}{'.'*(5-i)}$", negate=False)
                case 'y': self.apply(f"^{'.'*(i-1)}{c}{'.'*(5-i)}$", negate=True)