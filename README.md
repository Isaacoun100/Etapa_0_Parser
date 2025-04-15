# Etapa 0 — Lexical Analysis for the Notch Engine Language

Welcome to **Etapa 0**, the first stage in the development of a compiler for **Notch Engine**, a new programming language designed to compile into **Turbo Assembly**. This phase focuses on **lexical analysis**, laying the foundation for the full compilation pipeline.

---

## 🔍 Project Overview

**Etapa 0** is a Python-based lexical analysis tool that:

- Recognizes and classifies tokens from source files written in the `Notch Engine` language (`.ne` files).
- Generates a corresponding **HTML file** with syntax highlighting — each token type is displayed in a different color.
- Serves as a standalone **lexical analysis library** that will later be integrated into a full compiler backend targeting **Turbo Assembly**.

---

## 📦 Features

- Fully implemented in **Python**
- Tokenizes `.ne` source files
- Supports:
  - Keywords
  - Identifiers
  - Operators
  - Literals
  - Comments
- Outputs clean, color-coded **HTML** for visual debugging
- Easily extensible for future compiler phases

---

## 🧠 About Notch Engine

`Notch Engine` is a minimalistic, expressive programming language developed as part of an academic project. It is designed to be compiled into **Turbo Assembly**, a low-level target ideal for educational purposes. Source files use the `.ne` extension.

---

## 👥 Developers

- **Isaac Herrera Monge**
- **Mauro Andrés Navarro Obando**

---

## 🎓 Academic Details

- **Course**: Compiladores e Intérpretes  
- **Professor**: Kirstein Gatjens Soto  
- **University**: Tecnológico de Costa Rica  
- **Deadline**: 28/04/2025

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Recommended: virtual environment

### Installation

```bash
git clone https://github.com/Isaacoun100/Etapa_0_Parser.git
