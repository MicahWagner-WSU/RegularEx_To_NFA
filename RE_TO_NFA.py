import sys

stack = []

class NFA:
	def __init__(self, start, accept, transition):
		self.start = start
		self.accept = accept
		self.transition = transition

	@staticmethod
	def concat_NFAs(NFA1, NFA2):
		pass

	@staticmethod
	def union_NFAs(NFA1, NFA2):
		pass

	@staticmethod
	def kleene_star(NFA1):
		pass

input_file = open(sys.argv[1], 'r')
alphabet = ['a', 'b', 'c', 'd', 'e']
operations = ['|', '&', '*']

Lines = input_file.readlines()
 
count = 0

for line in Lines:
    for i, v in enumerate(line):
    	if(v != '\n'):
    		if(v == '&'):
    			NFA2 = stack.pop()
    			NFA1 = stack.pop()
    			stack.append(NFA.concat_NFAs(NFA1, NFA2))
    		elif(v == '|'):
    			NFA2 = stack.pop()
    			NFA1 = stack.pop()
    			stack.append(NFA.union_NFAs(NFA1, NFA2))
    		elif(v == '*'):
    			NFA1 = stack.pop()
    			stack.append(NFA.kleene_star(NFA1))
    		else:
    			stack.append(NFA('q' + str(1), 'q' + str(2), ['(q1,' + str(v) + ')->q2']))
    	else:
    		break
    print('\n')
