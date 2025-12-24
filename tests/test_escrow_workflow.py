import logging
import time
from algosdk import account, mnemonic, transaction
from algosdk.v2client import algod
from app.config import Config
from app.blockchain.escrow_service import EscrowService

# Configure Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def wait_for_confirmation(client, txid):
    last_round = client.status().get("last-round")
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get("confirmed-round") and txinfo.get("confirmed-round") > 0):
        logger.info("Waiting for confirmation...")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    logger.info(f"Transaction {txid} confirmed.")
    return txinfo

def fund_account(client, sender_sk, receiver_addr, amount_microalgos):
    sender_addr = account.address_from_private_key(sender_sk)
    sp = client.suggested_params()
    ptxn = transaction.PaymentTxn(sender_addr, sp, receiver_addr, amount_microalgos)
    stxn = ptxn.sign(sender_sk)
    txid = client.send_transaction(stxn)
    wait_for_confirmation(client, txid)
    logger.info(f"Funded {receiver_addr} with {amount_microalgos} microAlgos")

def test_escrow_service_flow():
    if not Config.ALGORAND_MNEMONIC:
        logger.error("ALGORAND_MNEMONIC not set. Cannot run test.")
        return

    service = EscrowService()
    platform_sk = service.platform_private_key
    platform_addr = service.platform_address
    client = service.algod_client
    
    # 1. Generate Test Accounts
    buyer_sk, buyer_addr = account.generate_account()
    seller_sk, seller_addr = account.generate_account()
    oracle_sk, oracle_addr = account.generate_account() # Oracle is usually platform, but strictly testing another account here
    
    logger.info("Funding test accounts...")
    fund_account(client, platform_sk, buyer_addr, 500000) # 0.5 Algo (Safe buffer)
    fund_account(client, platform_sk, seller_addr, 300000) # 0.3 Algo 
    fund_account(client, platform_sk, oracle_addr, 300000) # 0.3 Algo 
    
    # --- TEST 1: DUAL SIG RELEASE ---
    logger.info("--- START TEST 1: Dual Sig ---")
    app_id, app_addr = service.deploy_escrow(buyer_addr, seller_addr, oracle_addr, 60, platform_sk)
    if not app_id:
        logger.error("Failed to deploy escrow")
        return

    # Fund Escrow
    fund_account(client, buyer_sk, app_addr, 110000) # 0.11 Algo (min balance + small buffer)

    # Buyer Approves
    success = service.approve_release(app_id, buyer_sk)
    if not success:
         logger.error("Buyer approval failed")
    
    # Seller Approves (Trigger Release)
    success = service.approve_release(app_id, seller_sk)
    if not success:
         logger.error("Seller approval failed")
         
    # Check Balance (Should be ~0 inside app, ignoring min balance for now, but PyTeal sends 0 amount with CloseRemainderTo)
    app_info = client.account_info(app_addr)
    logger.info(f"Escrow Balance after dual-sig: {app_info['amount']}")
    assert app_info['amount'] == 0, "Escrow not emptied"
    logger.info("TEST 1 PASSED")

    # --- TEST 2: ORACLE RELEASE ---
    logger.info("--- START TEST 2: Oracle Release ---")
    app_id_2, app_addr_2 = service.deploy_escrow(buyer_addr, seller_addr, oracle_addr, 60, platform_sk)
    
    # Fund Escrow
    fund_account(client, buyer_sk, app_addr_2, 110000)
    
    # Oracle Releases (Triggers Release directly)
    success = service.oracle_release(app_id_2, oracle_sk, seller_addr)
    if not success:
         logger.error("Oracle release failed")
    
    app_info_2 = client.account_info(app_addr_2)
    logger.info(f"Escrow Balance after oracle release: {app_info_2['amount']}")
    assert app_info_2['amount'] == 0, "Escrow not emptied by Oracle"
    logger.info("TEST 2 PASSED")

    # --- TEST 3: BREEDER BOND ---
    logger.info("--- START TEST 3: Breeder Bond ---")
    bond_app_id, bond_addr = service.deploy_bond(seller_addr, platform_addr, platform_sk)
    if not bond_app_id:
        logger.error("Failed to deploy bond")
        return

    # Fund Bond (Breeder deposits 10% Lot Value -> minimal for test)
    fund_account(client, seller_sk, bond_addr, 110000)
    
    # Check Balance
    bond_info = client.account_info(bond_addr)
    logger.info(f"Bond Balance: {bond_info['amount']}")

    # Admin Releases Bond
    success = service.release_bond(bond_app_id, platform_sk, seller_addr)
    if not success:
         logger.error("Bond release failed")
    
    # Check Balance (Should be ~0)
    bond_info_post = client.account_info(bond_addr)
    logger.info(f"Bond Balance after release: {bond_info_post['amount']}")
    assert bond_info_post['amount'] == 0, "Bond not emptied"
    logger.info("TEST 3 PASSED")

if __name__ == "__main__":
    test_escrow_service_flow()
