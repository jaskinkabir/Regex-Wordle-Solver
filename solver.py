import re

words = ''
with open(file='words.txt', encoding='utf-8') as f:
    words = f.read()

# 

# ## New Strategy 
# - Baseline pattern after lookahead `^['forbidden_pos blacks]*5$`
#   - Greens should replace the char in the baseline pattern
# - Ensure yellows are seen exactly n times with `(?!'.*y1'*(n1+1))(?!'y2'*(n2+1))...`
#   - Make sure if a yellow is also a green, n for that char is +1
# # Problems

def gen_range_sing(char: str):
    chr_num = ord(char)
    
    if chr_num == 97: #a
        return 'b-z'
    if chr_num == 98: #b
        return 'ac-z'
    if chr_num == 121: #y
        return 'a-xz'
    if chr_num == 122: #z
        return 'a-y'
    
    
    return f'a-{chr(chr_num-1)}{chr(chr_num+1)}-z'


def gen_pattern(
        greens: list[str]=['','','','',''], 
        yellows: dict[str,int]={}, 
        blacks: str = '', 
        forbidden_yellow_pos: list[str]=['','','','','']
    ):           
    
    num_yellow = len(yellows)
    num_green=len(greens)
    num_black = len(blacks)
    
    pattern = ''
    for i in range(5):
        if greens[i] != '':
            pattern += greens[i]
            continue
        cur_block = '[^'
        
        if blacks:
            cur_block += blacks
        
        if forbidden_yellow_pos[i]:
            cur_block += forbidden_yellow_pos[i]
        cur_block += ']'
        pattern += cur_block
    pattern = fr'^{pattern}$'
    
    
    for char, cnt in yellows.items():
        if char in greens: 
            # BIG PROBLEM HERE
            # NEED TO BE ABLE TO RECOGNIZE WHEN A LETTER IS BOTH GREEN AND YELLOW
            # Probably can just work this into the ui
            # Doesn't have to be handled by this function
            # Solution: Just add a letter into yellow and remove it when it becomes green
            cnt += 1
        cur_range = gen_range_sing(char)
        
        # o[a-np-z]*
        # Lookeahead needs to be adjusted to allow for geq cnt
        #   Note: Max amount of duplicate chars in a word is 3
        #   Lol all it took was removing the '$' at the end
        cur_lookahead = fr'(?=^[{cur_range}]*{f"{char}[{cur_range}]*"*cnt})'
        pattern = cur_lookahead + pattern
        
    print(pattern)
    return pattern





def search(pattern, words):
    matches = re.findall(pattern, words,re.MULTILINE)
    if not matches:
        print("Not found")
        return None
    return [''.join(match) for match in matches]
        
# This is for 9/16/24 Wordle, answer was honey
# print(
#     search(
#         gen_pattern(
#             greens=['','','','',''], 
#             yellows = {'o' : 1}, 
#             blacks='audi', 
#             forbidden_yellow_pos=['','','','','o']
#         ),
#         words
#     )
# )

# print(
#     search(
#         gen_pattern(
#             greens=['','o','','e',''], 
#             yellows = {'y': 1}, 
#             blacks='audifr', 
#             forbidden_yellow_pos=['','','y','','o']
#         ),
#         words
#     )
# )

# print(
#     search(
#         gen_pattern(
#             greens=['','o','','e','y'], 
#             yellows = {'o':1, 'y':1}, 
#             blacks='audifrbg', 
#             forbidden_yellow_pos=['','','y','','o']
#         ),
#         words
#     )
# )


# Worked to find toxin
# print(
#     search(
#         gen_pattern(
#             greens=['','','','i',''], 
#             yellows = {'o':1}, 
#             blacks='aud', 
#             forbidden_yellow_pos=['','','','','o']
#         ),
#         words
#     )
# )

# print(
#     search(
#         gen_pattern(
#             greens=['','o','','i',''], 
#             yellows = {'o':1}, 
#             blacks='audbge', 
#             forbidden_yellow_pos=['','','','','o']
#         ),
#         words
#     )
# )

# print(
#     search(
#         gen_pattern(
#             greens=['','o','','i','n'], 
#             yellows = {'o':1}, 
#             blacks='audbgern', 
#             forbidden_yellow_pos=['','','','','o']
#         ),
#         words
#     )
# )

# Worked to find mince
# print(
#     search(
#         gen_pattern(
#             greens=['','','','',''], 
#             yellows = {'e':1}, 
#             blacks='hatr', 
#             forbidden_yellow_pos=['','','','e','']
#         ),
#         words
#     )
# )

# print(
#     search(
#         gen_pattern(
#             greens=['','','','c','e'], 
#             yellows = {'i':1}, 
#             blacks='hatrsp', 
#             forbidden_yellow_pos=['','','i','','']
#         ),
#         words
#     )
# )

# print(
#     search(
#         gen_pattern(
#             greens=['','i','n','c','e'], 
#             yellows = {}, 
#             blacks='hatrspw', 
#             forbidden_yellow_pos=['','','','','']
#         ),
#         words
#     )
# )

# print(
#     search(
#         gen_pattern(
#             greens=['','i','n','c','e'], 
#             yellows = {}, 
#             blacks='hatrspwy', 
#             forbidden_yellow_pos=['','','','','']
#         ),
#         words
#     )
# )


#Found quark correctly
# print(
#     search(
#         gen_pattern(
#             greens=['','','','',''], 
#             yellows = {'a' : 1, 'r' : 1}, 
#             blacks='son', 
#             forbidden_yellow_pos=['','','','a','r']
#         ),
#         words
#     )
# )

# print(
#     search(
#         gen_pattern(
#             greens=['','','','r',''], 
#             yellows = {'a' : 1, 'r' : 1}, 
#             blacks='sonlet', 
#             forbidden_yellow_pos=['a','','','a','r']
#         ),
#         words
#     )
# )

# print(
#     search(
#         gen_pattern(
#             greens=['','','','r',''], 
#             yellows = {'a' : 1, 'r' : 1}, 
#             blacks='sonlet', 
#             forbidden_yellow_pos=['a','','','a','r']
#         ),
#         words
#     )
# )

# print(
#     search(
#         gen_pattern(
#             greens=['','','','r',''], 
#             yellows = {'a' : 1, 'r' : 1}, 
#             blacks='sonletfiy', 
#             forbidden_yellow_pos=['a','a','','a','r']
#         ),
#         words
#     )
# )

# print(
#     search(
#         gen_pattern(
#             greens=['','','a','r',''], 
#             yellows = { 'r' : 1}, 
#             blacks='sonletfiychm', 
#             forbidden_yellow_pos=['a','a','','a','r']
#         ),
#         words
#     )
# )

# Found lemon
# print(
#     search(
#         gen_pattern(
#             greens=['','','','','n'], 
#             yellows = {'l':1, 'e':1}, 
#             blacks='ai', 
#             forbidden_yellow_pos=['','l','','e','']
#         ),
#         words
#     )
# )

# print(
#     search(
#         gen_pattern(
#             greens=['','e','','o','n'], 
#             yellows = {'l':1 }, 
#             blacks='aif', 
#             forbidden_yellow_pos=['','l','l','','']
#         ),
#         words
#     )
# )

print(
    search(
        gen_pattern(
            greens=['','r','e','a',''], 
            yellows = {}, 
            blacks='livcm', 
            forbidden_yellow_pos=['','','','','']
        ),
        words
    )
)

def gen_range_sing(char: str):
    chr_num = ord(char)
    
    if chr_num == 97: #a
        return 'b-z'
    if chr_num == 98: #b
        return 'ac-z'
    if chr_num == 121: #y
        return 'a-xz'
    if chr_num == 122: #z
        return 'a-y'
    
    
    return f'a-{chr(chr_num-1)}{chr(chr_num+1)}-z'


def gen_range(yellows: list[str],blacks: list[str]):
    
    # List of numbers
    # If black is between ranges[i] and ranges[i+1]
        # if black-1 == ranges[i], ranges[i] = black
        # if black +1 == ranges[i+1], ranges[i+1] = black
        # ranges = [ranges[:i], black-1, black+1, ranges[i:] ]
    
    yellows = [ord(char) for char in yellows]
    blacks = [ord(char) for char in blacks]
    yellows.sort()
    blacks.sort()
    
    start = ord('a')
    end = ord('z')
    
    # while start in yellows:
    #     start += 1
    # while end in yellows:
    #     end -= 1

    ranges = [[start, end]]
    
    for black in blacks:
        for i,num_range in enumerate(ranges):
            if not (num_range[0] <= black <= num_range[1]):
                continue
            dist = abs(num_range[0]-black)
            if dist < 2:
                num_range[0] = black+dist+1
                break
            if abs(num_range[1]-black) <2:
                num_range[1] = black
                break
            
            ranges = ranges[:i] + [[num_range[0], black-1], [black+1, num_range[1]]] + ranges[i+1:]
            break
    range_str = ''
    for num_range in ranges:
        dist = num_range[1]-num_range[0]
        if dist == 1:
            range_str+=f'{chr(num_range[0])}{chr(num_range[1])}'
        elif dist == 0:
            range_str += chr(num_range[0])
        else:
            range_str += f'{chr(num_range[0])}-{chr(num_range[1])}'
    
    return ''.join([chr(yellow) for yellow in yellows]) + ' ' + range_str
    



#a-ce-z
# a-ce-fh-z
    

    