
out_file = open('output.txt', 'w')
input_file = open('input.txt', 'r')

Lines = input_file.readlines()
 
count = 0
# Strips the newline character
for line in Lines:
    print(line.strip())