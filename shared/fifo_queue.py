"""
FIFOQueue

Simple FIFO queue wrapper used by the M/M/1 simulation.
"""

from collections import deque
from typing import Deque, Optional, Any


class FIFOQueue:
    """First-in, first-out queue."""

    def __init__(self) -> None:
        self._queue: Deque[Any] = deque()

    def push(self, item: Any) -> None:
        """Add an item to the back of the queue."""
        self._queue.append(item)

    def pop(self) -> Optional[Any]:
        """Remove and return the item at the front of the queue, or None if empty."""
        if self._queue:
            return self._queue.popleft()
        return None

    def __len__(self) -> int:
        return len(self._queue)


