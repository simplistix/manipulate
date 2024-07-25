from typing import Sequence

from manipulate.actions import Action
from manipulate.destinations import Destination
from manipulate.sources import Source


def manipulate(source: Source, actions: Sequence[Action], destination: Destination) -> None:
    elements = source.elements()
    for action in actions:
        elements = action(elements)
    destination.handle(elements)


__all__ = ['manipulate']
