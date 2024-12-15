#Arrumar ordem que o programa lê os estados e transições
#Mandar as varíaveis da AFD para o arquivo AFD.txt
#Remover frozen set do arquivo AFD.txt
#Fazer função do complementar
#Fazer função de arquivo do complementar
#Fazer função do reverso
#Fazer função de arquivo do reverso
#fazer função da simulação para informar se é válido ou não

from collections import defaultdict
import itertools

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
    q0 = lines[3].split(',')[0]
    F = lines[-4].split(' -> ')[1].strip()
    w = lines[-1].strip().split(': ')[1]

    print("Q:", Q)
    print("Σ:", Sigma)
    print("δ:", delta)
    print("q0:", q0)
    print("F:", F)
    print("w:", w + "\n")
    
    return Q, Sigma, delta, q0, F, w

def afn_to_afd(Q, Sigma, delta, q0, F):
    dfa_states = []
    dfa_delta = {}
    dfa_start_state = frozenset([q0])
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
            
            next_state = frozenset(next_state)
            dfa_delta[(current_state, symbol)] = next_state
            
            if next_state not in processed_states and next_state not in unprocessed_states:
                unprocessed_states.append(next_state)
            
            if any(sub_state in F for sub_state in next_state):
                dfa_final_states.add(next_state)
    
    return dfa_states, Sigma, dfa_delta, dfa_start_state, dfa_final_states

def main():
    # Gera o arquivo AFN.txt a partir do arquivo de entrada
    AFN('input.txt', 'AFN.txt')
    Q, Sigma, delta, q0, F, w = read_afn('input.txt')
    dfa_states, Sigma, dfa_delta, dfa_start_state, dfa_final_states = afn_to_afd(Q, Sigma, delta, q0, F)
    print("Q:",dfa_states)
    print("δ:",dfa_delta)
    print("q0:",dfa_start_state)
    print("F:",dfa_final_states)


    
    
    print("Arquivos gerados: AFN.txt, AFD.txt")

if __name__ == "__main__":
    main()