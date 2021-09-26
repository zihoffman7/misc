#####################
## Zachary Hoffman
## Hamlet Lines

# Holds all file lines
fileLines = []
# Times each character speaks
times = {}
# Line count
lines = {}

# Reads txt file and captures lines
with open("hamlet.txt") as file:
    for i in file:
        fileLines.append(i.replace('\n', ''))

# Holds speaking character and for how long
detect = ['', 0]

# Iterates through each line
for line in fileLines:
    # Skips spaces
    if not line == '':
        # Checks if line contains two actors
        count = []
        for i in actors:
            if i in line:
                count.append(i)
        # If more than one actor, add instance to times spoken and total lines
        if len(count) > 1:
            for i in count:
                try:
                    lines[i] += 1
                except:
                    lines[i] = 1
                try:
                    times[i] += 1
                except:
                    times[i] = 1
            continue
        # If line is a name
        if line.upper() in fileLines:
            line = line.upper()
            # Notice the instance
            if line.upper() in lines:
                times[line.upper()] += 1
            else:
                times[line.upper()] = 1
            # Get old speak character
            old = detect[0]
            # Set new speak character
            detect[0] = line
            # Detect if old speak is different from new
            if not old == detect[0]:
                # Save old speaker data to lines
                try:
                    lines[old] += detect[1]
                except:
                    lines[old] = detect[1]
                # Reset line count for new character
                detect[1] = 0
                continue
        # Adds 1 to line count if the line isn't a stage instruction
        check = True
        for i in actors:
            if not line.find(i) == -1:
                check = False
        if check == True:
            detect[1] += 1
    try:
        lines.pop('')
    except:
        pass
    # Sort actor list by lines
    actors = sorted(lines, key=lines.get, reverse=True)

# Remove acts
for i in lines:
    if not i.find("ACT") == -1:
        actors.remove(i)

# Shows data
print("--------------------")
for actor in actors:
    print(actor + " - Times spoken:", times[actor], "Lines read:", lines[actor])
print("--------------------")
