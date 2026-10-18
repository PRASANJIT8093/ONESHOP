


token_blocklist=set()


def add_token(token:str):
    token_blocklist.add(token)


def is_token_blocklisted(token: str) -> bool:
    return token in token_blocklist
