import os


API_KEY = os.environ.get("SCHOOL_INFO_KEY")
W_API_KEY = os.environ.get("W_API_KEY")
COVID_API_KEY = os.environ.get("COVID_API_KEY")

__all__ = (
    "API_KEY",
    "W_API_KEY",
    "COVID_API_KEY"
)
