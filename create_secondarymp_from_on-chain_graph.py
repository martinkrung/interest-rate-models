#!/usr/bin/env python3

import os
import sys
import boa

from secondary_rate_model import plot_final_rate


RPC_ETHEREUM = os.getenv('RPC_ETHEREUM')
RPC_ARBITRUM = os.getenv('RPC_ARBITRUM')
ARBISCAN_API_KEY = os.getenv('ARBISCAN_API_KEY')
ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')
DEPLOYED_CONTRACT = os.getenv('DEPLOYED_CONTRACT')

boa.env.fork(RPC_ETHEREUM)

# Secondary monetary policy on WBTC/crvUSD markets https://lend.curve.fi/#/ethereum/markets/one-way-market-9/create
# 0x188041ad83145351ef45f4bb91d08886648aeaf8


contract = boa.from_etherscan(
    0x188041ad83145351ef45f4bb91d08886648aeaf8,
    name="SecondaryMonetaryPolicy",
    uri="https://api.etherscan.io/api",
    api_key=ETHERSCAN_API_KEY
)

'''
params from contract:
struct Parameters:
    u_inf: uint256
    A: uint256
    r_minf: uint256
    shift: uint256
'''


parameters = contract.parameters()
print(f"parameters raw: {parameters}")

u_inf, A, r_minf, shift = [param / 10**18 for param in parameters]

# u_inf, A, r_minf, shift = parameters

print(f"parameters: {u_inf}, {A}, {r_minf}, {shift}")

amm_address = contract.AMM()

amm = boa.from_etherscan(
    amm_address,
    name="AMM",
    uri="https://api.etherscan.io/api",
    api_key=ETHERSCAN_API_KEY
)

r0 = int(amm.rate())
r0 = r0 / 10**10
print(f"rate: {r0}")

plot_final_rate(u_inf, r_minf, A, shift, r0, c="red")
