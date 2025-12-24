import json
import logging
import requests
from typing import Dict, Any, Optional, List

from algosdk.v2client import algod, indexer
from algosdk import account, mnemonic, transaction
from algosdk.transaction import AssetConfigTxn, AssetTransferTxn

from app.config import Config

logger = logging.getLogger(__name__)

class GNFTService:
    def __init__(self):
        self.algod_client = algod.AlgodClient(
            Config.ALGORAND_ALGOD_TOKEN, 
            Config.ALGORAND_ALGOD_ADDRESS
        )
        self.indexer_client = indexer.IndexerClient(
            Config.ALGORAND_INDEXER_TOKEN, 
            Config.ALGORAND_INDEXER_ADDRESS
        )
        
        self.ipfs_api_url = Config.IPFS_API_URL
        # Basic check if IPFS config is valid
        if not self.ipfs_api_url:
             logger.warning("IPFS_API_URL not set. IPFS uploads will fail.")

        self.platform_account = None
        if Config.ALGORAND_MNEMONIC:
            try:
                self.platform_private_key = mnemonic.to_private_key(Config.ALGORAND_MNEMONIC)
                self.platform_address = account.address_from_private_key(self.platform_private_key)
                logger.info(f"Initialized GNFTService with platform address: {self.platform_address}")
            except Exception as e:
                logger.error(f"Failed to load platform wallet: {e}")

    def upload_metadata_to_ipfs(self, metadata: Dict[str, Any]) -> Optional[str]:
        """
        Uploads JSON metadata to local IPFS node.
        Returns the IPFS hash (CID).
        """
        if not self.ipfs_api_url:
            logger.error("IPFS API URL not configured.")
            return None

        try:
            # IPFS /api/v0/add expects multipart/form-data
            # We convert the JSON metadata to a string file-like object
            files = {
                'file': ('metadata.json', json.dumps(metadata), 'application/json')
            }
            
            response = requests.post(f"{self.ipfs_api_url}/add", files=files)
            response.raise_for_status()
            
            result = response.json()
            # Result format: {'Name': 'metadata.json', 'Hash': 'Qm...', 'Size': '...'}
            
            if 'Hash' in result:
                cid = result['Hash']
                logger.info(f"Uploaded metadata to IPFS with CID: {cid}")
                return cid
            else:
                logger.error(f"IPFS upload response missing Hash: {result}")
                return None
        except Exception as e:
            logger.error(f"Error uploading to IPFS: {e}")
            return None

    
    def _create_arc69_note(self, metadata: Dict[str, Any]) -> bytes:
        """
        Creates an ARC-69 compliant note field.
        Format: {"standard": "arc69", ...properties}
        """
        arc69_payload = {
            "standard": "arc69",
            **metadata
        }
        return json.dumps(arc69_payload).encode()
        
    def create_master_nft(self, 
                          asset_name: str, 
                          unit_name: str, 
                          metadata_hash: str, 
                          url: str,
                          arc69_metadata: Optional[Dict[str, Any]] = None) -> Optional[int]:
        """
        Creates a 'Master' NFT (Total=1, Decimals=0).
        Returns the Asset ID.
        """
        if not self.platform_address:
            logger.error("Platform wallet not configured.")
            return None

        try:
            params = self.algod_client.suggested_params()
            note = self._create_arc69_note(arc69_metadata) if arc69_metadata else None
            
            # Create AssetConfigTxn
            txn = AssetConfigTxn(
                sender=self.platform_address,
                sp=params,
                total=1,
                default_frozen=False,
                unit_name=unit_name,
                asset_name=asset_name,
                manager=self.platform_address,
                reserve=self.platform_address,
                freeze=self.platform_address,
                clawback=self.platform_address,
                url=url,
                metadata_hash=metadata_hash.encode() if metadata_hash else None,
                decimals=0,
                strict_empty_address_check=False,
                note=note
            )

            # Sign and submit
            signed_txn = txn.sign(self.platform_private_key)
            tx_id = self.algod_client.send_transaction(signed_txn)
            
            # Wait for confirmation
            confirmed_txn = transaction.wait_for_confirmation(self.algod_client, tx_id, 4)
            asset_id = confirmed_txn["asset-index"]
            
            logger.info(f"Created Master NFT '{asset_name}' with ID: {asset_id}")
            return asset_id

        except Exception as e:
            logger.error(f"Failed to create Master NFT: {e}")
            return None

    def mint_pack_nft(self, 
                      asset_name: str, 
                      unit_name: str, 
                      total_supply: int, 
                      metadata_hash: str, 
                      url: str,
                      arc69_metadata: Optional[Dict[str, Any]] = None) -> Optional[int]:
        """
        Creates a 'Pack' NFT (Total=Suppy, Decimals=0).
        Used for selling packs of seeds.
        """
        if not self.platform_address:
            logger.error("Platform wallet not configured.")
            return None

        try:
            params = self.algod_client.suggested_params()
            note = self._create_arc69_note(arc69_metadata) if arc69_metadata else None
            
            txn = AssetConfigTxn(
                sender=self.platform_address,
                sp=params,
                total=total_supply,
                default_frozen=False,
                unit_name=unit_name,
                asset_name=asset_name,
                manager=self.platform_address,
                reserve=self.platform_address,
                freeze=self.platform_address,
                clawback=self.platform_address,
                url=url,
                metadata_hash=metadata_hash.encode() if metadata_hash else None,
                decimals=0, 
                strict_empty_address_check=False,
                note=note
            )

            signed_txn = txn.sign(self.platform_private_key)
            tx_id = self.algod_client.send_transaction(signed_txn)
            
            confirmed_txn = transaction.wait_for_confirmation(self.algod_client, tx_id, 4)
            asset_id = confirmed_txn["asset-index"]
            
            logger.info(f"Created Pack NFT '{asset_name}' (Total: {total_supply}) with ID: {asset_id}")
            return asset_id

        except Exception as e:
            logger.error(f"Failed to mint Pack NFT: {e}")
            return None
    
    def opt_in_asset(self, asset_id: int) -> bool:
        """
        Opts the platform account into an asset (if needed).
        Usually the creator is opted in automatically, but this is useful for other accounts.
        """
        # Logic to opt-in logic would go here if we were managing multiple wallets
        # For the creator, it's auto-opted.
        pass

    def get_asset_info(self, asset_id: int) -> Dict[str, Any]:
        """
        Retrieves asset information from the indexer.
        """
        try:
            response = self.indexer_client.asset_info(asset_id)
            return response.get("asset", {})
        except Exception as e:
            logger.error(f"Failed to get asset info: {e}")
            return {}
