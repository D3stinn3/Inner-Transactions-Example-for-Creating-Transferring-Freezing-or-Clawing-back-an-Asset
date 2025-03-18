from constants import algorand, test_app_client, address, signer
from test_client import CreateAssetArgs
from algokit_utils import CommonAppCallParams, AlgoAmount, PaymentParams

mbr_payment = algorand.create_transaction.payment(
    PaymentParams(
        sender=address,
        signer=signer,
        amount=AlgoAmount(algo=0.1),
        receiver=test_app_client.app_address
    )
)

print("Calling Create Asset method . . .")

'''
Set Freeze to True if you want the asset to have freeze enabled
Note that whenever a user wants to transfer the asset they must call the unfreeze/freeze method before/after the actual asset transfer
'''
tx_response = test_app_client.send.create_asset(
    args=CreateAssetArgs(
        mbr_payment=mbr_payment,
        freeze=True
    ),
    params=CommonAppCallParams(
        max_fee=AlgoAmount(micro_algo=2000)
    ),
    send_params={
        'cover_app_call_inner_transaction_fees': True
    }
)

print(tx_response.tx_ids)