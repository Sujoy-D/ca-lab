"""Pathfinding solver for the atom / proton-neutron grid challenge.

Moves:
  PROTON  -> (p + 1, n)
  NEUTRON -> (p, n + 1)
  ALPHA   -> (p - 2, n - 2)  # jumps; does not visit intermediate cells

Bounds: 0 <= protons <= 29, 0 <= neutrons <= 19
Unstable atoms are forbidden landing positions after each action.
"""

from __future__ import annotations

from collections import deque
from typing import Iterable, List, Optional, Sequence, Tuple

MAX_PROTONS = 29
MAX_NEUTRONS = 19
MAX_ACTIONS = 1000

ACTIONS: Tuple[Tuple[str, int, int], ...] = (
    ("PROTON", 1, 0),
    ("NEUTRON", 0, 1),
    ("ALPHA", -2, -2),
)


def _in_bounds(p: int, n: int) -> bool:
    return 0 <= p <= MAX_PROTONS and 0 <= n <= MAX_NEUTRONS


def solve(
    protons_start: int,
    neutrons_start: int,
    protons_target: int,
    neutrons_target: int,
    unstable_atoms: Iterable[Sequence[int]],
) -> List[str]:
    """Return a sequence of actions from start to target avoiding unstable atoms.

    Uses BFS so the path is shortest (well under the 1000-action limit when
    a path exists on this 30x20 grid).
    """
    walls = {(int(p), int(n)) for p, n in unstable_atoms}
    start = (int(protons_start), int(neutrons_start))
    target = (int(protons_target), int(neutrons_target))

    if start == target:
        return []

    if not _in_bounds(*start) or not _in_bounds(*target):
        return []
    if target in walls:
        return []

    # Start may sit on a wall (already there); never land on a wall after a move.
    parent: dict[Tuple[int, int], Tuple[Optional[Tuple[int, int]], str]] = {
        start: (None, "")
    }
    queue: deque[Tuple[int, int]] = deque([start])

    while queue:
        p, n = queue.popleft()
        for name, dp, dn in ACTIONS:
            np, nn = p + dp, n + dn
            if not _in_bounds(np, nn):
                continue
            if (np, nn) in walls:
                continue
            if (np, nn) in parent:
                continue
            parent[(np, nn)] = ((p, n), name)
            if (np, nn) == target:
                return _reconstruct(parent, target)
            queue.append((np, nn))

    return []


def _reconstruct(
    parent: dict[Tuple[int, int], Tuple[Optional[Tuple[int, int]], str]],
    target: Tuple[int, int],
) -> List[str]:
    path: List[str] = []
    node: Optional[Tuple[int, int]] = target
    while node is not None:
        prev, action = parent[node]
        if prev is None:
            break
        path.append(action)
        node = prev
    path.reverse()
    if len(path) > MAX_ACTIONS:
        return []
    return path


def apply_actions(
    protons: int,
    neutrons: int,
    actions: Sequence[str],
    unstable_atoms: Iterable[Sequence[int]],
) -> Tuple[int, int]:
    """Apply actions for verification; raises ValueError on illegal moves."""
    walls = {(int(p), int(n)) for p, n in unstable_atoms}
    deltas = {name: (dp, dn) for name, dp, dn in ACTIONS}
    p, n = protons, neutrons
    if len(actions) > MAX_ACTIONS:
        raise ValueError("too many actions")
    for action in actions:
        if action not in deltas:
            raise ValueError(f"invalid action: {action}")
        dp, dn = deltas[action]
        p, n = p + dp, n + dn
        if not _in_bounds(p, n):
            raise ValueError(f"out of bounds: {(p, n)}")
        if (p, n) in walls:
            raise ValueError(f"hit wall: {(p, n)}")
    return p, n
