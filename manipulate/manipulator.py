from dataclasses import dataclass
from typing import Sequence

from .actions import Action
from .destinations import Destination
from .sources import Source


@dataclass
class Manipulator:

    def __call__(self, source: Source, actions: Sequence[Action], destination: Destination) -> None:
        elements = source.elements()
        for action in actions:
            elements = action(elements)
        destination.handle(elements)
