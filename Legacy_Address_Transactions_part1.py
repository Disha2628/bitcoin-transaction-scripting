from bitcoinrpc.authproxy import AuthServiceProxy

# --- Connect to regtest bitcoind ---
rpc_user = "hyperledgerz4040"
rpc_password = "BitcoinTransactionAssignment2"
rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:18443")

wallet_name = "testwallet"

# --- Load or create wallet ---
try:
    rpc_connection.loadwallet(wallet_name)
except Exception as e:
    if "already loaded" not in str(e):
        raise

# --- Generate three legacy addresses ---
address_A = rpc_connection.getnewaddress("", "legacy")
address_B = rpc_connection.getnewaddress("", "legacy")
address_C = rpc_connection.getnewaddress("", "legacy")

print(f"Address A: {address_A}")
print(f"Address B: {address_B}")
print(f"Address C: {address_C}")

# --- Mine 101 blocks to fund the wallet (so coinbase becomes spendable) ---
# Only mine if wallet balance is zero
if rpc_connection.getbalance() == 0:
    rpc_connection.generatetoaddress(101, address_A)

print(f"Wallet balance: {rpc_connection.getbalance()} BTC")

# --- Create a raw transaction from A to B ---
# Use fundrawtransaction with explicit feeRate <= paytxfee
raw_tx = rpc_connection.createrawtransaction([], {address_B: 10})
funded_tx = rpc_connection.fundrawtransaction(raw_tx, {"feeRate": 0.0001})

# --- Decode transaction to show ScriptPubKey for B ---
decoded_tx = rpc_connection.decoderawtransaction(funded_tx['hex'])
print("\n--- ScriptPubKey for Address B ---")
for vout in decoded_tx["vout"]:
    if vout["scriptPubKey"].get("address") == address_B:
        print(vout["scriptPubKey"]["asm"])

# --- Sign transaction ---
signed_tx = rpc_connection.signrawtransactionwithwallet(funded_tx['hex'])
print("\nTransaction signed successfully.")

# --- Broadcast transaction ---
txid_broadcast = rpc_connection.sendrawtransaction(signed_tx['hex'])
print("Transaction broadcasted! TXID:", txid_broadcast)

# Confirm transaction
rpc_connection.generatetoaddress(1, address_A)

print("\n--- Finding UTXO for Address B ---")

# Get unspent outputs belonging to B
utxos = rpc_connection.listunspent(1, 9999999, [address_B])

if len(utxos) == 0:
    raise Exception("No UTXO found for address B")

utxo = utxos[0]

txid = utxo['txid']
vout = utxo['vout']
amount = utxo['amount']

print("UTXO from B:")
print("TXID:", utxo["txid"])
print("Amount:", utxo["amount"])


print("\n--- Creating Transaction B -> C ---")

inputs = [{
    "txid": txid,
    "vout": vout
}]

# subtract small fee
outputs = {
    address_C: float(amount) - 0.0001
}

raw_tx_BC = rpc_connection.createrawtransaction(inputs, outputs)

print("Raw transaction B -> C created.")


print("\n--- Decoding Raw Transaction B -> C ---")

decoded_tx_BC = rpc_connection.decoderawtransaction(raw_tx_BC)
print("\nScriptPubKey for C:")
print(decoded_tx_BC["vout"][0]["scriptPubKey"]["asm"])


print("\n--- Signing Transaction ---")

signed_tx_BC = rpc_connection.signrawtransactionwithwallet(raw_tx_BC)

if not signed_tx_BC["complete"]:
    raise Exception("Transaction signing failed")

print("Signed transaction:")
print("Transaction B -> C signed successfully.")


print("\n--- Broadcasting Transaction ---")

txid_BC = rpc_connection.sendrawtransaction(signed_tx_BC['hex'])

print("Transaction B -> C broadcasted!")
print("TXID:", txid_BC)


print("\n--- Mining a block to confirm transaction ---")

rpc_connection.generatetoaddress(1, address_A)


print("\n--- Decoding Final Transaction ---")

tx_details = rpc_connection.gettransaction(txid_BC)

# extract raw hex
raw_hex = tx_details["hex"]

# decode transaction
final_tx = rpc_connection.decoderawtransaction(raw_hex)

print("Transaction decoded successfully.")


print("\n--- ScriptSig Analysis ---")

for vin in final_tx["vin"]:
    print("Unlocking Script (scriptSig):", vin["scriptSig"]["asm"])

print("\n--- ScriptPubKey Analysis ---")

for vout in final_tx["vout"]:
    print("Locking Script (scriptPubKey):", vout["scriptPubKey"]["asm"])