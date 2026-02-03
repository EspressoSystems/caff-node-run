# Apechain

# Docker Image

```
ghcr.io/espressosystems/nitro-espresso-integration/nitro-node:apechain-v3.5.6-721a697
```

# Snapshot

Download the snapshot from here (TODO: add link). The `docker-compose.yml` file currently expects the snapshot folder to be named `arbitrum` and to be located under the same folder as the compose file. You can adjust this according to your setup in `docker-compose.yml`.

# Running the node

This folder is set up to easily run an ApeChain mainnet caff node. It is recommended to replace the Arbitrum RPC URL in `docker-compose.yml` with your own private URL to avoid rate-limiting issues. The config file included in the repository is prepopulated with mainnet parameters.

```
docker-compose up -d
```

# Monitoring the caff node

`Caff Node successfully started` means the node has now started. Before this message, the node is still being started and should not be shut down because it can lead to unclean shutdowns.

The `Produced block` log indicates that it has started producing blocks. You can check out the [explorer](https://apescan.io/) to see how many blocks are remaining to be synced.

The `Now processing hotshot block` log indicates which HotShot block number it is currently syncing from. Check the [explorer](https://explorer.main.net.espresso.network/) to determine how many blocks are remaining to be synced.
