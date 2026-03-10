# Bitcoin Transaction Scripting 

A Python-based project demonstrating how **Bitcoin transactions are created, signed, broadcast, and analyzed** using **Bitcoin Core RPC in Regtest mode**.
This project is part of a blockchain course assignment to understand **Legacy and SegWit transaction scripting and their structural differences**.

---

# Contributors

**Team Name:** HyperLedgerz

* **Siddhi Sandesh Patil** – 240041035
* **Rida Samrin** – 240001060
* **Deo Shriya Shamsunder** – 240041013
* **Disha Umesh Dange** – 240001026

---

# Table of Contents

* [Overview](#overview)
* [Features](#features)
* [Requirements](#requirements)
* [Installation](#installation)
* [Usage](#usage)

  * [Part 1 – Legacy Address Transactions](#part-1--legacy-address-transactions)
  * [Part 2 – SegWit Address Transactions](#part-2--segwit-address-transactions)
  * [Part 3 – Transaction Analysis](#part-3--transaction-analysis)
* [Project Structure](#project-structure)
* [Example Workflow](#example-workflow)
* [Testing](#testing)
* [Educational Purpose](#educational-purpose)

---

# Overview

This project interacts directly with **Bitcoin Core** through RPC using Python to simulate real Bitcoin transactions on a **local Regtest blockchain**.

The project is divided into **three parts**:

### Part 1 – Legacy Transactions

* Generate **P2PKH (Legacy) addresses**
* Create and fund transactions
* Sign transactions using wallet keys
* Broadcast transactions to the regtest network
* Decode transaction scripts

### Part 2 – SegWit Transactions

* Generate **P2SH-P2WPKH SegWit addresses**
* Create SegWit transactions
* Sign using witness data
* Broadcast and decode transactions

### Part 3 – Transaction Analysis

* Compare **Legacy vs SegWit transactions**
* Analyze:

  * Transaction size
  * Virtual size (vsize)
  * Weight
  * `scriptSig`
  * `scriptPubKey`
  * `witness data`

This demonstrates how **SegWit reduces transaction size and moves signatures to witness data**.

---

# Features

### Legacy Transaction Simulation

* Generate legacy Bitcoin addresses
* Create raw transactions
* Sign using wallet private keys
* Broadcast transactions

### SegWit Transaction Simulation

* Generate SegWit addresses
* Create witness-based transactions
* Broadcast and decode them

### Transaction Script Analysis

* Extract and display:

  * `scriptSig`
  * `scriptPubKey`
  * `witness data`

### Regtest Blockchain

* Local blockchain environment
* Mine blocks instantly
* No real Bitcoin required

---

# Requirements

* **Python 3.8+**
* **Bitcoin Core installed**
* Python package:

```bash
pip install python-bitcoinrpc
```

---

# Installation

### 1. Clone the repository

```bash
git clone https://github.com/Disha2628/bitcoin-transaction-scripting.git
cd bitcoin-transaction-scripting
```

### 2. Install Python dependency

```bash
pip install -r requirments.txt
```

or manually

```bash
pip install python-bitcoinrpc
```

---

### 3. Configure Bitcoin Core

Edit **bitcoin.conf**

```
regtest=1
server=1

rpcuser=hyperledgerz4040
rpcpassword=BitcoinTransactionAssignment2

fallbackfee=0.0002
paytxfee=0.0001
mintxfee=0.00001
txconfirmtarget=6
```

---

### 4. Start Bitcoin Node

```bash
bitcoind -regtest
```

---

# Usage

Run each part of the project separately.

---

## Part 1 – Legacy Address Transactions

Creates transactions using **P2PKH addresses**.

```bash
python Legacy_Address_Transactions_part1.py
```

This script:

* Generates addresses **A, B, C**
* Mines blocks to fund the wallet
* Sends BTC from **A → B**
* Broadcasts transaction

---

## Part 2 – SegWit Address Transactions

Creates transactions using **SegWit addresses**.

```bash
python Segwit_Address_Transactions_part2.py
```

This script:

* Generates SegWit addresses
* Creates **A' → B' → C' transactions**
* Signs with witness data
* Broadcasts them

---

## Part 3 – Transaction Analysis

Compares **Legacy and SegWit transactions**.

```bash
python analysis.py
```

You will enter:

* TXID of **Legacy transaction**
* TXID of **SegWit transaction**

The script outputs:

* Transaction size
* Virtual size
* Weight units
* Script structure comparison

---

# Project Structure

```
bitcoin-transaction-scripting
│
├── Legacy_Address_Transactions_part1.py
├── Segwit_Address_Transactions_part2.py
├── analysis.py
├── requirments.txt
└── README.md
```

---

# Example Workflow

1. Start Bitcoin node

```bash
bitcoind -regtest
```

2. Run legacy transaction script

```bash
python Legacy_Address_Transactions_part1.py
```

3. Run SegWit transaction script

```bash
python Segwit_Address_Transactions_part2.py
```

4. Run transaction analysis

```bash
python analysis.py
```

5. Verify transactions using Bitcoin CLI

```bash
bitcoin-cli -regtest getrawtransaction <txid> 1
```

---

# Testing

To confirm the project works correctly:

Run all scripts in order:

```bash
python Legacy_Address_Transactions_part1.py
python Segwit_Address_Transactions_part2.py
python analysis.py
```

Then verify transactions:

```bash
bitcoin-cli -regtest getrawtransaction <txid> 1
```

Check that:

* **Legacy transactions contain scriptSig**
* **SegWit transactions contain witness data**

---

# Educational Purpose

This project demonstrates key Bitcoin concepts:

* UTXO model
* Bitcoin Script
* Legacy P2PKH transactions
* SegWit architecture
* Transaction weight and virtual size
* Raw transaction creation using RPC

All transactions run on **Regtest**, meaning **no real Bitcoin is used** and blocks are mined locally for testing and learning purposes.

---
