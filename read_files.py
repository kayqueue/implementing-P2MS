# ask user for which file to read
def which_file():
	option = menu()
	while(option < 1 or option > 3):
		option = menu()
		
	if option == 1:
		print("You have selected to read scriptPubKey.txt and scriptSig.txt")
	elif option == 2:
		print("You have selected to read scriptPubKey2.txt and scriptSig2.txt")
	else:
		print("You have selected to read scriptPubKey3.txt and scriptSig3.txt")
	
	return option
   
# file reading options
def menu():
	print("Please select the pair of scriptPubKey and scriptSig files you wish to read in...")
	print("Option 1: scriptPubKey.txt and scriptSig.txt")
	print("Option 2: scriptPubKey2.txt and scriptSig2.txt")
	print("Option 3: scriptPubKey3.txt and scriptSig3.txt")
	print("\n")
	option = int(input("Your choice (enter 1, 2, or 3): "))
	
	return option

# read scriptPubKey.txt
def read_scriptPubKey(option):
	if option == 1:
		filename = "scriptPubKey.txt"
	elif option == 2:
		filename = "scriptPubKey2.txt"
	else:
		filename = "scriptPubKey3.txt"
	
	with open(filename, "r") as fin:
		# store contents in a list, separated by a space
		for line in fin:
			script_pubkey_contents = line.strip().split(" ")
	return script_pubkey_contents

# read scriptSig.txt
def read_scriptSig(option):
	if option == 1:
		filename = "scriptSig.txt"
	elif option == 2:
		filename = "scriptSig2.txt"
	else:
		filename = "scriptSig3.txt"
	with open(filename, "r") as fin:
		# store contents in a list, separated by a space
		for line in fin:
			script_sig_contents = line.strip().split(" ")
	return script_sig_contents

# read tup_list.txt
def read_tup_list():
	tup_list = []
	with open("tup_list.txt", "r") as fin:
		# store contents in a list
		contents = fin.read()
		for lines in contents.strip().split("\n"):
			tup = []
			for values in lines.strip().split(", "):
				tup.append(int(values.strip(",")))
			tup_list.append(tup)
	return tup_list
