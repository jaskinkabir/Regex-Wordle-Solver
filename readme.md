# REGEX Wordle Solver
The plan is to use Python to generate a single regex pattern based on your wordle attempts and apply this regex pattern to the word list to find all possible answers

# Ideas for implementation
- Use 1 positive lookaheads for the green characters
    - `(?>.ar..)` means the word has 'ar' as the 2nd and third letters
- Use a character range that excludes the black characters to eliminate words containing them
    - `a-ce-hj-z` to exclude d and i
- Stack negative lookaheads to ensure each yellow character is in the word however many times it must appear
    - Haven't quite figured this one out yet
## New Strategy 
- Baseline pattern after lookahead `^['forbidden_pos blacks]*5$`
  - Greens should replace the char in the baseline pattern
- Ensure yellows are seen exactly n times with `(?!'.*y1'*n1)(?!'y2'*n2)...`
  - Make sure if a yellow is also a green, n for that char is +1
# Problems
- **Problem:** I have no idea how to write regex
   - **Solution:** I am reading and learning
- **Problem:** The range generation function does not work 
    - **Solution**: Idk I'm going to bed
