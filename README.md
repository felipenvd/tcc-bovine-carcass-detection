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
  <img src="https://img.shields.io/badge/YOLOv11-Ultralytics-00599c?style=for-the-badge" alt="YOLOv11">
</p>

---

## 📖 Visão Geral

Este projeto apresenta um **protótipo computacional** para apoio à **inspeção visual de carcaças bovinas** em ambientes industriais (frigoríficos). Utilizando técnicas de **Deep Learning** com a arquitetura **YOLOv11**, o sistema é capaz de detectar automaticamente:

| Classe | Descrição |
|--------|-----------|
| 🔴 **Lesão** | Danos físicos na carcaça (hematomas, cortes, etc.) |
| 🔵 **Perda** | Áreas de tecido removido ou comprometido |

> **Contexto Acadêmico:** Este sistema foi desenvolvido como parte de um Trabalho de Conclusão de Curso (TCC) em Sistemas de Informação, demonstrando a aplicação prática de conceitos de Engenharia de Software, Visão Computacional e Desenvolvimento Web.

---

## 🎯 Funcionalidades

- ✅ **Upload de Imagens**: Interface drag-and-drop intuitiva
- ✅ **Inferência em Tempo Real**: Processamento via modelo YOLOv11 treinado
- ✅ **Visualização de Resultados**: Exibição clara das classes detectadas e níveis de confiança
- ✅ **Classificação Automática**: Identificação precisa de lesões e perdas
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
                                               │  (Ultralytics)  │
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
| Ultralytics | 8.x+ | Framework para execução do modelo YOLOv11 |
| uv | Latest | Gerenciador de pacotes Python ultrarrápido |

### Modelo de IA
| Componente | Arquivo | Descrição |
|------------|---------|-----------|
| Arquitetura | `YOLOv11 Medium` | Modelo state-of-the-art para detecção de objetos |

| Pesos | `backend/app/models/best.pt` | Pesos treinados no dataset customizado |
| Classes | 2 (Lesão, Perda) | Classes alvo da detecção |

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

### Por que YOLOv11 (Ultralytics)?
- **Acurácia Superior**: Melhor desempenho em relação às versões anteriores (v4, v5, v8).
- **Facilidade de Uso**: API Python intuitiva e robusta.
- **Modernidade**: State-of-the-art em detecção em tempo real.

---

### Opção 1: Docker (Recomendado) 🐳
O jeito mais fácil e rápido de rodar o projeto.

```bash
# Iniciar frontend e backend
docker compose up --build

# Backend: http://localhost:8000/docs
# Frontend: http://localhost
```


### 🐳 Comandos Docker Úteis

Aqui estão alguns comandos essenciais para gerenciar o projeto com Docker:

| Ação | Comando |
|------|---------|
| **Iniciar projeto** | `docker compose up --build` |
| **Parar projeto** | `docker compose down` |
| **Ver logs em tempo real** | `docker compose logs -f` |
| **Reconstruir apenas o Frontend** | `docker compose up -d --build frontend` |
| **Reconstruir apenas o Backend** | `docker compose up -d --build backend` |
| **Ver containers ativos** | `docker compose ps` |

> **Dica:** O backend pode demorar alguns minutos na primeira execução para instalar as dependências. Fique de olho nos logs!

### Opção 2: Instalação Manual
Caso prefira rodar localmente sem Docker.

#### Pré-requisitos
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
│   │   ├── 📁 models/                   # Arquivos do modelo
│   │   │   └── 📄 best.pt               # Pesos YOLOv11 treinados
│   │   ├── 📄 main.py                   # Entrypoint, rotas e CORS
│   │   └── 📄 yolo_service.py           # Serviço de inferência Ultralytics
│   ├── 📄 Dockerfile                    # Configuração Docker Backend
│   └── 📄 pyproject.toml                # Dependências Python (uv)
│
├── 📁 frontend/                         # Aplicação React
│   ├── 📁 public/                       # Assets estáticos (Images, Logo)
│   ├── 📁 src/
│   │   ├── 📁 components/
│   │   │   ├── 📄 Header.tsx            # Cabeçalho do sistema
│   │   │   ├── 📄 ImageUpload.tsx       # Upload drag-and-drop
│   │   │   └── 📄 AnalysisResult.tsx    # Exibição de resultados
│   │   ├── 📄 App.tsx                   # Componente principal
│   │   └── 📄 index.css                 # Estilos Tailwind
│   ├── 📄 Dockerfile                    # Configuração Docker Frontend
│   └── 📄 package.json
│
├── 📄 compose.yaml                      # Orquestração Docker (V2)
│
├── 📁 modelo-tcc/                       # Projeto de Treinamento e Dataset
│   ├── 📁 dataset/                      # Imagens e anotações
│   ├── 📁 runs/                         # Logs de treinamento e pesos
│   └── 📄 README.md                     # Detalhes do treinamento
│
├── 📁 docs/                             # Documentação adicional
│
└── 📄 README.md                         # Este arquivo
```

---

## 📊 Dataset e Treinamento

O modelo foi treinado utilizando a arquitetura **YOLOv11**, focando em duas classes principais: **Lesão** e **Perda**.

Para detalhes aprofundados sobre a metodologia de treinamento, distribuição do dataset, pré-processamento (data augmentation) e resultados, consulte a documentação específica em:

👉 [**Documentação do Modelo e Treinamento**](./modelo-tcc/README.md)

---

## 📚 Referências

- **Ultralytics YOLO**: Jocher, G., Chaurasia, A., & Qiu, J. (2023). *Ultralytics YOLO*. https://github.com/ultralytics/ultralytics
- **FastAPI**: Ramírez, S. (2018). *FastAPI Documentation*. https://fastapi.tiangolo.com/
- **React**: Facebook. *React Documentation*. https://react.dev/

---

## 👨‍💻 Autor

Felipe Vidal e José Pires

Desenvolvido como Trabalho de Conclusão de Curso em **Sistemas de Informação**.

---

## 📝 Licença

Este projeto é de uso acadêmico. Para uso comercial ou redistribuição, entre em contato com o autor.
