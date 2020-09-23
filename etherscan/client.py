import json

import requests

import etherscan
from etherscan.enums.fields_enum import FieldsEnum as fields
from etherscan.utils.parsing import ResponseParser as parser


class Client:
    @staticmethod
    def __load_config(config_path: str) -> dict:
        with open(config_path, "r") as f:
            return json.load(f)

    @staticmethod
    def __auth(func, api_key):
        def wrapper(*args, **kwargs):
            url = (
                f"{fields.PREFIX}"
                f"{func(*args, **kwargs)}"
                f"{fields.API_KEY}"
                f"{api_key}"
            )
            r = requests.get(url)
            return parser.get_result(r)

        return wrapper

    @classmethod
    def from_config(cls, config_path: str, api_key: str):
        config = cls.__load_config(config_path)
        for k, v in config.items():
            if not k.startswith("_"):
                attr = getattr(getattr(etherscan, v), k)
                setattr(cls, k, cls.__auth(attr, api_key))
        return cls