Grade: 98/100

# Goal:
Implement programs creating/executing P2MS script using Pycryptodome package


- Randomly generate 4 pairs of DSA 2048 bits PK/SK under thge same publikc parameters (g, p, q)
- PKs written to scriptPubKey.txt in the following format: OP_2 [PK1] [P2] … [PK4] OP_4 OP_CHECKMULTISIG
- Generate 2 DSA signatures using SKs generated.
- Store signatures in scriptSig.txt in the following format: OP_1 [Sig1] [Sig2]
- Execute P2MS script to verify the signatures


- A report is written to explain the workings of the program