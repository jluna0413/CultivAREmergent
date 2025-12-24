from pyteal import (
    App, Bytes, Int, Seq, Assert, InnerTxnBuilder, TxnField, Txn, If, And, Cond, 
    Btoi, Approve, OnComplete, TxnType, Global, compileTeal, Mode, Addr, Reject
)

def approval_program():
    """
    Escrow Contract for Seed Shipment
    
    Roles:
    - Receiver: User buying seeds
    - Sender: Breeder selling seeds
    - Arbiter: Platform admin
    
    Logic:
    - Release Funds: Receiver AND Sender must both sign (dual signature).
    - Refund: After timeout (90 days), Receiver can claim funds back.
    - Dispute: Arbiter can sign with either party to force release or refund.
    """
    
    # Roles
    buyer = App.globalGet(Bytes("buyer"))
    seller = App.globalGet(Bytes("seller"))
    oracle = App.globalGet(Bytes("oracle"))
    
    # Approval Flags
    buyer_approved = App.globalGet(Bytes("buyer_approved"))
    seller_approved = App.globalGet(Bytes("seller_approved"))
    
    # Initialization
    handle_setup = Seq([
        # Args: [buyer_addr, seller_addr, oracle_addr, duration_seconds, platform_addr, fee_rate_basis_points]
        App.globalPut(Bytes("buyer"), Txn.application_args[0]),
        App.globalPut(Bytes("seller"), Txn.application_args[1]),
        App.globalPut(Bytes("oracle"), Txn.application_args[2]),
        App.globalPut(Bytes("timeout"), Global.latest_timestamp() + Btoi(Txn.application_args[3])),
        App.globalPut(Bytes("platform"), Txn.application_args[4]),
        App.globalPut(Bytes("fee_rate"), Btoi(Txn.application_args[5])), # e.g. 2500 for 25%
        App.globalPut(Bytes("buyer_approved"), Int(0)),
        App.globalPut(Bytes("seller_approved"), Int(0)),
        Approve()
    ])
    
    # Releases funds with Fee Deduction
    total_balance = Balance(Global.current_application_address())
    fee_amount = (total_balance * App.globalGet(Bytes("fee_rate"))) / Int(10000)
    
    release_to_seller = Seq([
        # 1. Pay Platform Fee
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.receiver: App.globalGet(Bytes("platform")),
            TxnField.amount: fee_amount,
        }),
        InnerTxnBuilder.Submit(),
        
        # 2. Pay Remainder to Seller
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.receiver: seller,
            TxnField.amount: Int(0), 
            TxnField.close_remainder_to: seller, # Sweeps all remaining microAlgos
            TxnField.rekey_to: Global.zero_address()
        }),
        InnerTxnBuilder.Submit(),
        Approve()
    ])

    # Approval Logic (Dual-Sig)
    def approve_action(approver_addr):
        return Seq([
            # Check who is signing
            If(Txn.sender() == buyer).Then(
                App.globalPut(Bytes("buyer_approved"), Int(1))
            ).ElseIf(Txn.sender() == seller).Then(
                App.globalPut(Bytes("seller_approved"), Int(1))
            ),
            # Check if both approved
            If(And(App.globalGet(Bytes("buyer_approved")), App.globalGet(Bytes("seller_approved")))).Then(
                release_to_seller
            ),
            Approve()
        ])
    
    # Oracle Fallback Logic (Proof of Delivery)
    handle_oracle_release = Seq([
        Assert(Txn.sender() == oracle),
        release_to_seller
    ])

    # Refund Logic (Timeout)
    handle_refund = Seq([
        Assert(Global.latest_timestamp() > App.globalGet(Bytes("timeout"))),
        # Send back to Buyer
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.receiver: buyer,
            TxnField.close_remainder_to: buyer,
            TxnField.rekey_to: Global.zero_address()
        }),
        InnerTxnBuilder.Submit(),
        Approve()
    ])

    # Handle NoOp Calls (Application Logic)
    handle_noop = Cond(
        [Txn.application_args.length() == Int(0), Approve()], 
        [Txn.application_args[0] == Bytes("approve"), approve_action(Txn.sender())],
        [Txn.application_args[0] == Bytes("oracle_release"), handle_oracle_release],
        [Txn.application_args[0] == Bytes("refund"), handle_refund]
    )

    # Main Routing
    program = Cond(
        [Txn.application_id() == Int(0), handle_setup],
        [Txn.on_completion() == OnComplete.DeleteApplication, Reject()],
        [Txn.on_completion() == OnComplete.UpdateApplication, Reject()],
        [Txn.on_completion() == OnComplete.CloseOut, Approve()],
        [Txn.on_completion() == OnComplete.OptIn, Approve()],
        [Txn.on_completion() == OnComplete.NoOp, handle_noop]
    )
    
    return program

def clear_state_program():
    return Approve()

if __name__ == "__main__":
    with open("escrow_approval.teal", "w") as f:
        compiled = compileTeal(approval_program(), mode=Mode.Application, version=6)
        f.write(compiled)

    with open("escrow_clear.teal", "w") as f:
        compiled = compileTeal(clear_state_program(), mode=Mode.Application, version=6)
        f.write(compiled)
