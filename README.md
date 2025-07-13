# 🧠 PyCard - Sistema de Flashcards Estilo Anki

Um sistema completo de flashcards desenvolvido em Python com interface gráfica, baseado no método de repetição espaçada para otimizar o aprendizado e memorização.

## 📋 Sobre o Projeto

O PyCard é uma aplicação desktop que implementa o algoritmo SM-2 (SuperMemo 2) para criar um sistema de estudo eficiente através de flashcards. Inspirado no popular aplicativo Anki, oferece uma solução completa para estudos de idiomas, vocabulário, conceitos acadêmicos e qualquer conteúdo que requeira memorização.

## ✨ Funcionalidades Principais

### 📚 Gerenciamento de Flashcards
- **Criação de flashcards** com frente e verso personalizáveis
- **Edição e exclusão** de cartões existentes
- **Busca avançada** por conteúdo
- **Validação de entrada** para garantir qualidade dos dados

### 🗂️ Sistema de Baralhos
- **Organização em baralhos** temáticos
- **Criação, renomeação e exclusão** de baralhos
- **Movimentação de cartões** entre baralhos
- **Filtros por baralho** na listagem

### 🔄 Algoritmo de Revisão Inteligente
- **Algoritmo SM-2** para repetição espaçada otimizada
- **Revisão bidirecional** (frente→verso e verso→frente)
- **4 níveis de avaliação**: Esqueci, Difícil, Bom, Fácil
- **Cálculo automático** de intervalos de revisão
- **Fator de facilidade adaptativo**

### 📊 Estatísticas e Análise
- **Estatísticas gerais** do progresso
- **Gráficos de distribuição** por dificuldade
- **Análise por baralho** e atividade recente
- **Métricas de desempenho** detalhadas

### 🎨 Personalização
- **3 temas visuais**: Claro, Escuro e Azul
- **Tamanho de fonte ajustável**
- **Interface responsiva** e intuitiva
- **Atalhos de teclado** para agilizar o uso

### 📁 Import/Export
- **Importação de CSV** e arquivos de texto
- **Exportação completa** ou por baralho
- **Sistema de backup** e restauração
- **Formato JSON** para dados estruturados

## 🛠️ Tecnologias Utilizadas

- **Python 3.x**
- **Tkinter** - Interface gráfica nativa
- **JSON** - Armazenamento de dados
- **CSV** - Import/export de dados
- **Matplotlib** - Geração de gráficos (opcional)
- **Datetime** - Gerenciamento de datas e intervalos

## 📦 Instalação

### Pré-requisitos
```bash
Python 3.6 ou superior
```

### Dependências Opcionais
```bash
# Para gráficos estatísticos
pip install matplotlib
```

### Download e Execução
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/pycard-flashcards.git

# Entre no diretório
cd pycard-flashcards

# Execute o aplicativo
python Pycard.py
```

## 🚀 Como Usar

### 1. Primeira Execução
- Execute o arquivo `Pycard.py`
- O aplicativo criará automaticamente os arquivos de dados necessários
- Comece criando seus primeiros flashcards

### 2. Criando Flashcards
- Clique em "📝 Criar Flashcard"
- Preencha a frente (pergunta) e verso (resposta)
- Selecione o baralho desejado
- Salve o cartão

### 3. Organizando em Baralhos
- Use "🗂️ Gerenciar Baralhos" para criar novos baralhos
- Organize por temas: Inglês, Matemática, História, etc.
- Mova cartões entre baralhos conforme necessário

### 4. Estudando com Revisões
- Selecione um baralho no menu principal
- Clique em "🔄 Revisar Flashcards"
- Avalie sua resposta: Esqueci (1), Difícil (2), Bom (3), Fácil (4)
- O algoritmo calculará automaticamente quando revisar novamente

### 5. Acompanhando o Progresso
- Use "📊 Estatísticas" para ver seu desempenho
- Monitore cartões pendentes e progresso geral
- Analise gráficos de distribuição por dificuldade

## 📊 Algoritmo de Repetição Espaçada (SM-2)

O PyCard implementa uma versão aprimorada do algoritmo SM-2:

### Intervalos Base
- **Primeira revisão**: 1 dia
- **Segunda revisão**: 6 dias
- **Próximas revisões**: Intervalo anterior × Fator de Facilidade

### Fatores de Ajuste
- **Esqueci (0)**: Reinicia o ciclo, intervalo = 1 dia
- **Difícil (1)**: Intervalo × 1.2, fator de facilidade reduzido
- **Bom (2)**: Intervalo normal baseado no fator
- **Fácil (3)**: Intervalo × 1.3, fator de facilidade aumentado

### Métricas Tracked
- Fator de facilidade (1.3 - 4.0)
- Número de repetições
- Sequência de acertos
- Total de revisões
- Data da próxima revisão

## 📁 Estrutura de Arquivos

```
pycard-flashcards/
├── Pycard.py              # Arquivo principal da aplicação
├── main.py                # Versão simplificada (backup)
├── flashcards_data.json   # Dados dos flashcards e configurações
├── README.md              # Documentação
└── backups/               # Pasta para backups (criada automaticamente)
```

## 🔧 Configurações Avançadas

### Arquivo de Dados (flashcards_data.json)
```json
{
  "flashcards": [...],
  "decks": {...},
  "theme": "claro",
  "font_size": 12
}
```

### Formato de Importação CSV
```csv
Frente,Verso
"Hello","Olá"
"Thank you","Obrigado"
"Goodbye","Tchau"
```

### Atalhos de Teclado
- **Enter**: Mostrar resposta
- **1-4**: Avaliar resposta (Esqueci, Difícil, Bom, Fácil)
- **Esc**: Voltar ao menu (em desenvolvimento)

## 🎯 Casos de Uso Ideais

### 📖 Aprendizado de Idiomas
- Vocabulário inglês-português
- Phrasal verbs e expressões
- Conjugações verbais
- Pronúncia e fonética

### 🎓 Estudos Acadêmicos
- Fórmulas matemáticas
- Conceitos históricos
- Terminologia científica
- Definições e teoremas

### 💼 Capacitação Profissional
- Termos técnicos
- Procedimentos e protocolos
- Códigos e regulamentações
- Certificações e qualificações

## 🔄 Comparação com Anki

| Funcionalidade | PyCard | Anki |
|----------------|--------|------|
| Algoritmo SM-2 | ✅ | ✅ |
| Interface Gráfica | ✅ Tkinter | ✅ Qt |
| Multiplataforma | ✅ Python | ✅ |
| Sincronização | ❌ | ✅ |
| Plugins | ❌ | ✅ |
| Mídia (Audio/Video) | ❌ | ✅ |
| Código Aberto | ✅ | ✅ |
| Offline | ✅ | ✅ |
| Simplicidade | ✅ | ❌ |

## 🚧 Próximas Funcionalidades

### Em Desenvolvimento
- [ ] Suporte a imagens nos flashcards
- [ ] Sistema de tags e categorias
- [ ] Modo de estudo por tempo
- [ ] Estatísticas mais detalhadas
- [ ] Exportação para Anki (.apkg)

### Planejado
- [ ] Sincronização em nuvem
- [ ] Aplicativo mobile
- [ ] Suporte a áudio
- [ ] Temas personalizáveis
- [ ] Sistema de plugins

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. **Fork** o projeto
2. Crie uma **branch** para sua feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. **Push** para a branch (`git push origin feature/AmazingFeature`)
5. Abra um **Pull Request**

### Áreas que Precisam de Ajuda
- Testes automatizados
- Documentação
- Interface de usuário
- Otimizações de performance
- Novas funcionalidades

## 📝 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

Desenvolvido com ❤️ para a comunidade de estudantes e entusiastas do aprendizado eficiente.

## 📞 Suporte

- **Issues**: Use a aba Issues do GitHub para reportar bugs
- **Discussions**: Para dúvidas e sugestões gerais
- **Wiki**: Documentação detalhada e tutoriais

## 🙏 Agradecimentos

- Inspirado no método SuperMemo e no aplicativo Anki
- Comunidade Python pela excelente documentação
- Todos os colaboradores e testadores

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela no GitHub!**

📚 **Bons estudos e aprendizado eficiente!**# pycards
