from constants import test_app_client, algorand, address, signer, address_2, signer_2
from algokit_utils import CommonAppCallParams, AlgoAmount, AssetTransferParams, AssetOptInParams
from test_client import UserRequestUnfreezeArgs, UserRequestFreezeArgs


asset_id_created = algorand.app.get_global_state(test_app_client.app_id).get('asset').value

print("Calling Unfreeze method to unfreeze myself and another user,\n transferring some of the asset another user,\n then calling the Freeze method to refreeze myself and another user (refreeze is mandatory as per contract asserts) . . .")

new_group = test_app_client.new_group()

receiver_assete = algorand.account.get_information(address_2).assets

opted_into_asset = False
for asset in receiver_assete:
    if asset['asset-id'] == asset_id_created:
        opted_into_asset = True

if not opted_into_asset:
    print("Address #2 was not opted in, will opt in")

    address_2_optin = algorand.create_transaction.asset_opt_in(
        AssetOptInParams(
            sender=address_2,
            asset_id=asset_id_created,
            signer=signer_2,
        )
    )
    new_group.add_transaction(address_2_optin, signer_2)

else:
    print("Address #2 is opted in")

new_group.user_request_unfreeze(
    args=UserRequestUnfreezeArgs(
        receiver=address_2
    ),
    params=CommonAppCallParams(
        max_fee=AlgoAmount(micro_algo=5000)
    )
)

transfer_asset_to_another_account_now_that_we_are_unfrozen = algorand.create_transaction.asset_transfer(
    AssetTransferParams(
        sender=address,
        signer=signer,
        receiver=address_2,
        asset_id=asset_id_created,
        amount=1,
    )
)

new_group.add_transaction(transfer_asset_to_another_account_now_that_we_are_unfrozen, signer)

new_group.user_request_freeze(
    args=UserRequestFreezeArgs(
        receiver=address_2
    ),
    params=CommonAppCallParams(
        max_fee=AlgoAmount(micro_algo=5000)
    )
)

txn_response = new_group.send(
    send_params={
        'cover_app_call_inner_transaction_fees': True,
        'populate_app_call_resources': True
    }
)

print(txn_response.tx_ids)
