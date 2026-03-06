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
print("Decoded transaction (extract ScriptPubKey for B):", decoded_tx)

# --- Sign transaction ---
signed_tx = rpc_connection.signrawtransactionwithwallet(funded_tx['hex'])
print("Signed transaction:", signed_tx)

# --- Broadcast transaction ---
txid_broadcast = rpc_connection.sendrawtransaction(signed_tx['hex'])
print("Transaction broadcasted! TXID:", txid_broadcast)
