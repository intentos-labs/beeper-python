import time
from web3 import Web3
from beeper.chain import BeeperClient
from beeper.util import BSC_TESTNET_SETTINGS

wallet = "0x373C8E4947Ed9F939E5D25615607f11D5CcCe136"
with open("./out/0x373C8E4947Ed9F939E5D25615607f11D5CcCe136") as d:
    privkey = d.readline()

received = "0x1D8534E663F27AB422E50F532CA3193b7ac6e996"
bp = BeeperClient(BSC_TESTNET_SETTINGS, wallet, privkey) 
to = Web3.to_checksum_address("0x2e6b3f12408d5441e56c3C20848A57fd53a78931")
wbnb = Web3.to_checksum_address("0xae13d989daC2f0dEbFf460aC112a837C89BAa7cd")

def test_swap_token(): 

    paddr, pfee = bp.get_token_pool(to)
    print(f"pool addr: {paddr}")

    # token->token
    amount = bp.get_balance(wallet, to)
    print(f"has balance: {amount}")
    tx = bp.make_trade("", to, 2306184959924)
    print(f"tx: {tx}")
    #tx_info = bp.get_tx_info(tx)
    #print(f"tx_info: {tx_info}")
    time.sleep(5)
    # token-> bnb 
    amount = bp.get_balance(wallet, to)
    print(f"has balance: {amount}")
    bp.make_trade(to, "", int(amount/10)) 
    time.sleep(5)
    amount = bp.get_balance(wallet, to)
    print(f"after has balance: {amount}")
    # wbnb -> token 
    bp.make_trade(wbnb, to, 400000)
    # token -> wbnb 
    bp.make_trade(to, wbnb, int(amount/10)) 

def test_transfer():

    # transfer bnb
    print(f"==== transfer bnb")
    val = bp.get_balance(received, "")
    print(f"before {val}")
    bp.transfer_asset(received, "", 1000)
    val = bp.get_balance(received, "")
    print(f"{val}")

    # transfer token
    print(f"==== transfer token")
    val = bp.get_balance(received, to)
    print(f"before {val}")
    bp.transfer_asset(received, to, 2000)
    val = bp.get_balance(received, to)
    print(f"{val}")


    # claim reward
    print(f"==== claim reward")
    val = bp.get_balance(wallet, to)
    print(f"before {val}")
    bp.claim_reward(to)
    val = bp.get_balance(wallet, to) 
    print(f"{val}")

def test_get_price():
    to = Web3.to_checksum_address("0x8d008B313C1d6C7fE2982F62d32Da7507cF43551")
    print(f"==== get price")
    paddr, fee = bp.get_token_pool(to)
    print(f"{paddr} {fee}")

    token0_amount = bp.get_balance(paddr, to)
    token0_amount = token0_amount / 10**18
    print(f"token0: {token0_amount}")

    token1_amount = bp.get_balance(paddr, wbnb)
    token1_amount = token1_amount / 10**18
    print(f"token1: {token1_amount}")

    fee = fee / 1_000_000
    print(f"fee: {fee}")

    slippage = 0.01

    token0_trade_amount = token0_amount * slippage /((1-slippage)*(1-fee))
    print(f"token0_trade_amount: {token0_trade_amount}")

    token1_trade_amount = token1_amount * slippage /((1-slippage)*(1-fee))
    print(f"token1_trade_amount: {token1_trade_amount}")
    

    amount = 1_000_000_000_000_000_000
    raw_price = bp.get_raw_price(to, wbnb)
    print(f"raw_price: {raw_price}")

    
    real_price = bp.get_price_input(to, wbnb, amount)
    print(f"real_price: {real_price/amount}")

    raw_price = bp.get_raw_price(wbnb, to)
    print(f"raw_price: {raw_price}")

    
    real_price = bp.get_price_input(wbnb, to, amount)
    print(f"real_price: {real_price/amount}")

    impact = bp.estimate_price_impact(wbnb, to, amount)
    print(f"impact: {impact}")

try:
    test_swap_token()
    test_transfer()
    test_get_price()
except Exception as e:
    print(e)