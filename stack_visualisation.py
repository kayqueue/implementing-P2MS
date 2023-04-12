from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
import binascii

# Pushing scriptSig and scriptPubKey constants to stack
def push_to_stack(scriptSig, scriptPubKey):
	stack = []

	# Before any processing (empty stack)
	print("----------------------------")
	print("Stack before any processing:")
	print("----------------------------")
	display_stack(stack)
	
	# constants from scriptSig are added to the stack
	for index, value in enumerate(scriptSig):
		if index == 0: # OPCODE
			stack.append(value[3:]) # the value after OP_
		else: # signatures
			stack.append(binascii.unhexlify(value)) # convert back to bytes
	
	#  After adding scriptSig constants
	print("--------------------------------------------------------------------")
	print("Stack contents after adding scriptSig constants:")
	print("!!! Please note that the constants have been converted back to bytes")
	print("--------------------------------------------------------------------")
	display_stack(stack)
	
	# scriptPubKey constants are added to the stack
	for index, value in enumerate(scriptPubKey):
		if index == len(scriptPubKey) - 1: # OP_CHECKMULTISIG opcode
			# After adding scriptPubKey constants
			print("---------------------------------------------------")
			print("Stack contents after adding scriptPubKey constants:")
			print("---------------------------------------------------")
			display_stack(stack)
			
			# OP_CHECKMULTISIG OPCODE reached
			return execute_OP_CHECKMULTISIG(stack)
			break
		
		# Adding scriptPubKey constants
		if value[:3] == "OP_": # OPCODE
			stack.append(value[3:])
		else: # pubkeys
			stack.append(value)

# Execute OP_CHECKMULTISIG
def execute_OP_CHECKMULTISIG(stack):
	# pop the number of public keys
	print("---------------------------------------------------")
	print("Popping the opcode for the number of public keys...")
	print("---------------------------------------------------")
	number_of_pubkey = int(stack.pop())

	# show stack after processing
	display_stack(stack)
	
	# create a list to store the pubkeys
	scriptPubKey = []
	
	# pop the public keys and store them into a list
	print("-------------------------")
	print(f"Popping {number_of_pubkey} public keys...")
	print("-------------------------")
	
	# store pubkeys
	for index in range(number_of_pubkey):
		scriptPubKey = [stack.pop(), *scriptPubKey] # insert as per original order
	
	# show stack after processing
	display_stack(stack)
		
	# pop the number of signatures
	print("--------------------------------------------------")
	print("Popping the opcode for the number of signatures...")
	print("--------------------------------------------------")
	number_of_signatures = int(stack.pop())
	
	# show stack after processing
	display_stack(stack)
	
	# create a list to store the signatures
	scriptSig = []
	
	# pop the signatures and store them into a list
	print("-----------------------")
	print(f"Popping {number_of_signatures} signatures...")
	print("-----------------------")
	
	# store signatures
	for index in range(number_of_signatures):
		scriptSig = [stack.pop(), *scriptSig] # insert as per original order
	
	# show stack after processing
	display_stack(stack)
	
	return scriptPubKey, scriptSig, stack

# verify the signatures
def verify(scriptSig, scriptPubKey, tup, message, stack):
	# list of public keys to verifiy against
	verification_list = []
	
	# construct the public keys for signature verification
	for value in scriptPubKey:
		key_y = int(value, 16) # get the orginal public key format
		tup = [key_y, *tup] # insert to beginning of tup
		verification_list.append(DSA.construct(tup)) # add to verification list
		tup.pop(0) # reset tup
		
	# verify the signatures
	print("----Performing verification process----")
	
	verified = 0 # tracks the number of successful verification
	pubkeys_used = 0 # track the public keys that have been used
	hash_obj = SHA256.new(message)
	
	for i in scriptSig:
		# once 2 signatures are successfully verified, exit
		if verified == 2: 
			break # exit loop
			
		for index in range(pubkeys_used, len(verification_list)):
			verifier = DSS.new(verification_list[index], "fips-186-3")
			try:
				verifier.verify(hash_obj, i)
				verified += 1 # increment number of successful verification
				pubkeys_used += 1 # increment number of pubkeys used
				
				# print statement
				print(f" {verified} signature(s) successfully verified")

				# move on to the next signature
				break
			except ValueError:
				pubkeys_used += 1
				print(" Signature is invalid...")
				
	print("-----Verification process completed----\n")

	stack.pop() # remove the '1' that remains in the stack from OP_1, making it empty
	
	if verified == 2:
		stack.append(True) # indicates that the verification is successful
	else:
		stack.append(False) # indicates that the verification failed
	
	print("------------------------------------------------")
	print("Stack after appending the result of verification")
	print("------------------------------------------------")
	display_stack(stack)

	return stack
	

# displaying the stack
def display_stack(stack):
	print("[ Top of stack ]") # Last-in
	
	# reverse the list to better encapsulate a stack
	for value in reversed(stack):
		print(value)

	print("[ Bottom of stack ]\n") # First-in
