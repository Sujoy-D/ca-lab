"""Tests for the atom pathfinding solver."""

from __future__ import annotations

import unittest

from solve import apply_actions, solve


class SolveTests(unittest.TestCase):
    def assert_reaches(
        self,
        ps: int,
        ns: int,
        pt: int,
        nt: int,
        walls: list,
    ) -> None:
        actions = solve(ps, ns, pt, nt, walls)
        self.assertIsInstance(actions, list)
        self.assertLessEqual(len(actions), 1000)
        end = apply_actions(ps, ns, actions, walls)
        self.assertEqual(end, (pt, nt), f"actions={actions}")

    def test_already_at_target(self) -> None:
        self.assertEqual(solve(5, 5, 5, 5, []), [])

    def test_simple_proton(self) -> None:
        self.assert_reaches(0, 0, 3, 0, [])
        self.assertEqual(solve(0, 0, 3, 0, []), ["PROTON", "PROTON", "PROTON"])

    def test_simple_neutron(self) -> None:
        self.assert_reaches(0, 0, 0, 2, [])
        self.assertEqual(solve(0, 0, 0, 2, []), ["NEUTRON", "NEUTRON"])

    def test_example_net_move(self) -> None:
        # ALPHA + 3 PROTON => (+1, -2). From (2, 2) reach (3, 0).
        actions = solve(2, 2, 3, 0, [])
        self.assert_reaches(2, 2, 3, 0, [])
        self.assertIn("ALPHA", actions)

    def test_alpha_only(self) -> None:
        self.assert_reaches(4, 4, 2, 2, [])
        self.assertEqual(solve(4, 4, 2, 2, []), ["ALPHA"])

    def test_need_alpha_to_reduce(self) -> None:
        # Cannot decrease without ALPHA; go from (5, 5) to (4, 3).
        # Either ["ALPHA", "PROTON"] or ["PROTON", "ALPHA"] works.
        actions = solve(5, 5, 4, 3, [])
        self.assert_reaches(5, 5, 4, 3, [])
        self.assertEqual(len(actions), 2)
        self.assertEqual(actions.count("ALPHA"), 1)
        self.assertEqual(actions.count("PROTON"), 1)

    def test_wall_blocking_direct_path(self) -> None:
        # Direct PROTON path blocked at (1, 0); go around via neutrons + alpha.
        walls = [[1, 0]]
        actions = solve(0, 0, 2, 0, walls)
        self.assert_reaches(0, 0, 2, 0, walls)
        # Must not land on (1, 0)
        p, n = 0, 0
        for a in actions:
            if a == "PROTON":
                p += 1
            elif a == "NEUTRON":
                n += 1
            else:
                p -= 2
                n -= 2
            self.assertNotEqual((p, n), (1, 0))

    def test_alpha_crosses_wall(self) -> None:
        # From (4, 4) ALPHA to (2, 2). Wall at (3, 3) is jumped over.
        walls = [[3, 3]]
        self.assertEqual(solve(4, 4, 2, 2, walls), ["ALPHA"])
        self.assert_reaches(4, 4, 2, 2, walls)

    def test_cannot_land_on_wall_with_alpha(self) -> None:
        # ALPHA landing on wall is illegal; must find another route if possible.
        walls = [[2, 2]]
        actions = solve(4, 4, 2, 2, walls)
        # Target is a wall — unreachable
        self.assertEqual(actions, [])

    def test_target_is_wall_unreachable(self) -> None:
        self.assertEqual(solve(0, 0, 1, 1, [[1, 1]]), [])

    def test_unsorted_unstable_list(self) -> None:
        walls = [[5, 3], [1, 0], [2, 2]]
        self.assert_reaches(0, 0, 4, 1, walls)

    def test_near_bounds(self) -> None:
        self.assert_reaches(28, 18, 29, 19, [])
        self.assert_reaches(29, 19, 27, 17, [])  # ALPHA near corner

    def test_cannot_go_out_of_bounds(self) -> None:
        # From (0, 0) ALPHA is illegal; solver must not return it.
        actions = solve(0, 0, 1, 0, [])
        self.assertEqual(actions, ["PROTON"])
        apply_actions(0, 0, actions, [])

    def test_longer_detour(self) -> None:
        # Wall strip forcing alpha detours.
        walls = [[i, 0] for i in range(1, 10)]
        self.assert_reaches(0, 0, 10, 0, walls)

    def test_same_isotone_shift(self) -> None:
        self.assert_reaches(10, 8, 12, 6, [])


if __name__ == "__main__":
    unittest.main()
