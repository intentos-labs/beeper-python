# beeper-python

Python SDK for Beeper operations on BNB Smart Chain.

## Features

- Deploy and manage Beeper contracts
- Token deployment and management
- Trading functionality with PancakeSwap V3
- Price calculation and impact estimation
- Wallet management

## Installation
 
```bash
pip install beeper-python
```

## Usage

```python
from beeper.chain import BeeperClient
from beeper.util import BSC_MAINNET_SETTINGS, BSC_TESTNET_SETTINGS

# Initialize client
# config is BSC_TESTNET_SETTINGS or BSC_MAINNET_SETTINGS
client = BeeperClient(
    config=BSC_TESTNET_SETTINGS,
    wallet_address="your_wallet_address",
    private_key="your_private_key"
)

# Make trades
client.make_trade(
    input_token="input_token_address",
    output_token="output_token_address",
    amount=1000000
)

# Get price information
price = client.get_price_input(
    token0="input_token_address",
    token1="output_token_address",
)
```

## Configuration

The SDK requires a configuration dictionary with the following keys:
- RPC: BNB Smart Chain RPC endpoint
- PancakeV3SwapRouter: PancakeSwap V3 router address
- PancakeV3Quoter: PancakeSwap V3 quoter address
- PancakeV3Factory: PancakeSwap V3 factory address
- PostionManage: Position manager address

## License

MIT
