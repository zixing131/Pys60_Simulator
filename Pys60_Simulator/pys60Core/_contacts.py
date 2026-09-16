"""SQLite backend for Nokia's original contacts Python wrapper."""
from _compat import text_type as str

from _compat import casefold
import copy
import json
import time
import _device
import e32

_names = "none last_name first_name phone_number_general phone_number_home phone_number_work phone_number_mobile fax_number pager_number email_address postal_address url job_title company_name company_address dtmf_string date note picture thumbnail_image voice_tag speed_dial personal_ringtone po_box extended_address street_address city state postal_code country wvid second_name video_number last_name_reading first_name_reading locationid_indication voip push_to_talk share_view sip_id".split()
globals().update((name, i) for i, name in enumerate(_names))
prefix, suffix = 48, 49
location_none, location_home, location_work = 0, 1, 2
(
    storage_type_text,
    storage_type_store,
    storage_type_contact_item_id,
    storage_type_datetime,
) = range(4)
given_name_value, family_name_value = 268440444, 268440445
vcard_include_x, vcard_ett_format, vcard_exclude_uid = 1, 2, 4
vcard_dec_access_count, vcard_inc_access_count, vcard_import_single_contact = 8, 16, 32
_locks = {}


class Database:
    def __init__(self, filename=None, mode=None):
        self.path = _device.database_path(filename, "contacts.sqlite")
        self.store = _device.Store(self.path, "c" if filename is None else mode)
        import contacts

        self.templates = list(contacts._api_mappings)

    def __iter__(self):
        return iter(self.store.ids())

    def __getitem__(self, key):
        return self.get_entry(key)

    def __delitem__(self, key):
        self.delete_entry(key)

    def entry_count(self):
        return len(self.store.ids())

    def get_entry(self, key):
        return Entry(self, key, self.store.get(key))

    def create_entry(self):
        return Entry(
            self, 0, dict(fields=[], group=False, name="", members=[], modified=0.0)
        )

    def delete_entry(self, key):
        if (self.path, key) in _locks:
            raise e32.SymbianError(-14, "contact is busy")
        self.store.delete(key)
        for group in self.contact_groups():
            data = self.store.get(group)
            if key in data["members"]:
                data["members"].remove(key)
                self.store.put(group, data)

    def field_types(self):
        return ([list(t[0]) for t in self.templates], [t[1] for t in self.templates])

    def field_type_info(self, index):
        import contacts

        kind = contacts._api_mappings[self.templates[index]][0]
        name = contacts.fieldtypereversemap.get(kind, "unknown")
        storage = (
            storage_type_datetime
            if name == "date"
            else storage_type_store if name == "thumbnail_image" else storage_type_text
        )
        return dict(
            name=name.replace("_", " ").title(),
            storagetype=storage,
            vcard_mapping=self.templates[index][1],
        )

    def find(self, term, fields):
        return [
            key
            for key in self
            if any(
                f["storagetype"] == storage_type_text
                and set(fields).intersection(self.templates[f["template"]][0])
                and casefold(term) in casefold(f["value"])
                for f in self.store.get(key)["fields"]
            )
        ]

    def compact(self):
        self.store.compact()

    def compact_recommended(self):
        return 0

    def contact_groups(self):
        return [key for key in self if self.store.get(key)["group"]]

    def contact_group_count(self):
        return len(self.contact_groups())

    def create_contact_group(self):
        item = self.create_entry()
        item.data["group"] = True
        item.commit()
        return item.key

    def _group(self, key):
        data = self.store.get(key)
        if not data["group"]:
            raise RuntimeError("not a group")
        return data

    def contact_group_label(self, key):
        return self._group(key)["name"]

    def contact_group_set_label(self, key, name):
        data = self._group(key)
        data["name"] = name
        self.store.put(key, data)

    def contact_group_ids(self, key):
        return self._group(key)["members"]

    def add_contact_to_group(self, contact, group):
        self.store.get(contact)
        data = self._group(group)
        if contact not in data["members"]:
            data["members"].append(contact)
            self.store.put(group, data)

    def remove_contact_from_group(self, contact, group):
        data = self._group(group)
        data["members"].remove(contact)
        self.store.put(group, data)

    def export_vcards(self, ids, flags):
        if not ids:
            raise ValueError("empty contact id list")
        import contacts

        lines = []
        for key in ids:
            data = self.store.get(key)
            fields = data["fields"]

            def values(kind):
                return [
                    f["value"]
                    for f in fields
                    if contacts._api_mappings[self.templates[f["template"]]][0] == kind
                ]

            escape = (
                lambda s: str(s)
                .replace("\\", "\\\\")
                .replace("\n", "\\n")
                .replace(";", "\\;")
                .replace(",", "\\,")
            )
            last, first = values(last_name), values(first_name)
            lines += [
                "BEGIN:VCARD",
                "VERSION:3.0",
                "N:%s;%s;;;" % (escape(" ".join(last)), escape(" ".join(first))),
                "FN:" + escape(" ".join(last + first)),
            ]
            if not flags & vcard_exclude_uid:
                lines.append("UID:" + str(key))
            mapping = {
                3: "TEL",
                4: "TEL;TYPE=HOME",
                5: "TEL;TYPE=WORK",
                6: "TEL;TYPE=CELL",
                7: "TEL;TYPE=FAX",
                8: "TEL;TYPE=PAGER",
                9: "EMAIL",
                11: "URL",
                12: "TITLE",
                13: "ORG",
                17: "NOTE",
            }
            for field in fields:
                kind, location = contacts._api_mappings[
                    self.templates[field["template"]]
                ]
                tag = mapping.get(kind)
                if tag:
                    if location and kind not in (4, 5):
                        tag += ";TYPE=" + ("HOME" if location == 1 else "WORK")
                    lines.append(tag + ":" + escape(field["value"]))
            if flags & vcard_include_x:
                import base64

                lines.append(
                    "X-PYS60-FIELDS:"
                    + base64.b64encode(json.dumps(fields).encode("utf-8")).decode(
                        "ascii"
                    )
                )
            lines.append("END:VCARD")
        return ("\r\n".join(lines) + "\r\n").encode("utf-8")

    def import_vcards(self, text, flags):
        import contacts

        text = text.replace("\r\n ", "").replace("\r\n\t", "")
        result = []
        for block in text.split("BEGIN:VCARD")[1:]:
            if "END:VCARD" not in block:
                raise ValueError("invalid vCard")
            entry = self.create_entry()
            extended = False
            for line in block.splitlines():
                if ":" not in line:
                    continue
                tag, value = line.split(":", 1)
                if tag == "X-PYS60-FIELDS" and flags & vcard_include_x:
                    import base64

                    decoded = json.loads(base64.b64decode(value))
                    if not isinstance(decoded, list):
                        raise ValueError("invalid field data")
                    for f in decoded:
                        self.field_type_info(f["template"])
                    entry.data["fields"] = decoded
                    extended = True
                    break
            if not extended:

                def add(kind, value, location=0):
                    for index, template in enumerate(self.templates):
                        if contacts._api_mappings[template] == (kind, location):
                            entry.add_field(index, value=value)
                            break

                for line in block.splitlines():
                    if ":" not in line:
                        continue
                    tag, value = line.split(":", 1)
                    value = (
                        value.replace("\\n", "\n")
                        .replace("\\;", ";")
                        .replace("\\,", ",")
                        .replace("\\\\", "\\")
                    )
                    upper = tag.upper()
                    if upper == "N":
                        parts = value.split(";")
                        if parts[0]:
                            add(last_name, parts[0])
                        if len(parts) > 1 and parts[1]:
                            add(first_name, parts[1])
                    else:
                        kind = {
                            "EMAIL": 9,
                            "URL": 11,
                            "TITLE": 12,
                            "ORG": 13,
                            "NOTE": 17,
                        }.get(upper.split(";")[0])
                        loc = 1 if "HOME" in upper else 2 if "WORK" in upper else 0
                        if upper.startswith("TEL"):
                            kind = (
                                6
                                if "CELL" in upper
                                else (
                                    7
                                    if "FAX" in upper
                                    else (4 if loc == 1 else 5 if loc == 2 else 3)
                                )
                            )
                        if kind:
                            add(kind, value, loc)
            entry.commit()
            result.append(entry.key)
            if flags & vcard_import_single_contact:
                break
        if not result:
            raise ValueError("invalid vCard")
        return result


class Entry:
    def __init__(self, db, key, data):
        self.db, self.key, self.data = db, key, data

    def entry_data(self):
        return dict(uniqueid=self.key, lastmodified=self.data["modified"])

    def num_of_fields(self):
        return len(self.data["fields"])

    def __iter__(self):
        return iter([self.get_field(i) for i in range(self.num_of_fields())])

    def get_field(self, index):
        if not isinstance(index, int):
            raise TypeError("integer index expected")
        if index < 0:
            raise IndexError(index)
        field = copy.deepcopy(self.data["fields"][index])
        template = self.db.templates[field.pop("template")]
        field.update(
            fieldindex=index,
            fieldid=index,
            field_ids=list(template[0]),
            vcard_mapping=template[1],
            maxlength=0,
        )
        if field["storagetype"] == storage_type_store:
            import base64

            field["value"] = base64.b64decode(field["value"])
        return field

    def begin(self):
        import weakref

        key = (self.db.path, self.key)
        if key in _locks and _locks[key]() is not None:
            raise e32.SymbianError(-14, "contact is busy")
        self.data = self.db.store.get(self.key)
        _locks[key] = weakref.ref(
            self, lambda ref: _locks.pop(key, None) if _locks.get(key) is ref else None
        )

    def commit(self):
        self.data["modified"] = time.time()
        self.key = self.db.store.put(self.key, self.data)
        _locks.pop((self.db.path, self.key), None)

    def rollback(self):
        self.data = self.db.store.get(self.key)
        _locks.pop((self.db.path, self.key), None)

    def add_field(self, template, value=None, label=None):
        info = self.db.field_type_info(template)
        field = dict(
            template=template,
            label=info["name"] if label is None else label,
            storagetype=info["storagetype"],
            value=0.0 if info["storagetype"] == storage_type_datetime else "",
        )
        self.data["fields"].append(field)
        try:
            if value is not None:
                self.modify_field(len(self.data["fields"]) - 1, value=value)
        except Exception:
            self.data["fields"].pop()
            raise

    def modify_field(self, index, value=None, label=None):
        self.get_field(index)
        field = self.data["fields"][index]
        if value is not None:
            if field["storagetype"] == storage_type_datetime:
                value = float(value)
            elif field["storagetype"] == storage_type_store:
                import base64

                value = base64.b64encode(value).decode("ascii")
            field["value"] = value
        if label is not None:
            field["label"] = label

    def remove_field(self, index):
        self.get_field(index)
        del self.data["fields"][index]

    def find_field_indexes(self, uid):
        return [
            i
            for i, f in enumerate(self.data["fields"])
            if uid in self.db.templates[f["template"]][0]
        ]

    def is_contact_group(self):
        return int(self.data["group"])


def open(filename=None, mode=None):
    return Database(filename, mode)
