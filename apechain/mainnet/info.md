# ApeChain Mainnet

> For general caff node information, shutdown procedures, and dangerous configuration options, see the [main README](../../README.md).

## Docker Image

```
ghcr.io/espressosystems/nitro-espresso-integration/nitro-node:apechain-v3.5.6-721a697
```

## Snapshot

Download the snapshot from here (TODO: add link). The `docker-compose.yml` file currently expects the snapshot folder to be named `arbitrum` and to be located under the same folder as the compose file. You can adjust this according to your setup in `docker-compose.yml`.

## Running the Node

This folder is set up to run an ApeChain mainnet caff node.

### Prerequisites

1. **Parent Chain RPC**: Replace the default Arbitrum RPC URL in `docker-compose.yml` with your own private URL to avoid rate-limiting issues. Look for `--parent-chain.connection.url` in the entrypoint.

2. **Snapshot**: Download and extract the snapshot to the `arbitrum` folder.

### Start the Node

```bash
docker-compose up -d
```

### Stop the Node

Always use a proper timeout to allow graceful shutdown:

```bash
docker-compose stop -t 300
```

See the [main README](../../README.md#proper-shutdown-procedures) for why this is important.

## Monitoring

### Startup Complete

`Caff Node successfully started` in the logs indicates the node has fully initialized. Before this message appears, the node is still starting up and should not be shut down.

### Sync Progress

| Log Message | Meaning | How to Check Progress |
|-------------|---------|----------------------|
| `Produced block` | Node is producing L2 blocks | Compare block number to [ApeScan](https://apescan.io/) |
| `Now processing hotshot block` | Node is syncing HotShot blocks | Compare to [Espresso Explorer](https://explorer.main.net.espresso.network/) |

## Chain-Specific Configuration

The `nodeConfig.json` is preconfigured for ApeChain mainnet with:

| Parameter | Value |
|-----------|-------|
| Chain ID | 33139 |
| Parent Chain | Arbitrum One (42161) |
| Namespace | 33139 |
| HotShot URL | `https://query-0.main.net.espresso.network/` |

## Troubleshooting

### Node Won't Start After Unclean Shutdown

If the node fails to start after an unclean shutdown (e.g., `docker-compose stop` without `-t 300`):

1. Check logs for database corruption errors
2. If corrupted, delete the `arbitrum` data folder
3. Re-download and extract the snapshot
4. Restart with `docker-compose up -d`

### Node Stuck at Specific Block

If the node stops making progress:

1. Check parent chain RPC is accessible and not rate-limited
2. Check HotShot URL is accessible
3. Verify you're using the latest docker image

For advanced recovery using dangerous config options, see [Dangerous Configuration](../../README.md#dangerous-configuration-options) in the main README.
