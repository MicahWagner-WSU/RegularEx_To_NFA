import sys

stack = []
isValid = True

# NFA class containing all the attributes an NFA would have
# includes the start state, accept state, and set of transitions
# Dont include set of states since this is implied through the transition function
class NFA:

	# constructor for class
	def __init__(self, start, accept, transition):
		self.start = start
		self.accept = accept
		self.transition = transition

	# static method to concatinate NFA1 to NFA2
	# count will be used to label the new states
	@staticmethod
	def concat_NFAs(NFA1, NFA2, count):
		# set new start state to NFA1 start state
		# set new accept state the NFA2 accept state
		new_start = NFA1.start
		new_accept = NFA2.accept
		new_transition = NFA1.transition

		# adjust transition function such that NFA1 accept state as an epsilon transition to NFA2 start state
		new_transition.append('('+ str(NFA1.accept) + ', E) -> ' + str(NFA2.start))
		new_transition.extend(NFA2.transition)

		# return new NFA that recognizes L(NFA1).L(NFA2)
		new_NFA = NFA(new_start, new_accept, new_transition)
		return new_NFA

	# static method to union NFA1 with NFA2
	# count will be used to label the new states
	@staticmethod
	def union_NFAs(NFA1, NFA2, count):
		# create new start and accept states using count
		count += 1
		new_start = 'q' + str(count)
		count += 1
		new_accept = 'q' + str(count)

		# add transitions such that all accept states from NFA1 and NFA2 go to the new accept state
		# add transitions such that the new start state espilon transitions to the start states of NFA1 and NFA2
		new_transition = NFA1.transition
		new_transition.append('('+ str(NFA1.accept) + ', E) -> ' + str(new_accept))
		new_transition.extend(NFA2.transition)
		new_transition.append('('+ str(NFA2.accept) + ', E) -> ' + str(new_accept))
		new_transition.append('('+ str(new_start) + ', E) -> ' + str(NFA1.start))
		new_transition.append('('+ str(new_start) + ', E) -> ' + str(NFA2.start))

		# return new NFA that recognizes L(NFA1) | L(NFA2)
		new_NFA = NFA(new_start, new_accept, new_transition)
		return new_NFA

	# static method to perform the kleene star operation on NFA1
	# count is used to correctly label the new states
	@staticmethod
	def kleene_star(NFA1, count):
		# create a new state with count and make it the new start and accept 
		count += 1
		new_start = 'q' + str(count)
		new_accept = new_start
		new_transition = NFA1.transition

		# add an epsilon transition from the new start state to old start state
		# add an epsilon transition from the old accept state to the new accept state
		new_transition.append('('+ str(NFA1.accept) + ', E) -> ' + str(new_accept))
		new_transition.append('('+ str(new_start) + ', E) -> ' + str(NFA1.start))

		# return new NFA that recognizes L(NFA1*) 
		new_NFA = NFA(new_start, new_accept, new_transition)
		return new_NFA


input_file = open(sys.argv[1], 'r')

Lines = input_file.readlines()

# read line at a time from file in argv[1]
for line in Lines:
	# reset count for each NFA
    count = 0
    # itterate over each character in the line
    for i, v in enumerate(line):
    	# we dont read new line, coninute checking this character
    	if(v != '\n'):

    		# if we are the concat symbol, concat the two NFAs that are on the stack
    		if(v == '&'):
    			# if stack is less than two, the regex is not in postix form, skip to next line
    			if(len(stack) < 2):
    				print("ERROR: "+line[:-1]+" not formated in proper postfix notation\n")
    				isValid = False
    				stack.clear()
    				break
    			NFA2 = stack.pop()
    			NFA1 = stack.pop()
    			stack.append(NFA.concat_NFAs(NFA1, NFA2, count))
    		# if we are the union symbol, union the two NFAs that are on the stack
    		elif(v == '|'):
    			# if stack is less than two, the regex is not in postix form, skip to next line
    			if(len(stack) < 2):
    				print("ERROR: "+line[:-1]+" not formated in proper postfix notation\n")
    				isValid = False
    				stack.clear()
    				break
    			NFA2 = stack.pop()
    			NFA1 = stack.pop()
    			stack.append(NFA.union_NFAs(NFA1, NFA2, count))
    			# union operation adds two states, so adjust the global count accordingly
    			count += 2

    		# if we read the kleene star symbol, perform the kleene star operation on the NFA in the stack  
    		elif(v == '*'):
    			# if stack is less than one, the regex is not in postix form, skip to next line
    			if(len(stack) < 1):
    				print("ERROR: "+line[:-1]+" not formated in proper postfix notation\n")
    				isValid = False
    				stack.clear()				
    				break
    			NFA1 = stack.pop()
    			stack.append(NFA.kleene_star(NFA1, count))
    			# kleene start operation adds one state, adjust global count accordingly
    			count += 1
    		else:

    			# we reached a character, push an NFA that accepts this single character
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
    		# reached new line, print final regex and read next regex
    		break

    # if isvalid is false, we already hit an error, continue to next line
    if(isValid == False):
    	isValid = True
    	stack.clear()
    	continue

    # if the final stack doesn't have one NFA, regex is not in proper postfix form
    if(len(stack) != 1):
    	print("ERROR: "+line[:-1]+" not formated in proper postfix notation\n")
    	stack.clear()
    	continue

    # pop final NFA, print contents, and continue to next NFA
    final_NFA = stack.pop()
    print('RE: ' + line[:-1])
    print('Start: ' + final_NFA.start)
    print('Accept: ' + final_NFA.accept)
    for maping in final_NFA.transition:
    	print(maping)
    print('')
