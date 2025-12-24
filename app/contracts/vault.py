from pyteal import *
from typing import Dict

def approval_program():
    """
    Vault Contract for Neuro-Verified Commerce.
    Holds 10% Bond. Triggers AI Audit.
    """
    
    # Global State Keys
    admin_addr = Bytes("admin") # Oracle/Orchestrator
    reserve_addr = Bytes("reserve") # Platform Reserve for fees
    min_bond_bps = Bytes("min_bond") # 1000 = 10%
    
    # Local State (per listing/merchant interaction?) 
    # Actually, usually one app per flow or utilize LocalState on Merchant Account?
    # For simplicity here, assuming App Call with arguments initiates flow.
    
    # Ops
    op_deposit_bond = Bytes("deposit_bond")
    op_refund_bond = Bytes("refund_bond")
    op_lock_listing = Bytes("lock_listing")
    
    # Init
    handle_creation = Seq([
        App.globalPut(admin_addr, Txn.sender()),
        App.globalPut(min_bond_bps, Int(1000)), # 10%
        Approve()
    ])
    
    # Bond Deposit
    # Args: [listing_hash_bytes, listing_price_uint]
    # Payment Transaction must accompany this call.
    listing_hash = Txn.application_args[1]
    listing_price = Btoi(Txn.application_args[2])
    
    valid_payment = And(
        Gtxn[Txn.group_index() - Int(1)].type_enum() == TxnType.Payment,
        Gtxn[Txn.group_index() - Int(1)].receiver() == Global.current_application_address(),
        Gtxn[Txn.group_index() - Int(1)].amount() >= (listing_price * App.globalGet(min_bond_bps)) / Int(10000)
    )
    
    handle_deposit_bond = Seq([
        Assert(valid_payment),
        # Log event for Off-chain Listener (Orchestrator)
        # Format: G-NFT_AUDIT_REQ: <Sender>: <ListingHash>
        Log(Concat(Bytes("G-NFT_AUDIT_REQ:"), Txn.sender(), Bytes(":"), listing_hash)),
        Approve()
    ])
    
    # Refund Bond / Fail Audit
    # Callable only by Admin (Orchestrator)
    # Args: [merchant_addr, refund_amount]
    merchant_addr = Txn.application_args[1]
    refund_amt = Btoi(Txn.application_args[2])
    
    is_admin = Txn.sender() == App.globalGet(admin_addr)
    
    handle_refund = Seq([
        Assert(is_admin),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.receiver: merchant_addr,
            TxnField.amount: refund_amt,
            TxnField.fee: Int(0) # Pooled fees
        }),
        InnerTxnBuilder.Submit(),
        Approve()
    ])
    
    # Payout to Seller (Harvest Confirmed)
    # Callable only by Admin (Orchestrator/Shipping Service)
    # Args: [seller_addr, total_amt, commission_bps]
    # Sends (total_amt - comm) to Seller, comm to Reserve
    seller_addr = Txn.application_args[1]
    total_sales_amt = Btoi(Txn.application_args[2])
    commission_bps = Btoi(Txn.application_args[3])
    
    op_confirm_delivery = Bytes("confirm_delivery")
    
    comm_amt = (total_sales_amt * commission_bps) / Int(10000)
    seller_payout = total_sales_amt - comm_amt
    
    handle_payout = Seq([
        Assert(is_admin),
        # Payout Seller
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.receiver: seller_addr,
            TxnField.amount: seller_payout,
            TxnField.fee: Int(0)
        }),
        InnerTxnBuilder.Submit(),
        # Pay Reserve (Commission)
        If(comm_amt > Int(0)).Then(
            Seq([
                InnerTxnBuilder.Begin(),
                InnerTxnBuilder.SetFields({
                    TxnField.type_enum: TxnType.Payment,
                    TxnField.receiver: App.globalGet(reserve_addr), # Assuming reserve_addr is set? Or use admin for now
                    TxnField.amount: comm_amt,
                    TxnField.fee: Int(0)
                }),
                InnerTxnBuilder.Submit()
            ])
        ),
        Log(Concat(Bytes("FUNDS_RELEASED:"), seller_addr, Bytes(":"), Itob(seller_payout))),
        Approve()
    ])
    
    program = Cond(
        [Txn.application_id() == Int(0), handle_creation],
        [Txn.on_completion() == OnComplete.DeleteApplication, Return(Txn.sender() == App.globalGet(admin_addr))],
        [Txn.on_completion() == OnComplete.UpdateApplication, Return(Txn.sender() == App.globalGet(admin_addr))],
        [Txn.application_args[0] == op_deposit_bond, handle_deposit_bond],
        [Txn.application_args[0] == op_refund_bond, handle_refund],
        [Txn.application_args[0] == op_confirm_delivery, handle_payout],
    )
    
    return compileTeal(program, Mode.Application, version=6)

def clear_state_program():
    return compileTeal(Approve(), Mode.Application, version=6)

if __name__ == "__main__":
    with open("vault_approval.teal", "w") as f:
        f.write(approval_program())
    with open("vault_clear.teal", "w") as f:
        f.write(clear_state_program())
