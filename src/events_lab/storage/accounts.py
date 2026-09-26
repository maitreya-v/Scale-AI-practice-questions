from ..models.events import Account


class Accounts:
    def __init__(self):
        self.rows: dict[str, Account] = {}

    def apply(self, account_id: str, amount: int) -> Account:
        account = self.rows.setdefault(account_id, Account(account_id))
        account.balance += amount
        account.version += 1
        return account
