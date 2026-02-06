# Caff Node

Espresso's caff nodes are a wrapper around standard rollup nodes that derive data from what Espresso has finalized. It's important to understand that a caff node has the same setup as a regular L2 node with only certain Espresso flags enabled and follows the same JSON RPC API.

## Running Caff Nodes

This repo provides guides for running caff nodes for our existing rollup integrations. Each chain has its instructions stored under its respective folder

- [ApeChain Mainnet](./apechain/mainnet/README.md)
- [Rari Mainnet](./rari/mainnet/README.md) [WIP]

## Using the Caff Node

You can use your caff node like any other RPC node. Here's an example using cast:

```bash
cast block --rpc-url CAFF_NODE_URL
```

## Detailed Docs

For more detailed docs on how to monitor/debug the caff node, please read our [detailed docs](./monitoring.md)

## Disclaimer

This repo is intended as an example of how to run caff nodes. For production deployments, please contact us.
