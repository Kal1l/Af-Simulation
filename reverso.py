from collections import defaultdict

def afd_reverso(dfa_states, Sigma, dfa_delta, dfa_start_state, dfa_final_states):
    # 1. Inverter as transições
    reversed_delta = defaultdict(list)
    for (state, symbol), next_state in dfa_delta.items():
        reversed_delta[(next_state, symbol)].append(state)

    # 2. Novos estados finais e estado inicial
    new_final_states = {dfa_start_state}
    new_start_state = frozenset(dfa_final_states)  # Novo estado inicial é um conjunto dos estados finais
    
    # 3. Gerar os novos estados
    unprocessed_states = [new_start_state]
    processed_states = set()  # Usando um set para armazenar os estados processados
    new_dfa_states = []

    while unprocessed_states:
        current_state = unprocessed_states.pop()
        if current_state not in processed_states:
            processed_states.add(current_state)  # Adiciona o estado como frozenset
            new_dfa_states.append(current_state)
            
            # Adicionar os próximos estados
            for symbol in Sigma:
                next_state = set()
                for sub_state in current_state:
                    if (sub_state, symbol) in reversed_delta:
                        next_state.update(reversed_delta[(sub_state, symbol)])
                next_state = frozenset(next_state)  # Converter para frozenset
                
                if next_state and next_state not in processed_states:
                    unprocessed_states.append(next_state)
    
    return new_dfa_states, Sigma, reversed_delta, new_start_state, new_final_states

def format_state(state):
    # Se o estado for um frozenset, converta ele para string de forma ordenada
    if isinstance(state, frozenset):
        return "{" + ", ".join(sorted(str(x) for x in state)) + "}" if state else "∅"
    return str(state)  # Caso contrário, converte o estado para string

def save_reversed_afd(output_path, reversed_dfa_states, Sigma, reversed_dfa_delta, reversed_dfa_start_state, reversed_dfa_final_states):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write("# AFD Reverso\n")
        file.write(f"Q: {', '.join(sorted(format_state(s) for s in reversed_dfa_states))}\n")
        file.write(f"Σ: {', '.join(Sigma)}\n")
        file.write(f"q0: {format_state(reversed_dfa_start_state)}: inicial\n")
        file.write(f"F: {', '.join(sorted(format_state(f) for f in reversed_dfa_final_states))}\n")
        file.write("δ:\n")
        for (state, symbol), next_state in reversed_dfa_delta.items():
            file.write(f"{format_state(state)}, {symbol} -> {', '.join(format_state(ns) for ns in next_state)}\n")
