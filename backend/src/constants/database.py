from enum import Enum

class SessionStatus(Enum):
    ACTIVE = 'active'
    EXPIRED = 'expired'
    REVOKED = 'revoked'
