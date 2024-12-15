from collections import defaultdict

def ler_afd_do_arquivo(filename):
    """
    Lê o AFD a partir de um arquivo no formato especificado.
    """
    dfa_states = []
    Sigma = []
    dfa_delta = defaultdict(list)  # Usando defaultdict para as transições
    dfa_start_state = None
    dfa_final_states = set()

    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        for line in lines:
            if line.startswith("Q:"):
                states = line[3:].strip().split("}, {")
                states = [frozenset(s.strip("{}").split(", ")) for s in states]
                dfa_states = states
            elif line.startswith("Σ:"):
                Sigma = line[3:].strip().split(", ")
            elif line.startswith("q0:"):
                dfa_start_state = frozenset(line.split(":")[1].strip().strip("{}").split(", "))
            elif line.startswith("F:"):
                states = line[3:].strip().split("}, {")
                states = [frozenset(s.strip("{}").split(", ")) for s in states]
                dfa_final_states = states
            elif line.startswith("{"):
                # Transições de estados no formato "{estado}, simbolo -> {estado seguinte}"
                state, rest = line.split("}, ")
                symbol, next_state = rest.split(" -> ")
                # Aqui usamos frozenset para garantir que o estado é único, mas podemos usar tuplas também
                state = frozenset(state.strip("{").split(", "))
                symbol = symbol.strip()
                next_state = frozenset(next_state.strip("{}").split(", "))
                
                # Agora a chave é uma tupla (estado, símbolo) e a transição é uma lista de estados seguintes
                dfa_delta[(state, symbol)].append(next_state)

    return dfa_states, Sigma, dfa_delta, dfa_start_state, dfa_final_states

def afd_complemento(dfa_states, Sigma, dfa_delta, dfa_start_state, dfa_final_states):
    all_states = set(map(frozenset, dfa_states))
    # Novos estados finais: tudo que não era final originalmente
    new_final_states = all_states - set(dfa_final_states)
    return dfa_states, Sigma, dfa_delta, dfa_start_state, new_final_states

def save_complement_afd(output_path, dfa_states, Sigma, dfa_delta, dfa_start_state, new_final_states):
    """
    Salva o AFD no formato especificado com formatação consistente.
    """
    with open(output_path, 'w', encoding='utf-8') as file:
        # Escrevendo o cabeçalho do AFD
        file.write("# AFD Complemento\n")
        file.write(f"Q: {', '.join(format_state(s) for s in sorted(dfa_states, key=str))}\n")
        file.write(f"Σ: {', '.join(sorted(Sigma))}\n")
        file.write(f"q0: {format_state(dfa_start_state)}: inicial\n")
        file.write(f"F: {', '.join(format_state(f) for f in sorted(new_final_states, key=str))}\n")
        file.write("δ:\n")
        
        # Escrevendo as transições (no formato {estado}, simbolo -> {estado seguinte})
        for (state, symbol), next_states in sorted(dfa_delta.items(), key=lambda x: (str(x[0]), x[1])):
            # O next_states precisa ser uma lista de estados, e não uma lista de frozensets
            # Então, vamos processar para extrair o formato correto para os estados
            for next_state in next_states:
                if isinstance(next_state, frozenset):
                    next_state_str = "{" + ", ".join(sorted(next_state)) + "}"
                else:
                    next_state_str = str(next_state)

                # Grava as transições sem quebras de linha extras
                file.write(f"{format_state(state)}, {symbol} -> {next_state_str}\n")

def format_state(state):
    """
    Formata o estado para o formato desejado (com chaves).
    """
    if isinstance(state, frozenset):  # Verifica se o estado é um frozenset
        return "{" + ", ".join(sorted(state)) + "}"  # Ordena os estados e os coloca entre chaves
    return str(state)