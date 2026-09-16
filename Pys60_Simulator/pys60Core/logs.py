"""Read the same event history used by telephone and messaging."""

import _device

_types = ("call", "sms", "data", "fax", "email", "scheduler")
_modes = ("in", "out", "missed", "fetched", "in_alt", "out_alt")

types = dict((name, index) for index, name in enumerate(_types))
modes = dict((name, index) for index, name in enumerate(_modes))


def log_data(type, start_log=0, num_of_logs=0, mode="in"):
    if type not in _types or mode not in _modes:
        raise RuntimeError("invalid log type or mode")
    if not isinstance(start_log, int) or not isinstance(num_of_logs, int):
        raise TypeError("integer index expected")
    store = _device.Store(_device.data_path("logs.sqlite"))
    result = []
    try:
        for key in reversed(store.ids()):
            entry = store.get(key)
            if entry.pop("_type") == type and entry["direction"] == mode:
                entry["id"] = key
                entry["data"] = entry["data"].encode("latin1")[:500]
                result.append(entry)
    finally:
        store.conn.close()
    return (
        result[start_log : start_log + num_of_logs]
        if num_of_logs
        else result[start_log:]
    )


def raw_log_data():
    return [
        entry
        for type in _types
        for mode in _modes
        for entry in log_data(type, mode=mode)
    ]


def log_data_by_time(type, start_time, end_time, mode="in"):
    return [x for x in log_data(type, mode=mode) if start_time <= x["time"] <= end_time]


def _getter(kind):
    def query(start_log=0, num_of_logs=0, mode="in"):
        return log_data(kind, start_log, num_of_logs, mode)

    return query


calls, sms, data_logs, faxes, emails, scheduler_logs = [_getter(k) for k in _types]
