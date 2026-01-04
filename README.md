# 📝 Simple Text Editor (Tkinter)

Um editor de texto simples e funcional desenvolvido em **Python** utilizando **Tkinter**, com foco em organização de código, usabilidade e aprendizado de fundamentos de aplicações desktop.

Este projeto foi criado como um exercício prático para consolidar conhecimentos em Python, interfaces gráficas e estruturação de projetos.

---

## 🚀 Funcionalidades

* 📂 Abrir arquivos `.txt`
* 💾 Salvar e salvar como
* 🌓 Temas **Light** e **Dark**
* ↩️ Undo / Redo
* 🔍 Busca de texto (Find Next)
* 📊 Barra de status (linha e coluna do cursor)
* ⚠️ Aviso de arquivo não salvo ao fechar
* 💽 Restauração de sessão (tema salvo)
* 🖥️ Interface limpa e responsiva

---

## 🛠️ Tecnologias Utilizadas

* **Python 3**
* **Tkinter** (GUI nativa)
* **PyInstaller** (geração de executável)

---

## 📦 Como executar o projeto

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/gusthecurious/basic-text-editor
cd basic-text-editor
```

### 2️⃣ Executar com Python

```bash
python editor_app.py
```

> Certifique-se de ter o Python instalado (versão 3.8 ou superior).

---

## 🪟 Gerar o executável (.exe)

Instale o PyInstaller:

```bash
pip install pyinstaller
```

Gere o executável:

```bash
pyinstaller --onefile --windowed editor_app.py
```

O arquivo final estará em:

```text
dist/editor.exe
```

---

## 📁 Estrutura do Projeto

```text
editor_app.py        # Código principal do editor
session.json     # Arquivo de sessão (gerado automaticamente)
README.md        # Documentação do projeto
```

---

## 🎯 Objetivos do Projeto

* Praticar desenvolvimento de aplicações desktop
* Trabalhar com eventos e widgets do Tkinter
* Aprender a estruturar um projeto real em Python
* Criar um executável distribuível para Windows

---

## 🔮 Possíveis Melhorias Futuras

* Sistema de abas
* Numeração de linhas
* Autocomplete básico
* Suporte a outros formatos de arquivo
* Configurações avançadas de tema

---
