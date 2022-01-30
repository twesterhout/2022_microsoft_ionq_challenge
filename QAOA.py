from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import Aer, execute
from qiskit.circuit import Parameter
import numpy as np
import qiskit
from qiskit.quantum_info import Pauli
from qiskit import opflow
from qiskit.opflow import PauliSumOp


def to_matrix(onsite, pair, n_qubits):
    W = np.zeros((n_qubits, n_qubits), dtype=np.float64)
    for onsite_term in onsite:
        i, pi = onsite_term
        W[i, i] += pi / 2.

    for pair_term in pair:
        i, j, pij = pair_term
        W[i, j] += pij / 8.
        W[j, i] += pij / 8

        W[i, i] += pij / 8
        W[j, j] += pij / 8

    return W


def transform_interaction_to_qiskit_format(n_qubits, hamiltonian):
    r"""Generate Hamiltonian for the problem
    """

    onsite = hamiltonian.onsite
    pair = hamiltonian.pair

    def get_shift(onsite, pair):
        shift = 0.
        for onsite_term in onsite:
            _, pi = onsite_term

            shift += pi / 2.

        for pair_term in pair:
            _, _, pij = pair_term

            shift += pij / 4.
        return shift

    shift = get_shift(onsite, pair)

    W = to_matrix(onsite, pair, n_qubits)

    pauli_list = []

    for i in range(n_qubits):
        for j in range(n_qubits):
            if np.isclose(W[i, j], 0.0):
                continue
            x_p = np.zeros(n_qubits, dtype=bool)
            z_p = np.zeros(n_qubits, dtype=bool)
            z_p[i] = True
            z_p[j] = True
            pauli_list.append([W[i, j], Pauli((z_p, x_p))])

    pauli_list = [(pauli[1].to_label(), pauli[0]) for pauli in pauli_list]
    return PauliSumOp.from_list(pauli_list), shift

def evaluate_cost(solution, hamiltonian):
    energy = 0
    for single_term in hamiltonian.onsite:
        energy += single_term[1] * (solution[single_term[0]] == 1)

    for pair_term in hamiltonian.pair:
        energy += pair_term[2] * (solution[pair_term[0]] == 1) * (solution[pair_term[1]] == 1)

    return energy


def index_to_spin(index, n_qubits):
    return (((np.array([index]).reshape(-1, 1) & (1 << np.arange(n_qubits)))) > 0).astype(np.int64)

def bruteforce_solution(n_qubits, hamiltonian):
    energies = []
    bit_representations = []
    for idx in range(2 ** n_qubits):
        solution = index_to_spin(idx, n_qubits)[0]


        bit_representations.append(solution.copy())
        energies.append(evaluate_cost(solution, hamiltonian))

    energies = np.array(energies)
    bit_representations = np.array(bit_representations)

    return np.sort(energies), bit_representations[np.argsort(energies)]



def maxcut_obj(x, G):
    """
    Given a bitstring as a solution, this function returns
    the number of edges shared between the two partitions
    of the graph.

    Args:
        x: str
           solution bitstring

        G: networkx graph

    Returns:
        obj: float
             Objective
    """
    obj = 0
    for i, j in G.edges():
        if x[i] != x[j]:
            obj -= 1

    return obj


def compute_expectation(counts, ham):
    """
    Computes expectation value based on measurement results

    Args:
        counts: dict
                key as bitstring, val as count
        ham: hamiltonian instance
    Returns:
        avg: float
             expectation value
    """

    def cast_to_int_array(bitstring):
        return np.asarray([int(y) for y in (list(bitstring))])

    avg = 0
    sum_count = 0
    for bitstring, count in counts.items():
        obj = evaluate_cost(cast_to_int_array(bitstring), ham) ## BEWARE: order of bitstring
        avg += obj * count
        sum_count += count
    #print('CURRENT LOSS:', avg / sum_count)
    return avg/sum_count


# We will also bring the different circuit components that
# build the qaoa circuit under a single function
def create_qaoa_circ(ham, theta):
    """
    Creates a parametrized qaoa circuit

    Args:
        ham: networkx graph
        theta: list
               unitary parameters

    Returns:
        qc: qiskit circuit
    """

    nqubits = ham.n_qubits
    p = len(theta) // 2  # number of alternating unitaries
    qc = QuantumCircuit(nqubits)

    beta = theta[:p]
    gamma = theta[p:]  # TODO add rz parameters

    # initial_state
    for i in range(nqubits):
        qc.h(i)

    for irep in range(p):
        # problem unitary
        for pair in list(ham.pair):
            qc.rzz(2 * gamma[irep] * pair[2], pair[0], pair[1])

        for onsite in list(ham.onsite):
            qc.rz(2 * gamma[irep] * onsite[1], onsite[0])

        # mixer unitary
        for i in range(nqubits):
            qc.rx(2 * beta[irep], i)

    qc.measure_all()

    return qc

# Finally we write a function that executes the circuit on the chosen backend
def get_expectation(ham, p, shots):

    """
    Runs parametrized circuit

    Args:
        hham: hamiltonian
        p: int,
           Number of repetitions of unitaries
    """

    backend = Aer.get_backend('qasm_simulator')
    backend.shots = shots

    def execute_circ(theta):
        qc = create_qaoa_circ(ham, theta)
        counts = backend.run(qc).result().get_counts()

        return compute_expectation(counts, ham)

    return execute_circ


from collections import OrderedDict
from qiskit import Aer
from qiskit import algorithms
from qiskit.algorithms import QAOA
from qiskit.opflow import StateFn
from qiskit.algorithms.optimizers import ADAM, COBYLA
from qiskit.circuit.library import TwoLocal
from qiskit.algorithms import VQE
from qiskit.circuit.library import TwoLocal


def most_frequent_strings(state_vector, num_most_frequent):
    """Compute the most likely binary string from state vector.
    Args:
        state_vector (numpy.ndarray or dict): state vector or counts.
    Returns:
        numpy.ndarray: binary string as numpy.ndarray of ints.
    """
    most_frequent_strings = [x[0] for x in sorted(state_vector.items(), \
                                                  key=lambda kv: kv[1])[-num_most_frequent:]]
    return [np.asarray([int(y) for y in (list(binary_string))]) for binary_string in most_frequent_strings]


def qaoa_solve(ham, n_shots):
    from scipy.optimize import minimize
    p = ham.n_qubits
    expectation = get_expectation(ham, p=p, shots=n_shots)

    res = minimize(expectation, np.ones(2 * p), method='COBYLA')

    backend = Aer.get_backend('aer_simulator')
    backend.shots = n_shots

    qc_res = create_qaoa_circ(ham, res.x)

    counts = backend.run(qc_res).result().get_counts()
    x = most_frequent_strings(counts, 4)

    costs = [evaluate_cost(xi, ham) for xi in x]

    return [(np.min(costs), x[np.argmin(costs)])]

