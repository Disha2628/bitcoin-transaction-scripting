from bitcoinrpc.authproxy import AuthServiceProxy

# RPC connection
rpc_user = "hyperledgerz4040"
rpc_password = "BitcoinTransactionAssignment2"
rpc_port = 18443
wallet_name = "testwallet"

# Connect to wallet RPC
rpc = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:{rpc_port}/wallet/{wallet_name}")

print("Connected to Bitcoin Core RPC\n")

# Input TXIDs from previous parts
legacy_txid = input("Enter TXID of Legacy P2PKH transaction (Part 1): ").strip()
segwit_txid = input("Enter TXID of SegWit transaction (Part 2): ").strip()

# Fetch transactions
legacy_tx = rpc.getrawtransaction(legacy_txid, True)
segwit_tx = rpc.getrawtransaction(segwit_txid, True)

print("\n====================================")
print("LEGACY P2PKH TRANSACTION ANALYSIS")
print("====================================")

print("TXID:", legacy_tx["txid"])
print("Size (bytes):", legacy_tx["size"])
print("Virtual Size (vbytes):", legacy_tx["vsize"])
print("Weight:", legacy_tx["weight"])

print("\n--- Unlocking Script (scriptSig) ---")
for vin in legacy_tx["vin"]:
    if "scriptSig" in vin and vin["scriptSig"]:
        print(vin["scriptSig"]["asm"])

print("\n--- Locking Script (scriptPubKey) ---")
for vout in legacy_tx["vout"]:
    print(vout["scriptPubKey"]["asm"])


print("\n\n====================================")
print("P2SH-P2WPKH SEGWIT TRANSACTION ANALYSIS")
print("====================================")

print("TXID:", segwit_tx["txid"])
print("Size (bytes):", segwit_tx["size"])
print("Virtual Size (vbytes):", segwit_tx["vsize"])
print("Weight:", segwit_tx["weight"])

print("\n--- scriptSig ---")
for vin in segwit_tx["vin"]:
    if "scriptSig" in vin and vin["scriptSig"]:
        print(vin["scriptSig"]["asm"])

print("\n--- Witness Data ---")
for vin in segwit_tx["vin"]:
    if "txinwitness" in vin:
        for w in vin["txinwitness"]:
            print(w)

print("\n--- scriptPubKey ---")
for vout in segwit_tx["vout"]:
    print(vout["scriptPubKey"]["asm"])


print("\n\n====================================")
print("TRANSACTION SIZE COMPARISON")
print("====================================")

print(f"P2PKH size: {legacy_tx['size']} bytes")
print(f"SegWit size: {segwit_tx['size']} bytes\n")

print(f"P2PKH vsize: {legacy_tx['vsize']} vbytes")
print(f"SegWit vsize: {segwit_tx['vsize']} vbytes\n")

print(f"P2PKH weight: {legacy_tx['weight']}")
print(f"SegWit weight: {segwit_tx['weight']}")

print("\n====================================")

if segwit_tx["vsize"] < legacy_tx["vsize"]:
    print("Result: SegWit transaction uses fewer virtual bytes and is more efficient.")
else:
    print("Result: Legacy transaction is larger compared to SegWit.")
