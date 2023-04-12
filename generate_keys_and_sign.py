from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
import binascii

# generate 3x 4 pairs of DSA keys using same public parameters
# and write to scriptPubKey.txt --> generate 3 text files
def generate_DSA_keys():	
	private_keys_list = []
	tup_list = []
	
	for i in range(3):
		key = DSA.generate(2048)
		key_pem = key.public_key().export_key()
		filename = "scriptPubKey"
		if i != 0:
			filename = f"{filename}{i + 1}.txt"
		else:
			filename = f"{filename}.txt"
			
		# write to scriptPubKey.txt
		with open(filename, "w") as fout:
			fout.write("OP_2 ")

		# list of private keys generated
		private_keys = []
		
		key = DSA.import_key(key_pem)
		param = [key.p, key.q, key.g] # parameter
		tup = [key.g, key.p, key.q] # for verification use
		
		fout = open(filename, "a") # append to file
		
		for i in range(4): # 4 pairs
			temp = DSA.generate(2048, domain = param) # using same public parameters
			private_keys.append(temp)
			hex_public_key = hex(temp.y) # public key in hexadecimal notation

			fout.write(hex_public_key)
			fout.write(" ") # spacing
		
		fout.write("OP_4 OP_CHECKMULTISIG")
		fout.close() # close file
		
		private_keys_list.append(private_keys)
		tup_list.append(tup)
	

	# write tup to a file
	filename_tup = "tup_list.txt"
	with open(filename_tup, "w") as ftup:
		for i in range(len(tup_list)):
			for j in range(len(tup_list[i])):
				ftup.write(str(tup_list[i][j]))
				ftup.write(", ")
			ftup.write("\n")	
			
	return private_keys_list
	
# generates 3x 2 DSA signatures and write to scriptSig.txt --> generate 3 text files
def sign(message, private_keys_list):
	for i in range(3):
		private_keys = private_keys_list[i]
		filename = "scriptSig"
		if i != 0:
			filename = f"{filename}{i + 1}.txt"
		else:
			filename = f"{filename}.txt"
			
		# writing to scriptSig.txt
		fout = open(filename, "w")
		fout.write("OP_1 ")
		fout.close()

		fout = open(filename, "ab") # append to file
		
		# Sign message
		for j in range(2):
			hash_obj = SHA256.new(message)
			signer = DSS.new(private_keys[j], 'fips-186-3')
			signature = signer.sign(hash_obj)

			fout.write(binascii.hexlify(signature)) # write in hexadecimal notation
			fout.write(b" ") # spacing
		
		fout.close()


# GENERATE KEYS
private_keys_list = generate_DSA_keys()

# SIGN
message = b"Contemporary topic in security"
sign(message, private_keys_list)
