"""
This module contains constants and functions that are different across
hardware, e.g. T1 and TT.
"""

from trezor import ui, utils

if False:
    from typing import Dict

if utils.MODEL == "1":
    from .t1.layout import LAYOUTS
elif utils.MODEL == "T":
    from .tt.layout import LAYOUTS
else:
    raise ValueError("Unknown Trezor model")


# FIXME: list of tuples instead of Dict[]
#    ... or Dict[str,Union[str,List[str]]]
def lookup_layout(brtype: str, content: Dict[str, str]) -> ui.Layout:
    layout = LAYOUTS[brtype]
    return layout({})
