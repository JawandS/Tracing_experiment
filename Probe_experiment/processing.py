def read_file(file):
    # add file lines to list
    lines = []
    with open(file, 'r') as f:
        for line in f:
            if ln := line.strip():
                lines.append(round(float(ln), 3))
    diffs = []
    for counter in range(0, len(lines), 2):
        diffs.append(float(lines[counter + 1]) - float(lines[counter]))
    return round(sum(diffs) / len(diffs), 3), round(min(diffs), 3), round(max(diffs), 3)


if __name__ == "__main__":
    # get the run number
    import sys

    args = sys.argv
    if len(args) > 1:
        run = args[1]
    else:
        run = '1'
    # read file
    lines = read_file("Logs/run" + run + ".txt")
    # process data
    avg, smallest, largest = read_file(lines)
    # write results to file
    with open("Results/result" + run + ".txt", 'w') as f:
        f.write("average, min, max\n")
        f.write("Average: " + str(avg) + "\n")
        f.write("Min: " + str(smallest) + "\n")
        f.write("Max: " + str(largest) + "\n")
