#!/usr/bin/python3
import sys

# Pipe the input file into this script
ROWS = 5
COLUMNS = 5

def parse():
    models = []
    parse = False
    model_count = 0
    for line in sys.stdin:
        if "}" == line.rstrip():
            parse = False
            model_count += 1
            
        if parse and ("Bomen" in line or "Tenten" in line or "Verbonden" in line):
            print(line)
            name, data = line.strip().split(" = ")
            data = data.replace("{", "")
            data = data.replace("}", "")
            data = data.replace(";", "")
            coordinates = data.strip().split(" ")
            appel = []
            for c in coordinates:
                if c:
                    appel.append(tuple([int(x) for x in c.split(",")]))
            
            print("{}: {}".format(name, data))
            print(appel)
            models[model_count][name] = appel
    
        if "structure" in line:
            parse = True
            models.append({})
            
    return models


def pretty_print(models):
    for i, m in enumerate(models):
        print("Model {}".format(i + 1))
        print("=" * 25)
        print("")
        print(" ---" * COLUMNS)
        for r in range(1, ROWS + 1):
            
            for c in range(1, COLUMNS + 1):
                if (r, c) in m["Bomen"]:
                    #print("Boompie: {}".format((r, c)))
                    print("| B ", end="")
                    
                elif (r, c) in m["Tenten"]:
                    #print("Tenties: {}".format((r, c)))
                    print("| T ", end="")
                    
                else:
                    #print("NIKSKE")
                    print("|   ", end="")
            print("|")
            print(" ---" * COLUMNS)
                    
                
        

if __name__ == "__main__":
    models = parse()
    pretty_print(models)
