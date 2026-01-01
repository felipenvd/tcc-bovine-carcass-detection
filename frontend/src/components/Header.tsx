
import React from 'react';
import { Home, Info, Github } from 'lucide-react';
import logo from '../assets/logo.png';

interface HeaderProps {
    onAboutClick: () => void;
    currentPage: 'home' | 'about';
}

export const Header: React.FC<HeaderProps> = ({ onAboutClick, currentPage }) => {
    return (
        <header className="fixed top-0 w-full z-50 glass-header text-white transition-all duration-300">
            <div className="container mx-auto px-6 h-20 flex items-center justify-between">
                <div className="flex items-center space-x-4">
                    {/* Logo with Glow Effect */}
                    <div className="relative group">
                        <div className="absolute -inset-2 bg-gradient-to-r from-green-400 to-emerald-600 rounded-2xl opacity-0 group-hover:opacity-40 blur-md transition duration-500"></div>
                        <div className="relative w-14 h-14 rounded-2xl flex items-center justify-center overflow-hidden shadow-2xl ring-2 ring-white/10">
                            <img
                                src={logo}
                                alt="AgroScan Logo"
                                className="w-full h-full object-cover"
                            />
                        </div>
                    </div>

                    <div className="hidden sm:block">
                        <h1 className="text-xl font-bold tracking-tight leading-tight">
                            AgroScan <span className="text-green-300 font-light hidden md:inline">| Análise Bovina</span>
                        </h1>
                        <p className="text-green-200/80 text-xs font-medium tracking-wider uppercase mt-0.5">
                            Inspeção Visual Inteligente
                        </p>
                    </div>
                </div>

                {/* Navigation */}
                <nav className="flex items-center space-x-1 pl-8">
                    <button
                        onClick={() => currentPage !== 'home' && onAboutClick()}
                        className={`flex items-center space-x-2 px-5 py-2.5 rounded-xl transition-all duration-300 font-medium text-sm ${currentPage === 'home'
                            ? 'bg-white/15 text-white shadow-inner backdrop-blur-sm'
                            : 'text-green-100 hover:bg-white/10 hover:text-white'
                            }`}
                    >
                        <Home className="w-4 h-4" />
                        <span>Painel</span>
                    </button>

                    <button
                        onClick={() => currentPage !== 'about' && onAboutClick()}
                        className={`flex items-center space-x-2 px-5 py-2.5 rounded-xl transition-all duration-300 font-medium text-sm ${currentPage === 'about'
                            ? 'bg-white/15 text-white shadow-inner backdrop-blur-sm'
                            : 'text-green-100 hover:bg-white/10 hover:text-white'
                            }`}
                    >
                        <Info className="w-4 h-4" />
                        <span>Sobre</span>
                    </button>

                    <div className="h-6 w-px bg-white/10 mx-2 hidden md:block"></div>

                    <a href="#" className="p-2.5 text-green-200 hover:text-white transition-colors hidden md:block opacity-60 hover:opacity-100">
                        <Github className="w-5 h-5" />
                    </a>
                </nav>
            </div>
        </header>
    );
};
