from constants import test_app_client, address, signer, algorand
from algokit_utils import CommonAppCallParams, AssetOptInParams, AlgoAmount


asset_id_created = algorand.app.get_global_state(test_app_client.app_id).get('asset').value

account_assets = algorand.account.get_information(address).assets

opted_into_asset = False
for asset in account_assets:
    if asset['asset-id'] == asset_id_created:
        opted_into_asset = True

if not opted_into_asset:
    print("User was not opted in, opting in")

    algorand.send.asset_opt_in(
        AssetOptInParams(
            sender=address,
            asset_id=asset_id_created,
            signer=signer,
        )
    )


print("User opted in")
print("Calling Transfer Asset method . . .")
txn_response = test_app_client.send.transfer_asset(
    params=CommonAppCallParams(
        max_fee=AlgoAmount(micro_algo=4000)
    ),
    send_params={
        'cover_app_call_inner_transaction_fees': True,
        'populate_app_call_resources': True
        
    }
)

print(txn_response.tx_ids)
