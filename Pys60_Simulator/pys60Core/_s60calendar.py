"""Persistent desktop backend for the original S60 3rd edition wrapper."""

import copy
import datetime as dt
import time
import _device

rep_open, rep_private, rep_restricted = 0, 1, 2
(
    entry_type_appt,
    entry_type_event,
    entry_type_anniv,
    entry_type_todo,
    entry_type_reminder,
) = range(5)
(
    appts_inc_filter,
    events_inc_filter,
    annivs_inc_filter,
    todos_inc_filter,
    reminders_inc_filter,
) = (1, 2, 4, 8, 16)


class Database:
    def __init__(self, filename=None, mode=None):
        self.store = _device.Store(
            _device.database_path(filename, "calendar.sqlite"),
            "c" if filename is None else mode,
        )

    def __iter__(self):
        return iter(self.store.ids())

    def __getitem__(self, key):
        return self.get_entry(key)

    def entry_count(self):
        return len(self.store.ids())

    def delete_entry(self, key):
        self.store.delete(key)

    def get_entry(self, key):
        return Entry(self, key, self.store.get(key))

    def add_entry(self, kind):
        return Entry(
            self,
            0,
            dict(
                type=kind,
                content="",
                description="",
                location="",
                priority=0,
                replication=rep_open,
                start_datetime=None,
                end_datetime=None,
                last_modified=0.0,
                crossed_out_date=None,
                alarm_datetime=None,
                repeat_data={"type": "no_repeat"},
            ),
        )

    def monthly_instances(self, month, filter=0):
        start = dt.datetime.fromtimestamp(month).replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        end = (start.replace(day=28) + dt.timedelta(days=4)).replace(day=1)
        return self.find_instances(
            start.timestamp(), end.timestamp() - 0.000001, "", filter
        )

    def daily_instances(self, day, filter=0):
        start = dt.datetime.fromtimestamp(day).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        return self.find_instances(
            start.timestamp(),
            (start + dt.timedelta(days=1)).timestamp() - 0.000001,
            "",
            filter,
        )

    def find_instances(self, start, end, search="", filter=0):
        if end < start:
            raise ValueError("end date before start date")
        start = (
            dt.datetime.fromtimestamp(start)
            .replace(hour=0, minute=0, second=0, microsecond=0)
            .timestamp()
        )
        end = (
            dt.datetime.fromtimestamp(end).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            + dt.timedelta(days=1)
        ).timestamp() - 0.000001
        result = []
        for key in self:
            entry = self.get_entry(key)
            if filter and not filter & (1 << entry.type()):
                continue
            if (
                search.casefold()
                not in (
                    entry.content()
                    + "\n"
                    + entry.description()
                    + "\n"
                    + entry.location()
                ).casefold()
            ):
                continue
            for stamp in entry.instances(start, end):
                result.append({"id": key, "datetime": stamp})
        return sorted(result, key=lambda x: (x["datetime"], x["id"]))

    def export_vcals(self, ids):
        if not isinstance(ids, tuple) or not ids:
            raise TypeError("nonempty tuple of IDs expected")
        import base64, json

        lines = ["BEGIN:VCALENDAR", "VERSION:1.0"]
        for key in ids:
            entry = self.get_entry(key)
            kind = "VTODO" if entry.type() == entry_type_todo else "VEVENT"
            lines += ["BEGIN:" + kind, "UID:" + str(key)]
            for keyname, tag in [
                ("content", "SUMMARY"),
                ("description", "DESCRIPTION"),
                ("location", "LOCATION"),
            ]:
                lines.append(
                    tag
                    + ":"
                    + entry.data[keyname]
                    .replace("\\", "\\\\")
                    .replace("\n", "\\n")
                    .replace(";", "\\;")
                    .replace(",", "\\,")
                )
            for keyname, tag in [
                ("start_datetime", "DTSTART"),
                ("end_datetime", "DTEND"),
            ]:
                if entry.data[keyname] is not None:
                    lines.append(
                        tag
                        + ":"
                        + dt.datetime.fromtimestamp(
                            entry.data[keyname], dt.timezone.utc
                        ).strftime("%Y%m%dT%H%M%SZ")
                    )
            lines.append(
                "X-PYS60-DATA:"
                + base64.b64encode(json.dumps(entry.data).encode("utf-8")).decode(
                    "ascii"
                )
            )
            lines.append("END:" + kind)
        return ("\r\n".join(lines + ["END:VCALENDAR"]) + "\r\n").encode("utf-8")

    def import_vcals(self, text):
        import re, base64, json

        if isinstance(text, bytes):
            text = text.decode("utf-8")
        result = []
        for kind, block in re.findall(
            r"BEGIN:(VEVENT|VTODO)\s*(.*?)END:\1", text, re.S
        ):
            entry = self.add_entry(
                entry_type_todo if kind == "VTODO" else entry_type_appt
            )
            for line in block.splitlines():
                if ":" not in line:
                    continue
                tag, value = line.split(":", 1)
                if tag == "X-PYS60-DATA":
                    decoded = json.loads(base64.b64decode(value))
                    if not isinstance(decoded, dict) or set(decoded) != set(entry.data):
                        raise ValueError("invalid calendar data")
                    entry.data = decoded
                    break
                if tag in ("SUMMARY", "DESCRIPTION", "LOCATION"):
                    entry.data[
                        {
                            "SUMMARY": "content",
                            "DESCRIPTION": "description",
                            "LOCATION": "location",
                        }[tag]
                    ] = (
                        value.replace("\\n", "\n")
                        .replace("\\;", ";")
                        .replace("\\,", ",")
                        .replace("\\\\", "\\")
                    )
                if tag in ("DTSTART", "DTEND", "DUE"):
                    date = dt.datetime.strptime(value.rstrip("Z"), "%Y%m%dT%H%M%S")
                    if value.endswith("Z"):
                        date = date.replace(tzinfo=dt.timezone.utc)
                    entry.data[
                        "start_datetime" if tag == "DTSTART" else "end_datetime"
                    ] = date.timestamp()
            entry.commit()
            result.append(entry.key)
        if not result:
            raise ValueError("invalid vCalendar")
        return result


class Entry:
    def __init__(self, db, key, data):
        self.db, self.key, self.data = db, key, data

    def unique_id(self):
        return self.key

    def originating_entry(self):
        return 1

    def commit(self):
        if self.data["start_datetime"] is None and self.type() != entry_type_todo:
            raise RuntimeError("entry time not set")
        self.data["last_modified"] = time.time()
        self.key = self.db.store.put(self.key, self.data)

    def set_priority(self, value):
        if not isinstance(value, int):
            raise TypeError("integer expected")
        if value < 0 or value > 255:
            raise ValueError("illegal priority")
        self.data["priority"] = value

    def set_replication(self, value):
        self.data["replication"] = value

    def set_crossed_out(self, value, stamp):
        if self.type() != entry_type_todo:
            raise TypeError("cross out property is valid only for todo entries")
        self.data["crossed_out_date"] = float(stamp) if value else None

    def crossed_out_date(self):
        if self.type() != entry_type_todo:
            raise TypeError("cross out property is valid only for todo entries")
        return self.data["crossed_out_date"]

    def set_start_and_end_datetime(self, start, end):
        start, end = float(start), float(end)
        if end < start:
            raise ValueError("end date before start date")
        if self.type() in (entry_type_event, entry_type_anniv):
            start = (
                dt.datetime.fromtimestamp(start)
                .replace(hour=0, minute=0, second=0, microsecond=0)
                .timestamp()
            )
            end = (
                dt.datetime.fromtimestamp(end)
                .replace(hour=0, minute=0, second=0, microsecond=0)
                .timestamp()
            )
        self.data.update(start_datetime=start, end_datetime=end)

    def make_undated(self):
        self.data.update(start_datetime=None, end_datetime=None)

    def cancel_alarm(self):
        self.data["alarm_datetime"] = None

    def set_alarm(self, stamp):
        stamp = float(stamp)
        start = self.data["start_datetime"]
        if start is None or stamp > start or start - stamp > 1001 * 86400:
            raise ValueError("illegal alarm time")
        self.data["alarm_datetime"] = stamp

    def set_repeat_data(self, repeat):
        if not isinstance(repeat, dict):
            raise TypeError("dictionary expected")
        repeat = copy.deepcopy(repeat)
        kind = repeat.get("type")
        kinds = (
            "daily",
            "weekly",
            "monthly_by_dates",
            "monthly_by_days",
            "yearly_by_date",
            "yearly_by_day",
            "no_repeat",
        )
        if kind not in kinds:
            raise ValueError("illegal repeat type")
        if kind == "no_repeat":
            self.data["repeat_data"] = {"type": "no_repeat"}
            return
        repeat["start"] = float(repeat["start"])
        repeat["end"] = None if repeat["end"] is None else float(repeat["end"])
        if repeat["end"] is not None and repeat["end"] < repeat["start"]:
            raise ValueError("illegal repeat end")
        repeat.setdefault("interval", 1)
        if not isinstance(repeat["interval"], int) or repeat["interval"] < 1:
            raise ValueError("illegal interval")
        repeat["exceptions"] = [float(t) for t in repeat.get("exceptions", [])]
        date = dt.datetime.fromtimestamp(repeat["start"])
        if kind == "weekly":
            repeat.setdefault("days", [date.weekday()])
        if kind == "monthly_by_dates":
            repeat.setdefault("days", [date.day - 1])
        if kind in ("weekly", "monthly_by_dates"):
            limit = 6 if kind == "weekly" else 30
            if not repeat["days"] or any(
                not isinstance(d, int) or d < 0 or d > limit for d in repeat["days"]
            ):
                raise ValueError("illegal repeat days")
        if kind in ("monthly_by_days", "yearly_by_day"):
            repeat.setdefault(
                "days",
                (
                    [{"week": (date.day - 1) // 7, "day": date.weekday()}]
                    if kind == "monthly_by_days"
                    else {
                        "week": (date.day - 1) // 7,
                        "day": date.weekday(),
                        "month": date.month - 1,
                    }
                ),
            )
            for day in (
                repeat["days"] if kind == "monthly_by_days" else [repeat["days"]]
            ):
                if (
                    not 0 <= day["day"] <= 6
                    or not 0 <= day["week"] <= 4
                    or ("month" in day and not 0 <= day["month"] <= 11)
                ):
                    raise ValueError("illegal repeat day")
        self.data["repeat_data"] = repeat

    def instances(self, start, end):
        stamp = self.data["start_datetime"]
        if stamp is None:
            return []
        repeat = self.data["repeat_data"]
        if repeat["type"] == "no_repeat":
            return [stamp] if start <= stamp <= end else []
        from dateutil import rrule as rr

        kind = repeat["type"]
        frequency = {
            "daily": rr.DAILY,
            "weekly": rr.WEEKLY,
            "monthly_by_dates": rr.MONTHLY,
            "monthly_by_days": rr.MONTHLY,
            "yearly_by_date": rr.YEARLY,
            "yearly_by_day": rr.YEARLY,
        }[kind]
        first = dt.datetime.fromtimestamp(repeat["start"])
        clock = dt.datetime.fromtimestamp(stamp)
        first = first.replace(hour=clock.hour, minute=clock.minute, second=clock.second)
        kwargs = dict(dtstart=first, interval=repeat["interval"])
        if repeat["end"] is not None:
            kwargs["until"] = dt.datetime.fromtimestamp(repeat["end"]).replace(
                hour=23, minute=59, second=59
            )
        if kind == "weekly":
            kwargs["byweekday"] = repeat["days"]
        if kind == "monthly_by_dates":
            kwargs["bymonthday"] = [d + 1 for d in repeat["days"]]
        if kind in ("monthly_by_days", "yearly_by_day"):
            days = repeat["days"] if kind == "monthly_by_days" else [repeat["days"]]
            kwargs["byweekday"] = [
                rr.weekday(d["day"], -1 if d["week"] == 4 else d["week"] + 1)
                for d in days
            ]
            if kind == "yearly_by_day":
                kwargs["bymonth"] = days[0]["month"] + 1
        excluded = {dt.datetime.fromtimestamp(v).date() for v in repeat["exceptions"]}
        return [
            d.timestamp()
            for d in rr.rrule(frequency, **kwargs).between(
                dt.datetime.fromtimestamp(start),
                dt.datetime.fromtimestamp(end),
                inc=True,
            )
            if d.date() not in excluded
        ]


def _getter(key):
    return lambda self: copy.deepcopy(self.data[key])


def _setter(key):
    return lambda self, value: self.data.__setitem__(key, str(value))


for _key in (
    "type",
    "content",
    "description",
    "location",
    "priority",
    "replication",
    "start_datetime",
    "end_datetime",
    "last_modified",
    "alarm_datetime",
    "repeat_data",
):
    setattr(Entry, _key, _getter(_key))
for _key in ("content", "description", "location"):
    setattr(Entry, "set_" + _key, _setter(_key))


def open(filename=None, mode=None):
    return Database(filename, mode)
