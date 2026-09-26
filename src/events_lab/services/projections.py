from ..models.events import Account


def balances(accounts: list[Account]) -> dict[str, int]:
    return {account.id: account.balance for account in accounts}
