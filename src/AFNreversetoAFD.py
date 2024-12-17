#Arrumar ordem que o programa lê os estados e transições
#Fazer função do complementar
#Fazer função de arquivo do complementar
#Fazer função do reverso
#Fazer função de arquivo do reverso
from collections import defaultdict

def read_afn(output_path_reverso):
    with open(output_path_reverso, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Remover espaços extras e quebras de linha
    lines = [line.strip() for line in lines if line.strip()]

    # Verificando se o arquivo tem as seções mínimas necessárias
    if len(lines) < 6:
        raise ValueError("O arquivo não contém o número de linhas esperado. Verifique o formato do arquivo.")

    # Inicializando variáveis
    Q = set()
    Sigma = set()
    delta = defaultdict(list)
    q0 = None
    F = set()
    w = None

    # Buscando a linha que contém Q (estados)
    for line in lines:
        if line.startswith("Q:"):
            Q = set(line.split(': ')[1].split(', '))
        elif line.startswith("Σ:"):
            Sigma = set(line.split(': ')[1].split(', '))
        elif line.startswith("δ:"):  # Início das transições
            continue  # A linha "δ:" pode ser ignorada, pois a próxima linha contém as transições
        elif "->" in line:  # Aqui capturamos as transições
            state, rest = line.split(', ')
            symbol, next_state = rest.split(' -> ')
            delta[(state, symbol)].append(next_state)
        elif line.endswith(": inicial"):  # Estado inicial
            q0 = line.split(': ')[0].strip()
        elif line.startswith("F:"):  # Estados finais
            F = set(line.split(': ')[1].split(', '))
        elif line.startswith("w:"):  # Palavra (não necessariamente utilizada aqui)
            w = line.split(': ')[1].strip()

    # Verificando se todos os dados necessários foram encontrados
    if not Q or not Sigma or not delta or q0 is None or not F:
        raise ValueError("O arquivo está incompleto ou mal formatado. Verifique as seções de Q, Σ, δ, estado inicial e estados finais.")

    return Q, Sigma, delta, q0, F, w

def afn_to_afd(Q, Sigma, delta, q0, F):
    # Lista para armazenar os estados do AFD
    dfa_states = []
    # Dicionário para as transições do AFD
    dfa_delta = {}
    # Estado inicial do AFD como conjunto congelado (frozenset)
    dfa_start_state = frozenset([q0])
    # Conjunto de estados finais do AFD
    dfa_final_states = set()

    # Estado morto (representado por frozenset vazio)
    dead_state = frozenset(["dead_state"])

    # Adicionando o estado inicial do AFD à lista de estados
    if q0 in F:
        dfa_final_states.add(dfa_start_state)

    # Fila de estados não processados (começando com o estado inicial)
    unprocessed_states = [dfa_start_state]
    # Conjunto de estados processados
    processed_states = set()

    while unprocessed_states:
        current_state = unprocessed_states.pop()
        processed_states.add(current_state)

        # Adicionando o estado atual à lista de estados do AFD
        if current_state not in dfa_states:
            dfa_states.append(current_state)

        # Para cada símbolo no alfabeto
        for symbol in Sigma:
            next_state = set()  # Conjunto para armazenar os próximos estados

            # Para cada subestado no conjunto de estados atual
            for sub_state in current_state:
                # Se houver transições no delta do AFN, adicione os próximos estados
                if (sub_state, symbol) in delta:
                    next_state.update(delta[(sub_state, symbol)])

            # Se não houver transições válidas, o próximo estado é o estado morto
            if not next_state:
                next_state = dead_state

            # Convertendo para frozenset (para garantir que sejam tratados como estados únicos)
            next_state = frozenset(next_state)

            # Registrando a transição no AFD
            dfa_delta[(current_state, symbol)] = next_state

            # Se o próximo estado ainda não foi processado, adicione-o à fila de estados não processados
            if next_state not in processed_states and next_state not in unprocessed_states:
                unprocessed_states.append(next_state)

            # Se algum subestado do próximo estado for final no AFN, adicione o estado ao conjunto de estados finais
            if any(sub_state in F for sub_state in next_state):
                dfa_final_states.add(next_state)

    return dfa_states, Sigma, dfa_delta, dfa_start_state, dfa_final_states

def format_state(state):
    # Se o estado for um frozenset vazio, retorna o símbolo "∅"
    if isinstance(state, frozenset) and len(state) == 0:
        return "dead_state"
    if isinstance(state, frozenset):  # Quando o estado é um frozenset com elementos
        return "{" + ", ".join(sorted(str(x) for x in state)) + "}"
    return str(state)  # Caso contrário, converte o estado para string

def save_afd(output_path, dfa_states, Sigma, dfa_delta, dfa_start_state, dfa_final_states):
    """
    Salva o AFD em um arquivo de saída formatado.
    """
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write("# AFD Reverso\n")
        file.write(f"Q: {', '.join(format_state(s) for s in dfa_states)}\n")
        file.write(f"Σ: {', '.join(Sigma)}\n")
        file.write(f"q0: {format_state(dfa_start_state)}: inicial\n")
        file.write(f"F: {', '.join(format_state(f) for f in dfa_final_states)}\n")
        file.write("δ:\n")
        for (state, symbol), next_state in dfa_delta.items():
            file.write(f"{format_state(state)}, {symbol} -> {format_state(next_state)}\n")

