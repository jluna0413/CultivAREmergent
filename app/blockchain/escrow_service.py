import logging
import base64
from typing import Optional, Tuple

from algosdk import account, mnemonic, transaction, encoding
from algosdk.v2client import algod, indexer
from algosdk.logic import get_application_address
from pyteal import compileTeal, Mode

from app.config import Config
from app.blockchain.escrow_contract import approval_program as escrow_approval, clear_state_program as escrow_clear
from app.blockchain.bond_contract import approval_program as bond_approval, clear_state_program as bond_clear

logger = logging.getLogger(__name__)

class EscrowService:
    def __init__(self):
        self.algod_client = algod.AlgodClient(
            Config.ALGORAND_ALGOD_TOKEN, 
            Config.ALGORAND_ALGOD_ADDRESS
        )
        self.indexer_client = indexer.IndexerClient(
            Config.ALGORAND_INDEXER_TOKEN, 
            Config.ALGORAND_INDEXER_ADDRESS
        )
        
        # Load platform account (Admin/Oracle)
        self.platform_account = None
        if Config.ALGORAND_MNEMONIC:
            try:
                self.platform_private_key = mnemonic.to_private_key(Config.ALGORAND_MNEMONIC)
                self.platform_address = account.address_from_private_key(self.platform_private_key)
            except Exception as e:
                logger.error(f"Failed to load platform wallet: {e}")

    def compile_program(self, source_func) -> bytes:
        teal_code = compileTeal(source_func(), mode=Mode.Application, version=6)
        compile_response = self.algod_client.compile(teal_code)
        return base64.b64decode(compile_response["result"])

    def deploy_escrow(self, 
                      buyer_addr: str, 
                      seller_addr: str, 
                      oracle_addr: str, 
                      timeout_seconds: int,
                      sender_sk: str) -> Optional[Tuple[int, str]]:
        """
        Deploys a new Escrow Contract.
        Returns (AppID, AppAddress).
        """
        try:
            sender_addr = account.address_from_private_key(sender_sk)
            params = self.algod_client.suggested_params()

            approval_bytes = self.compile_program(escrow_approval)
            clear_bytes = self.compile_program(escrow_clear)

            app_args = [
                encoding.decode_address(buyer_addr),
                encoding.decode_address(seller_addr),
                encoding.decode_address(oracle_addr),
                timeout_seconds.to_bytes(8, 'big')
            ]

            txn = transaction.ApplicationCreateTxn(
                sender=sender_addr,
                sp=params,
                on_complete=transaction.OnComplete.NoOpOC,
                approval_program=approval_bytes,
                clear_program=clear_bytes,
                global_schema=transaction.StateSchema(num_uints=4, num_byte_slices=4),
                local_schema=transaction.StateSchema(num_uints=0, num_byte_slices=0),
                app_args=app_args
            )
            
            signed_txn = txn.sign(sender_sk)
            tx_id = self.algod_client.send_transaction(signed_txn)
            
            confirmed_txn = transaction.wait_for_confirmation(self.algod_client, tx_id, 4)
            app_id = confirmed_txn["application-index"]
            app_addr = get_application_address(app_id)
            
            logger.info(f"Deployed Escrow App ID: {app_id}, Address: {app_addr}")
            return app_id, app_addr

        except Exception as e:
            logger.error(f"Failed to deploy escrow: {e}")
            return None

    def approve_release(self, app_id: int, sender_sk: str) -> bool:
        """
        Signs 'approve' action (Buyer or Seller).
        """
        try:
            sender_addr = account.address_from_private_key(sender_sk)
            params = self.algod_client.suggested_params()
            
            txn = transaction.ApplicationCallTxn(
                sender=sender_addr,
                sp=params,
                index=app_id,
                on_complete=transaction.OnComplete.NoOpOC,
                app_args=[b"approve"]
            )
            
            signed_txn = txn.sign(sender_sk)
            tx_id = self.algod_client.send_transaction(signed_txn)
            transaction.wait_for_confirmation(self.algod_client, tx_id, 4)
            logger.info(f"Approved Escrow {app_id} by {sender_addr}")
            return True
        except Exception as e:
            logger.error(f"Failed to approve escrow: {e}")
            return False

    def oracle_release(self, app_id: int, oracle_sk: str, seller_addr: str) -> bool:
        """
        Triggers 'oracle_release' action (Admin/Oracle).
        Requires seller_addr to be passed in accounts array for InnerTxn visibility.
        """
        try:
            sender_addr = account.address_from_private_key(oracle_sk)
            params = self.algod_client.suggested_params()
            
            # Since this triggers InnerTxn (Payment), fees are paid by App account (from its balance).
            # The txn fee for THIS call is paid by Sender (Oracle).
            # If InnerTxn needs fees, we might need to send extra fee here or ensure App is funded.
            # PyTeal `InnerTxnBuilder` usually defaults fee to 0 if pooled, 
            # so the outer txn must cover it.
            # Let's set fee to 2x min fee to cover inner txn.
            params.fee = 2000 
            params.flat_fee = True

            txn = transaction.ApplicationCallTxn(
                sender=sender_addr,
                sp=params,
                index=app_id,
                on_complete=transaction.OnComplete.NoOpOC,
                app_args=[b"oracle_release"],
                accounts=[seller_addr] # Must include seller to allow payment to them
            )
            
            signed_txn = txn.sign(oracle_sk)
            tx_id = self.algod_client.send_transaction(signed_txn)
            transaction.wait_for_confirmation(self.algod_client, tx_id, 4)
            logger.info(f"Oracle Release triggered for Escrow {app_id} by {sender_addr}")
            return True
        except Exception as e:
            logger.error(f"Failed to trigger Oracle release: {e}")
            return False

    # --- BOND CONTRACT METHODS ---

    def deploy_bond(self, 
                    breeder_addr: str, 
                    admin_addr: str, 
                    sender_sk: str) -> Optional[Tuple[int, str]]:
        """
        Deploys a Breeder Bond Contract.
        Returns (AppID, AppAddress).
        """
        try:
            sender_addr = account.address_from_private_key(sender_sk)
            params = self.algod_client.suggested_params()

            approval_bytes = self.compile_program(bond_approval)
            clear_bytes = self.compile_program(bond_clear)

            app_args = [
                encoding.decode_address(breeder_addr),
                encoding.decode_address(admin_addr)
            ]

            txn = transaction.ApplicationCreateTxn(
                sender=sender_addr,
                sp=params,
                on_complete=transaction.OnComplete.NoOpOC,
                approval_program=approval_bytes,
                clear_program=clear_bytes,
                global_schema=transaction.StateSchema(num_uints=0, num_byte_slices=2),
                local_schema=transaction.StateSchema(num_uints=0, num_byte_slices=0),
                app_args=app_args
            )
            
            signed_txn = txn.sign(sender_sk)
            tx_id = self.algod_client.send_transaction(signed_txn)
            
            confirmed_txn = transaction.wait_for_confirmation(self.algod_client, tx_id, 4)
            app_id = confirmed_txn["application-index"]
            app_addr = get_application_address(app_id)
            
            logger.info(f"Deployed Bond App ID: {app_id}, Address: {app_addr}")
            return app_id, app_addr

        except Exception as e:
            logger.error(f"Failed to deploy bond: {e}")
            return None

    def release_bond(self, app_id: int, admin_sk: str, breeder_addr: str) -> bool:
        """
        Triggers 'release_bond' action (Admin).
        """
        return self._call_bond_action(app_id, admin_sk, b"release_bond", accounts=[breeder_addr])

    def slash_bond(self, app_id: int, admin_sk: str) -> bool:
        """
        Admin slashes bond (confiscates funds).
        """
        try:
            return self._call_bond_action(app_id, admin_sk, b"slash")
        except Exception as e:
            logger.error(f"Failed to slash bond: {e}")
            return False

    def _call_bond_action(self, app_id: int, sender_sk: str, action_arg: bytes, accounts: list = None) -> bool:
        sender_addr = account.address_from_private_key(sender_sk)
        params = self.algod_client.suggested_params()
        
        # Fee for inner txn
        params.fee = 2000
        params.flat_fee = True

        txn = transaction.ApplicationCallTxn(
            sender=sender_addr,
            sp=params,
            index=app_id,
            on_complete=transaction.OnComplete.NoOpOC,
            app_args=[action_arg],
            accounts=accounts
        )
        
        signed_txn = txn.sign(sender_sk)
        tx_id = self.algod_client.send_transaction(signed_txn)
        transaction.wait_for_confirmation(self.algod_client, tx_id, 4)
        logger.info(f"Bond Action '{action_arg}' executed on App {app_id} by {sender_addr}")
        return True

    def check_financial_health(self, app_id: int) -> dict:
        """
        Checks if the contract account has enough funds for operations.
        Returns detailed status dict.
        """
        try:
            app_info = self.algod_client.application_info(app_id)
            app_addr = app_info['params']['application-account']
            acct_info = self.algod_client.account_info(app_addr)
            
            balance = acct_info['amount']
            min_balance = acct_info['min-balance']
            
            # Safe buffer for ~10 inner transactions (2000 * 10 = 20000)
            safe_buffer = 20000 
            target = min_balance + safe_buffer
            
            status = {
                "app_id": app_id,
                "address": app_addr,
                "balance": balance,
                "min_balance": min_balance,
                "is_healthy": balance >= target,
                "is_critical": balance < min_balance,
                "shortfall": target - balance if balance < target else 0
            }
            
            if status["is_critical"]:
                logger.critical(f"App {app_id} is UNDERFUNDED! Bal: {balance} < Min: {min_balance}")
            elif not status["is_healthy"]:
                logger.warning(f"App {app_id} is low on funds. Bal: {balance} < Target: {target}")
            else:
                logger.info(f"App {app_id} is healthy. Bal: {balance}")
                
            return status
            
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"error": str(e)}
