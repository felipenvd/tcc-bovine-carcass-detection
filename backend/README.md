# 🐂 Backend - API de Detecção de Carcaças Bovinas

API RESTful construída com **FastAPI** para detecção de lesões e perdas em carcaças bovinas utilizando **YOLOv11**.

---

## 📖 Visão Geral

Este backend fornece endpoints para upload e análise de imagens de carcaças bovinas, retornando:
- Detecções de **Lesões** e **Perdas**
- Níveis de confiança
- Imagem anotada com bounding boxes

---

## 🛠️ Stack Tecnológica

| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| Python | 3.12+ | Linguagem base |
| FastAPI | 0.128+ | Framework web assíncrono |
| Ultralytics | 8.3+ | Framework YOLOv11 |
| OpenCV | 4.11+ | Processamento de imagens |
| uv | Latest | Gerenciador de pacotes Python |

---

## 📁 Estrutura

```
backend/
├── app/
│   ├── main.py           # Entrypoint, rotas e configuração CORS
│   ├── yolo_service.py   # Serviço de inferência YOLOv11
│   └── models/
│       └── best.pt       # Pesos do modelo treinado
├── Dockerfile            # Configuração Docker
├── pyproject.toml        # Dependências (uv)
├── uv.lock               # Lockfile de dependências
└── README.md             # Este arquivo
```

---

## 🚀 Como Rodar

### Opção 1: Docker (Recomendado)

```bash
# A partir da raiz do projeto
docker compose up --build backend
```

### Opção 2: Localmente com uv

```bash
cd backend

# Sincronizar dependências e iniciar servidor
uv run uvicorn app.main:app --reload

# Servidor disponível em: http://localhost:8000
```

---

## 🔌 Endpoints da API

### `GET /`
Health check da API.

**Response:**
```json
{
  "message": "API de Detecção de Carcaças Bovinas Online"
}
```

---

### `POST /predict`
Recebe uma imagem e retorna as detecções do modelo.

**Request:**
- `Content-Type`: `multipart/form-data`
- `file`: Arquivo de imagem (JPEG, PNG)

**Response:**
```json
{
  "filename": "carcaca.jpg",
  "detections": [
    {
      "class": "Lesao",
      "confidence": 0.87,
      "box": [x, y, width, height]
    },
    {
      "class": "Perda",
      "confidence": 0.92,
      "box": [x, y, width, height]
    }
  ],
  "summary": "Crítico (Lesão e Perda)",
  "annotated_image": "data:image/jpeg;base64,..."
}
```

**Status Possíveis no `summary`:**
| Status | Condição |
|--------|----------|
| `Normal` | Nenhuma detecção |
| `Atenção (Lesão Detectada)` | Apenas lesão(ões) |
| `Perda Identificada` | Apenas perda(s) |
| `Crítico (Lesão e Perda)` | Ambos detectados |

---

## 📚 Documentação Interativa

Após iniciar o servidor, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## 🎨 Cores das Detecções

| Classe | Cor |
|--------|-----|
| Lesão | 🔴 Vermelho |
| Perda | 🟠 Laranja |

---

## ⚙️ Configuração CORS

A API está configurada para aceitar requisições de qualquer origem (`*`), ideal para desenvolvimento. Para produção, restrinja as origens permitidas em `app/main.py`.

---

## 📦 Dependências

Gerenciadas via `uv` no arquivo `pyproject.toml`:

```toml
dependencies = [
    "fastapi>=0.128.0",
    "numpy>=2.4.0",
    "opencv-python-headless>=4.11.0.86",
    "python-multipart>=0.0.21",
    "ultralytics>=8.3.246",
    "uvicorn>=0.40.0",
]
```

Para adicionar novas dependências:
```bash
uv add <pacote>
```

---

## 🐳 Docker

O Dockerfile utiliza a imagem oficial do `uv` com Python 3.12:

```dockerfile
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
```

Inclui dependências do sistema para OpenCV (`libgl1`, `libglib2.0-0`).

---

## 👨‍💻 Autores

Felipe Vidal e José Pires

Desenvolvido como parte do TCC em **Sistemas de Informação**.
