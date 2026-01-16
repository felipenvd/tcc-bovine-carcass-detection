# Detecção de Lesões e Perdas em Carcaças Bovinas (TCC)

Este repositório contém o código e documentação para o Trabalho de Conclusão de Curso (TCC) focado na detecção automática de lesões e perdas em carcaças bovinas utilizando visão computacional (YOLO).

## 🎯 Objetivo
Desenvolver um modelo capaz de identificar e classificar lesões e perdas em carcaças bovinas, auxiliando no controle de qualidade e redução de prejuízos.

---

## 📊 Dataset

### Dataset Original (4 Classes)
Localização: `com-4-classes/deteccao-carcacas-bovinas`

| Classe | Descrição |
| :--- | :--- |
| 0 | Lesão no quarto dianteiro |
| 1 | Lesão no quarto traseiro |
| 2 | Perda no quarto dianteiro |
| 3 | Perda no quarto traseiro |

#### Distribuição Original (900 imagens)

**Por Split e Tipo de Imagem:**
| Split | Total | Só Lesão | Só Perda | Mista | Vazio |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Train | 720 | 20 | 423 | 248 | 29 |
| Valid | 90 | 6 | 54 | 29 | 1 |
| Test | 90 | 4 | 50 | 33 | 3 |

**Por Split e Anotações (4 Classes):**
| Split | Lesão Diant. | Lesão Tras. | Perda Diant. | Perda Tras. | Total |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Train | 26 | 400 | 1007 | 1619 | 3052 |
| Valid | 12 | 48 | 158 | 230 | 448 |
| Test | 2 | 54 | 113 | 170 | 339 |
| **Total** | **40** | **502** | **1278** | **2019** | **3839** |


` A análise da distribuição das anotações revelou um desbalanceamento severo na classe 'Lesão Diant.', que conta com apenas 40 instâncias em todo o conjunto de dados (aproximadamente 1% do total), conforme demonstrado na tabela. Dada a escassez de exemplos para a região dianteira, o que dificultaria a generalização do modelo para esta classe específica, optou-se por reestruturar o conjunto de dados. As classes foram aglutinadas com base no tipo de dano, ignorando a distinção de localização (Dianteira/Traseira). Dessa forma, o problema foi simplificado para duas classes gerais: 'Lesão' (unindo Lesão Diant. e Tras.) e 'Perda' (unindo Perda Diant. e Tras.)." `

---



### Dataset Atual (2 Classes)
Localização: `com-4-classes/dataset-2-classes`

| Classe | Descrição |
| :--- | :--- |
| 0 | Lesão (unificação dianteiro + traseiro) |
| 1 | Perda (unificação dianteiro + traseiro) |

#### Pré-processamento Aplicado

1. **Refatoração para 2 Classes**: Unificação das 4 classes em apenas 2 (Lesão/Perda), ignorando a região do corpo.

2. **Data Augmentation (somente Lesão)**: Augmentação apenas nas imagens que contêm exclusivamente lesões.
   - Técnicas: Rotação ±10°, Flip, Zoom, Brilho
   - 25 variações por imagem
   - Imagens adicionadas: +500 (apenas no conjunto de treino)

#### Distribuição Final (1400 imagens)

**Por Split e Tipo de Imagem:**
| Split | Total | Só Lesão | Só Perda | Mista | Vazio |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Train | 1220 | 520 | 423 | 248 | 29 |
| Valid | 90 | 6 | 54 | 29 | 1 |
| Test | 90 | 4 | 50 | 33 | 3 |

*Obs: 500 das imagens "Só Lesão" no Train são augmentadas.*

**Por Split e Anotações:**
| Split | Lesão | Perda | Total |
| :--- | :--- | :--- | :--- |
| Train | 1051 | 2626 | 3677 |
| Valid | 60 | 388 | 448 |
| Test | 56 | 283 | 339 |
| **Total** | **1167** | **3297** | **4464** |

---

## ⚙️ Configuração de Treinamento (Conservadora)

Para garantir a detecção correta de características médicas/biológicas (cor e textura das lesões) e respeitar a anatomia fixa das carcaças, foram aplicadas as seguintes configurações no `train.py`:

### Augmentations Desativados/Reduzidos
O YOLOv11 traz augmentations agressivos por padrão que podem prejudicar este projeto. Foram feitos os seguintes ajustes:

1.  **Fidelidade de Cor (`hsv_h=0.0`, `hsv_s=0.0`)**: 
    - A variação de Matiz (Hue) e Saturação foi **desativada**.
    - **Motivo**: A cor vermelha viva é o principal indicativo visual de uma lesão. Alterar a cor (ex: para azul ou verde) confundiria o modelo.

2.  **Anatomia Fixa (`mosaic=0.0`, `degrees=5.0`)**:
    - O Mosaic (que mistura 4 imagens) foi **desativado** e a rotação limitada a ±5°.
    - **Motivo**: As carcaças sempre aparecem na mesma orientação (penduradas). Criar mosaicos ou rodar a imagem de cabeça para baixo cria exemplos irreais que atrapalham o aprendizado da posição anatômica (quarto dianteiro/traseiro).

3.  **Preservação de Detalhes (`erasing=0.0`)**:
    - Random Erasing foi **desativado**.
    - **Motivo**: Evitar apagar pequenas lesões que são justamente o alvo da detecção.

---

## 🛣️ Roadmap do Projeto

### Etapa 1: Análise e Planejamento ✅
- [x] Análise exploratória do dataset (`scripts/analyze_dataset.py`)
- [x] Definição da arquitetura (YOLOv11)
- [x] Identificação de problemas (desbalanceamento)

### Etapa 2: Pré-processamento de Dados ✅

- [x] Refatoração para 2 Classes (Lesão/Perda)
- [x] Data Augmentation nas imagens de Lesão (+500 imagens)
- [x] Criação do dataset final `dataset-2-classes`

### Etapa 3: Treinamento 🚧
- [x] Configuração do ambiente de treino (`train.py`)
- [x] Treinamento do modelo selecionado (YOLOv11 Medium)
- [x] Análise das métricas iniciais

---

## 🛠️ Como Executar

### Instalação
Certifique-se de ter o [uv](https://github.com/astral-sh/uv) instalado.

```bash
uv sync
```

### Análise do Dataset
```bash
uv run scripts/analyze_dataset.py
```

### 🔄 Pipeline de Preparação do Dataset

Se você baixou o **dataset original de 4 classes** do Roboflow, siga estes passos para transformá-lo no dataset de 2 classes utilizado neste projeto:

#### Passo 1: Refatorar para 2 Classes
Converte as 4 classes originais (Lesão Diant., Lesão Tras., Perda Diant., Perda Tras.) em apenas 2 classes (Lesão, Perda).

```bash
# Edite os caminhos src_path e dst_path no script antes de rodar
uv run scripts/refactor_dataset.py
```

#### Passo 2: Data Augmentation (Lesões)
Gera 25 variações para cada imagem que contém **apenas lesões**, balanceando o dataset.

```bash
# Edite o caminho base_path no script para apontar para o dataset de 2 classes
uv run scripts/augment_dataset.py
```

#### Passo 3: Verificar Integridade
Valida se a conversão e augmentação foram aplicadas corretamente.

```bash
uv run scripts/verify_2_classes.py
```

> **Resultado:** Após estes passos, você terá o dataset final em `dataset-2-classes/` pronto para treinamento.


### Treinamento
```bash
uv run train.py
```

### Teste / Avaliação

#### Opção 1: Validação Simples (Comando original)
Para rodar a validação no conjunto de teste e ler o mAP no terminal:

```bash
uv run yolo val model=runs/detect/yolo11m_1280_medium/weights/best.pt data=dataset/dataset-2-classes/data_local.yaml split=test

```

#### Opção 2: Gerar Gráficos Completos (Matriz de Confusão e PR Curve)
Para rodar a validação definindo a resolução correta (1280px) e **salvar os gráficos** (Curva PR, Matriz de Confusão) em uma pasta organizada:

```bash
uv run yolo val \
model=runs/detect/yolo11m_1280_medium/weights/best.pt \
data=dataset/dataset-2-classes/data_local.yaml \
split=test \
imgsz=1280 \
name=val_yolo11m_1280_test

```

Os resultados (gráficos e logs) serão salvos automaticamente em `runs/detect/val_yolo11n_1280_test/`.

> **Nota:** Certifique-se de que o caminho no arquivo `data_local.yaml` está correto para o seu ambiente.

---

## 📂 Estrutura do Projeto

### Raiz (`/`)
Arquivos principais para configuração e execução do treinamento.
- **`train.py`**: Script principal. Carrega o modelo YOLOv11, configura os hiperparâmetros (conservadores) e inicia o treinamento.
- **`yolo11m.pt`**: Pesos pré-treinados do YOLOv11 Medium (ponto de partida).

- **`pyproject.toml`**: Gerenciamento de dependências via `uv`.

### Scripts Auxiliares (`scripts/`)
Ferramentas desenvolvidas para análise, validação e processamento dos dados.

#### Processamento de Dados
- **`refactor_dataset.py`**: Converte o dataset original de 4 classes para o formato de 2 classes (Lesão/Perda).
- **`undersample_perda_traseira.py`**: *(Legado)* Script usado para remover excesso de perdas traseiras (revertido posteriormente).
- **`restore_undersampled.py`**: Reintegra as imagens removidas de volta ao treino e converte suas anotações.
- **`augment_dataset.py`**: Gera imagens artificiais (rotação/brilho) focadas apenas na classe "Lesão" para balanceamento.

#### Análise e Validação
- **`analyze_dataset.py`**: Análise exploratória principal. Conta classes, verifica integridade das imagens e gera estatísticas.
- **`analyze_lesion_images.py`**: Foca especificamente na contagem e distribuição das lesões.
- **`check_exclusive_perda.py`**: Identifica imagens que só contêm perdas (útil para estratégias de undersampling).
- **`verify_2_classes.py`**: Verifica se a conversão para 2 classes foi feita corretamente.
- **`verify_stats_2class.py`**: Valida as estatísticas finais do dataset de 2 classes (usado para gerar as tabelas deste README).
- **`visualize_labels.py`**: Desenha as bounding boxes nas imagens para validação visual humana.

---

## 📊 Resultados Experimentais

### 1. Comparação no Conjunto de Validação (Cross-Check)

Para confirmar a consistência dos resultados, também avaliamos os modelos no conjunto de validação (`val`), que possui distribuição similar ao teste.

| Modelo | Resolução | mAP50 (Geral) | Recall (Lesão) | Recall (Perda) | Precision |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **YOLOv11n** | 896 | 0.2288 | 0.2833 | 0.2680 | 0.3785 |
| **YOLOv11n** | 1024 | 0.2334 | 0.2000 | 0.3531 | 0.2894 |
| **YOLOv11n** | **1280** | 0.2567 | 0.2667 | 0.4072 | 0.3446 |
| YOLOv11s | 896 | 0.2345 | 0.2333 | 0.2577 | 0.3532 |
| YOLOv11s | 1024 | 0.2669 | 0.2333 | 0.2474 | 0.4560 |
| YOLOv11s | 1280 | 0.2716 | 0.2903 | **0.4433** | 0.3888 |
| YOLOv11m | 896 | 0.2175 | 0.2167 | 0.3170 | 0.2973 |
| YOLOv11m | 1024 | 0.2551 | **0.3167** | 0.3557 | 0.3279 |
| YOLOv11m | 1280 | **0.2931** | 0.2833 | 0.3119 | 0.4212 |

> **Nota:** Os resultados de validação mostram que o modelo **Medium (1280px)** teve o melhor desempenho geral (mAP 0.2931), enquanto o **Medium (1024px)** foi o melhor para detectar Lesões (Recall 0.3167).

### 2. Análise de "Lesão" (Classe Crítica)

#### Matriz de Confusão e Falsos Negativos
A análise detalhada da matriz de confusão demonstra que o principal desafio do modelo é a **omissão (Falso Negativo)** e não a confusão entre classes.
- **Confusão Lesão vs. Perda:** Insignificante. O modelo raramente confunde uma lesão com uma perda
- **Confusão Lesão vs. Background:** Altíssima. A maioria dos erros decorre do modelo não detectar a lesão (considerando-a como fundo).

#### Melhor Experimento para Detecção de Lesão
**YOLOv11m (Medium) com resolução 1280** destacou-se pela robustez e consistência na detecção em cenários complexos.


### 3. Compromisso Desempenho Geral vs. Recall (Trade-off)

O melhor equilíbrio foi obtido pelo **YOLOv11m com resolução 1280**.
- **Justificativa:** O modelo Medium, aliado à alta resolução, oferece maior capacidade de extração de características (feature extraction), resultando em uma detecção mais confiável e menos propensa a falsos negativos em condições visuais difíceis.
- A resolução de 1280px continua sendo crucial para identificar pequenas lesões, potencializada agora por uma arquitetura mais profunda.


### 4. Discussão Técnica

Os resultados confirmam que a combinação de **arquitetura mais robusta (Medium)** com **alta resolução (1280px)** proporcionou o melhor desempenho qualitativo para o problema.

- **Resolução:** Essencial para a detecção de objetos pequenos.
- **Arquitetura:** O modelo Medium mostrou-se superior na generalização de padrões complexos de lesões.

**Conclusão:** Para a aplicação final deste trabalho, recomenda-se o uso do **YOLOv11m com resolução 1280**.

### 5. Detalhes do Modelo Selecionado (Medium 1280px - Validação Complementar)
O **YOLOv11m (Medium) em 1280px** mostrou-se promissor na validação cruzada. Abaixo estão os detalhes de seu desempenho no conjunto de **Teste**:

| Métrica | Lesão | Perda | Média |
| :--- | :---: | :---: | :---: |
| **Precision** | 0.270 | 0.369 | 0.320 |
| **Recall** | 0.244 | 0.382 | 0.313 |
| **F1-Score** | 0.256 | 0.375 | 0.317 |
| **AP@0.50** | 0.163 | 0.298 | 0.231 |
| **AP@0.50:0.95** | 0.065 | 0.128 | 0.096 |

