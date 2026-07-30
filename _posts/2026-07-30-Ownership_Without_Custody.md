---
layout: post
title: Ownership Without Custody
subtitle: What Envelop Is Building Next
meta-description: Owning assets without touching them with your own address — the road from Envelop V2 through a Uniswap V4 hook incubator to Unisafe, and why unfreezable is not the same as untraceable.
tags: [Ethereum, wNFT, Uniswap]
---

Almost two years since [Envelop V2](https://github.com/dao-envelop/envelop-protocol-v2) shipped. Time to talk about what's next and what the way there actually was.

### The elephant nobody wants to name

Since the start of 2026, the two biggest stablecoin issuers have frozen roughly $2B across 3,000+ wallets. That's the public number. The real takeaway: any address can end up on that list.

So what do you do about it?

Not every address is equal. Some are much harder to freeze — for reasons that have nothing to do with you. Take a big AMM or lending protocol: the whole liquidity sits on a handful of addresses. Freezing those breaks the entire stablecoin market. Nobody's touching them.

Cool. Assets are "safe" there.

Except now they're stuck.

Say I need to pay $100 for a service. My position in the protocol is $7K. So: partial exit, swap to one asset, transfer. And what if (funny coincidence) the position owner's address is already blacklisted on USDT?

What if you could own the assets without ever touching them with your own address? And earn yield while you're at it?

### Attempt #1: ETHGlobal, August 2025

First PoC. Rough, but the shape was there:

- [Batch Swapper on ETHGlobal](https://ethglobal.com/showcase/batch-swapper-j5q2a)
- [github.com/dao-envelop/ethglobal-batch-swap](https://github.com/dao-envelop/ethglobal-batch-swap)
- Contract example — [arbiscan.io/address/0x93aebbc6...](https://arbiscan.io/address/0x93aebbc6e15eb53abf277d8c366f7d7cbda2f067)

Not a product yet. But now I knew where to dig.

### Going deep on Uniswap V4

April–June 2026: [Atrium Academy — Uniswap Hook Incubator, Cohort 9](https://x.com/AtriumAcademy). Serious deep-dive into V4 architecture, exactly the piece I was missing.

Final hackathon — the jury picked my launchpad hook:

- [Atrium Academy announcement](https://x.com/AtriumAcademy/status/2068005023460815049)
- [github.com/maxsiz/uhi9-token-launch-hook](https://github.com/maxsiz/uhi9-token-launch-hook)

### The obvious move

By May it clicked. Envelop V2 + Uniswap PositionManager. Plus the AI wave — you don't skip that.

That's [Unisafe](https://unisafe.envelop.is/). Full write-up dropping soon on Envelop: [@Envelop_project](https://x.com/Envelop_project).

### What this is not

Not laundering. Not a mixer. Every tx is on-chain and traceable — which is exactly why criminals don't care about it.

It's about being unstoppable. Which is what this whole thing was supposed to be about in the first place.

And it's honest.

### Links
[LinkedIn post, ](https://www.linkedin.com/feed/update/urn:li:activity:7487511339267973120/)  
