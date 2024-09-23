#!/usr/bin/env python3

import boa
import os
import sys

boa.interpret.set_cache_dir() 

RPC_ETHEREUM = os.getenv('RPC_ETHEREUM')
RPC_ARBITRUM = os.getenv('RPC_ARBITRUM')
ARBISCAN_API_KEY = os.getenv('ARBISCAN_API_KEY')
ETHERSCAN_API_KEY = os.getenv('ETHERSCAN_API_KEY')
ACCOUNT_ADDRESS = os.getenv('ACCOUNT_ADDRESS')
LLAMA_MARKET = os.getenv('LLAMA_MARKET')

min_rate = int(0.005 * 10**18 / (365 * 86400) )
max_rate = int(0.5 * 10**18 / (365 * 86400) )



CONTROLLER_ADDRESS = "0xecf99de21c31ec75b4fb97e980f9d084b1d8da8f"
amm = "0x6e729dc02d7b81b0ea29678745a3bc8ed9abdb37"
vault = "0xa6C2E6A83D594e862cDB349396856f7FFE9a979B"

boa.fork(RPC_ARBITRUM)

'''
arbtoken = boa.from_etherscan(
    "0x912CE59144191C1204E64559FE8253a0e49E6548",
    name="ARB",
    uri="https://api.arbiscan.io/api",
    api_key=ARBISCAN_API_KEY
)

amm = boa.from_etherscan(
    amm,
    name="amm",
    uri="https://api.arbiscan.io/api",
    api_key=ARBISCAN_API_KEY
)

'''

crvusd = boa.from_etherscan(
    "0x498Bf2B1e120FeD3ad3D42EA2165E9b73f99C1e5",
    name="crvUSD",
    uri="https://api.arbiscan.io/api",
    api_key=ARBISCAN_API_KEY
)

controller = boa.from_etherscan(
    CONTROLLER_ADDRESS,
    name="controller",
    uri="https://api.arbiscan.io/api",
    api_key=ARBISCAN_API_KEY
)

# semilog = boa.load("SemilogMonetaryPolicy.vy", crvusd, min_rate, max_rate)

semilog = boa.load("SemilogMonetaryPolicyWPowerTest.vy", crvusd, min_rate, max_rate, 2)

#semilog.eval("self._total_debt=0")

total_debt = controller.total_debt()
print(f"total_debt: {total_debt}")
print(f"total_debt: {total_debt/ 10**18}")


total_reserves = crvusd.balanceOf(CONTROLLER_ADDRESS)

print(f"total_reserves: {total_reserves}")
print(f"total_reserves: {total_reserves/ 10**18}")

utilisation =  total_debt / (total_reserves + total_debt)
print(f"utilisation: {utilisation}")

with boa.env.prank(CONTROLLER_ADDRESS):
    rate = semilog.rate(controller)
    rate = rate * 365 * 86400
    print(f"rate: {rate}")
    print(f"rate: {rate / 10**18}")
# supply 100'000 crvUSD out
supply = int(100000 * 10**18)

results = []

for i in range(0, 101):
    new_debt = int(i * 1000 * 10**18)
    new_reserves = supply

    future_rate = semilog.calculate_rate_test(new_reserves, new_debt)
    future_rate = future_rate * 365 * 86400

    utilisation = new_debt / new_reserves

    results.append({
        'supply': supply,
        'supply_human': supply / 10**18,
        'new_debt': new_debt,
        'new_debt_human': new_debt / 10**18,
        'new_reserves': new_reserves,
        'new_reserves_human': new_reserves / 10**18,
        'future_rate': future_rate,
        'future_rate_human': future_rate / 10**18,
        'utilisation': utilisation
    })

# Print results
for result in results:
    print(f"Supply: {result['supply']} ({result['supply_human']} crvUSD)")
    print(f"New debt: {result['new_debt']} ({result['new_debt_human']} crvUSD)")
    print(f"New reserves: {result['new_reserves']} ({result['new_reserves_human']} crvUSD)")
    print(f"Future rate: {result['future_rate']} ({result['future_rate_human']})")
    print(f"Utilisation: {result['utilisation']}")
    print("---")

# Export to CSV
print("supply;supply_human;new_debt;new_debt_human;new_reserves;new_reserves_human;future_rate;future_rate_human;utilisation")
for result in results:
    print(f"{result['supply']};{result['supply_human']};{result['new_debt']};{result['new_debt_human']};{result['new_reserves']};{result['new_reserves_human']};{result['future_rate']};{result['future_rate_human']};{result['utilisation']}")
