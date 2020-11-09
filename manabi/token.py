from typing import Optional

from attr import dataclass
from branca import Branca  # type: ignore

from .util import fromstring


@dataclass
class Token:
    key: str
    ttl_init: int
    ttl_refresh: int

    @classmethod
    def from_config(cls, config: dict):
        return cls(
            config["manabi"]["key"],
            config["manabi"]["ttl_init"],
            config["manabi"]["ttl_refresh"],
        )

    def make(self, path: str) -> str:
        return make_token(self.key, path)

    def check_ttl(self, data: str, ttl: Optional[int] = None) -> Optional[str]:
        try:
            return check_token(self.key, data, ttl)
        except (RuntimeError, ValueError):
            return None

    def check(self, data: str) -> Optional[str]:
        return self.check_ttl(data, self.ttl_init)

    def refresh_check(self, data: str) -> Optional[str]:
        return self.check_ttl(data, self.ttl_refresh)


def make_token(key: str, path: str, now: Optional[int] = None) -> str:
    f = Branca(fromstring(key))
    p = path.encode("UTF-8")
    ct = f.encode(p, now)
    return ct


def check_token(key: str, data: str, ttl=None) -> str:
    f = Branca(fromstring(key))
    return f.decode(data, ttl).decode("UTF-8")
