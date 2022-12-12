import random

def makeTokenSymbols(amount):
    # 0: Comments, 1: SET, 2: OUT, 3: STRING, 4: ... - ETC
    result = []
    for t in range(amount+1):
        rnd = random.choice([
            random.randint(33, 47),
            random.randint(58, 64),
            random.randint(91, 96),
            random.randint(123, 126)
        ])
        while chr(rnd) in result:
            rnd = random.choice([
                random.randint(33, 47),
                random.randint(58, 64),
                random.randint(91, 96),
                random.randint(123, 126)
            ])
        result.append(chr(rnd))
    return result