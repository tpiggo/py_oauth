from dataclasses import dataclass

@dataclass
class TokenInfo:
    granted_authorities: list[str]
    granted_roles: list[str]