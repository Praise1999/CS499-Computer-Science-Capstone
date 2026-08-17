"""Configuration values for the Grazioso Salvare dashboard."""

import os

from dotenv import load_dotenv


load_dotenv()


USERNAME = os.getenv("MONGO_USERNAME")
PASSWORD = os.getenv("MONGO_PASSWORD")


if not USERNAME:
    raise ValueError(
        "MONGO_USERNAME was not found in the environment."
    )

if not PASSWORD:
    raise ValueError(
        "MONGO_PASSWORD was not found in the environment."
    )