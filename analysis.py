from bitcoinrpc.authproxy import AuthServiceProxy

# RPC connection details
rpc_user = "hyperledgerz4040"
rpc_password = "BitcoinTransactionAssignment2"
rpc_port = 18443
wallet_name = "testwallet"

# Connect to wallet RPC
rpc = AuthServiceProxy(
    f"http://{rpc_user}:{rpc_password}@127.0.0.1:{rpc_port}/wallet/{wallet_name}"
)

print("Connected to Bitcoin Core RPC")

# Get TXIDs from user (from Part 1 and Part 2 outputs)
legacy_txid = input("\nEnter TXID of Legacy P2PKH transaction (from Part 1): ").strip()
segwit_txid = input("Enter TXID of SegWit transaction (from Part 2): ").strip()

# Fetch transaction details
legacy_tx = rpc.getrawtransaction(legacy_txid, True)
segwit_tx = rpc.getrawtransaction(segwit_txid, True)

# -------------------------------
# LEGACY TRANSACTION ANALYSIS
# -------------------------------

print("\n==============================")
print("Legacy P2PKH Transaction")
print("==============================")

print("TXID:", legacy_tx["txid"])
print("Size:", legacy_tx["size"], "bytes")
print("Virtual Size:", legacy_tx["vsize"], "vbytes")
print("Weight:", legacy_tx["weight"])

print("\n--- ScriptSig (Unlocking Script) ---")
for vin in legacy_tx["vin"]:
    if "scriptSig" in vin:
        print(vin["scriptSig"]["asm"])

print("\n--- ScriptPubKey (Locking Script) ---")
for vout in legacy_tx["vout"]:
    print(vout["scriptPubKey"]["asm"])


# -------------------------------
# SEGWIT TRANSACTION ANALYSIS
# -------------------------------

print("\n==============================")
print("P2SH-P2WPKH SegWit Transaction")
print("==============================")

print("TXID:", segwit_tx["txid"])
print("Size:", segwit_tx["size"], "bytes")
print("Virtual Size:", segwit_tx["vsize"], "vbytes")
print("Weight:", segwit_tx["weight"])

print("\n--- scriptSig ---")
for vin in segwit_tx["vin"]:
    if "scriptSig" in vin:
        print(vin["scriptSig"]["asm"])

print("\n--- Witness Data ---")
for vin in segwit_tx["vin"]:
    if "txinwitness" in vin:
        for item in vin["txinwitness"]:
            print(item)

print("\n--- ScriptPubKey ---")
for vout in segwit_tx["vout"]:
    print(vout["scriptPubKey"]["asm"])


# -------------------------------
# SIZE COMPARISON
# -------------------------------

print("\n==============================")
print("Transaction Size Comparison")
print("==============================")

print(f"P2PKH Transaction Size: {legacy_tx['size']} bytes")
print(f"SegWit Transaction Size: {segwit_tx['size']} bytes")

print(f"P2PKH Virtual Size: {legacy_tx['vsize']} vbytes")
print(f"SegWit Virtual Size: {segwit_tx['vsize']} vbytes")

print(f"P2PKH Weight: {legacy_tx['weight']}")
print(f"SegWit Weight: {segwit_tx['weight']}")

print("\n------------------------------")

if segwit_tx["vsize"] < legacy_tx["vsize"]:
    print("Result: SegWit transaction is smaller in virtual size.")
else:
    print("Result: Legacy transaction is larger.")

print("\nSegWit separates signature data into the witness field.")
print("Witness data counts less toward block weight, reducing transaction size and fees.")
