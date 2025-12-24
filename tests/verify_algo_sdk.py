import sys
import os

# Add app to path
sys.path.append(os.getcwd())

from algosdk import account, mnemonic
from pyteal import compileTeal, Mode

try:
    print("Importing GNFTService...")
    from app.blockchain.gnft_service import GNFTService
    print("GNFTService imported successfully.")
except ImportError as e:
    print(f"Failed to import GNFTService: {e}")
    sys.exit(1)

try:
    print("Importing Smart Contracts...")
    from app.blockchain.escrow_contract import approval_program as escrow_approval, clear_state_program as escrow_clear
    from app.blockchain.bond_contract import approval_program as bond_approval, clear_state_program as bond_clear
    
    print("Compiling Escrow Contract...")
    compiled_escrow = compileTeal(escrow_approval(), mode=Mode.Application, version=6)
    print(f"Escrow Contract compiled successfully (Length: {len(compiled_escrow)} bytes)")

    print("Compiling Bond Contract...")
    compiled_bond = compileTeal(bond_approval(), mode=Mode.Application, version=6)
    print(f"Bond Contract compiled successfully (Length: {len(compiled_bond)} bytes)")
    
except Exception as e:
    print(f"Failed to compile Smart Contracts: {e}")
    sys.exit(1)

print("Blockchain SDK Verification Successful!")
