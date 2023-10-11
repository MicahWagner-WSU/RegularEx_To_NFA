import sys

stack = []

class NFA:
	def __init__(self, start, accept, transition):
		self.start = start
		self.accept = accept
		self.transition = transition

	@staticmethod
	def concat_NFAs(NFA1, NFA2, count):
		new_start = NFA1.start
		new_accept = NFA2.accept
		new_transition = NFA1.transition
		new_transition.append('('+ str(NFA1.accept) + ', E) -> ' + str(NFA2.start))
		new_transition.extend(NFA2.transition)
		new_NFA = NFA(new_start, new_accept, new_transition)
		return new_NFA

	@staticmethod
	def union_NFAs(NFA1, NFA2, count):
		count += 1
		new_start = 'q' + str(count)
		count += 1
		new_accept = 'q' + str(count)
		new_transition = NFA1.transition
		new_transition.append('('+ str(NFA1.accept) + ', E) -> ' + str(new_accept))
		new_transition.extend(NFA2.transition)
		new_transition.append('('+ str(NFA2.accept) + ', E) -> ' + str(new_accept))
		new_transition.append('('+ str(new_start) + ', E) -> ' + str(NFA1.start))
		new_transition.append('('+ str(new_start) + ', E) -> ' + str(NFA2.start))

		new_NFA = NFA(new_start, new_accept, new_transition)
		return new_NFA

	@staticmethod
	def kleene_star(NFA1, count):
		count += 1
		new_start = 'q' + str(count)
		new_accept = new_start
		new_transition = NFA1.transition
		new_transition.append('('+ str(NFA1.accept) + ', E) -> ' + str(new_accept))
		new_transition.append('('+ str(new_start) + ', E) -> ' + str(NFA1.start))

		new_NFA = NFA(new_start, new_accept, new_transition)
		return new_NFA

input_file = open(sys.argv[1], 'r')

Lines = input_file.readlines()

for line in Lines:
    count = 0
    for i, v in enumerate(line):
    	if(v != '\n'):
    		if(v == '&'):
    			if(len(stack) < 2):
    				print("ERROR: "+line[:-1]+" not formated in proper postfix notation\n")
    				stack.clear()
    				break
    			NFA2 = stack.pop()
    			NFA1 = stack.pop()
    			stack.append(NFA.concat_NFAs(NFA1, NFA2, count))
    		elif(v == '|'):
    			if(len(stack) < 2):
    				print("ERROR: "+line[:-1]+" not formated in proper postfix notation\n")
    				stack.clear()
    				break
    			NFA2 = stack.pop()
    			NFA1 = stack.pop()
    			stack.append(NFA.union_NFAs(NFA1, NFA2, count))
    			count += 2
    		elif(v == '*'):
    			if(len(stack) < 1):
    				print("ERROR: "+line[:-1]+" not formated in proper postfix notation\n")
    				stack.clear()				
    				break
    			NFA1 = stack.pop()
    			stack.append(NFA.kleene_star(NFA1, count))
    			count += 1
    		else:
    			count += 1
    			first_state = count
    			count += 1
    			second_state = count
    			stack.append(NFA(
    				'q' + str(first_state), 
    				'q' + str(second_state), 
    				['(q'+ str(first_state) +', ' + str(v) + ') -> q' + str(second_state)]
    			))
    	else:
    		break

    if(len(stack) != 1):
    	print("ERROR: "+line[:-1]+" not formated in proper postfix notation\n")
    	stack.clear()
    	continue
    final_NFA = stack.pop()
    print('RE: ' + line[:-1])
    print('Start: ' + final_NFA.start)
    print('Accept: ' + final_NFA.accept)
    for maping in final_NFA.transition:
    	print(maping)
    print('')
