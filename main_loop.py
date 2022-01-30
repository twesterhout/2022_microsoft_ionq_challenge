"""Game logic
"""

import numpy as np
import scipy
import scipy.sparse
from typing import Any, Dict, List, Tuple


def index_to_spin(index: int, n_qubits: int) -> np.ndarray:
    return (((np.array([index]).reshape(-1, 1) & (1 << np.arange(n_qubits)))) > 0).astype(np.int64)


class Hamiltonian:
    n_qubits: int
    onsite: List[Tuple[int, float]]
    pair: List[Tuple[int, int, float]]

    def __init__(self, n_qubits, onsite, pair, qaoa_solve=None):
        self.n_qubits = n_qubits
        self.onsite = onsite
        self.pair = pair
        self.qaoa_solve = qaoa_solve

    def _pretty_graph(self) -> str:
        raise NotImplementedError()

    def pretty_graph(self, x: np.ndarray) -> str:
        x = tuple(x.astype(int).tolist())
        x = tuple(map(lambda x: "X" if x == 1 else " ", x))
        return self._pretty_graph().format(*x)

    def _solve_bruteforce(self):
        energies = []
        bit_representations = []
        for idx in range(2 ** self.n_qubits):
            solution = index_to_spin(idx, self.n_qubits)[0]
            bit_representations.append(solution.copy())
            energies.append(self.energy(solution))
        energies = np.array(energies)
        bit_representations = np.array(bit_representations)
        return [
            (x, y) for x, y in zip(np.sort(energies), bit_representations[np.argsort(energies)])
        ]

    def solve(self, backend, n_shots: int = 100) -> List[Tuple[float, np.ndarray]]:
        if backend == "bruteforce":
            return self._solve_bruteforce()
        elif backend == "qaoa":
            print("Running QAOA with {} shots ...".format(n_shots))
            return self.qaoa_solve(self, n_shots)
        else:
            assert False

    def energy(self, x: np.ndarray) -> float:
        assert np.all((x == 0) | (x == 1))
        energy = 0
        for (i, h) in self.onsite:
            energy += h * x[i]
        for (i, j, J) in self.pair:
            energy += J * x[i] * x[j]
        return energy


def _array_to_int(xs: np.ndarray) -> int:
    r = 0
    k = 0
    for i in xs[::-1]:
        assert i == 0 or i == 1
        r |= i << k
        k += 1
    return r


def _int_to_array(r: int, n: int) -> np.ndarray:
    xs = np.zeros(n, dtype=bool)
    for i in range(n):
        xs[n - 1 - i] = (r >> i) & 1
    return xs


class ExampleHamiltonian01(Hamiltonian):
    def __init__(self):
        n_qubits = 4
        onsite = [(0, +3), (1, 0), (2, -2), (3, -3)]
        pair = [(0, 1, -2), (0, 2, +1), (1, 2, -1.5), (2, 3, -1)]
        # onsite = [(0, -2), (1, +3), (2, 0), (3, -3)]
        # pair = [(0, 1, +1), (0, 2, -1.5), (0, 3, -1), (1, 2, -2)]
        super().__init__(n_qubits, onsite, pair)

    def _pretty_graph(self) -> str:
        return """\
  ┌────────────────────┬────────────────────────────┐
  │┌───┐  Cadmium      │    Battery           ┌───┐ │
  ││+3 │   mining      │   technology         │ 0 │ │
  │└───┘    [{}]       -2  investments  [{}]    └───┘ │
  └────┬────── +1 ─────┴─────── -1.5 ──────┬────────┘
       │                          ┌───┐    │
       │   Elecrical vehicle      │-2 │    │
       │       investments  [{}]   └───┘    │
       ├───── -1 ──────────────────────────┤
       │                            ┌───┐  │
       │      Opening a nuclear     │-3 │  │
       │         power plant  [{}]   └───┘  │
       └───────────────────────────────────┘"""

class GameState:
    def __init__(self, mode, hamiltonian: Hamiltonian, x: np.ndarray, backend):
        self.mode = mode
        self.hamiltonian = hamiltonian
        self.x = x
        self.backend = backend
        if isinstance(self.mode, StandardMode):
            self.solution = self.hamiltonian.solve(self.backend, n_shots=self.mode.level)
        else:
            self.solution = None

    def select(self, index: int):
        self.x[index] ^= 1  # Flip index'th spin
        pass


def display_current_state(state):
    print(state.hamiltonian.pretty_graph(state.x))
    print(
        "Current energy: {}    (current state: {})"
        "".format(state.hamiltonian.energy(state.x), state.x.astype(int))
    )
    if isinstance(state.mode, StandardMode):
        (e, _) = state.solution[0]
        print("QAOA    energy: {}".format(e))


class SelectCommand:
    def __init__(self, index):
        self.index = index


class SolveAllCommand:
    def __init__(self):
        pass


class CheatCommand:
    def __init__(self):
        pass


class SolveSubsetCommand:
    def __init__(self, indices):
        self.indices = indices


def parse_command(s):
    first, *rest = s.strip(" ").split(" ")
    if first == "solve":
        if rest == ["all"]:
            return SolveAllCommand()
        else:
            indices = sum(map(lambda r: r.split(","), rest), [])
            indices = list(map(lambda r: int(r), filter(lambda r: r != "", indices)))
            return SolveSubsetCommand(indices)
    elif first == "cheat":
        return CheatCommand()
    else:
        assert len(rest) == 0
        index = int(first)
        return SelectCommand(index)


class StandardMode:
    def __init__(self, level: int):
        self.level = level


class CooperativeMode:
    def __init__(self):
        pass


def game_setup():
    mode = input("Game mode: 1) standard, 2) cooperative: ")
    mode = int(mode)
    if mode == 1:
        level = input("Difficulty level (between 1 and 500): ")
        level = int(level)
        return StandardMode(level)
    else:
        assert mode == 2, "invalid mode"
        return CooperativeMode()


def step_in_standard_mode(state, command):
    if isinstance(command, SelectCommand):
        state.select(command.index)
    elif isinstance(command, CheatCommand):
        (_, x) = state.solution[0]
        print("IonQ obtained its best energy on ", x)
    else:
        assert False, "invalid command"


def step_in_cooperative_mode(state, command):
    if isinstance(command, SelectCommand):
        state.select(command.index)
    elif isinstance(command, SolveSubsetCommand):
        assert len(set(command.indices)) == len(command.indices)
        indices = sorted(command.indices)

        def _find_new_index(x):
            assert x in indices
            for (k, y) in enumerate(indices):
                if y == x:
                    return k
            assert False

        n_qubits = len(command.indices)
        onsite = np.zeros(n_qubits)
        for i, h in state.hamiltonian.onsite:
            if i in command.indices:
                onsite[_find_new_index(i)] += h

        pair = []
        for i, j, J in state.hamiltonian.pair:
            if (i in command.indices) and (j in command.indices):
                pair.append((_find_new_index(i), _find_new_index(j), J))
            if i in command.indices:
                onsite[_find_new_index(i)] += state.x[j] * J
            if j in command.indices:
                onsite[_find_new_index(j)] += state.x[i] * J

        onsite = [(i, h) for i, h in enumerate(onsite) if h != 0]
        hamiltonian = Hamiltonian(n_qubits, onsite, pair, qaoa_solve=state.hamiltonian.qaoa_solve)
        (_, solution) = hamiltonian.solve(state.backend)[0]
        for (i, y) in zip(indices, solution):
            state.x[i] = y
    else:
        assert False, "invalid command"


def play(state: GameState):
    while True:
        display_current_state(state)
        try:
            command = parse_command(input("Specify the index of a component to select/deselect: "))
        except EOFError as e:
            print()
            break
        if isinstance(state.mode, StandardMode):
            step_in_standard_mode(state, command)
        elif isinstance(state.mode, CooperativeMode):
            step_in_cooperative_mode(state, command)
        else:
            assert False


def main(qaoa_solve=None, hamiltonian=None):
    if hamiltonian is None:
        hamiltonian = ExampleHamiltonian01()
    x = np.random.choice([0, 1], size=hamiltonian.n_qubits)
    mode = game_setup()
    if qaoa_solve is not None:
        backend = "qaoa"
        hamiltonian.qaoa_solve = qaoa_solve
    else:
        backend = "bruteforce"  # qaoa
    play(GameState(mode, hamiltonian, x, backend))


#
# import main_loop
# main_loop.main(your_custom_function)
#


if __name__ == "__main__":
    main()
