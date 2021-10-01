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
    const ethers = require('ethers');
    const contracts = require('@darkforest-eth/contracts');
    const from = "0xACE32941F16ec7f528067Ed4745e4411A42a5609";
    const salt = "0xa57605b2e24b1510bf138d6701553196cf98ca6c1e364020d33d6cef72d1be96";
    const creationHash = "0x86529331489ea7a1cc82140188cdba7d19dcd8f3d1376d95981e61e511308a42";
    function tokensAddress(){
        return contracts.TOKENS_ADDRESS
    }
    function newRoundAddress(){
        return ethers.utils.getCreate2Address(from,salt,creationHash);
    }
''' % os.path.join(os.path.dirname(__file__),'node_modules'))

tokens_address = js.call('tokensAddress')
network.connect('xdai-main')
network.accounts.add(sys.argv[1])
factory = Contract.from_ABI("MarketFactory",abi,'0xACE32941F16ec7f528067Ed4745e4411A42a5609')
factory.newRound(tokens_address ,{'from': network.accounts[-1]})
js.call('newRoundAddress')