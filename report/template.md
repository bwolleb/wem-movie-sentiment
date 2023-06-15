---
title: |
    | ![](images/mse-logo.pdf){width=3in}
    |
    |
    |
    | \textbf{MA-WEM} 
subtitle: |
    | \textbf{Analyse de sentiments des films basés sur les dialogues}
    | 
    |
    |
    |
    |
    |
    |
    |
    |
    |
author: 
    - Massimo De Santis
    - Benoist Wolleb
date: 18 juin 2023
output: pdf_document
toc: false
geometry: margin=2.5cm
urlcolor: blue
numbersections: true
secnumdepth: 4
header-includes:
    \usepackage{fancyhdr}
    \pagestyle{fancy}
    \fancyhead[C]{}
    \fancyhead[R]{Massimo De Santis, Benoist Wolleb}
    \fancyfoot[L]{MA-WEM - Projet}
    \fancyfoot[C]{Page \thepage}
    \usepackage{subcaption}
    \usepackage{xcolor}
    \usepackage{textcomp}
    \usepackage{float}
    \floatplacement{figure}{H}
    \renewcommand{\thepart}{\Roman{part}}
    \renewcommand{\thesection}{\arabic{section}}
    \renewcommand{\thesubsection}{\arabic{section}.\arabic{subsection}}
    \renewcommand{\thesubsubsection}{\arabic{section}.\arabic{subsection}.\arabic{subsubsection}}
    \renewcommand{\tightlist}{\setlength{\itemsep}{4pt}\setlength{\parskip}{0pt}}
    \renewcommand{\labelitemii}{$\circ$}
    \pagenumbering{gobble}
include-before:
- '`\newpage{}`{=latex}'
...

\newpage
\pagenumbering{arabic}
\renewcommand{\contentsname}{Table des matières}
\hypersetup{colorlinks = true, linkcolor = black}
\tableofcontents
\hypersetup{colorlinks = true, linkcolor = blue}
\newpage
