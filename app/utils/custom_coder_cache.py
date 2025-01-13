from typing import Any

import orjson
from fastapi.encoders import jsonable_encoder
from fastapi_cache import Coder


class ORJsonCoder(Coder):
    # Из документации https://pypi.org/project/fastapi-cache2/

    @classmethod
    def encode(cls, value: Any) -> bytes:
        return orjson.dumps(
            value,
            default=jsonable_encoder,
            option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY,
        )

    @classmethod
    def decode(cls, value: bytes) -> Any:
        return orjson.loads(value)
