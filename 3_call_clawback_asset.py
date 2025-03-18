from constants import test_app_client
from algokit_utils import CommonAppCallParams, AlgoAmount


print("Calling Clawback Asset method . . .")
txn_response = test_app_client.send.clawback_asset(
    params=CommonAppCallParams(
        max_fee=AlgoAmount(micro_algo=2000)
    ),
    send_params={
        'cover_app_call_inner_transaction_fees': True,
        'populate_app_call_resources': True
        
    }
)

print(txn_response.tx_ids)
