from typing import Sequence, Any, Iterable

from .actions import Action
from .destinations import Destination
from .elements import Element
from .sources import Source


class Tracker:
    current_action: Action
    current_element: Element[Any]

    def before(self, action: Action, elements: Iterable[Element[Any]]) -> Iterable[Element[Any]]:
        for element in elements:
            self.current_action = action
            self.current_element = element
            yield element

    def after(self, elements: Iterable[Element[Any]]) -> Iterable[Element[Any]]:
        try:
            yield from elements
        except Exception as e:
            breadcrumbs = [self.current_element]
            current = self.current_element
            while current := current.parent:  # type: ignore[assignment]
                breadcrumbs.append(current)
            breadcrumb_text = ' -> '.join(str(e) for e in reversed(breadcrumbs))
            e.add_note(f'Performing {self.current_action} on {breadcrumb_text}')
            raise


def manipulate(source: Source, actions: Sequence[Action], destination: Destination) -> None:
    tracker = Tracker()
    elements = source.elements()
    for action in actions:
        elements = action(tracker.before(action, elements))
    destination.handle(tracker.after(elements))


__all__ = ['manipulate']
