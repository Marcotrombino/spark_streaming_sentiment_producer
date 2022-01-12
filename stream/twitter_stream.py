from typing import Callable, Any, Optional
import os
import json
import requests
from dotenv import load_dotenv, find_dotenv

STREAM_URL = "https://api.twitter.com/2/tweets/search/stream"
RULES_URL = "https://api.twitter.com/2/tweets/search/stream/rules"


class TwitterStream:
    bearer_token: str = ""

    url: str = ""
    query_params: dict = {}

    rules: dict = {}

    callback_func: Callable = lambda t: t

    def __init__(self):
        load_dotenv(find_dotenv())
        self.bearer_token = os.getenv("BEARER_TOKEN")

    def __set_bearer_oauth__(self, req: Any):
        req.headers["Authorization"] = f"Bearer {self.bearer_token}"
        req.headers["User-Agent"] = "v2FilteredStreamPython"
        return req

    def __get_rules__(self):
        response = requests.get(RULES_URL, auth=self.__set_bearer_oauth__)
        if response.status_code != 200:
            raise Exception("Cannot get rules (HTTP {}): {}".format(response.status_code, response.text))
        print(json.dumps(response.json()))
        return response.json()

    def __delete_all_rules__(self, rules):
        if rules is None or "data" not in rules:
            return None

        ids = list(map(lambda rule: rule["id"], rules["data"]))
        payload = {"delete": {"ids": ids}}
        response = requests.post(
            RULES_URL,
            auth=self.__set_bearer_oauth__,
            json=payload
        )
        if response.status_code != 200:
            raise Exception(
                "Cannot delete rules (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )
        print(json.dumps(response.json()))

    def __set_rules__(self, delete):
        # You can adjust the rules if needed
        sample_rules = self.rules
        payload = {"add": sample_rules}
        response = requests.post(
            RULES_URL,
            auth=self.__set_bearer_oauth__,
            json=payload,
        )
        if response.status_code != 201:
            raise Exception(
                "Cannot add rules (HTTP {}): {}".format(response.status_code, response.text)
            )
        print(json.dumps(response.json()))

    def __get_stream__(self, set):
        response = requests.get(
            STREAM_URL,
            auth=self.__set_bearer_oauth__,
            params=self.query_params,
            stream=True,
        )
        print(response.url)
        # print(response.url)
        # print(response.status_code)
        if response.status_code != 200:
            raise Exception(
                "Cannot get stream (HTTP {}): {}".format(
                    response.status_code, response.text
                )
            )
        for response_line in response.iter_lines():
            if response_line:
                json_response = json.loads(response_line)
                # print(json.dumps(json_response, indent=4, sort_keys=True))
                self.callback_func(json_response)

    # ------- configuration methods ------------

    def with_params(self, query_params: dict):
        self.query_params = query_params
        return self

    def with_rules(self, rules: [dict]):
        self.rules = rules
        return self

    def apply(self, func: Callable):
        self.callback_func = func
        return self

    def listen(self):
        rules = self.__get_rules__()
        delete = self.__delete_all_rules__(rules)
        set = self.__set_rules__(delete)
        self.__get_stream__(set)






