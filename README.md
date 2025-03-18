# Overview

- Generate two arbitrary accounts (These must be funded via https://bank.testnet.algorand.network/ as the codebase works around testnet)
- Deploy the contract, should you make changes you can recompile with `algokit compile py contract.py --output-arc56`
- Call the "Create Asset" method in the contract with the Freeze argument toggled to either True or False
- Call the "Transfer Asset" method in the contract to obtain 1 asset unit from the contract
- Call the "Clawback Asset" method in the contract to clawback 1 asset unit from the dispensed account global state set in "Transfer Asset" method
- Call the "User Request Unfreeze Asset" and "User Request Freeze Asset" methods, these calls request that the sender and the receiver for an asset transfer be unfrozen, the sender can now perform the transfer, and then the refreeze occurs for both the sender and receiver.

*Notes:*
- *the "User Request Unfreeze Asset" will fail if the transaction 2 indexes ahead in the group is not "User Request Freeze Asset", see line below in "User Request Unfreeze Asset":
`assert gtxn.ApplicationCallTransaction(txn_index + 2).app_args(0) == arc4_signature("user_request_freeze(account)void"), "User did not request freeze after unfreeze and transfer"`
- *the clawback asset transfer bypasses freeze, so it doesn't matter if an account is frozen or not when clawing back an asset*
- *the args for the "Clawback Asset" method can be adjusted to accept a target clawback account, just set the asset_sender field to the argument received*
Eg;
```    @abimethod
    def clawback_asset(
        self,
        from: Account,
    ) -> None:
        
        itxn.AssetTransfer(
            xfer_asset=self.asset,
            asset_receiver=Global.current_application_address,
            sender=Global.current_application_address,
            asset_sender=from,
            asset_amount=1
        ).submit()

```
