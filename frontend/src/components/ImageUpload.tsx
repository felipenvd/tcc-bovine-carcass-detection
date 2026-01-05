
import React, { useState, type ChangeEvent, type DragEvent } from 'react';
import { Loader2, UploadCloud, FileImage } from 'lucide-react';

interface ImageUploadProps {
    onImageSelected: (file: File) => void;
    isLoading: boolean;
}

export const ImageUpload: React.FC<ImageUploadProps> = ({ onImageSelected, isLoading }) => {
    const [preview, setPreview] = useState<string | null>(null);
    const [isDragging, setIsDragging] = useState(false);

    const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
        if (e.target.files && e.target.files[0]) {
            const file = e.target.files[0];
            setPreview(URL.createObjectURL(file));
            onImageSelected(file);
        }
    };

    const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        setIsDragging(true);
    };

    const handleDragLeave = (e: DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        setIsDragging(false);
    };

    const handleDrop = (e: DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        setIsDragging(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            const file = e.dataTransfer.files[0];
            setPreview(URL.createObjectURL(file));
            onImageSelected(file);
        }
    };

    return (
        <div className="flex flex-col items-center animate-slide-up w-full">
            <div
                className={`w-full max-w-2xl min-h-[400px] relative group transition-all duration-300 ease-out
          ${isDragging
                        ? 'scale-[1.02] border-[#2d5a3d] bg-[#f0f9f4]'
                        : 'border-gray-200 hover:border-[#2d5a3d]/50 bg-white'
                    }
          border-2 border-dashed rounded-3xl shadow-xl overflow-hidden cursor-pointer
        `}
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
            >
                <label className="absolute inset-0 flex flex-col items-center justify-center p-8 cursor-pointer z-10">
                    {preview ? (
                        <div className="relative w-full h-full flex flex-col items-center justify-center">
                            <img
                                src={preview}
                                alt="Preview"
                                className="max-h-[300px] w-auto object-contain rounded-lg shadow-lg"
                            />
                            <div className="mt-4 flex items-center space-x-2 text-sm text-gray-500 bg-white/90 px-4 py-2 rounded-full backdrop-blur-sm shadow-sm">
                                <RefreshCwIcon className="w-4 h-4 animate-spin-slow" />
                                <span>Clique ou arraste para trocar</span>
                            </div>
                        </div>
                    ) : (
                        <div className="text-center p-10 transition-transform duration-300 group-hover:scale-105">
                            <div className="w-24 h-24 bg-gradient-to-tr from-[#e8f5e9] to-[#c8e6c9] rounded-full flex items-center justify-center mx-auto mb-6 shadow-inner group-hover:shadow-lg transition-shadow">
                                <UploadCloud className="w-12 h-12 text-[#2d5a3d] opacity-80" strokeWidth={1.5} />
                            </div>
                            <h3 className="text-2xl font-bold text-[#1a472a] mb-3">
                                Upload da Imagem
                            </h3>
                            <p className="text-gray-500 mb-6 max-w-xs mx-auto leading-relaxed">
                                Arraste e solte o arquivo da carcaça aqui, ou clique para explorar seus arquivos.
                            </p>

                            <div className="flex items-center justify-center space-x-3 text-xs text-gray-400 font-medium tracking-wide uppercase">
                                <span className="flex items-center bg-gray-50 px-3 py-1 rounded border border-gray-100">
                                    <FileImage className="w-3 h-3 mr-1.5" /> JPG
                                </span>
                                <span className="flex items-center bg-gray-50 px-3 py-1 rounded border border-gray-100">
                                    <FileImage className="w-3 h-3 mr-1.5" /> PNG
                                </span>
                            </div>
                        </div>
                    )}
                    <input
                        type="file"
                        className="hidden"
                        accept="image/*"
                        onChange={handleFileChange}
                        disabled={isLoading}
                    />
                </label>

                {/* Loading Overlay */}
                {isLoading && (
                    <div className="absolute inset-0 bg-white/90 backdrop-blur-md z-20 flex flex-col items-center justify-center">
                        <div className="relative">
                            <div className="w-20 h-20 border-4 border-[#e8f5e9] border-t-[#2d5a3d] rounded-full animate-spin"></div>
                            <div className="absolute inset-0 flex items-center justify-center">
                                <Loader2 className="w-8 h-8 text-[#2d5a3d] animate-pulse" />
                            </div>
                        </div>
                        <h4 className="mt-6 text-xl font-bold text-[#1a472a]">Analisando Carcaça</h4>
                        <p className="text-gray-500 mt-2 animate-pulse">Processando rede neural...</p>
                    </div>
                )}
            </div>
        </div>
    );
};

// Helper component just for this file
const RefreshCwIcon = ({ className }: { className?: string }) => (
    <svg
        xmlns="http://www.w3.org/2000/svg"
        width="24"
        height="24"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className={className}
    >
        <path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8" />
        <path d="M21 3v5h-5" />
        <path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16" />
        <path d="M8 16H3v5" />
    </svg>
);
