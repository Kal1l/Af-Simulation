import AFNtoAFD
import reverso
import complement
import AFN_reverse_to_AFD

def main():
    input_path = 'input.txt'
    
    # Gera o arquivo AFN.txt a partir do arquivo de entrada
    AFNtoAFD.AFN(input_path, 'AFN.txt')  # Aqui chamamos a função para criar o AFN.txt
    
    # Lê e converte o AFN para AFD
    Q, Sigma, delta, q0, F, w = AFNtoAFD.read_afn(input_path)
    dfa_states, Sigma, dfa_delta, dfa_start_state, dfa_final_states = AFNtoAFD.afn_to_afd(Q, Sigma, delta, q0, F)
    
    # Salva o AFD em um arquivo
    AFNtoAFD.save_afd('AFD.txt', dfa_states, Sigma, dfa_delta, dfa_start_state, dfa_final_states)
    
    # Simula a cadeia no AFD original
    result = AFNtoAFD.simulate(dfa_start_state, dfa_final_states, dfa_delta, w)

    # Imprime os resultados no terminal
    print(f"Cadeia: {w}")
    print(f"Resultado: {result}")
    
    # 1. Leitura do arquivo de entrada (AFN original)

    output_path_reverso = "AFN_reverso.txt"

    # 2. Reversão do AFN e conversão para AFD
    dfa_states, Sigma, dfa_delta, dfa_start_state, dfa_final_states = reverso.afn_reverso_para_afd(Q, Sigma, delta, q0, F)
    
    # 3. Salvar o AFD revertido em um arquivo
    reverso.save_reversed_afn(output_path_reverso, dfa_states, Sigma, dfa_delta, dfa_start_state, dfa_final_states)

    Q, Sigma, delta, q0, F, w = AFN_reverse_to_AFD.read_afn(output_path_reverso)
    dfa_states, Sigma, dfa_delta, dfa_start_state, dfa_final_states = AFNtoAFD.afn_to_afd(Q, Sigma, delta, q0, F)
    AFN_reverse_to_AFD.save_afd('REV.txt',dfa_states, Sigma, dfa_delta, dfa_start_state, dfa_final_states)

    dfa_states, Sigma, dfa_delta, dfa_start_state, dfa_final_states = complement.ler_afd_do_arquivo('AFD.txt')
    
    # Complementar o AFD
    complemented_dfa_states, Sigma, complemented_dfa_delta, complemented_dfa_start_state, complemented_dfa_final_states = complement.afd_complemento(
        dfa_states, Sigma, dfa_delta, dfa_start_state, dfa_final_states
    )
    
    # Salvar o AFD complementado em um arquivo
    complement.save_complement_afd('COMP.txt', complemented_dfa_states, Sigma, complemented_dfa_delta, complemented_dfa_start_state, complemented_dfa_final_states)
    
    print("Arquivos gerados: AFN.txt, AFD.txt, REV.txt, COMP.txt")

if __name__ == "__main__":
    main()
