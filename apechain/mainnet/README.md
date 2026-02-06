# Apechain

> For general caff node information, shutdown procedures, and dangerous configuration options, see the our [detailed docs](../../monitoring.md).

### Docker Image

```
ghcr.io/espressosystems/nitro-espresso-integration/nitro-node:apechain-v3.5.6-721a697
```

### Snapshot

Download the snapshot from [here](https://public-nitro-snapshots-sr44vxsww.s3.us-east-2.amazonaws.com/mainnet/apechain/pruned_20260204.tar). The `docker-compose.yml` file currently expects the snapshot folder to be named `arbitrum` and to be located under the same folder as the compose file. You can adjust this according to your setup in `docker-compose.yml`.

### Running the node

This folder is set up to easily run an ApeChain mainnet caff node. **Please replace the default Arbitrum RPC URL for the `--parent-chain.connection.url` argument in `docker-compose.yml` with your own private URL to avoid rate-limiting issues.** The config file included in the repository is prepopulated with mainnet parameters.

```
docker-compose up -d
```

### Shutting down the node

```bash
# Allow 5 minutes (300 seconds) for graceful shutdown
docker-compose stop -t 300
```
