from pyteal import (
    App, Bytes, Int, Seq, Assert, InnerTxnBuilder, TxnField, Txn, If, Cond, 
    Btoi, Approve, OnComplete, TxnType, Global, compileTeal, Mode, Reject
)

def approval_program():
    """
    Breeder Bond Contract
    
    Roles:
    - Breeder: The creator/depositor of the bond.
    - Admin: The platform account that controls release/slash.
    
    Logic:
    - Deposit: Implicitly handled by funding the contract account.
    - Release: Admin calls 'release' -> 100% of funds sent back to Breeder.
    - Slash: Admin calls 'slash' -> Funds sent to Admin (or Burn Address).
    """
    
    # Roles
    breeder = App.globalGet(Bytes("breeder"))
    admin = App.globalGet(Bytes("admin"))
    
    # Initialization
    # Args: [breeder_addr, admin_addr]
    handle_setup = Seq([
        App.globalPut(Bytes("breeder"), Txn.application_args[0]),
        App.globalPut(Bytes("admin"), Txn.application_args[1]),
        Approve()
    ])
    
    # Admin-only Logic
    def check_admin(sender):
        return Sender == admin
        
    # Validation helpers
    is_admin = Txn.sender() == admin
    
    # Release Bond to Breeder
    handle_release = Seq([
        Assert(is_admin),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.receiver: breeder,
            TxnField.amount: Int(0), 
            TxnField.close_remainder_to: breeder,
            TxnField.rekey_to: Global.zero_address()
        }),
        InnerTxnBuilder.Submit(),
        Approve()
    ])

    # Slash Bond (Confiscate to Admin)
    handle_slash = Seq([
        Assert(is_admin),
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
            TxnField.type_enum: TxnType.Payment,
            TxnField.receiver: admin,
            TxnField.amount: Int(0), 
            TxnField.close_remainder_to: admin,
            TxnField.rekey_to: Global.zero_address()
        }),
        InnerTxnBuilder.Submit(),
        Approve()
    ])

    # Handle NoOp Calls
    handle_noop = Cond(
        [Txn.application_args.length() == Int(0), Approve()], 
        [Txn.application_args[0] == Bytes("release_bond"), handle_release],
        [Txn.application_args[0] == Bytes("slash_bond"), handle_slash]
    )

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
    with open("bond_approval.teal", "w") as f:
        compiled = compileTeal(approval_program(), mode=Mode.Application, version=6)
        f.write(compiled)

    with open("bond_clear.teal", "w") as f:
        compiled = compileTeal(clear_state_program(), mode=Mode.Application, version=6)
        f.write(compiled)
