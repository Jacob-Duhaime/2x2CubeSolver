from typing import List
from typing import Optional

import rubik


def shortest_path(
        start: rubik.Position,
        end: rubik.Position,
) -> Optional[List[rubik.Permutation]]:
    """
    Using 2-way BFS, finds the shortest path from start to end.
    Returns a list of Permutations representing that shortest path.
    If there is no path to be found, return None instead of a list.

    You can use the rubik.quarter_twists move 6-tuple.
    Each move can be applied using rubik.perm_apply.
    """
    raise NotImplementedError
