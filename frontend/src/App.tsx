
import { useState } from 'react'
import { Header } from './components/Header'
import { ImageUpload } from './components/ImageUpload'
import { AnalysisResult } from './components/AnalysisResult'
import { About } from './components/About'

interface AnalysisData {
  filename: string;
  detections: any[];
  summary: string;
  annotated_image?: string;
}

function App() {
  const [result, setResult] = useState<AnalysisData | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState<'home' | 'about'>('home');

  const handleImageSelected = async (file: File) => {
    setIsLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/predict', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Erro na API: ${response.statusText}`);
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setError('Falha ao processar a imagem. Verifique se o servidor backend está rodando.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setResult(null);
    setError(null);
  };

  const togglePage = () => {
    setCurrentPage(currentPage === 'home' ? 'about' : 'home');
    setResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen flex flex-col pt-20 pb-10">
      <Header onAboutClick={togglePage} currentPage={currentPage} />

      <main className="grow container mx-auto px-4 py-8 flex flex-col items-center justify-center min-h-[calc(100vh-140px)]">
        {currentPage === 'about' ? (
          <About />
        ) : (
          <div className="w-full max-w-5xl flex flex-col items-center">

            {!result && !error && (
              <div className="text-center mb-12 max-w-3xl animate-slide-up">
                <span className="inline-block py-1 px-3 rounded-full bg-green-100 text-[#1a472a] text-xs font-bold tracking-wider uppercase mb-4 border border-green-200">
                  Sistema de Inspeção V1.0
                </span>
                <h2 className="text-4xl md:text-5xl font-extrabold text-[#1a472a] mb-6 leading-tight">
                  Controle de Qualidade <br />
                  <span className="text-transparent bg-clip-text bg-gradient-to-r from-[#2d5a3d] to-[#6b8e23]">
                    Inteligente & Automatizado
                  </span>
                </h2>
                <p className="text-xl text-gray-600 leading-relaxed font-light">
                  Tecnologia de ponta para identificação instantânea de <span className="font-semibold text-red-600">lesões</span> e <span className="font-semibold text-amber-600">perdas</span> em linhas de produção.
                </p>
              </div>
            )}

            {!result && (
              <ImageUpload
                onImageSelected={handleImageSelected}
                isLoading={isLoading}
              />
            )}

            {error && (
              <div className="mt-8 p-6 bg-red-50 text-red-700 border border-red-100 rounded-2xl shadow-lg animate-slide-up max-w-2xl text-center">
                <span className="block text-3xl mb-2">⚠️</span>
                <span className="font-bold text-lg block mb-1">Não foi possível processar</span>
                <span className="opacity-80">{error}</span>
              </div>
            )}

            {result && (
              <AnalysisResult
                filename={result.filename}
                detections={result.detections}
                summary={result.summary}
                annotatedImage={result.annotated_image}
                onReset={handleReset}
              />
            )}
          </div>
        )}
      </main>

      <footer className="text-center text-gray-400 py-8 text-sm font-medium">
        <p>© 2025 ScanBovino • TCC - Sistemas de Informação</p>
        <p className="mt-2 text-xs opacity-60">Felipe Vidal & José Pires</p>
      </footer>
    </div>
  )
}

export default App
