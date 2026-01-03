
import React from 'react';
import {
    Target,
    Users,
    Brain,
    Sparkles,
    Linkedin,
    Github
} from 'lucide-react';
import fotoFelipe from '../assets/foto-felipe.jpeg';
import fotoJose from '../assets/foto-jose.jpeg';

export const About: React.FC = () => {
    return (
        <div className="animate-slide-up max-w-5xl mx-auto w-full">
            {/* Hero Section */}
            <div className="text-center mb-16 relative">
                <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-64 h-64 bg-green-400/20 rounded-full blur-3xl -z-10"></div>

                <div className="inline-flex items-center justify-center w-24 h-24 bg-gradient-to-br from-[#1a472a] to-[#2d5a3d] rounded-3xl mb-8 shadow-xl rotate-3 hover:rotate-6 transition-transform duration-300">
                    <Sparkles className="w-10 h-10 text-white" />
                </div>
                <h2 className="text-4xl md:text-5xl font-extrabold text-[#1a472a] mb-4 tracking-tight">
                    Sobre o Sistema
                </h2>
                <p className="text-xl text-gray-500 font-light max-w-2xl mx-auto">
                    Unindo pesquisa acadêmica e inovação tecnológica para transformar o controle de qualidade no agronegócio.
                </p>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                {/* Main Info Column */}
                <div className="lg:col-span-2 space-y-8">

                    {/* Project Card */}
                    <div className="glass-panel rounded-3xl p-8 md:p-10 relative overflow-hidden group h-full">
                        <div className="absolute top-0 right-0 w-40 h-40 bg-[#e8f5e9] rounded-bl-full -mr-10 -mt-10 opacity-50 transition-transform group-hover:scale-110 duration-700"></div>

                        <div className="flex items-center mb-6">
                            <div className="w-12 h-12 bg-[#1a472a]/10 rounded-2xl flex items-center justify-center mr-4 text-[#1a472a]">
                                <Target className="w-6 h-6" />
                            </div>
                            <h3 className="text-2xl font-bold text-[#1a472a]">O Projeto</h3>
                        </div>

                        <div className="space-y-4 text-gray-600 leading-relaxed text-lg">
                            <p>
                                Este sistema foi desenvolvido como parte integrante do <strong>Trabalho de Conclusão de Curso (TCC)</strong> no curso de Sistemas de Informação.
                            </p>
                            <p>
                                O objetivo central é a automação da inspeção visual de carcaças bovinas em frigoríficos, utilizando algoritmos de Inteligência Artificial de última geração.
                            </p>
                            <div className="p-5 bg-green-50/50 rounded-2xl border border-green-100 flex items-start gap-3 mt-4">
                                <Brain className="w-6 h-6 text-green-700 shrink-0 mt-1" />
                                <p className="text-sm text-green-800">
                                    Implementamos a arquitetura <strong>YOLO</strong> (You Only Look Once) para detecção em tempo real de não conformidades como <span className="font-semibold text-red-600">lesões</span> e <span className="font-semibold text-amber-600">perdas</span> de tecido.
                                </p>
                            </div>
                        </div>
                    </div>
                </div>

                {/* Creators Column */}
                <div className="lg:col-span-1 space-y-6">
                    <div className="bg-gradient-to-b from-[#1a472a] to-[#0f2919] rounded-3xl p-8 text-white shadow-2xl relative overflow-hidden h-full flex flex-col">
                        {/* Background Pattern */}
                        <div className="absolute inset-0 opacity-10" style={{ backgroundImage: 'radial-gradient(circle at 2px 2px, white 1px, transparent 0)', backgroundSize: '24px 24px' }}></div>

                        <div className="relative z-10 flex-grow">
                            <div className="flex items-center mb-8">
                                <div className="w-12 h-12 bg-white/10 rounded-2xl flex items-center justify-center mr-4 backdrop-blur-sm">
                                    <Users className="w-6 h-6 text-green-300" />
                                </div>
                                <div>
                                    <h3 className="text-xl font-bold">Pesquisadores</h3>
                                    <p className="text-green-300/60 text-xs uppercase tracking-widest font-semibold">Desenvolvedores</p>
                                </div>
                            </div>

                            <div className="space-y-4">
                                {/* Felipe */}
                                <div className="group bg-white/5 hover:bg-white/10 p-4 rounded-2xl transition-all duration-300 border border-white/5 hover:border-white/20 flex items-center justify-between">
                                    <div className="flex items-center space-x-4">
                                        <div className="w-20 h-20 rounded-full overflow-hidden border-2 border-white/20 shadow-lg shrink-0">
                                            <img
                                                src={fotoFelipe}
                                                alt="Felipe Vidal"
                                                className="w-full h-full object-cover"
                                            />
                                        </div>
                                        <div>
                                            <h4 className="font-bold text-lg leading-tight group-hover:text-green-300 transition-colors">Felipe Vidal</h4>
                                            <p className="text-sm text-gray-400">Pesquisador</p>
                                        </div>
                                    </div>
                                    <div className="flex flex-col space-y-2 opacity-100 lg:opacity-0 lg:group-hover:opacity-100 transition-opacity duration-300">
                                        <a href="https://github.com/felipenvd" target="_blank" rel="noopener noreferrer" className="p-2 hover:bg-white/10 rounded-lg transition-colors text-white/70 hover:text-white">
                                            <Github className="w-5 h-5" />
                                        </a>
                                        <a href="https://www.linkedin.com/in/felipe-vidal-ba4180295" target="_blank" rel="noopener noreferrer" className="p-2 hover:bg-white/10 rounded-lg transition-colors text-white/70 hover:text-white">
                                            <Linkedin className="w-5 h-5" />
                                        </a>
                                    </div>
                                </div>

                                {/* Jose */}
                                <div className="group bg-white/5 hover:bg-white/10 p-4 rounded-2xl transition-all duration-300 border border-white/5 hover:border-white/20 flex items-center justify-between">
                                    <div className="flex items-center space-x-4">
                                        <div className="w-20 h-20 rounded-full overflow-hidden border-2 border-white/20 shadow-lg shrink-0">
                                            <img
                                                src={fotoJose}
                                                alt="José Pires"
                                                className="w-full h-full object-cover"
                                            />
                                        </div>
                                        <div>
                                            <h4 className="font-bold text-lg leading-tight group-hover:text-green-300 transition-colors">José Pires</h4>
                                            <p className="text-sm text-gray-400">Pesquisador</p>
                                        </div>
                                    </div>
                                    <div className="flex flex-col space-y-2 opacity-100 lg:opacity-0 lg:group-hover:opacity-100 transition-opacity duration-300">
                                        <a href="https://github.com/jose-pires-neto" target="_blank" rel="noopener noreferrer" className="p-2 hover:bg-white/10 rounded-lg transition-colors text-white/70 hover:text-white">
                                            <Github className="w-5 h-5" />
                                        </a>
                                        <a href="https://www.linkedin.com/in/josé-pires-a97430237" target="_blank" rel="noopener noreferrer" className="p-2 hover:bg-white/10 rounded-lg transition-colors text-white/70 hover:text-white">
                                            <Linkedin className="w-5 h-5" />
                                        </a>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="mt-8 pt-6 border-t border-white/10 text-center relative z-10 space-y-4">
                            <div>
                                <p className="text-[10px] uppercase tracking-wider text-green-300/40 mb-1">Orientador</p>
                                <p className="text-xs text-green-100 font-medium">Prof. Dr. Gilberto Nerino de Souza Junior</p>
                            </div>

                            <div>
                                <p className="text-[10px] uppercase tracking-wider text-green-300/40 mb-1">Coorientador</p>
                                <p className="text-xs text-green-100 font-medium">Prof. Dr. Marcus de Barros Braga</p>
                            </div>

                            <p className="text-[10px] text-green-200/30 pt-4">
                                UFRA • 2026
                            </p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};
