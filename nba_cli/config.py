from __future__ import annotations

import os

API_BASE_URL_V1 = "https://api.balldontlie.io/v1"
ENV_API_KEY = "BALLDONTLIE_API_KEY"


def get_api_key() -> str:
    api_key = os.getenv(ENV_API_KEY)
    if not api_key:
        raise RuntimeError(
            f"Missing API key. Set environment variable {ENV_API_KEY}."
        )
    return api_key
