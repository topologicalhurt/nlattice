import json
from functools import reduce
from operator import getitem


def seek_modify(fn: str, ow, *args) -> None:
    with open(fn, 'r+') as f:
        data = json.load(f)
        reduce(getitem, args[:-1], data)[args[-1]] = ow
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
