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
- [ ] Treinamento do modelo baseline (YOLOv11 Nano)
- [ ] Análise das métricas iniciais

### Etapa 4: Validação e Ajustes 📅
- [ ] Matriz de confusão
- [ ] Testes com imagens de validação
- [ ] Ajuste de hiperparâmetros (se necessário)

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

### Treinamento
```bash
uv run train.py
```

---

## 📂 Estrutura do Projeto

### Raiz (`/`)
Arquivos principais para configuração e execução do treinamento.
- **`train.py`**: Script principal. Carrega o modelo YOLOv11, configura os hiperparâmetros (conservadores) e inicia o treinamento.
- **`yolo11n.pt`**: Pesos pré-treinados do YOLOv11 Nano (ponto de partida).
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
