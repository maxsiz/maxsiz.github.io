---
layout: post
title: Distributed Liquidity
subtitle: NFT secured with ERC20
tags: [Ethereum, wNFT, erc721]
---

To move toward truly decentralized liquidity (DL), we need to conceive its ideal model. In our view, the more addresses with a non-zero balance of a given asset are exists, the higher its degree of decentralization takes place. From this perspective (storage location), a multitude of EOAs that have approved the use of a certain amount of a particular asset forms an ideal pool.  

Before EIP 7702, EOA 1 cannot delegate to another EOA 2 the right to spend its balance of the native network coin (in an EVM network).  

More than a year ago, an interesting proposal for improvement was submitted to the Ethereum community: [ERC-6551: Non-fungible Token Bound Accounts](https://eips.ethereum.org/EIPS/eip-6551). The authors suggested using a Minimal Proxy Contract (ERC-1167) as a smart wallet, with an NFT confirming ownership of this wallet.

In the new version of the Envelop protocol, we tried to take another step forward—and a slight step to the side :). We decided not to complicate the proxy contract itself but instead turned its implementation into an NFT contract with a single token: the [Envelop Singleton NFT](https://github.com/dao-envelop/envelop-protocol-v2/blob/master/src/impl/Singleton721.sol).  

Thus, in the new version of the Envelope protocol, wNFT is the both simultaneously: a pool and a wallet . Additionally, there is no longer reason to maintain a collateral registry for each wNFT.
Everything were ever transferred to this contract address will be considered as the collateral for the wNFT.
This wNFT structure allows for the construction of new properties and mechanisms for DeFi dApps, including pools.

### Links
[Full Menaskop article with my quotation, (RU)](https://hackernoon.com/your-airdrop-dust-can-finally-be-usefulthanks-to-this-ingenious-protocol)  

