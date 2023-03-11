from planning.search.abstract import PriorityQueue
from planning.space.primitives import DiscreteState

from collections import deque


class FIFO(PriorityQueue):
    def __init__(self) -> None:
        self.queue = deque()

    def get(self) -> DiscreteState:
        return self.queue.popleft()

    def add(self, state: DiscreteState) -> None:
        self.queue.append(state)

    def is_empty(self) -> bool:
        return len(self.queue) == 0
