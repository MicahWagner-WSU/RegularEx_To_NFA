import sys
input_file = open(sys.argv[1], 'r')


Lines = input_file.readlines()
 
count = 0
# Strips the newline character
for line in Lines:
    print(line.strip())