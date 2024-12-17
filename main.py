import os
import src.AFNtoAFD as AFNtoAFD
import src.reverso as reverso
import src.complement as complement
import src.AFNreversetoAFD as AFNreversetoAFD

def main():
    results_dir = 'results'
    os.makedirs(results_dir, exist_ok=True)
    
    input_path = 'input.txt'
    output_path_reverso = os.path.join(results_dir, "AFN_reverso.txt")
    afd_path = os.path.join(results_dir, 'AFD.txt')
    rev_path = os.path.join(results_dir, 'REV.txt')
    comp_path = os.path.join(results_dir, 'COMP.txt')
    afn_path = os.path.join(results_dir, 'AFN.txt')

    # Gera o arquivo AFN.txt a partir do arquivo de entrada
    AFNtoAFD.AFN(input_path, afn_path) 
    Q, Sigma, delta, q0, F, w = AFNtoAFD.read_afn(input_path)
    dfa_states, Sigma, dfa_delta, dfa_start_state, dfa_final_states = AFNtoAFD.afn_to_afd(Q, Sigma, delta, q0, F)
    AFNtoAFD.save_afd(afd_path, dfa_states, Sigma, dfa_delta, dfa_start_state, dfa_final_states)    
    result = AFNtoAFD.simulate(dfa_start_state, dfa_final_states, dfa_delta, w)    
    
    # Reversão do AFN e conversão para AFD
    dfa_states, Sigma, dfa_delta, dfa_start_state, dfa_final_states = reverso.afn_reverso_para_afd(Q, Sigma, delta, q0, F)
    reverso.save_reversed_afn(output_path_reverso, dfa_states, Sigma, dfa_delta, dfa_start_state, dfa_final_states)

    Q, Sigma, delta, q0, F, w = AFNreversetoAFD.read_afn(output_path_reverso)
    dfa_states, Sigma, dfa_delta, dfa_start_state, dfa_final_states = AFNtoAFD.afn_to_afd(Q, Sigma, delta, q0, F)
    AFNreversetoAFD.save_afd(rev_path, dfa_states, Sigma, dfa_delta, dfa_start_state, dfa_final_states)

    dfa_states, Sigma, dfa_delta, dfa_start_state, dfa_final_states = complement.ler_afd_do_arquivo(afd_path)
    
    # Complementar o AFD
    complemented_dfa_states, Sigma, complemented_dfa_delta, complemented_dfa_start_state, complemented_dfa_final_states = complement.afd_complemento(
        dfa_states, Sigma, dfa_delta, dfa_start_state, dfa_final_states
    )
    
    # Salvar o AFD complementado em um arquivo
    complement.save_complement_afd(comp_path, complemented_dfa_states, Sigma, complemented_dfa_delta, complemented_dfa_start_state, complemented_dfa_final_states)
    
    print(f"Cadeia: {w}")
    print(f"Resultado: {result}")
    print(f"Arquivos gerados na pasta '{results_dir}': AFN.txt, AFD.txt, REV.txt, COMP.txt")

if __name__ == "__main__":
    main()
