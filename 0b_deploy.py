from constants import test_factory, algorand, address, signer
from algokit_utils import PaymentParams, AlgoAmount
from dotenv import load_dotenv, set_key

load_dotenv()

test_app_client, deploy_response = test_factory.send.bare.create()

set_key('.env', 'app_id', str(test_app_client.app_id))

print("Creating app . . .")
fund_app = algorand.send.payment(
    PaymentParams(
        sender=address,
        receiver=test_app_client.app_address,
        amount=AlgoAmount(algo=0.1),
        signer=signer,
    )
)
print("App Funded with 0.1A MBR to be an active account")