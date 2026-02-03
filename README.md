# Caff Node

Espresso's caff nodes are a wrapper around standard rollup nodes that derive data from what Espresso has finalized. It's important to understand that a caff node has the same setup as a regular L2 node with only certain Espresso flags enabled and follows the same JSON RPC API.

# Running the caff nodes

This repo provides a guide on how to run a caff node for our existing rollup integrations. Each chain has its instructions stored under its respective folder.

# Using the caff node

You can use your caff node like any other RPC node. Here's an example using cast:

```
cast block  --rpc-url CAFF_NODE_RPC_URL
```

# Disclaimer

It's important to note that this repo is only intended as an example of how to run caff nodes. For production deployments, please contact us.
