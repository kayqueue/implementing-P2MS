# other files
from read_files import read_scriptPubKey, read_scriptSig, which_file, read_tup_list
from stack_visualisation import push_to_stack, verify

# imports
from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
import binascii

# main()
def main():
	option = which_file()
	
	# message
	message = b"Contemporary topic in security"
	
	# read scriptPubKey.txt and scriptSig.txt
	scriptPubKey_contents = read_scriptPubKey(option)
	scriptSig_contents = read_scriptSig(option)
	
	# tup_list
	tup_list = read_tup_list()
	
	# execute P2MS script with additional stack information
	scriptPubKey, scriptSig, stack = push_to_stack(scriptSig_contents, scriptPubKey_contents)
	
	# once all pubkeys and signatures are popped, verify the signatures against the pubkeys
	stack = verify(scriptSig, scriptPubKey, tup_list[option -1], message, stack)

	# Evaluate the result of the verification
	if stack[0] == True:
		print("Signature verification is successful!")
	else:
		print("Signature verification is unsuccessful...")
	

# driver of the program
if __name__ == "__main__":
	main()
