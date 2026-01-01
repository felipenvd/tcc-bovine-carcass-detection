<p align="center">
  <h1 align="center">🐂 Sistema de Detecção de Lesões e Perdas em Carcaças Bovinas</h1>
  <p align="center">
    <strong>Protótipo de Visão Computacional para Inspeção Visual Automatizada</strong>
  </p>
  <p align="center">
    <em>Trabalho de Conclusão de Curso — Sistemas de Informação</em>
  </p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-3776ab?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.115+-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/React-19-61dafb?style=for-the-badge&logo=react&logoColor=black" alt="React">
  <img src="https://img.shields.io/badge/TypeScript-5.9-3178c6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/YOLOv4-Darknet-00599c?style=for-the-badge" alt="YOLOv4">
</p>

---

## 📖 Visão Geral

Este projeto apresenta um **protótipo computacional** para apoio à **inspeção visual de carcaças bovinas** em ambientes industriais (frigoríficos). Utilizando técnicas de **Deep Learning** com a arquitetura **YOLOv4**, o sistema é capaz de detectar automaticamente:

| Classe | Descrição |
|--------|-----------|
| 🔴 **Lesão** | Danos físicos na carcaça (hematomas, cortes, etc.) |
| 🔵 **Perda** | Áreas de tecido removido ou comprometido |

> **Contexto Acadêmico:** Este sistema foi desenvolvido como parte de um Trabalho de Conclusão de Curso (TCC) em Sistemas de Informação, demonstrando a aplicação prática de conceitos de Engenharia de Software, Visão Computacional e Desenvolvimento Web.

---

## 🎯 Funcionalidades

- ✅ **Upload de Imagens**: Interface drag-and-drop intuitiva
- ✅ **Inferência em Tempo Real**: Processamento via modelo YOLOv4 treinado
- ✅ **Visualização de Resultados**: Exibição clara das classes detectadas e níveis de confiança
- ✅ **Classificação Automática**: Status da carcaça (Normal, Atenção, Crítico)
- ✅ **API RESTful**: Documentação automática via OpenAPI/Swagger

---

## 🏗️ Arquitetura do Sistema

O sistema segue uma arquitetura **cliente-servidor** com separação clara de responsabilidades:

```
┌─────────────────┐         HTTP/REST          ┌─────────────────┐
│                 │  ──────────────────────▶   │                 │
│    FRONTEND     │       POST /predict        │     BACKEND     │
│  (React + TS)   │  ◀──────────────────────   │   (FastAPI)     │
│                 │       JSON Response        │                 │
└─────────────────┘                            └────────┬────────┘
                                                        │
                                                        ▼
                                               ┌─────────────────┐
                                               │   YOLO MODEL    │
                                               │  (OpenCV DNN)   │
                                               └─────────────────┘
```

### Frontend (Camada de Apresentação)
| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| React | 19.x | Biblioteca para construção de interfaces componentizadas |
| TypeScript | 5.9 | Tipagem estática para maior robustez e manutenibilidade |
| Tailwind CSS | 4.x | Estilização utilitária moderna e responsiva |
| Vite | 7.x | Build tool de alta performance |

### Backend (Camada de Serviço)
| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| Python | 3.10+ | Linguagem base para ML/IA |
| FastAPI | 0.115+ | Framework web assíncrono de alta performance |
| OpenCV | 4.x | Processamento de imagem e execução do modelo DNN |
| uv | Latest | Gerenciador de pacotes Python ultrarrápido |

### Modelo de IA
| Componente | Arquivo | Descrição |
|------------|---------|-----------|
| Arquitetura | `deteccao-carcacas-bovinas.cfg` | Configuração YOLOv4 customizada |
| Pesos | `backup/*_best.weights` | Pesos treinados no dataset balanceado |
| Classes | `deteccao-carcacas-bovinas.names` | Definição das classes (Lesao, Perda) |

---

## 🛠️ Justificativa Tecnológica

### Por que React + TypeScript?
- **Componentização**: Facilita a reutilização e manutenção do código
- **Tipagem Estática**: Reduz erros em tempo de desenvolvimento, essencial para projetos acadêmicos que exigem qualidade de código
- **Ecossistema Maduro**: Ampla documentação e comunidade ativa

### Por que FastAPI?
- **Performance**: Um dos frameworks Python mais rápidos (baseado em Starlette/Uvicorn)
- **Documentação Automática**: Swagger UI integrado em `/docs`
- **Async Nativo**: Ideal para operações de I/O como upload de imagens

### Por que uv ao invés de pip/poetry?
- **Velocidade**: 10-100x mais rápido que pip
- **Reprodutibilidade**: Lock file determinístico via `pyproject.toml`
- **Simplicidade**: Substitui pip, poetry e virtualenv em uma única ferramenta

### Por que OpenCV DNN ao invés de Darknet nativo?
- **Portabilidade**: Não requer compilação da biblioteca Darknet
- **Facilidade de Deploy**: Funciona em qualquer ambiente com Python
- **Manutenção**: Menos dependências externas

---

## 🚀 Como Executar

### Pré-requisitos
```bash
# Node.js (v18+)
node --version

# Python (v3.10+)
python --version

# uv (gerenciador de pacotes Python)
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 1. Backend (API)
```bash
cd backend

# Sincronizar dependências e rodar servidor
uv run uvicorn app.main:app --reload

# Servidor disponível em: http://localhost:8000
# Documentação Swagger: http://localhost:8000/docs
```

### 2. Frontend (Interface)
```bash
cd frontend

# Instalar dependências
npm install

# Rodar servidor de desenvolvimento
npm run dev

# Aplicação disponível em: http://localhost:5173
```

---

## 📦 Estrutura do Projeto

```
tcc-deteccao-carcacas/
│
├── 📁 backend/                          # API FastAPI
│   ├── 📁 app/
│   │   ├── 📄 main.py                   # Entrypoint, rotas e CORS
│   │   └── 📄 yolo_service.py           # Serviço de inferência YOLO
│   └── 📄 pyproject.toml                # Dependências Python (uv)
│
├── 📁 frontend/                         # Aplicação React
│   ├── 📁 src/
│   │   ├── 📁 components/
│   │   │   ├── 📄 Header.tsx            # Cabeçalho do sistema
│   │   │   ├── 📄 ImageUpload.tsx       # Upload drag-and-drop
│   │   │   └── 📄 AnalysisResult.tsx    # Exibição de resultados
│   │   ├── 📄 App.tsx                   # Componente principal
│   │   └── 📄 index.css                 # Estilos Tailwind
│   ├── 📄 tailwind.config.js
│   └── 📄 package.json
│
├── 📁 deteccao-carcacas-bovinas/        # Dataset e Modelo
│   ├── 📁 train/                        # Imagens de treino
│   ├── 📁 valid/                        # Imagens de validação
│   ├── 📁 backup/                       # Checkpoints de pesos (.weights)
│   ├── 📄 *.cfg                         # Configuração YOLOv4
│   └── 📄 *.names                       # Classes do modelo
│
├── 📁 docs/                             # Documentação adicional
│
└── 📄 README.md                         # Este arquivo
```

---

## 📊 Dataset e Treinamento

O modelo foi treinado com um dataset próprio de imagens de carcaças bovinas, aplicando técnicas de **balanceamento por oversampling** para lidar com o desbalanceamento de classes:

| Métrica | Valor |
|---------|-------|
| Total de Imagens | 810 |
| Anotações "Lesão" | 486 (minoritária) |
| Anotações "Perda" | 3014 (majoritária) |
| Estratégia | Oversampling 8x/3x |

> Para detalhes sobre o processo de treinamento, consulte o [README do dataset](./deteccao-carcacas-bovinas/README.md).

---

## 📚 Referências

- **YOLOv4**: Bochkovskiy, A., Wang, C. Y., & Liao, H. Y. M. (2020). *YOLOv4: Optimal Speed and Accuracy of Object Detection*. arXiv preprint arXiv:2004.10934.
- **FastAPI**: Ramírez, S. (2018). *FastAPI Documentation*. https://fastapi.tiangolo.com/
- **OpenCV DNN**: OpenCV Team. *Deep Neural Networks module*. https://docs.opencv.org/4.x/d2/d58/tutorial_table_of_content_dnn.html

---

## 👨‍💻 Autor

Desenvolvido como Trabalho de Conclusão de Curso em **Sistemas de Informação**.

---

## 📝 Licença

Este projeto é de uso acadêmico. Para uso comercial ou redistribuição, entre em contato com o autor.
