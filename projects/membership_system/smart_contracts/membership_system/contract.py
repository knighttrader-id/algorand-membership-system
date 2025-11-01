from algopy import (
    ARC4Contract,
    arc4,
    gtxn,
    Global,
    Txn,
    UInt64,
    LocalState,
    Account,
)

# --- ARC-4 Event Definition (Removed for simplicity) ---

class MembershipContract(ARC4Contract):
    """
    A simple membership contract built with Algopy and ARC4.

    Members pay a fee and gain a membership for a set number of rounds,
    tracked in their local state.
    """

    def __init__(self) -> None:
        # --- APPLICATION LOCAL STATE ---
        # Key to store the expiration round for each member
        # The value is an UInt64 representing the expiration round number
        self.expiration_round = LocalState(
            UInt64,
            key="exp_r",
            description="Round number when membership expires"
        )

    @arc4.abimethod(create="allow")
    def create_app(self) -> None:
        """
        The method called when the application is deployed.
        A simple initializer that takes no parameters.
        """
        # Note: Global state initialization would go here if needed.
        pass

    @arc4.abimethod(allow_actions=["OptIn", "NoOp"])
    def join_membership(
        self,
        payment: gtxn.PaymentTransaction,
        member: Account,
    ) -> arc4.Bool:
        """
        Allows a user to join or renew their membership.
        This method must be called in an atomic group with a Payment transaction.

        Args:
            payment: The payment transaction to cover the membership fee.
            member: The account becoming a member (must be Txn.sender).
        Returns:
            True if membership was successfully joined/renewed.
        """

        # 1. Assert Payment Details
        # Payment must be sent by the application caller (Txn.sender)
        assert payment.sender == Txn.sender, "Payment sender must match app caller"

        # Payment must be sent to this application's address
        assert payment.receiver == Global.current_application_address, "Payment receiver must be the application"

        # Payment amount must match the required fee
        assert payment.amount == UInt64(1_000_000), "Payment amount must be 1000000 microAlgos"

        # The 'member' account must be the transaction sender
        assert member == Txn.sender, "Member account must be the transaction sender"

        # 2. Calculate new expiration round
        # Membership is valid from the *current* round plus the duration.
        new_expiration_round = Global.round + UInt64(1000)

        # 3. Update the sender's local state
        # The ARC4 ABI method setup ensures the 'member' account is available for
        # LocalState access. This line will attempt to write the new expiration round.
        self.expiration_round[member] = new_expiration_round

        # 4. No event emission (Removed for simplicity)

        return arc4.Bool(True)

    @arc4.abimethod(readonly=True)
    def is_member(self, member: Account) -> arc4.Bool:
        """
        Checks if the given account currently has an active membership.

        Args:
            member: The account to check.
        Returns:
            True if the current round is less than the expiration round, False otherwise.
        """
        
        # Try to get the expiration round from local state for the member account.
        # maybe_get returns the value and a boolean indicating if the key exists.
        current_expiration_round, exists = self.expiration_round.maybe(member)

        # The user is NOT a member if:
        # a) The local state key doesn't exist (i.e., they haven't opted in or paid).
        # b) The stored expiration round is less than the current round.
        if not exists or current_expiration_round < Global.round:
            return arc4.Bool(False)
        
        return arc4.Bool(True)

    @arc4.abimethod(readonly=True)
    def get_expiration_round(self, member: Account) -> arc4.UInt64:
        """
        Returns the expiration round number for the given member.
        Returns 0 if no membership data is found.
        """
        
        expiration_round, exists = self.expiration_round.maybe(member)

        if not exists:
            # Return 0 if the account hasn't opted-in or the key hasn't been set
            return arc4.UInt64(0)

        return arc4.UInt64(expiration_round)
