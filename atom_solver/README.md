# Atom pathfinding solver

Solution for the language-independent challenge: move an atom from
`(protons_start, neutrons_start)` to `(protons_target, neutrons_target)`
using:

| Action     | Δ protons | Δ neutrons |
|------------|-----------|------------|
| `PROTON`   | +1        | 0          |
| `NEUTRON`  | 0         | +1         |
| `ALPHA`    | −2        | −2         |

Constraints:

- Stay in `0..29` protons and `0..19` neutrons after every action
- Do not land on `unstable_atoms` (ALPHA jumps and does not visit intermediates)
- At most 1000 actions (BFS keeps paths short)

## Usage

```python
from atom_solver import solve

actions = solve(
    protons_start=2,
    neutrons_start=2,
    protons_target=3,
    neutrons_target=0,
    unstable_atoms=[],
)
# e.g. ["ALPHA", "PROTON", "PROTON", "PROTON"]
```

Paste-ready function: see `solve.py` (`solve(...)`).

## Tests

```bash
cd atom_solver && python3 -m unittest test_solve.py -v
```
