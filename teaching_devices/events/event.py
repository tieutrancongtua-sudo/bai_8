
from __future__ import annotations

from typing import Callable, Generic, TypeVar

T = TypeVar("T")
Handler = Callable[[object, T], None]


class EventSubscription(Generic[T]):

    def __init__(self, handlers: list) -> None:
        self._handlers = handlers

    def __iadd__(self, handler: Handler[T]) -> "EventSubscription[T]":
        if not callable(handler):
            raise TypeError("handler phải là callable")
        self._handlers.append(handler)
        return self

    def __isub__(self, handler: Handler[T]) -> "EventSubscription[T]":
        try:
            self._handlers.remove(handler) 
        except ValueError:
            pass  
        return self

    def __len__(self) -> int:
        return len(self._handlers)


class EventHandlerError(Exception):

    def __init__(self, errors: list[Exception]) -> None:
        super().__init__(f"{len(errors)} subscriber ném lỗi: {errors}")
        self.errors = errors


class Event(Generic[T]):

    def __init__(self) -> None:
        self._handlers: list = []
        self.public: EventSubscription[T] = EventSubscription(self._handlers)

    def invoke(self, sender: object, args: T) -> None:
        errors: list[Exception] = []
        for handler in list(self._handlers):
            try:
                handler(sender, args)
            except Exception as ex:  
                errors.append(ex)
        if errors:
            raise EventHandlerError(errors)
