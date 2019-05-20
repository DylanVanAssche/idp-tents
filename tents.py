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

        if parse and ("Kolom" in line) and not ("AantalPerKolom" in line):
            name, data = line.strip().split(" = ")
            data = data.replace("{", "")
            data = data.replace("}", "")
            data = data.replace(" ", "")
            global ROWS, COLUMNS
            ROWS = int(data.split('..')[1])
            COLUMNS = ROWS

        if parse and ("Bomen" in line or "Tenten" in line or "Verbonden" in line):
            name, data = line.strip().split(" = ")
            data = data.replace("{", "")
            data = data.replace("}", "")
            data = data.replace(";", "")
            coordinates = data.strip().split()
            output = []

            for c in coordinates:
                if c:
                    output.append(tuple([int(x) for x in c.split(",")]))

            models[model_count][name] = output

        if parse and ("AantalPerRij" in line or "AantalPerKolom" in line):
            name, data = line.strip().split(" = ")
            data = data.replace("{", "")
            data = data.replace("}", "")
            data = data.replace(";", "")
            amounts = data.strip().split()
            output = []
            for i, a in enumerate(amounts):
                output.append(-1)
                if a:
                    output[i] = int(a.split("->")[1])

            models[model_count][name] = output

        if "structure" in line:
            parse = True
            models.append({})

    return models


def pretty_print(models):
    for i, m in enumerate(models):
        print("Model {}".format(i + 1))
        print("=" * 25, end="\n\n")
        print(" ---" * COLUMNS)
        for r in range(1, ROWS + 1):
            for c in range(1, COLUMNS + 1):
                # Tree
                if (r, c) in m["Bomen"]:
                    print("| B ", end="")

                # Tent
                elif (r, c) in m["Tenten"]:
                    print("| T ", end="")

                # Empty
                else:
                    print("|   ", end="")
            print("|", end="")

            # Amount of tents in a row
            print(" {}".format(m["AantalPerRij"][r - 1]))
            print(" ---" * COLUMNS)

        # Amount of tents in a column
        for c in range(COLUMNS):
            print("  {} ".format(m["AantalPerKolom"][c]), end="")
        print("\n\n")

def validate(models):
    for i, m in enumerate(models):
        ok = True

        # Count tents in row and compare with given
        for r in range(1, ROWS + 1):
            amount_in_row = 0
            for c in range(1, COLUMNS + 1):
                if (r, c) in m["Tenten"]:
                    amount_in_row += 1

            if amount_in_row != m["AantalPerRij"][r - 1]:
                print("\tERROR: {}, invalid amount of tents in row".format((r, c)))
                ok = False

        # Count tents in column and compare with given
        for c in range(1, COLUMNS + 1):
            amount_in_column = 0
            for r in range(1, ROWS + 1):
                if (r, c) in m["Tenten"]:
                    amount_in_column += 1

            if amount_in_column != m["AantalPerKolom"][c - 1]:
                print("\tERROR: {}, invalid amount of tents in column".format((r, c)))
                ok = False

        print("Model {} is valid: {}".format(i, ok))

# Launch
if __name__ == "__main__":
    models = parse()
    pretty_print(models)
    validate(models)
