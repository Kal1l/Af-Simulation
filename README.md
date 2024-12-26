# AF-Simulation

Este projeto em Python realiza a conversão de Autômatos Finitos Não Determinísticos (AFN) para Autômatos Finitos Determinísticos (AFD), além de realizar operações de reversão e complemento em autômatos.

## Estrutura do Projeto

- `main.py`: Script principal que executa as operações de conversão, reversão e complemento.
- `src/AFNtoAFD.py`: Módulo que contém funções para converter AFN para AFD.
- `src/reverso.py`: Módulo que contém funções para reverter um AFN.
- `src/complement.py`: Módulo que contém funções para complementar um AFD.
- `src/AFNreversetoAFD.py`: Módulo que contém funções para ler e salvar autômatos.

## Funcionalidades

1. **Conversão de AFN para AFD**:
   - Leitura de um AFN a partir de um arquivo de entrada.
   - Conversão do AFN para AFD.
   - Salvamento do AFD em um arquivo de saída.

2. **Reversão de AFN**:
   - Reversão de um AFN.
   - Conversão do AFN reverso para AFD.
   - Salvamento do AFD reverso em um arquivo de saída.

3. **Complemento de AFD**:
   - Leitura de um AFD a partir de um arquivo.
   - Complemento do AFD.
   - Salvamento do AFD complementado em um arquivo de saída.
  
## Como Executar

1. Modifique o arquivo de entrada da de acordo a estrutura do template
2. Execute o script principal: `python main.py`

## Estrutura do Arquivo de Entrada

O arquivo de entrada `input.txt` deve seguir o seguinte formato:

- `Q`: Conjunto de estados do autômato.
- `Σ`: Alfabeto do autômato.
- `δ`: Função de transição, onde cada linha representa uma transição no formato `estado_atual, símbolo -> estado_destino`.
- `q0`: Estado inicial do autômato.
- `F`: Conjunto de estados finais do autômato.
- `w`: Cadeia de entrada a ser processada pelo autômato.

