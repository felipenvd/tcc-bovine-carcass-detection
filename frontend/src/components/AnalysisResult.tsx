
import React from 'react';
import { Camera, Search, CheckCircle2, AlertTriangle, AlertOctagon, History, Download, ZoomIn } from 'lucide-react';
import Zoom from 'react-medium-image-zoom';
import 'react-medium-image-zoom/dist/styles.css';
import { saveAs } from 'file-saver';

interface Detection {
    class: string;
    confidence: number;
    box: number[];
}

interface AnalysisResultProps {
    filename: string;
    detections: Detection[];
    summary: string;
    annotatedImage?: string;
    onReset: () => void;
}

export const AnalysisResult: React.FC<AnalysisResultProps> = ({
    filename,
    detections,
    summary,
    annotatedImage,
    onReset
}) => {
    const [expandedClass, setExpandedClass] = React.useState<string | null>(null);
    const getSummaryStyle = (sum: string) => {
        if (sum.includes("Crítico")) return {
            bg: "bg-red-50 border-red-100",
            text: "text-red-800",
            accent: "bg-red-500",
            icon: AlertOctagon
        };
        if (sum.includes("Atenção") || sum.includes("Perda")) return {
            bg: "bg-amber-50 border-amber-100",
            text: "text-amber-800",
            accent: "bg-amber-500",
            icon: AlertTriangle
        };
        return {
            bg: "bg-emerald-50 border-emerald-100",
            text: "text-emerald-800",
            accent: "bg-emerald-500",
            icon: CheckCircle2
        };
    };

    const style = getSummaryStyle(summary);
    const StatusIcon = style.icon;

    return (
        <div className="w-full max-w-5xl animate-slide-up grid grid-cols-1 lg:grid-cols-2 gap-8">

            {/* Left Column: Visuals */}
            <div className="space-y-6">
                <div className="glass-panel rounded-3xl overflow-hidden p-2 shadow-lg hover:shadow-xl transition-shadow duration-300">
                    <div className="relative rounded-2xl overflow-hidden bg-gray-100 min-h-[300px] flex items-center justify-center group/image">
                        {annotatedImage ? (
                            <>
                                <Zoom>
                                    <img
                                        src={annotatedImage}
                                        alt="Resultado da Análise"
                                        className="w-full h-auto object-contain cursor-zoom-in"
                                    />
                                </Zoom>

                                {/* Overlay Actions */}
                                <div className="absolute top-4 right-4 flex space-x-2 opacity-0 group-hover/image:opacity-100 transition-opacity duration-300">
                                    <button
                                        onClick={() => saveAs(annotatedImage, `analysis_${filename}`)}
                                        className="bg-white/90 backdrop-blur-md p-2 rounded-full shadow-sm hover:bg-white text-gray-700 hover:text-blue-600 transition-colors"
                                        title="Baixar Imagem"
                                    >
                                        <Download className="w-5 h-5" />
                                    </button>
                                </div>

                                {/* Zoom Hint */}
                                <div className="absolute bottom-4 right-4 bg-black/50 backdrop-blur-sm px-3 py-1.5 rounded-full text-xs font-medium text-white flex items-center opacity-0 group-hover/image:opacity-100 transition-opacity duration-300 pointer-events-none">
                                    <ZoomIn className="w-3 h-3 mr-1.5" />
                                    Clique para ampliar
                                </div>
                            </>
                        ) : (
                            <div className="text-gray-400 flex flex-col items-center">
                                <Camera className="w-12 h-12 opacity-20 mb-2" />
                                <span>Sem visualização</span>
                            </div>
                        )}

                        {/* Floating Badge */}
                        <div className="absolute top-4 left-4 bg-white/90 backdrop-blur-md px-3 py-1.5 rounded-full text-xs font-semibold text-gray-600 shadow-sm flex items-center">
                            <Search className="w-3 h-3 mr-1.5" />
                            {filename.length > 20 ? filename.substring(0, 20) + '...' : filename}
                        </div>
                    </div>
                </div>

                <button
                    onClick={onReset}
                    className="w-full btn-primary py-4 rounded-xl font-semibold text-lg shadow-lg flex items-center justify-center space-x-2 group"
                >
                    <History className="w-5 h-5 group-hover:-rotate-180 transition-transform duration-500" />
                    <span>Realizar Nova Análise</span>
                </button>
            </div>

            {/* Right Column: Data */}
            <div className="space-y-6">
                {/* Status Card */}
                <div className={`rounded-3xl p-8 border ${style.bg} ${style.text} shadow-sm relative overflow-hidden group`}>
                    <div className={`absolute top-0 right-0 w-32 h-32 ${style.accent} opacity-5 rounded-bl-full -mr-8 -mt-8 transition-transform group-hover:scale-110 duration-700`}></div>

                    <div className="relative z-10">
                        <p className="text-sm font-bold uppercase tracking-wider opacity-70 mb-2">Diagnóstico Geral</p>
                        <div className="flex items-start space-x-4">
                            <div className={`p-3 rounded-2xl bg-white shadow-sm ring-4 ring-white/50 ${style.text}`}>
                                <StatusIcon className="w-8 h-8" />
                            </div>
                            <div>
                                <h2 className="text-3xl font-extrabold tracking-tight">{summary}</h2>

                            </div>
                        </div>
                    </div>
                </div>

                {/* Detections List */}
                <div className="glass-panel rounded-3xl p-8">
                    <h3 className="text-lg font-bold text-gray-800 mb-6 flex items-center">
                        <span className="w-1.5 h-6 bg-[#2d5a3d] rounded-full mr-3"></span>
                        Detecções Identificadas
                        <span className="ml-auto text-xs bg-gray-100 text-gray-500 px-2 py-1 rounded-full">
                            {detections.length} total
                        </span>
                    </h3>

                    <div className="space-y-4 max-h-[400px] overflow-y-auto pr-2 custom-scrollbar">
                        {detections.length === 0 ? (
                            <div className="text-center py-10 text-gray-400 bg-gray-50/50 rounded-2xl border border-dashed border-gray-200">
                                <CheckCircle2 className="w-10 h-10 mx-auto mb-3 opacity-20" />
                                <p>Nenhuma anomalia detectada.</p>
                            </div>
                        ) : (
                            Array.from(new Set(detections.map(d => d.class))).map((className) => {
                                const classDetections = detections.filter(d => d.class === className);
                                const isExpanded = expandedClass === className;
                                const isLesao = className === 'Lesao';

                                return (
                                    <div key={className} className="bg-white border border-gray-100 p-2 rounded-2xl shadow-sm hover:shadow-md transition-all duration-300">
                                        <button
                                            onClick={() => setExpandedClass(isExpanded ? null : className)}
                                            className="w-full flex justify-between items-center p-2 rounded-xl hover:bg-gray-50 transition-colors"
                                        >
                                            <div className="flex items-center space-x-3">
                                                <span className={`px-3 py-1 rounded-lg text-xs font-bold uppercase tracking-wide ${isLesao
                                                    ? 'bg-red-100 text-red-700'
                                                    : 'bg-blue-100 text-blue-700'
                                                    }`}>
                                                    {className}
                                                </span>
                                                <span className="text-xs font-semibold text-gray-400 bg-gray-100 px-2 py-0.5 rounded-md">
                                                    {classDetections.length} {classDetections.length === 1 ? 'ocorrência' : 'ocorrências'}
                                                </span>
                                            </div>
                                            <div className="text-gray-400">
                                                {isExpanded ? (
                                                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 15l7-7 7 7" /></svg>
                                                ) : (
                                                    <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" /></svg>
                                                )}
                                            </div>
                                        </button>

                                        {isExpanded && (
                                            <div className="mt-3 space-y-3 px-2 pb-2">
                                                {classDetections.map((d, index) => (
                                                    <div key={index} className="group">
                                                        <div className="flex justify-between items-center mb-1.5">
                                                            <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">
                                                                Confiança
                                                            </span>
                                                            <span className="text-sm font-mono font-bold text-gray-500 group-hover:text-gray-800 transition-colors">
                                                                {(d.confidence * 100).toFixed(1)}%
                                                            </span>
                                                        </div>
                                                        <div className="h-2 w-full bg-gray-100 rounded-full overflow-hidden">
                                                            <div
                                                                className={`h-full rounded-full transition-all duration-1000 ease-out ${isLesao
                                                                    ? 'bg-gradient-to-r from-red-400 to-red-500'
                                                                    : 'bg-gradient-to-r from-blue-400 to-blue-500'
                                                                    }`}
                                                                style={{ width: `${d.confidence * 100}%` }}
                                                            ></div>
                                                        </div>
                                                    </div>
                                                ))}
                                            </div>
                                        )}
                                    </div>
                                );
                            })
                        )}
                    </div>
                </div>
            </div>
        </div>
    );
};
