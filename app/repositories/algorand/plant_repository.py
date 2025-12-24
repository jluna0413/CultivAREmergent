from typing import List, Optional, Any, Dict
from datetime import datetime
import json
import base64
from algosdk.v2client import algod
from algosdk import transaction, account, encoding
from app.repositories.interfaces import PlantRepository, PlantDTO, ActivityDTO, PlantCreateDTO, PlantUpdateDTO

class AlgorandPlantRepository(PlantRepository):
    """
    Algorand blockchain implementation of PlantRepository.
    Interacts with a stateful smart contract (Application) to store plant data.
    """
    
    def __init__(self, algod_client: algod.AlgodClient, app_id: int, signer_private_key: str):
        self.client = algod_client
        self.app_id = app_id
        # Debugging key format
        print(f"DEBUG REPO INIT: Key len={len(signer_private_key)} Key={signer_private_key[:10]}...")
        self.signer_sk = signer_private_key # In production, use a wallet provider/signer, not raw key
        self.signer_addr = account.address_from_private_key(signer_private_key)

    async def create(self, plant_data: PlantCreateDTO) -> PlantDTO:
        """
        Create a new plant on-chain via ApplicationCall.
        """
        params = self.client.suggested_params()
        
        # Serialize arguments
        # args: [method_name, name, cultivar_id, metadata_json]
        app_args = [
            b"create_plant",
            plant_data.name.encode("utf-8"),
            (str(plant_data.cultivar_id) if plant_data.cultivar_id else "0").encode("utf-8"),
            json.dumps(plant_data.model_dump(exclude={"user_id", "name", "cultivar_id"}, mode="json")).encode("utf-8")
        ]
        
        # Create transaction
        txn = transaction.ApplicationCallTxn(
            sender=self.signer_addr,
            sp=params,
            index=self.app_id,
            on_complete=transaction.OnComplete.NoOpOC,
            app_args=app_args
        )
        
        # Sign and Send
        signed_txn = txn.sign(self.signer_sk)
        tx_id = self.client.send_transaction(signed_txn)
        
        # Ideally, we wait for confirmation here. 
        # For prototype/mixed mode, we might just return the ID or wait.
        # confirmed_txn = transaction.wait_for_confirmation(self.client, tx_id, 4)
        
        # MOCK RETURN: We can't easily get the return value from the app call logs 
        # without a real node response. 
        # We will return a partial DTO with the TX_ID as the ID.
        
        return PlantDTO(
            id=tx_id, # Using TX ID as temporary Plant ID until confirmed
            user_id=str(plant_data.user_id), 
            name=plant_data.name,
            status_id=plant_data.status_id,
            cultivar_id=plant_data.cultivar_id,
            is_clone=plant_data.is_clone,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

    async def get_by_id(self, plant_id: int | str) -> Optional[PlantDTO]:
        """
        Fetch plant data from smart contract Box Storage or Global State.
        """
        try:
            # Box name could be plant_id (int encoded)
            box_name = encoding.encode_as_bytes(int(plant_id))
            response = self.client.application_box_by_name(self.app_id, box_name)
            box_value = base64.b64decode(response['value'])
            
            # Assuming simple JSON storage in box for prototype
            data = json.loads(box_value.decode("utf-8"))
            return PlantDTO(**data)
        except Exception:
            # Box not found or error
            return None

    async def get_by_user(self, user_id: int) -> List[PlantDTO]:
        """
        Getting by user requires an Indexer or specific local state mapping.
        For prototype, we return empty list as SQL is primary read source.
        """
        return []

    async def update(self, plant_id: int | str, plant_data: PlantUpdateDTO) -> PlantDTO:
        params = self.client.suggested_params()
        app_args = [
            b"update_plant",
            str(plant_id).encode("utf-8"),
            json.dumps(plant_data.model_dump(exclude_unset=True, mode="json")).encode("utf-8")
        ]
        
        txn = transaction.ApplicationCallTxn(
            sender=self.signer_addr,
            sp=params,
            index=self.app_id,
            on_complete=transaction.OnComplete.NoOpOC,
            app_args=app_args
        )
        
        signed_txn = txn.sign(self.signer_sk)
        tx_id = self.client.send_transaction(signed_txn)
        
        # Return approximate state
        return PlantDTO(
            id=str(plant_id),
            user_id="unknown", # Cannot retrieve easily in update
            name=plant_data.name or "Updated",
            status_id=plant_data.status_id or 1,
            updated_at=datetime.now()
        )

    async def delete(self, plant_id: int | str) -> bool:
        params = self.client.suggested_params()
        app_args = [b"delete_plant", str(plant_id).encode("utf-8")]
        
        txn = transaction.ApplicationCallTxn(
            sender=self.signer_addr,
            sp=params,
            index=self.app_id,
            on_complete=transaction.OnComplete.NoOpOC,
            app_args=app_args
        )
        
        signed_txn = txn.sign(self.signer_sk)
        self.client.send_transaction(signed_txn)
        return True

    async def record_activity(
        self,
        plant_id: int | str,
        activity_type: str,
        details: Dict[str, Any]
    ) -> ActivityDTO:
        params = self.client.suggested_params()
        
        app_args = [
            b"record_activity",
            str(plant_id).encode("utf-8"),
            activity_type.encode("utf-8"),
            json.dumps(details).encode("utf-8")
        ]
        
        txn = transaction.ApplicationCallTxn(
            sender=self.signer_addr,
            sp=params,
            index=self.app_id,
            on_complete=transaction.OnComplete.NoOpOC,
            app_args=app_args
        )
        
        signed_txn = txn.sign(self.signer_sk)
        tx_id = self.client.send_transaction(signed_txn)
        
        return ActivityDTO(
            id=tx_id,
            plant_id=str(plant_id),
            activity_type=activity_type,
            activity_name=activity_type,
            timestamp=datetime.now(), # Blockchain time is block time, using local for DTO
            details=details
        )
