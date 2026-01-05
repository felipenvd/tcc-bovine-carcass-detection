import base64
import requests
import json

graph = """graph TD
    subgraph "Cliente (Frontend)"
        UI[Interface do Usuário\\n(React 19 + TypeScript)]
        Upload[Componente de Upload\\n(Drag-and-Drop)]
        View[Visualizador de Resultados]
        
        UI --> Upload
        Upload -- "1. Envia Imagem (HTTP POST)" --> API
        View -- "5. Exibe Resultado" --> UI
    end

    subgraph "Servidor (Backend - Docker Container)"
        API[API Gateway\\n(FastAPI)]
        
        subgraph "Processamento"
            PreProc[Pré-processamento\\n(OpenCV / NumPy)]
            Infer[Módulo de Inferência\\n(Classe Python)]
            PostProc[Pós-processamento\\n(Desenho de Caixas)]
        end
        
        subgraph "Modelo de IA"
            YOLO[Modelo YOLOv11\\n(Ultralytics)]
            Weights[Pesos Treinados\\n(best.pt)]
            YOLO -.-> Weights
        end
    end

    API -- "2. Encaminha Imagem" --> PreProc
    PreProc --> Infer
    Infer -- "3. Executa Detecção" --> YOLO
    YOLO -- "Resultados Brutos" --> Infer
    Infer --> PostProc
    PostProc -- "4. Retorna JSON + Base64" --> API
    API -- "Reposta JSON" --> View

    style UI fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    style API fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style YOLO fill:#fff3e0,stroke:#ef6c00,stroke-width:2px"""

graph_bytes = graph.encode('utf8')
base64_bytes = base64.b64encode(graph_bytes)
base64_string = base64_bytes.decode('ascii')
url = "https://mermaid.ink/img/" + base64_string

print(f"Downloading from: {url}")

response = requests.get(url)
if response.status_code == 200:
    with open('docs/figura_5_arquitetura.png', 'wb') as f:
        f.write(response.content)
    print("Successfully saved to docs/figura_5_arquitetura.png")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
