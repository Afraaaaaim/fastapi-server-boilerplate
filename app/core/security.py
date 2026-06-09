import hashlib
import secrets


def hash_key(key: str) -> str:
    """SHA-256 hash an API key. Never store or compare raw keys."""
    return hashlib.sha256(key.encode()).hexdigest()


def build_key_set(raw_keys: list[str]) -> set[str]:
    """Pre-hash all valid API keys at startup for O(1) lookup."""
    return {hash_key(k) for k in raw_keys if k.strip()}


def verify_key(raw_key: str, hashed_keys: set[str]) -> bool:
    """Verify an incoming raw key against the set of hashed valid keys."""
    return hash_key(raw_key) in hashed_keys


def extract_client_id(raw_key: str) -> str:
    """Return first 8 chars of the key hash as a safe client identifier."""
    return hash_key(raw_key)[:8]


def generate_key() -> str:
    """Generate a cryptographically secure random API key."""
    return secrets.token_urlsafe(32)