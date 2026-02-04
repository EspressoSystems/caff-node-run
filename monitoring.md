# Detailed Documentation

## Monitoring

### Startup

The `successfully started` log message indicates the node has fully started. Before this message appears, the node is still initializing and should not be shut down as it can lead to unclean shutdowns.

### Block Production

The `Produced block` log indicates block production has begun. You can check the explorer of the chain to see how many blocks remain to be synced.

### Sync Progress

The `Now processing hotshot block` log shows which HotShot block number the node is currently syncing from. Check the HotShot explorer ([mainnet](https://explorer.main.net.espresso.network/) for mainnet chains and [decaf](https://explorer.decaf.testnet.espresso.network/) for testnet chains) to determine how many blocks remain to be synced.

## Proper Shutdown Procedures

Caff nodes use LevelDB for storage. Improper shutdowns can corrupt the database and require a full resync.

### How to Shut Down Properly

#### Docker Compose

```bash
# Allow 5 minutes (300 seconds) for graceful shutdown
docker-compose stop -t 300
```

## Dangerous Configuration Options

The `dangerous` configuration namespace contains options that can cause data loss or inconsistent state if misused. Only use these if you understand the implications.

### Caff Node Dangerous Options

Located under `node.espresso.caff-node.dangerous`:

| Option                          | Default | Description                                                                                                                                                            |
| ------------------------------- | ------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `ignore-database-hotshot-block` | `false` | Ignores the HotShot block number stored in the database and uses the config value instead. Use when you need to force the node to start from a specific HotShot block. |
| `ignore-database-from-block`    | `false` | Ignores the L1 from-block stored in the database and uses the config value instead. Use when you need to force the node to start monitoring from a specific L1 block.  |

### Example: Forcing a Fresh Start

Here we added the dangerous config and updated the `hotshot-block` to the block we want the node to sync from and similarly for `address-monitor-start-l1` which is the parent chain block number we want the node to start syncing from.

To get the `hotshot-block` and `address-monitor-start-l1` first get the current block produced by caff node using cast

```
cast block --rpc-url CAFF_NODE_RPC
```

Then use any `hotshot-block` from the hotshot explorer (decaf/mainnet depending on whether the chain is testnet or mainnet) which is around 24 hours old as compared to the last block produced by the caff node. Similar thing has to be done for `address-monitor-start-l1` get a parent chain block which is around 24 hours old as compared to the last block produced by the caff node.

```json
{
  "node": {
    "espresso": {
      "caff-node": {
        "dangerous": {
          "ignore-database-hotshot-block": true,
          "ignore-database-from-block": true
        }
      },
      "streamer": {
        "hotshot-block": 9919440,
        "address-monitor-start-l1": 428273028
      }
    }
  }
}
```

After the node syncs past the specified blocks, you should remove the dangerous flags and restart to resume normal operation.
