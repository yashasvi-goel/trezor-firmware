# This file is part of the Trezor project.
#
# Copyright (C) 2020 SatoshiLabs and contributors
#
# This library is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the License along with this library.
# If not, see <https://www.gnu.org/licenses/lgpl-3.0.html>.

import pytest

from trezorlib import btc, messages
from trezorlib.tools import parse_path

from ..tx_cache import TxCache
from .signtx import request_finished, request_input, request_meta, request_output

B = messages.ButtonRequestType

TX_CACHE_TESTNET = TxCache("Testnet")
TX_CACHE_MAINNET = TxCache("Bitcoin")

TXHASH_c63e24 = bytes.fromhex(
    "c63e24ed820c5851b60c54613fbc4bcb37df6cd49b4c96143e99580a472f79fb"
)
TXHASH_c6be22 = bytes.fromhex(
    "c6be22d34946593bcad1d2b013e12f74159e69574ffea21581dad115572e031c"
)
TXHASH_58497a = bytes.fromhex(
    "58497a7757224d1ff1941488d23087071103e5bf855f4c1c44e5c8d9d82ca46e"
)


@pytest.mark.skip_t1
def test_p2pkh_fee_bump(client):
    # tx: c6be22d34946593bcad1d2b013e12f74159e69574ffea21581dad115572e031c
    # input 1: 0.0010 BTC
    # tx: 58497a7757224d1ff1941488d23087071103e5bf855f4c1c44e5c8d9d82ca46e
    # input 1: 0.0011 BTC
    # Original tx accepted by network: c63e24ed820c5851b60c54613fbc4bcb37df6cd49b4c96143e99580a472f79fb
    # The transaction was produced for different address_n, so the publick keys don't match, which is why the test fails :-(.

    inp1 = messages.TxInputType(
        address_n=parse_path("44h/0h/0h/0/0"),
        amount=100000,
        prev_hash=TXHASH_c6be22,
        prev_index=1,
        orig_hash=TXHASH_c63e24,
        orig_index=0,
    )

    inp2 = messages.TxInputType(
        address_n=parse_path("44h/0h/0h/0/1"),
        amount=110000,
        prev_hash=TXHASH_58497a,
        prev_index=1,
        orig_hash=TXHASH_c63e24,
        orig_index=1,
    )

    out1 = messages.TxOutputType(
        address="15Jvu3nZNP7u2ipw2533Q9VVgEu2Lu9F2B",
        amount=100000,
        script_type=messages.OutputScriptType.PAYTOADDRESS,
        orig_hash=TXHASH_c63e24,
        orig_index=0,
    )

    out2 = messages.TxOutputType(
        address_n=parse_path("44h/0h/0h/1/0"),
        amount=210000 - 100000 - 20000,
        script_type=messages.OutputScriptType.PAYTOADDRESS,
        orig_hash=TXHASH_c63e24,
        orig_index=1,
    )

    with client:
        client.set_expected_responses(
            [
                request_input(0),
                request_meta(TXHASH_c63e24),
                request_input(1),
                request_output(0),
                messages.ButtonRequest(code=B.ConfirmOutput),
                request_output(1),
                messages.ButtonRequest(code=B.SignTx),
                request_input(0),
                request_meta(TXHASH_c6be22),
                request_input(0, TXHASH_c6be22),
                request_output(0, TXHASH_c6be22),
                request_output(1, TXHASH_c6be22),
                request_input(1),
                request_meta(TXHASH_58497a),
                request_input(0, TXHASH_58497a),
                request_output(0, TXHASH_58497a),
                request_output(1, TXHASH_58497a),
                request_input(0, TXHASH_c63e24),
                request_input(0, TXHASH_c63e24),
                request_input(1, TXHASH_c63e24),
                request_output(0, TXHASH_c63e24),
                request_output(1, TXHASH_c63e24),
                request_input(0),
                request_input(1),
                request_output(0),
                request_output(1),
                request_input(0),
                request_input(1),
                request_output(0),
                request_output(1),
                request_output(0),
                request_output(1),
                request_finished(),
            ]
        )
        _, serialized_tx = btc.sign_tx(
            client, "Bitcoin", [inp1, inp2], [out1, out2], prev_txes=TX_CACHE_MAINNET,
        )
