from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
from decimal import Decimal

# RPC connection
rpc_user = "hyperledgerz4040"
rpc_password = "BitcoinTransactionAssignment2"
rpc_port = 18443

rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:{rpc_port}")

wallet_name = "testwallet"

# Load wallet
try:
    rpc_connection.loadwallet(wallet_name)
except:
    pass

rpc = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@127.0.0.1:{rpc_port}/wallet/{wallet_name}")

# Generate P2SH-SegWit addresses
A = rpc.getnewaddress("", "p2sh-segwit")
B = rpc.getnewaddress("", "p2sh-segwit")
C = rpc.getnewaddress("", "p2sh-segwit")

print("Address A':", A)
print("Address B':", B)
print("Address C':", C)

# Fund Address A'
fund_txid = rpc.sendtoaddress(A, Decimal("10"))
print("Funding TXID:", fund_txid)

# Mine block so funds confirm
miner_addr = rpc.getnewaddress()
rpc.generatetoaddress(1, miner_addr)

# Get UTXO for A'
utxos = rpc.listunspent(1, 9999999, [A])
utxo = utxos[0]

txid = utxo["txid"]
vout = utxo["vout"]
amount = utxo["amount"]

print("UTXO for A':", txid, vout, amount)

# Create transaction A' -> B'
outputs = {B: float(amount - Decimal("0.0001"))}

raw_tx = rpc.createrawtransaction(
    [{"txid": txid, "vout": vout}],
    outputs
)

print("\nRaw Transaction A'->B':", raw_tx)

decoded = rpc.decoderawtransaction(raw_tx)
print("\nDecoded Transaction (Challenge Script B'):\n", decoded)

# Sign transaction
signed_tx = rpc.signrawtransactionwithwallet(raw_tx)
print("\nSigned Transaction:", signed_tx)

# Broadcast
txid_ab = rpc.sendrawtransaction(signed_tx["hex"])
print("\nTransaction Broadcasted A' -> B'")
print("TXID:", txid_ab)

# Mine block
rpc.generatetoaddress(1, miner_addr)

# -------------------------------
# SECOND TRANSACTION B' -> C'
# -------------------------------

utxos_B = rpc.listunspent(1, 9999999, [B])
utxoB = utxos_B[0]

txidB = utxoB["txid"]
voutB = utxoB["vout"]
amountB = utxoB["amount"]

print("\nUTXO for B':", txidB)

outputs2 = {C: float(amountB - Decimal("0.0001"))}

raw_tx2 = rpc.createrawtransaction(
    [{"txid": txidB, "vout": voutB}],
    outputs2
)

print("\nRaw Transaction B'->C':", raw_tx2)

decoded2 = rpc.decoderawtransaction(raw_tx2)
print("\nDecoded Transaction (Script Analysis):\n", decoded2)

signed_tx2 = rpc.signrawtransactionwithwallet(raw_tx2)
print("\nSigned Transaction:", signed_tx2)

txid_bc = rpc.sendrawtransaction(signed_tx2["hex"])

print("\nTransaction Broadcasted B' -> C'")
print("TXID:", txid_bc)

# Mine block
rpc.generatetoaddress(1, miner_addr)

print("\nSegWit transaction chain complete!")