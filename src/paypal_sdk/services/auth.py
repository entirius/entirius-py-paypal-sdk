# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.

from dataclasses import dataclass


@dataclass
class Authorization:
    scope: str
    access_token: str
    token_type: str
    app_id: str
    expires_in: int
    nonce: str
    expires_at: int = None

    def get_auth_header(self):
        return {"Authorization": f"Bearer {self.access_token}"}
