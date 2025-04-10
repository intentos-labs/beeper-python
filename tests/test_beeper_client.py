import pytest
from web3 import Web3
from beeper.chain import BeeperClient
from beeper.util import BSC_TESTNET_SETTINGS

wbnb = "0xae13d989daC2f0dEbFf460aC112a837C89BAa7cd"
busd = "0xaB1a4d4f1D656d2450692D237fdD6C7f9146e814"

@pytest.fixture
def config():
    return BSC_TESTNET_SETTINGS

@pytest.fixture
def wallet():
    wallet_address = Web3.to_checksum_address("0x373C8E4947Ed9F939E5D25615607f11D5CcCe136")
    with open("../out/0x373C8E4947Ed9F939E5D25615607f11D5CcCe136") as d:
        wallet_privkey = d.readline()
    return {
        "address": wallet_address,
        "private_key": wallet_privkey
    }

@pytest.fixture
def beeper_client(config, wallet):
    client = BeeperClient(
        config=config,
        wallet_address=wallet["address"],
        private_key=wallet["private_key"],
        check_rpc=True  
    )
    return client

def test_init(beeper_client, config, wallet):
    """Test BeeperClient initialization"""
    assert beeper_client.config == config
    assert beeper_client.wallet_address == Web3.to_checksum_address(wallet["address"])
    assert beeper_client.private_key == wallet["private_key"]
    assert beeper_client.router_address == Web3.to_checksum_address(config["PancakeV3SwapRouter"])
    assert beeper_client.quoter_address == Web3.to_checksum_address(config["PancakeV3Quoter"])
    assert len(beeper_client.fees) == 4
    assert beeper_client.fees == [10000, 2500, 500, 100]

def test_get_raw_price(beeper_client):
    """Test price query functionality"""
    
    price = beeper_client.get_raw_price(wbnb, busd)
    assert isinstance(price, float)
    assert price > 0

def test_get_token_pool(beeper_client):
    """Test getting token pool address"""
    
    pool, fee = beeper_client.get_token_pool(busd)
    assert isinstance(pool, str)
    assert Web3.is_address(pool)
    assert isinstance(fee, int)
    assert fee in beeper_client.fees

def test_get_balance(beeper_client):
    """Test getting token balance"""
    
    balance = beeper_client.get_balance(beeper_client.wallet_address, wbnb)
    assert isinstance(balance, int)
    assert balance >= 0

def test_context_manager(beeper_client):
    """Test context manager functionality"""
    with beeper_client as client:
        assert isinstance(client, BeeperClient)
        # Test if we can make a simple call while in context
        balance = client.get_balance(client.wallet_address, wbnb)
        assert isinstance(balance, int) 