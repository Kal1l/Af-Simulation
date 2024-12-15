import AFNtoAFD

def main():
    input_path = 'input.txt'
    
    # Gera o arquivo AFN.txt
    AFNtoAFD.AFN(input_path, 'AFN.txt')  # Aqui chamamos a função para criar o AFN.txt
    
    # Lê e converte o AFN para AFD
    Q, Sigma, delta, q0, F, w = AFNtoAFD.read_afn(input_path)
    dfa_states, Sigma, dfa_delta, dfa_start_state, dfa_final_states = AFNtoAFD.afn_to_afd(Q, Sigma, delta, q0, F)
    
    # Salva o AFD em um arquivo
    AFNtoAFD.save_afd('AFD.txt', dfa_states, Sigma, dfa_delta, dfa_start_state, dfa_final_states)
    
    # Simula a cadeia
    result = AFNtoAFD.simulate(dfa_start_state, dfa_final_states, dfa_delta, w)

    # Imprime os resultados no terminal
    print(f"Cadeia: {w}")
    print(f"Resultado: {result}")
    print("Arquivos gerados: AFN.txt, AFD.txt")

if __name__ == "__main__":
    main()
