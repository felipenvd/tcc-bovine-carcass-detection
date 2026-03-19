# 🐂 Frontend - MeatGuard

Interface web moderna para o sistema de detecção de lesões e perdas em carcaças bovinas, construída com **React 19**, **TypeScript** e **Tailwind CSS 4**.

---

## 📖 Visão Geral

Aplicação SPA (Single Page Application) que oferece:
- Upload de imagens via **drag-and-drop**
- Visualização em tempo real das detecções
- Exibição da imagem anotada com bounding boxes
- Página "Sobre" com informações dos pesquisadores

---

## 🛠️ Stack Tecnológica

| Tecnologia | Versão | Propósito |
|------------|--------|-----------|
| React | 19.x | Biblioteca de UI componentizada |
| TypeScript | 5.9 | Tipagem estática |
| Vite | 7.x | Build tool de alta performance |
| Tailwind CSS | 4.x | Estilização utilitária moderna |
| Lucide React | Latest | Ícones SVG |

---

## 📁 Estrutura

```
frontend/
├── public/                     # Assets estáticos (imagens, logos)
├── src/
│   ├── components/
│   │   ├── Header.tsx          # Navegação e cabeçalho
│   │   ├── ImageUpload.tsx     # Upload drag-and-drop
│   │   ├── AnalysisResult.tsx  # Exibição dos resultados
│   │   └── About.tsx           # Página sobre os pesquisadores
│   ├── assets/                 # Assets importáveis
│   ├── App.tsx                 # Componente principal
│   ├── main.tsx                # Entrypoint React
│   └── index.css               # Estilos Tailwind
├── Dockerfile                  # Build multi-stage + Nginx
├── package.json                # Dependências npm
├── vite.config.ts              # Configuração Vite
├── tailwind.config.js          # Configuração Tailwind
└── README.md                   # Este arquivo
```

---

## 🚀 Como Rodar

### Opção 1: Docker (Recomendado)

```bash
# A partir da raiz do projeto
docker compose up --build frontend

# Disponível em: http://localhost
```

### Opção 2: Localmente com npm

```bash
cd frontend

# Instalar dependências
npm install

# Iniciar servidor de desenvolvimento
npm run dev

# Disponível em: http://localhost:5173
```

---

## 📜 Scripts Disponíveis

| Script | Comando | Descrição |
|--------|---------|-----------|
| `dev` | `npm run dev` | Inicia servidor de desenvolvimento |
| `build` | `npm run build` | Compila para produção |
| `preview` | `npm run preview` | Preview da build de produção |
| `lint` | `npm run lint` | Executa ESLint |

---

## 🧩 Componentes

### `Header`
Cabeçalho fixo com navegação entre páginas (Home/Sobre).

### `ImageUpload`
- Upload via clique ou drag-and-drop
- Preview da imagem selecionada
- Estado de loading durante inferência
- Suporte a JPEG e PNG

### `AnalysisResult`
- Exibe imagem anotada com bounding boxes
- Lista detecções com classe e confiança
- Status geral (Normal, Atenção, Crítico)
- Botão para download da imagem anotada
- Opção de nova análise

### `About`
- Informações sobre o projeto
- Perfis dos pesquisadores com links para redes sociais

---

## 🎨 Design System

O projeto utiliza uma paleta **Agro-Tech** com tons de verde:

| Cor | Hex | Uso |
|-----|-----|-----|
| Verde Escuro | `#1a472a` | Títulos, elementos primários |
| Verde Médio | `#2d5a3d` | Gradientes, hovers |
| Verde Oliva | `#6b8e23` | Acentos, gradientes |
| Vermelho | `#dc2626` | Indicador de Lesão |
| Âmbar | `#d97706` | Indicador de Perda |

### Animações
- `animate-slide-up`: Entrada suave de baixo para cima
- Transições suaves em hovers e estados

---

## 🔌 Integração com Backend

A aplicação se comunica com o backend via:

```
POST http://localhost:8000/predict
Content-Type: multipart/form-data
Body: file (imagem)
```

> ⚠️ **Nota:** Certifique-se de que o backend está rodando antes de usar a interface.

---

## 🐳 Docker

Build multi-stage com duas etapas:

1. **Builder**: Node 20 Alpine - compila a aplicação
2. **Runtime**: Nginx Alpine - serve os arquivos estáticos

```dockerfile
FROM node:20-alpine AS builder
# ... build ...

FROM nginx:alpine
# ... serve ...
```

---

## 📦 Dependências Principais

### Produção
- `react` / `react-dom` - Framework UI
- `lucide-react` - Biblioteca de ícones
- `file-saver` - Download de arquivos
- `react-medium-image-zoom` - Zoom em imagens

### Desenvolvimento
- `typescript` - Tipagem estática
- `vite` - Build tool
- `tailwindcss` - CSS utilitário
- `eslint` - Linting

---

## 👨‍💻 Autores

Felipe Vidal e José Pires

Desenvolvido como parte do TCC em **Sistemas de Informação**.
