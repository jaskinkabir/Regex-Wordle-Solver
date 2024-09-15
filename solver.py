import re

words = ''
with open(file='aesrl.txt', encoding='utf-8') as f:
    words = f.read()


def gen_pattern(greens: str='', yellows: str='', blacks: str = '', forbidden_yellow_pos: dict = {}):           
    
    num_yellow = len(yellows)
    num_green=len(greens)
    num_black = len(blacks)
    
    case_int = int(bool(num_yellow)) <<2 + int(bool(num_green)) <<1 + int(bool(num_black))
    
    accepted_chars_str = fr'([{yellows}])'
    
    # If yellow, accepted chars string must include yellow group and pattern must include non repeat logic
    # If black, accepted chars string must include black group, but this group should not be captured
    
    def gen_accepted_chars(pos=1):
        pos_yellows = yellows
        forbidden_yellows = forbidden_yellow_pos.get(pos)
        if forbidden_yellows is not None:
            pos_yellows = ''.join( re.findall(fr'[^{forbidden_yellows}]',yellows) )
        accepted_chars_str = fr'[]'
        
        
    
    def gen_yellow_refs():
        
        for i in range(1,num_yellow+1):
            yield fr'{accepted_chars_str}(?!' + r''.join([fr'\{i}|' for i in range(1,i+1)])[:-1]+f")"
            
    
    
        
    yellow_generator = gen_yellow_refs()
    # group_str = ''.join([yellow_generator.__next__() for i in range(1,num_yellow+1)])[:-1]
    # pattern = "^" + f"(?!{group_str})([{yellows}])" * (5-num_green)
    pattern = r'^' + r''.join([yellow_generator.__next__() for i in range(num_yellow)])
    print(pattern)
    
    return fr'{pattern}'

def search(pattern, words):
    matches = re.findall(pattern, words,re.MULTILINE)
    if not matches:
        print("false")
        return None
    return [''.join(match) for match in matches]
        
    
#print(search(r'^([aesrl])(?!\1)([aesrl])(?!\1|\2)([aesrl])(?!\1|\2|\3)([aesrl])(?!\1|\2|\3|\4)([aesrl])', words))


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
    

print(gen_range(yellows=['a','b','w','z'],blacks=['d','g','h','j','x'])) # EXCLUDES I

#a-ce-z
# a-ce-fh-z
    

    