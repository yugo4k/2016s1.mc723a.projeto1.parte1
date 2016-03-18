# Convolução - Grupo 3
## O que faz? Para que serve?
O programa de benchmark processa convoluções em images tridimensionais, o que é uma operação fundamental em processamento de imagens.  
Com ele podem-se realizar transformações geométricas, radiométricas, etc.
No benchmark em questão, a operação de convolução utilizada é a Transformada de Fourier.


## Por que é bom para medir desempenho?
A convolução de imagens é bastante intensiva em processamento e uso de memória, e por ser uma operação extremamente importante para diversas áreas (engenharia, medicina diagnóstica etc), é fundamental avaliar se uma máquina é apropriada para este tipo de uso.

## O que baixar
https://github.com/yugo4k/2016s1.mc723a.projeto1.parte1

## Como compilar/instalar
O programa roda em `python3` e exige que estejam instalados os módulos `numpy` e `multiprocessing`. O ideal é que esses recursos não sejam baixados de repositórios compilados (e.g. _apt-get install_), mas sim sejam compilados através do `pip3` para obter a melhor performance na arquitetura da máquina utilizada.

## Como executar
Basta dar permissão de execução ao arquivo `convolutions.py` e executá-lo; pode-se alterar o número de voxels do cubo, o número de threads utilizadas e o número de convoluções executadas por thread, mas esses parâmetros foram _hardcoded_ para que o desempenho seja igualmente avaliado em todas execuções do programa.  
Ele fornece como output uma sequência na forma:  
```
(ID_THREAD, ID_CONV) VAR_TYPE (N_LAYERS, N_ROWS, N_COLS)  
write: #MB/s  
read: #MB/s  
```  
que se refere, respectivamente, aos identificadores de thread e convolução, o tipo de variável armazenada, as 3 dimensões do cubo e as velocidades de escrita e leitura.  
Os dois últimos valores são estatisticamente avaliados no final do output.

## Como medir o desempenho
Como que o desempenho é medido através deste programa? Se for através de tempo, você deve especificar claramente qual tempo deverá ser utilizado e indicar o motivo aqui. Quantas vezes a medida deverá ser feita? O que fazer com ela (média, etc) ? Não especificar o tempo será considerado falha grave.

## Como apresentar o desempenho
Como o desempenho deverá ser mostrado. Margem de erro, etc. 

## Medições base (uma máquina)
Inclua a especificação dos componentes relevantes e os resultados de desempenho.