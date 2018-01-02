# -*- coding: utf-8 -*-
import csv

def valid_time(h, m):
    try:
        assert 0 <= h and h < 24
        assert 0 <= m and m < 60
    except AssertionError as ex:
        print("invalid: {}:{}".format(h, m))
        raise ex
    

def fixer(s):
    if ":" in s:
        try:
            h, m = s.split(":")
        except ValueError as ex:
            print("{} failed".format(s))
            raise ex
        h = int(h) % 24
        m = int(m)
        valid_time(h, m)
        return h + m / 60.0
    elif s == "xxx":
        return None
    else:
        h = int(s) % 24
        valid_time(h, 0)
        return float(h)
        
    return s

def timediff(h1, h2):
    if h1 > h2:
        return 24 - h1 + h2
    else:
        return h2 - h1

filename = "unepaevik_reaal.csv"
col_nums = [8, 9, 15, 17]
names = set()
dates = set()


with open(filename) as f:
    reader = csv.reader(f)

    is_header = True
    row_num = 1
    for row in reader:
        #print(row_num)
        
        # Drop header row
        if is_header:
            is_header = False
            continue

        # Check for data quality
        names.add(row[1])
        dates.add(row[2])

        # Fix time fields
        result = []
        for c in col_nums:
            result.append(fixer(row[c]))

        if result[0] is None:
            result += [0.0, 0.0, 0.0]
        else:
            result += [timediff(result[1], result[2]), timediff(result[0], result[1]), timediff(result[2], result[3])]
            #print("\t".join(["{}:{}".format(round(x // 1), round((x % 1)*60)) for x in result[0:4]]))
            #print("\t".join(["{}:{}".format(x // 1, (x % 1)*60) for x in result[4:]]))

        # Output nicely formatted times
        print("\t".join(["{:02.0f}:{:02.0f}".format(round(x // 1), round((x % 1)*60.0)) for x in result[:4]]), end="")
        print("\t" + "\t".join(["{}".format(x) for x in result[4:]]))
        
        row_num += 1

# Kontroll, kas kõik nimed ja kuupäevad on õiged
#print(len(names))
#print(len(dates))
#print(sorted(list(names)))
#print(dates)
