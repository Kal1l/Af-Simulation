from collections import defaultdict

def afn_reverso(Q, Sigma, delta, q0, F):
    # Novo conjunto de transições
    reversed_delta = defaultdict(list)
    
    # Invertendo as transições
    for (state, symbol), next_states in delta.items():
        for next_state in next_states:
            reversed_delta[(next_state, symbol)].append(state)
    
    # Novo estado inicial será o conjunto dos estados finais do AFN original
    reversed_start_states = F
    
    # Os novos estados finais serão o estado inicial do AFN original
    reversed_final_states = {q0}
    
    return Q, Sigma, reversed_delta, reversed_start_states, reversed_final_states

def format_state(state):
    # Se o estado for um frozenset, converte ele para string de forma ordenada
    if isinstance(state, frozenset):
        return "{" + ", ".join(sorted(str(x) for x in state)) + "}"
    return str(state)  # Caso contrário, converte o estado para string

def afn_reverso_para_afd(Q, Sigma, delta, q0, F):
    reversed_Q, reversed_Sigma, reversed_delta, reversed_start_state, reversed_final_states = afn_reverso(Q, Sigma, delta, q0, F)
    return reversed_Q, reversed_Sigma, reversed_delta, reversed_start_state, reversed_final_states

def save_reversed_afn(output_path, Q, Sigma, delta, q0, F):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write("# AFN Reverso\n")
        file.write(f"Q: {', '.join(sorted(Q))}\n")
        file.write(f"Σ: {', '.join(sorted(Sigma))}\n")
        file.write("δ:\n")
        for (state, symbol), next_states in delta.items():
            for next_state in next_states:
                file.write(f"{state}, {symbol} -> {next_state}\n")
        file.write(f"{', '.join(q0)}: inicial\n")
        file.write(f"F: {', '.join(sorted(F))}\n")

