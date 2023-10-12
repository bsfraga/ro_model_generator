# Nome do Projeto

Descrição geral do projeto aqui.

## Scripts

### crawler.py

Este script faz o scraping de sprites de monstros de Ragnarok Online de um site específico. Ele baixa esses sprites e os armazena em diretórios correspondentes a cada monstro.

### folder_mapping.py

Este script mapeia pastas contendo sprites e gera um arquivo JSON correspondente que detalha informações como o número de imagens na pasta, a dimensão das imagens e a cor dominante.

### model_builder.py

Este script é responsável por processar arquivos JSON que contêm informações sobre imagens em um diretório. Ele agrupa as imagens por dimensões, encontra o grupo com a maior quantidade de imagens e calcula a cor dominante média para esse grupo. Em seguida, ele filtra as imagens com base na cor dominante média e atualiza o arquivo JSON.

### negative_recorder.py

Este script ajuda a registrar sprites negativos para treinamento do modelo. Ele lê um arquivo de anotações em formato JSON e compara as imagens de sprite com as anotações. Se um sprite não corresponder a uma anotação, ele é registrado como um sprite negativo.

### pre_process.py

Este script processa arquivos JSON e imagens em diretórios de treinamento. Ele lê os arquivos JSON, filtra os dados e sobrescreve os arquivos com as informações filtradas. Além disso, ele remove as imagens que não estão nos dados filtrados.

### sprite_cutter.py

Este script corta sprites de uma folha de sprite. Ele lê a folha de sprite e as informações de corte de um arquivo JSON. Em seguida, ele corta a folha de sprite em sprites individuais com base nessas informações e salva os sprites em um diretório específico.

### sprite_gather.py

Este script coleta sprites de diversos diretórios e os coloca em um diretório comum. Ele faz isso para reunir dados para treinamento do modelo.

### training_data_handler.py

Este script lida com a manipulação e organização de dados de treinamento. Ele percorre subdiretórios dentro de um diretório base, processando arquivos JSON e realizando a limpeza dos dados conforme necessário.

## Dependências

As dependências necessárias para executar os scripts podem ser encontradas no arquivo `requirements.txt`.

Para instalar as dependências, execute:

```bash
pip install -r requirements.txt
```

### requirements.txt 

numpy
requests
lxml
tensorflow
opencv-python
Pillow
scikit-learn
pandas
pygetwindow
keyboard
pyautogui
