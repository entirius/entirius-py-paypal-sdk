# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.


def get_href_for_rel(data, rel):
    for item in data:
        if item["rel"] == rel:
            return item["href"]
    return None
