from algokit_utils import AlgorandClient, AppFactory, AppFactoryParams
from test_client import TestClient, SourceMap
from algosdk.atomic_transaction_composer import AccountTransactionSigner
from algosdk.account import address_from_private_key
from dotenv import load_dotenv
from pathlib import Path
import json
import os

load_dotenv()

algorand = AlgorandClient.testnet()

assert os.getenv('pk') and os.getenv('pk_2'), "Please generate accounts first before doing anything else using 0a_generate_accounts.py"
print("DONT FORGET TO FUND BOTH ACCOUNTS USING https://bank.testnet.algorand.network/")
pk = os.getenv('pk')
address = address_from_private_key(pk)
signer = AccountTransactionSigner(pk)

pk_2 = os.getenv('pk_2')
address_2 = address_from_private_key(pk_2)
signer_2 = AccountTransactionSigner(pk_2)

test_app_spec = (Path(__file__).parent / 'Test.arc56.json').read_text()
test_app_sourcemap = SourceMap(json.loads((Path(__file__).parent / 'Test.approval.puya.map').read_text()))

test_factory_params = AppFactoryParams(
    algorand=algorand,
    app_spec=test_app_spec,
    default_sender=address,
    default_signer=signer,
)

test_factory = AppFactory(
    params=test_factory_params
)

if os.getenv('app_id'):
    app_id = int(os.getenv('app_id'))

    test_app_client = algorand.client.get_typed_app_client_by_id(
        TestClient, 
        app_id=app_id, 
        default_sender=address, 
        default_signer=signer, 
        approval_source_map=test_app_sourcemap
    )

else:
    print("No app ID created yet, call 0b_deploy.py first if not doing so now")