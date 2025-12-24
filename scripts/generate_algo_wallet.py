"""
Algorand Wallet Generator
Generates a new Algorand testnet wallet with mnemonic phrase.
Run this script to create credentials for ALGORAND_MNEMONIC in .env
"""
from algosdk import account, mnemonic

def generate_wallet():
    # Generate new account
    private_key, address = account.generate_account()
    
    # Convert private key to mnemonic (25 words)
    mnemonic_phrase = mnemonic.from_private_key(private_key)
    
    print("=" * 60)
    print("       ALGORAND TESTNET WALLET GENERATED")
    print("=" * 60)
    print()
    print(f"ADDRESS: {address}")
    print()
    print("MNEMONIC (25 words - SAVE THIS SECURELY!):")
    print("-" * 60)
    print(mnemonic_phrase)
    print("-" * 60)
    print()
    print("NEXT STEPS:")
    print("1. Copy the mnemonic phrase above")
    print("2. Add to your .env file:")
    print(f'   ALGORAND_MNEMONIC="{mnemonic_phrase}"')
    print()
    print("3. Fund this wallet on Algorand Testnet:")
    print(f"   https://bank.testnet.algorand.network/?account={address}")
    print()
    print("=" * 60)
    
    return address, mnemonic_phrase

if __name__ == "__main__":
    generate_wallet()
