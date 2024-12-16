#Arrumar ordem que o programa lê os estados e transições
#Fazer função do complementar
#Fazer função de arquivo do complementar
#Fazer função do reverso
#Fazer função de arquivo do reverso
from collections import defaultdict

def AFN(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write("# AFN Original\n")
        file.writelines(lines[:-1])  # Copia todas as linhas, exceto a primeira e a última

def read_afn(input_path):
    with open(input_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    Q = set(lines[0].strip().split(': ')[1].split(', '))
    Sigma = set(lines[1].strip().split(': ')[1].split(', '))
    delta = defaultdict(list)
    for line in lines[3:-3]:
        state, rest = line.strip().split(', ')
        symbol, next_state = rest.split(' -> ')
        delta[(state, symbol)].append(next_state)
    q0 = None
    F = set()
    w = None

    for line in lines:
        if line.endswith(": inicial\n"):
            q0 = line.split(': ')[0].strip()
        elif line.startswith("F:"):
            F = set(line.split(': ')[1].strip().split(', '))
        elif line.startswith("w:"):
            w = line.split(': ')[1].strip()

    return Q, Sigma, delta, q0, F, w


def afn_to_afd(Q, Sigma, delta, q0, F):
    dfa_states = []
    dfa_delta = {}
    dfa_start_state = frozenset([q0])  # Estado inicial configurável
    dfa_final_states = set()

    unprocessed_states = [dfa_start_state]
    processed_states = set()

    while unprocessed_states:
        current_state = unprocessed_states.pop()
        processed_states.add(current_state)

        if current_state not in dfa_states:
            dfa_states.append(current_state)

        for symbol in Sigma:
            next_state = set()
            for sub_state in current_state:
                if (sub_state, symbol) in delta:
                    next_state.update(delta[(sub_state, symbol)])

            # Convertendo para frozenset
            next_state = frozenset(next_state)

            dfa_delta[(current_state, symbol)] = next_state

            if next_state not in processed_states and next_state not in unprocessed_states:
                unprocessed_states.append(next_state)

            if any(sub_state in F for sub_state in next_state):
                dfa_final_states.add(next_state)

    return dfa_states, Sigma, dfa_delta, dfa_start_state, dfa_final_states



def format_state(state):
    if isinstance(state, frozenset):  # Quando o estado é um frozenset
        return "{" + ", ".join(sorted(map(str, state))) + "}"
    elif state:  # Quando o estado não é vazio e não é frozenset
        return str(state)
    else:  # Estado vazio
        return "∅"


def save_afd(output_path, dfa_states, Sigma, dfa_delta, dfa_start_state, dfa_final_states):
    """
    Salva o AFD em um arquivo de saída formatado.
    """
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write("# AFD Determinizado\n")
        file.write(f"Q: {', '.join(format_state(s) for s in dfa_states)}\n")
        file.write(f"Σ: {', '.join(Sigma)}\n")
        file.write(f"q0: {format_state(dfa_start_state)}: inicial\n")
        file.write(f"F: {', '.join(format_state(f) for f in dfa_final_states)}\n")
        file.write("δ:\n")
        for (state, symbol), next_state in dfa_delta.items():
            file.write(f"{format_state(state)}, {symbol} -> {format_state(next_state)}\n")


def simulate(dfa_start_state, dfa_final_states, dfa_delta, input_string):
    """
    Simula uma entrada no AFD.
    """
    current_state = dfa_start_state
    for symbol in input_string:
        if (current_state, symbol) in dfa_delta:
            current_state = dfa_delta[(current_state, symbol)]
        else:
            return "Rejeitada"

    return "Aceita" if current_state in dfa_final_states else "Rejeitada"

