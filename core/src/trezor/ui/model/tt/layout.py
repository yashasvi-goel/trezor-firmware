from trezor import ui

from .confirm import Confirm
from .text import Text

if False:
    from typing import Dict, Callable


def layout_confirm_ping(content: Dict[str, str]) -> Confirm:
    text = Text("Confirm")
    text.mono("ping???")
    return Confirm(text)


LAYOUTS = {
    "confirm_ping": layout_confirm_ping,
}  # type: Dict[str, Callable[[Dict[str, str]], ui.Layout]]
