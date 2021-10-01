# script for deploying new contract each round
import sys
import os 
from brownie import network, Contract
from execjs import get

abi = '''
[
	{
		"type": "function",
		"stateMutability": "nonpayable",
		"outputs": [],
		"name": "newRound",
		"inputs": [
			{
				"type": "address",
				"name": "newTokens",
				"internalType": "address"
			}
		]
	}
]
'''

node = get('Node')
js = node.compile(
'''
    import '@darkforest-eth/contracts';
    function tokensAddress(){
        return contracts.TOKENS_ADDRESS
    }
''' % os.path.join(os.path.dirname(__file__),'node_modules'))

tokens_address = js.call('tokensAddress')
network.connect('xdai-main')
network.accounts.add(sys.argv[1])
factory = Contract.from_ABI("MarketFactory",abi,'0xACE32941F16ec7f528067Ed4745e4411A42a5609')
factory.newRound(tokens_address ,{'from': network.accounts[-1]})