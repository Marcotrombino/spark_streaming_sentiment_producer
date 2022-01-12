import traceback
from typing import Any, Callable, Type, Tuple


class DictListable:
    def to_dict(self):
        dict_output = {}
        for attribute, value in self.__dict__.items():
            dict_output[attribute] = value
        return dict_output


class NotFunctionException(Exception):
    pass


def get_exc_log():
    return traceback.format_exc()


def safe_factory(
        e: Tuple[Type[BaseException], ...],
        return_value: Any,
        exc_func: Callable = None
) -> Callable:
    def safe_func(attr: Any, r_value: Any = return_value) -> Any:
        try:
            if hasattr(attr, "__call__"):
                return attr()
            else:
                return attr
        except e:
            if exc_func:
                exc_func(e)
            else:
                print(get_exc_log())

            return r_value

    return safe_func
