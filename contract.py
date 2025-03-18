from algopy import ARC4Contract, subroutine, arc4, itxn, Global, Asset, Txn, gtxn, Account, UInt64
from algopy.arc4 import abimethod, arc4_signature


class Test(ARC4Contract):
    def __init__(self) -> None:
        self.asset = Asset(0)
        self.account_dispensed_to: Account

    @abimethod
    def create_asset(
        self,
        mbr_payment: gtxn.PaymentTransaction,
        freeze: bool,
    ) -> UInt64:
        
        assert mbr_payment.amount == 100_000

        if freeze:
            create_asset = itxn.AssetConfig(
                asset_name='Test',
                unit_name='T1',
                manager=Global.current_application_address,
                reserve=Global.current_application_address,
                clawback=Global.current_application_address,
                freeze=Global.current_application_address,
                default_frozen=True,
                decimals=0,
                total=100,
            ).submit()



        else:
            create_asset = itxn.AssetConfig(
                asset_name='Test',
                unit_name='T1',
                manager=Global.current_application_address,
                reserve=Global.current_application_address,
                clawback=Global.current_application_address,
                decimals=0,
                total=100,
            ).submit()

        self.asset = create_asset.created_asset

        return create_asset.created_asset.id

    @abimethod
    def transfer_asset(
        self,
    ) -> None:
        
        if self.asset.default_frozen == True:
            

            #unfreeze user, transfer to user, refreeze user
            
            itxn.AssetFreeze(
                freeze_account=Txn.sender,
                freeze_asset=self.asset,
                frozen=False,
            ).submit()
            
            itxn.AssetTransfer(
                asset_receiver=Txn.sender,
                asset_amount=1,
                xfer_asset=self.asset
            ).submit()

            itxn.AssetFreeze(
                freeze_account=Txn.sender,
                freeze_asset=self.asset,
                frozen=True,
            ).submit()

        else:

            itxn.AssetTransfer(
                asset_receiver=Txn.sender,
                asset_amount=1,
                xfer_asset=self.asset
            ).submit()

        self.account_dispensed_to = Txn.sender

    @abimethod
    def user_request_unfreeze(
        self,
        receiver: Account
    ) -> None:
        
        txn_index = Txn.group_index
        assert gtxn.ApplicationCallTransaction(txn_index + 2).app_args(0) == arc4_signature("user_request_freeze(account)void"), "User did not request freeze after unfreeze and transfer"
        itxn.AssetFreeze(
            freeze_account=Txn.sender,
            freeze_asset=self.asset,
            frozen=False,
        ).submit()

        itxn.AssetFreeze(
            freeze_account=receiver,
            freeze_asset=self.asset,
            frozen=False,
        ).submit()

    @abimethod
    def user_request_freeze(
        self,
        receiver: Account
    ) -> None:
        
        itxn.AssetFreeze(
            freeze_account=Txn.sender,
            freeze_asset=self.asset,
            frozen=True,
        ).submit()

        itxn.AssetFreeze(
            freeze_account=receiver,
            freeze_asset=self.asset,
            frozen=True,
        ).submit()


    @abimethod
    def clawback_asset(
        self
    ) -> None:
        
        itxn.AssetTransfer(
            xfer_asset=self.asset,
            asset_receiver=Global.current_application_address,
            sender=Global.current_application_address,
            asset_sender=self.account_dispensed_to,
            asset_amount=1
        ).submit()



