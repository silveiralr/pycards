import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, ttk
import json
import random
import datetime
import os
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import re

class FlashcardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Flashcards - Estilo Anki")
        self.root.geometry("800x600")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Configurações de tema
        self.themes = {
            "claro": {"bg": "#f0f0f0", "fg": "#000000", "card_bg": "#ffffff"},
            "escuro": {"bg": "#2b2b2b", "fg": "#ffffff", "card_bg": "#404040"},
            "azul": {"bg": "#e3f2fd", "fg": "#0d47a1", "card_bg": "#ffffff"}
        }
        self.current_theme = "claro"
        self.font_size = 12
        
        # Inicializar variáveis
        self.flashcards = []
        self.decks = {}
        self.current_deck = "Geral"
        self.current_card = None
        self.showing_answer = False
        self.bidirectional_mode = False
        self.load_data()
        
        # Aplicar tema
        self.apply_theme()
        
        # Frame principal
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Interface inicial - Menu principal
        self.show_main_menu()
    
    def apply_theme(self):
        """Aplica o tema selecionado"""
        theme = self.themes[self.current_theme]
        self.root.configure(bg=theme["bg"])
    
    def load_data(self):
        """Carrega os flashcards e baralhos do arquivo JSON"""
        try:
            if os.path.exists("flashcards_data.json"):
                with open("flashcards_data.json", "r", encoding="utf-8") as file:
                    data = json.load(file)
                    self.flashcards = data.get("flashcards", [])
                    self.decks = data.get("decks", {"Geral": []})
                    self.current_theme = data.get("theme", "claro")
                    self.font_size = data.get("font_size", 12)
                    
                    # Garantir que todos os flashcards estejam em algum baralho
                    all_deck_cards = set()
                    for deck_cards in self.decks.values():
                        all_deck_cards.update(deck_cards)
                    
                    for i, card in enumerate(self.flashcards):
                        if i not in all_deck_cards:
                            self.decks["Geral"].append(i)
            else:
                self.flashcards = []
                self.decks = {"Geral": []}
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao carregar dados: {e}")
            self.flashcards = []
            self.decks = {"Geral": []}
    
    def save_data(self):
        """Salva os flashcards e baralhos no arquivo JSON"""
        try:
            data = {
                "flashcards": self.flashcards,
                "decks": self.decks,
                "theme": self.current_theme,
                "font_size": self.font_size
            }
            with open("flashcards_data.json", "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao salvar dados: {e}")
    
    def clear_frame(self):
        """Limpa todos os widgets do frame principal"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def validate_text_input(self, text):
        """Valida entrada de texto para evitar apenas espaços ou caracteres inválidos"""
        text = text.strip()
        if not text:
            return False
        # Verificar se não é apenas espaços ou caracteres especiais
        if not re.search(r'[a-zA-Z0-9À-ÿ]', text):
            return False
        return True
    
    def show_main_menu(self):
        """Exibe o menu principal"""
        self.clear_frame()
        theme = self.themes[self.current_theme]
        
        # Frame do título
        title_frame = tk.Frame(self.main_frame, bg=theme["bg"])
        title_frame.pack(pady=20)
        
        title_label = tk.Label(title_frame, text="🧠 Sistema de Flashcards - Estilo Anki", 
                              font=("Arial", 20, "bold"), bg=theme["bg"], fg=theme["fg"])
        title_label.pack()
        
        # Seletor de baralho
        deck_frame = tk.Frame(self.main_frame, bg=theme["bg"])
        deck_frame.pack(pady=10)
        
        deck_label = tk.Label(deck_frame, text="Baralho atual:", 
                             font=("Arial", self.font_size), bg=theme["bg"], fg=theme["fg"])
        deck_label.pack(side=tk.LEFT, padx=5)
        
        self.deck_var = tk.StringVar(value=self.current_deck)
        deck_combo = ttk.Combobox(deck_frame, textvariable=self.deck_var, 
                                 values=list(self.decks.keys()), state="readonly")
        deck_combo.pack(side=tk.LEFT, padx=5)
        deck_combo.bind("<<ComboboxSelected>>", self.change_deck)
        
        # Botões principais
        buttons_frame = tk.Frame(self.main_frame, bg=theme["bg"])
        buttons_frame.pack(pady=20)
        
        # Primeira linha de botões
        row1 = tk.Frame(buttons_frame, bg=theme["bg"])
        row1.pack(pady=5)
        
        btn_create = tk.Button(row1, text="📝 Criar Flashcard", 
                              font=("Arial", self.font_size), width=20, 
                              command=self.create_flashcard,
                              bg="#4caf50", fg="white", pady=8)
        btn_create.pack(side=tk.LEFT, padx=5)
        
        btn_review = tk.Button(row1, text="🔄 Revisar Flashcards", 
                              font=("Arial", self.font_size), width=20, 
                              command=self.start_review,
                              bg="#2196f3", fg="white", pady=8)
        btn_review.pack(side=tk.LEFT, padx=5)
        
        # Segunda linha de botões
        row2 = tk.Frame(buttons_frame, bg=theme["bg"])
        row2.pack(pady=5)
        
        btn_list = tk.Button(row2, text="📋 Listar Flashcards", 
                            font=("Arial", self.font_size), width=20, 
                            command=self.list_flashcards,
                            bg="#9c27b0", fg="white", pady=8)
        btn_list.pack(side=tk.LEFT, padx=5)
        
        btn_decks = tk.Button(row2, text="🗂️ Gerenciar Baralhos", 
                             font=("Arial", self.font_size), width=20, 
                             command=self.manage_decks,
                             bg="#ff9800", fg="white", pady=8)
        btn_decks.pack(side=tk.LEFT, padx=5)
        
        # Terceira linha de botões
        row3 = tk.Frame(buttons_frame, bg=theme["bg"])
        row3.pack(pady=5)
        
        btn_import = tk.Button(row3, text="📥 Importar", 
                              font=("Arial", self.font_size), width=12, 
                              command=self.import_flashcards,
                              bg="#607d8b", fg="white", pady=8)
        btn_import.pack(side=tk.LEFT, padx=2)
        
        btn_export = tk.Button(row3, text="📤 Exportar", 
                              font=("Arial", self.font_size), width=12, 
                              command=self.export_flashcards,
                              bg="#795548", fg="white", pady=8)
        btn_export.pack(side=tk.LEFT, padx=2)
        
        btn_stats = tk.Button(row3, text="📊 Estatísticas", 
                             font=("Arial", self.font_size), width=12, 
                             command=self.show_statistics,
                             bg="#e91e63", fg="white", pady=8)
        btn_stats.pack(side=tk.LEFT, padx=2)
        
        btn_settings = tk.Button(row3, text="⚙️ Configurações", 
                                font=("Arial", self.font_size), width=12, 
                                command=self.show_settings,
                                bg="#9e9e9e", fg="white", pady=8)
        btn_settings.pack(side=tk.LEFT, padx=2)
        
        # Estatísticas resumidas
        stats_frame = tk.Frame(self.main_frame, bg=theme["bg"])
        stats_frame.pack(pady=20)
        
        deck_cards = self.get_deck_cards(self.current_deck)
        total_cards = len(deck_cards)
        
        # Calcular cartões pendentes para hoje
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pending_cards = sum(1 for i in deck_cards 
                           if i < len(self.flashcards) and 
                           (not self.flashcards[i]["next_review"] or 
                            self.flashcards[i]["next_review"] <= current_date))
        
        stats_text = f"📚 Total no baralho '{self.current_deck}': {total_cards} | "
        stats_text += f"⏰ Pendentes hoje: {pending_cards}"
        
        status_label = tk.Label(stats_frame, text=stats_text, 
                               font=("Arial", self.font_size), bg=theme["bg"], fg=theme["fg"])
        status_label.pack()
        
        # Botão sair
        btn_exit = tk.Button(self.main_frame, text="🚪 Sair", 
                            font=("Arial", self.font_size), width=15, 
                            command=self.on_closing,
                            bg="#f44336", fg="white", pady=8)
        btn_exit.pack(pady=20)
    
    def change_deck(self, event=None):
        """Muda o baralho atual"""
        self.current_deck = self.deck_var.get()
        self.show_main_menu()
    
    def get_deck_cards(self, deck_name):
        """Retorna os índices dos flashcards de um baralho específico"""
        return self.decks.get(deck_name, [])
    
    def manage_decks(self):
        """Interface para gerenciar baralhos"""
        self.clear_frame()
        theme = self.themes[self.current_theme]
        
        title_label = tk.Label(self.main_frame, text="🗂️ Gerenciar Baralhos", 
                              font=("Arial", 18, "bold"), bg=theme["bg"], fg=theme["fg"])
        title_label.pack(pady=10)
        
        # Frame para lista de baralhos
        list_frame = tk.Frame(self.main_frame, bg=theme["bg"])
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.deck_listbox = tk.Listbox(list_frame, font=("Arial", self.font_size), 
                                      yscrollcommand=scrollbar.set,
                                      bg=theme["card_bg"], fg=theme["fg"])
        self.deck_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.deck_listbox.yview)
        
        # Preencher lista de baralhos
        for deck_name, cards in self.decks.items():
            self.deck_listbox.insert(tk.END, f"{deck_name} ({len(cards)} cartões)")
        
        # Botões de gerenciamento
        btn_frame = tk.Frame(self.main_frame, bg=theme["bg"])
        btn_frame.pack(pady=10)
        
        btn_new = tk.Button(btn_frame, text="➕ Novo Baralho", 
                           font=("Arial", self.font_size), bg="#4caf50", fg="white",
                           command=self.create_deck)
        btn_new.grid(row=0, column=0, padx=5)
        
        btn_rename = tk.Button(btn_frame, text="✏️ Renomear", 
                              font=("Arial", self.font_size), bg="#ff9800", fg="white",
                              command=self.rename_deck)
        btn_rename.grid(row=0, column=1, padx=5)
        
        btn_delete = tk.Button(btn_frame, text="🗑️ Excluir", 
                              font=("Arial", self.font_size), bg="#f44336", fg="white",
                              command=self.delete_deck)
        btn_delete.grid(row=0, column=2, padx=5)
        
        btn_back = tk.Button(self.main_frame, text="⬅️ Voltar", 
                            font=("Arial", self.font_size), bg="#9e9e9e", fg="white",
                            command=self.show_main_menu)
        btn_back.pack(pady=10)
    
    def create_deck(self):
        """Cria um novo baralho"""
        name = simpledialog.askstring("Novo Baralho", "Nome do baralho:")
        if name and self.validate_text_input(name):
            name = name.strip()
            if name not in self.decks:
                self.decks[name] = []
                self.save_data()
                messagebox.showinfo("Sucesso", f"Baralho '{name}' criado!")
                self.manage_decks()
            else:
                messagebox.showwarning("Aviso", "Já existe um baralho com este nome!")
        elif name:
            messagebox.showwarning("Aviso", "Nome inválido!")
    
    def rename_deck(self):
        """Renomeia um baralho"""
        try:
            selected_idx = self.deck_listbox.curselection()[0]
            old_name = list(self.decks.keys())[selected_idx]
            
            if old_name == "Geral":
                messagebox.showwarning("Aviso", "Não é possível renomear o baralho 'Geral'!")
                return
            
            new_name = simpledialog.askstring("Renomear Baralho", 
                                             f"Novo nome para '{old_name}':")
            if new_name and self.validate_text_input(new_name):
                new_name = new_name.strip()
                if new_name not in self.decks:
                    self.decks[new_name] = self.decks.pop(old_name)
                    if self.current_deck == old_name:
                        self.current_deck = new_name
                    self.save_data()
                    messagebox.showinfo("Sucesso", f"Baralho renomeado para '{new_name}'!")
                    self.manage_decks()
                else:
                    messagebox.showwarning("Aviso", "Já existe um baralho com este nome!")
            elif new_name:
                messagebox.showwarning("Aviso", "Nome inválido!")
        except IndexError:
            messagebox.showwarning("Aviso", "Selecione um baralho para renomear.")
    
    def delete_deck(self):
        """Exclui um baralho"""
        try:
            selected_idx = self.deck_listbox.curselection()[0]
            deck_name = list(self.decks.keys())[selected_idx]
            
            if deck_name == "Geral":
                messagebox.showwarning("Aviso", "Não é possível excluir o baralho 'Geral'!")
                return
            
            confirm = messagebox.askyesno("Confirmar Exclusão", 
                                         f"Excluir o baralho '{deck_name}'? Os cartões serão movidos para 'Geral'.")
            if confirm:
                # Mover cartões para o baralho Geral
                cards_to_move = self.decks[deck_name]
                self.decks["Geral"].extend(cards_to_move)
                del self.decks[deck_name]
                
                if self.current_deck == deck_name:
                    self.current_deck = "Geral"
                
                self.save_data()
                messagebox.showinfo("Sucesso", f"Baralho '{deck_name}' excluído!")
                self.manage_decks()
        except IndexError:
            messagebox.showwarning("Aviso", "Selecione um baralho para excluir.")
    
    def create_flashcard(self):
        """Interface para criar um novo flashcard"""
        self.clear_frame()
        theme = self.themes[self.current_theme]
        
        title_label = tk.Label(self.main_frame, text="📝 Criar Novo Flashcard", 
                              font=("Arial", 16, "bold"), bg=theme["bg"], fg=theme["fg"])
        title_label.pack(pady=10)
        
        # Seletor de baralho
        deck_frame = tk.Frame(self.main_frame, bg=theme["bg"])
        deck_frame.pack(pady=10)
        
        deck_label = tk.Label(deck_frame, text="Baralho:", 
                             font=("Arial", self.font_size), bg=theme["bg"], fg=theme["fg"])
        deck_label.grid(row=0, column=0, padx=5, sticky="w")
        
        self.new_card_deck = tk.StringVar(value=self.current_deck)
        deck_combo = ttk.Combobox(deck_frame, textvariable=self.new_card_deck, 
                                 values=list(self.decks.keys()), state="readonly")
        deck_combo.grid(row=0, column=1, padx=5)
        
        # Frame para entradas
        entry_frame = tk.Frame(self.main_frame, bg=theme["bg"])
        entry_frame.pack(pady=10, fill="both", expand=True)
        
        # Frente do cartão
        front_label = tk.Label(entry_frame, text="Frente (Pergunta):", 
                              font=("Arial", self.font_size), bg=theme["bg"], fg=theme["fg"])
        front_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        
        self.front_text = tk.Text(entry_frame, height=5, width=50, 
                                 font=("Arial", self.font_size), wrap=tk.WORD,
                                 bg=theme["card_bg"], fg=theme["fg"])
        self.front_text.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # Verso do cartão
        back_label = tk.Label(entry_frame, text="Verso (Resposta):", 
                             font=("Arial", self.font_size), bg=theme["bg"], fg=theme["fg"])
        back_label.grid(row=1, column=0, padx=10, pady=10, sticky="nw")
        
        self.back_text = tk.Text(entry_frame, height=5, width=50, 
                                font=("Arial", self.font_size), wrap=tk.WORD,
                                bg=theme["card_bg"], fg=theme["fg"])
        self.back_text.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        entry_frame.grid_columnconfigure(1, weight=1)
        
        # Frame para botões
        button_frame = tk.Frame(self.main_frame, bg=theme["bg"])
        button_frame.pack(pady=10)
        
        # Botão salvar
        save_btn = tk.Button(button_frame, text="💾 Salvar", 
                            font=("Arial", self.font_size), bg="#4caf50", fg="white",
                            command=self.save_new_flashcard)
        save_btn.grid(row=0, column=0, padx=10)
        
        # Botão cancelar
        cancel_btn = tk.Button(button_frame, text="❌ Cancelar", 
                              font=("Arial", self.font_size), bg="#f44336", fg="white",
                              command=self.show_main_menu)
        cancel_btn.grid(row=0, column=1, padx=10)
    
    def save_new_flashcard(self):
        """Salva um novo flashcard"""
        front = self.front_text.get("1.0", "end-1c").strip()
        back = self.back_text.get("1.0", "end-1c").strip()
        
        if not self.validate_text_input(front) or not self.validate_text_input(back):
            messagebox.showwarning("Aviso", "Preencha todos os campos com conteúdo válido!")
            return
        
        # Criar novo flashcard
        new_card = {
            "front": front,
            "back": back,
            "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_review": None,
            "next_review": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ease_factor": 2.5,
            "interval": 0,
            "repetitions": 0,
            "correct_streak": 0,
            "total_reviews": 0
        }
        
        # Adicionar ao final da lista e ao baralho selecionado
        self.flashcards.append(new_card)
        deck_name = self.new_card_deck.get()
        self.decks[deck_name].append(len(self.flashcards) - 1)
        
        self.save_data()
        messagebox.showinfo("Sucesso", "Flashcard criado com sucesso!")
        self.show_main_menu()
    
    def list_flashcards(self):
        """Lista flashcards com busca e filtros"""
        self.clear_frame()
        theme = self.themes[self.current_theme]
        
        title_label = tk.Label(self.main_frame, text="📋 Lista de Flashcards", 
                              font=("Arial", 16, "bold"), bg=theme["bg"], fg=theme["fg"])
        title_label.pack(pady=10)
        
        # Frame de busca
        search_frame = tk.Frame(self.main_frame, bg=theme["bg"])
        search_frame.pack(pady=10, fill="x")
        
        search_label = tk.Label(search_frame, text="🔍 Buscar:", 
                               font=("Arial", self.font_size), bg=theme["bg"], fg=theme["fg"])
        search_label.pack(side=tk.LEFT, padx=5)
        
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.update_flashcard_list)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, 
                               font=("Arial", self.font_size), width=30)
        search_entry.pack(side=tk.LEFT, padx=5)
        
        # Filtro de baralho
        filter_label = tk.Label(search_frame, text="Baralho:", 
                               font=("Arial", self.font_size), bg=theme["bg"], fg=theme["fg"])
        filter_label.pack(side=tk.LEFT, padx=(20, 5))
        
        self.filter_deck = tk.StringVar(value="Todos")
        deck_options = ["Todos"] + list(self.decks.keys())
        deck_filter = ttk.Combobox(search_frame, textvariable=self.filter_deck, 
                                  values=deck_options, state="readonly", width=15)
        deck_filter.pack(side=tk.LEFT, padx=5)
        deck_filter.bind("<<ComboboxSelected>>", self.update_flashcard_list)
        
        # Frame para a lista
        list_frame = tk.Frame(self.main_frame)
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.flashcard_listbox = tk.Listbox(list_frame, font=("Arial", self.font_size), 
                                          yscrollcommand=scrollbar.set,
                                          bg=theme["card_bg"], fg=theme["fg"])
        self.flashcard_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.flashcard_listbox.yview)
        
        # Preencher lista inicial
        self.update_flashcard_list()
        
        # Frame para botões
        btn_frame = tk.Frame(self.main_frame, bg=theme["bg"])
        btn_frame.pack(pady=10)
        
        btn_view = tk.Button(btn_frame, text="👁️ Ver Detalhes", 
                            font=("Arial", self.font_size), bg="#2196f3", fg="white",
                            command=self.view_card_details_from_list)
        btn_view.grid(row=0, column=0, padx=5)
        
        btn_edit = tk.Button(btn_frame, text="✏️ Editar", 
                            font=("Arial", self.font_size), bg="#ff9800", fg="white",
                            command=self.edit_flashcard_from_list)
        btn_edit.grid(row=0, column=1, padx=5)
        
        btn_move = tk.Button(btn_frame, text="📁 Mover", 
                            font=("Arial", self.font_size), bg="#9c27b0", fg="white",
                            command=self.move_flashcard)
        btn_move.grid(row=0, column=2, padx=5)
        
        btn_delete = tk.Button(btn_frame, text="🗑️ Excluir", 
                              font=("Arial", self.font_size), bg="#f44336", fg="white",
                              command=self.delete_flashcard_from_list)
        btn_delete.grid(row=0, column=3, padx=5)
        
        btn_back = tk.Button(self.main_frame, text="⬅️ Voltar", 
                            font=("Arial", self.font_size), bg="#9e9e9e", fg="white",
                            command=self.show_main_menu)
        btn_back.pack(pady=10)
    
    def update_flashcard_list(self, *args):
        """Atualiza a lista de flashcards com base na busca e filtros"""
        self.flashcard_listbox.delete(0, tk.END)
        self.filtered_indices = []
        
        search_term = self.search_var.get().lower()
        selected_deck = self.filter_deck.get()
        
        for i, card in enumerate(self.flashcards):
            # Filtrar por baralho
            if selected_deck != "Todos":
                if i not in self.decks.get(selected_deck, []):
                    continue
            
            # Filtrar por busca
            if search_term:
                if (search_term not in card["front"].lower() and 
                    search_term not in card["back"].lower()):
                    continue
            
            # Encontrar o baralho do cartão
            card_deck = "Geral"
            for deck_name, deck_cards in self.decks.items():
                if i in deck_cards:
                    card_deck = deck_name
                    break
            
            display_text = f"[{card_deck}] {card['front'][:50]}{'...' if len(card['front']) > 50 else ''}"
            self.flashcard_listbox.insert(tk.END, display_text)
            self.filtered_indices.append(i)
    
    def view_card_details_from_list(self):
        """Exibe detalhes do cartão selecionado na lista"""
        try:
            selected_idx = self.flashcard_listbox.curselection()[0]
            card_idx = self.filtered_indices[selected_idx]
            self.view_card_details_by_index(card_idx)
        except IndexError:
            messagebox.showwarning("Aviso", "Selecione um flashcard para visualizar.")
    
    def view_card_details_by_index(self, idx):
        """Exibe os detalhes de um flashcard pelo índice"""
        card = self.flashcards[idx]
        
        # Encontrar o baralho
        card_deck = "Geral"
        for deck_name, deck_cards in self.decks.items():
            if idx in deck_cards:
                card_deck = deck_name
                break
        
        details = f"🗂️ Baralho: {card_deck}\n\n"
        details += f"❓ Frente: {card['front']}\n\n"
        details += f"✅ Verso: {card['back']}\n\n"
        details += f"📅 Criado em: {card['created_at']}\n"
        details += f"🔄 Última revisão: {card['last_review'] or 'Nunca'}\n"
        details += f"⏰ Próxima revisão: {card['next_review']}\n"
        details += f"🔢 Repetições: {card['repetitions']}\n"
        details += f"📊 Fator facilidade: {card['ease_factor']:.2f}\n"
        details += f"🎯 Sequência correta: {card.get('correct_streak', 0)}\n"
        details += f"📈 Total de revisões: {card.get('total_reviews', 0)}"
        
        messagebox.showinfo(f"Detalhes do Flashcard #{idx+1}", details)
    
    def edit_flashcard_from_list(self):
        """Edita um flashcard selecionado na lista"""
        try:
            selected_idx = self.flashcard_listbox.curselection()[0]
            card_idx = self.filtered_indices[selected_idx]
            self.edit_flashcard(card_idx)
        except IndexError:
            messagebox.showwarning("Aviso", "Selecione um flashcard para editar.")
    
    def edit_flashcard(self, idx):
        """Edita um flashcard específico"""
        card = self.flashcards[idx]
        self.clear_frame()
        theme = self.themes[self.current_theme]
        
        title_label = tk.Label(self.main_frame, text=f"✏️ Editar Flashcard #{idx+1}", 
                              font=("Arial", 16, "bold"), bg=theme["bg"], fg=theme["fg"])
        title_label.pack(pady=10)
        
        # Frame para entradas
        entry_frame = tk.Frame(self.main_frame, bg=theme["bg"])
        entry_frame.pack(pady=10, fill="both", expand=True)
        
        # Frente do cartão
        front_label = tk.Label(entry_frame, text="Frente:", 
                              font=("Arial", self.font_size), bg=theme["bg"], fg=theme["fg"])
        front_label.grid(row=0, column=0, padx=10, pady=10, sticky="nw")
        
        self.front_text = tk.Text(entry_frame, height=5, width=50, 
                                 font=("Arial", self.font_size), wrap=tk.WORD,
                                 bg=theme["card_bg"], fg=theme["fg"])
        self.front_text.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        self.front_text.insert(tk.END, card["front"])
        
        # Verso do cartão
        back_label = tk.Label(entry_frame, text="Verso:", 
                             font=("Arial", self.font_size), bg=theme["bg"], fg=theme["fg"])
        back_label.grid(row=1, column=0, padx=10, pady=10, sticky="nw")
        
        self.back_text = tk.Text(entry_frame, height=5, width=50, 
                                font=("Arial", self.font_size), wrap=tk.WORD,
                                bg=theme["card_bg"], fg=theme["fg"])
        self.back_text.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        self.back_text.insert(tk.END, card["back"])
        
        entry_frame.grid_columnconfigure(1, weight=1)
        
        # Frame para botões
        button_frame = tk.Frame(self.main_frame, bg=theme["bg"])
        button_frame.pack(pady=10)
        
        # Botão atualizar
        update_btn = tk.Button(button_frame, text="💾 Atualizar", 
                              font=("Arial", self.font_size), bg="#4caf50", fg="white",
                              command=lambda: self.update_flashcard(idx))
        update_btn.grid(row=0, column=0, padx=10)
        
        # Botão cancelar
        cancel_btn = tk.Button(button_frame, text="❌ Cancelar", 
                              font=("Arial", self.font_size), bg="#f44336", fg="white",
                              command=self.list_flashcards)
        cancel_btn.grid(row=0, column=1, padx=10)
    
    def update_flashcard(self, idx):
        """Atualiza um flashcard existente"""
        front = self.front_text.get("1.0", "end-1c").strip()
        back = self.back_text.get("1.0", "end-1c").strip()
        
        if not self.validate_text_input(front) or not self.validate_text_input(back):
            messagebox.showwarning("Aviso", "Preencha todos os campos com conteúdo válido!")
            return
        
        # Atualizar dados mantendo estatísticas
        self.flashcards[idx]["front"] = front
        self.flashcards[idx]["back"] = back
        
        self.save_data()
        messagebox.showinfo("Sucesso", "Flashcard atualizado com sucesso!")
        self.list_flashcards()
    
    def move_flashcard(self):
        """Move um flashcard para outro baralho"""
        try:
            selected_idx = self.flashcard_listbox.curselection()[0]
            card_idx = self.filtered_indices[selected_idx]
            
            # Encontrar baralho atual
            current_deck = None
            for deck_name, deck_cards in self.decks.items():
                if card_idx in deck_cards:
                    current_deck = deck_name
                    break
            
            # Selecionar novo baralho
            deck_options = [d for d in self.decks.keys() if d != current_deck]
            if not deck_options:
                messagebox.showinfo("Info", "Não há outros baralhos disponíveis.")
                return
            
            new_deck = None
            deck_window = tk.Toplevel(self.root)
            deck_window.title("Mover Flashcard")
            deck_window.geometry("300x200")
            deck_window.grab_set()
            
            tk.Label(deck_window, text="Selecione o novo baralho:", 
                    font=("Arial", 12)).pack(pady=10)
            
            deck_var = tk.StringVar()
            for deck in deck_options:
                tk.Radiobutton(deck_window, text=deck, variable=deck_var, 
                              value=deck, font=("Arial", 11)).pack(anchor="w", padx=20)
            
            def move_card():
                nonlocal new_deck
                new_deck = deck_var.get()
                if new_deck:
                    deck_window.destroy()
            
            tk.Button(deck_window, text="Mover", command=move_card, 
                     bg="#4caf50", fg="white").pack(pady=10)
            tk.Button(deck_window, text="Cancelar", command=deck_window.destroy, 
                     bg="#f44336", fg="white").pack(pady=5)
            
            deck_window.wait_window()
            
            if new_deck:
                # Remover do baralho atual e adicionar ao novo
                self.decks[current_deck].remove(card_idx)
                self.decks[new_deck].append(card_idx)
                self.save_data()
                messagebox.showinfo("Sucesso", f"Flashcard movido para '{new_deck}'!")
                self.update_flashcard_list()
            
        except IndexError:
            messagebox.showwarning("Aviso", "Selecione um flashcard para mover.")
    
    def delete_flashcard_from_list(self):
        """Exclui um flashcard selecionado na lista"""
        try:
            selected_idx = self.flashcard_listbox.curselection()[0]
            card_idx = self.filtered_indices[selected_idx]
            
            confirm = messagebox.askyesno("Confirmar Exclusão", 
                                         "Tem certeza que deseja excluir este flashcard?")
            
            if confirm:
                # Remover das listas de baralhos
                for deck_cards in self.decks.values():
                    if card_idx in deck_cards:
                        deck_cards.remove(card_idx)
                    # Ajustar índices dos cartões após o removido
                    for i in range(len(deck_cards)):
                        if deck_cards[i] > card_idx:
                            deck_cards[i] -= 1
                
                # Remover o flashcard
                del self.flashcards[card_idx]
                
                self.save_data()
                messagebox.showinfo("Sucesso", "Flashcard excluído com sucesso!")
                self.update_flashcard_list()
        except IndexError:
            messagebox.showwarning("Aviso", "Selecione um flashcard para excluir.")
    
    def import_flashcards(self):
        """Importa flashcards de um arquivo CSV"""
        file_path = filedialog.askopenfilename(
            title="Importar Flashcards",
            filetypes=[("CSV files", "*.csv"), ("Text files", "*.txt"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            imported_count = 0
            deck_name = simpledialog.askstring("Baralho", 
                                              "Nome do baralho para os flashcards importados:",
                                              initialvalue="Importados")
            
            if not deck_name or not self.validate_text_input(deck_name):
                deck_name = "Importados"
            
            # Criar baralho se não existir
            if deck_name not in self.decks:
                self.decks[deck_name] = []
            
            with open(file_path, 'r', encoding='utf-8') as file:
                if file_path.endswith('.csv'):
                    csv_reader = csv.reader(file)
                    for row in csv_reader:
                        if len(row) >= 2 and self.validate_text_input(row[0]) and self.validate_text_input(row[1]):
                            new_card = {
                                "front": row[0].strip(),
                                "back": row[1].strip(),
                                "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "last_review": None,
                                "next_review": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "ease_factor": 2.5,
                                "interval": 0,
                                "repetitions": 0,
                                "correct_streak": 0,
                                "total_reviews": 0
                            }
                            self.flashcards.append(new_card)
                            self.decks[deck_name].append(len(self.flashcards) - 1)
                            imported_count += 1
                else:
                    # Formato texto: linha ímpar = frente, linha par = verso
                    lines = file.readlines()
                    for i in range(0, len(lines) - 1, 2):
                        front = lines[i].strip()
                        back = lines[i + 1].strip()
                        
                        if self.validate_text_input(front) and self.validate_text_input(back):
                            new_card = {
                                "front": front,
                                "back": back,
                                "created_at": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "last_review": None,
                                "next_review": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "ease_factor": 2.5,
                                "interval": 0,
                                "repetitions": 0,
                                "correct_streak": 0,
                                "total_reviews": 0
                            }
                            self.flashcards.append(new_card)
                            self.decks[deck_name].append(len(self.flashcards) - 1)
                            imported_count += 1
            
            self.save_data()
            messagebox.showinfo("Sucesso", f"{imported_count} flashcards importados com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao importar flashcards: {e}")
    
    def export_flashcards(self):
        """Exporta flashcards para um arquivo CSV"""
        if not self.flashcards:
            messagebox.showwarning("Aviso", "Não há flashcards para exportar.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Exportar Flashcards",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        try:
            # Perguntar se quer exportar todos ou apenas de um baralho
            export_all = messagebox.askyesno("Exportar", 
                                           "Exportar todos os flashcards?\n(Não = apenas do baralho atual)")
            
            cards_to_export = []
            if export_all:
                cards_to_export = [(i, card) for i, card in enumerate(self.flashcards)]
            else:
                deck_cards = self.get_deck_cards(self.current_deck)
                cards_to_export = [(i, self.flashcards[i]) for i in deck_cards if i < len(self.flashcards)]
            
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                csv_writer = csv.writer(file)
                csv_writer.writerow(['Frente', 'Verso', 'Baralho', 'Criado', 'Repetições', 'Facilidade'])
                
                for idx, card in cards_to_export:
                    # Encontrar baralho do cartão
                    card_deck = "Geral"
                    for deck_name, deck_cards in self.decks.items():
                        if idx in deck_cards:
                            card_deck = deck_name
                            break
                    
                    csv_writer.writerow([
                        card['front'],
                        card['back'],
                        card_deck,
                        card['created_at'],
                        card['repetitions'],
                        card['ease_factor']
                    ])
            
            messagebox.showinfo("Sucesso", f"{len(cards_to_export)} flashcards exportados com sucesso!")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao exportar flashcards: {e}")
    
    def show_statistics(self):
        """Exibe estatísticas detalhadas"""
        self.clear_frame()
        theme = self.themes[self.current_theme]
        
        title_label = tk.Label(self.main_frame, text="📊 Estatísticas", 
                              font=("Arial", 18, "bold"), bg=theme["bg"], fg=theme["fg"])
        title_label.pack(pady=10)
        
        # Calcular estatísticas
        total_cards = len(self.flashcards)
        if total_cards == 0:
            no_data = tk.Label(self.main_frame, text="Não há dados para exibir.", 
                              font=("Arial", 14), bg=theme["bg"], fg=theme["fg"])
            no_data.pack(pady=20)
            
            btn_back = tk.Button(self.main_frame, text="⬅️ Voltar", 
                                font=("Arial", self.font_size), bg="#9e9e9e", fg="white",
                                command=self.show_main_menu)
            btn_back.pack(pady=10)
            return
        
        # Estatísticas gerais
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pending_today = sum(1 for card in self.flashcards 
                           if not card["next_review"] or card["next_review"] <= current_date)
        
        reviewed_cards = sum(1 for card in self.flashcards if card["last_review"])
        never_reviewed = total_cards - reviewed_cards
        
        # Estatísticas por nível de facilidade
        easy_cards = sum(1 for card in self.flashcards if card["ease_factor"] >= 2.8)
        medium_cards = sum(1 for card in self.flashcards if 2.2 <= card["ease_factor"] < 2.8)
        hard_cards = sum(1 for card in self.flashcards if card["ease_factor"] < 2.2)
        
        # Frame de estatísticas
        stats_frame = tk.Frame(self.main_frame, bg=theme["bg"])
        stats_frame.pack(pady=10, fill="both", expand=True)
        
        # Estatísticas em texto
        text_stats = tk.Text(stats_frame, height=15, width=60, 
                            font=("Arial", self.font_size), wrap=tk.WORD,
                            bg=theme["card_bg"], fg=theme["fg"])
        text_stats.pack(side=tk.LEFT, padx=10, fill="both", expand=True)
        
        stats_text = f"""📚 ESTATÍSTICAS GERAIS
        
Total de flashcards: {total_cards}
Pendentes para hoje: {pending_today}
Já revisados: {reviewed_cards}
Nunca revisados: {never_reviewed}

🎯 POR DIFICULDADE
Fáceis (≥2.8): {easy_cards}
Médios (2.2-2.7): {medium_cards}
Difíceis (<2.2): {hard_cards}

🗂️ POR BARALHO"""
        
        for deck_name, deck_cards in self.decks.items():
            valid_cards = [i for i in deck_cards if i < len(self.flashcards)]
            stats_text += f"\n{deck_name}: {len(valid_cards)} cartões"
        
        # Estatísticas de atividade recente
        recent_reviews = []
        for card in self.flashcards:
            if card["last_review"]:
                try:
                    review_date = datetime.datetime.strptime(card["last_review"], "%Y-%m-%d %H:%M:%S")
                    days_ago = (datetime.datetime.now() - review_date).days
                    if days_ago <= 7:
                        recent_reviews.append(days_ago)
                except:
                    pass
        
        stats_text += f"\n\n📅 ATIVIDADE RECENTE (7 dias)\nRevisões: {len(recent_reviews)} cartões"
        
        text_stats.insert(tk.END, stats_text)
        text_stats.config(state=tk.DISABLED)
        
        # Gráfico simples usando matplotlib
        try:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
            
            # Gráfico de dificuldade
            ax1.pie([easy_cards, medium_cards, hard_cards], 
                   labels=['Fáceis', 'Médios', 'Difíceis'],
                   colors=['#4caf50', '#ff9800', '#f44336'],
                   autopct='%1.1f%%')
            ax1.set_title('Distribuição por Dificuldade')
            
            # Gráfico de revisões por baralho
            deck_names = list(self.decks.keys())[:5]  # Top 5 baralhos
            deck_counts = [len([i for i in self.decks[name] if i < len(self.flashcards)]) 
                          for name in deck_names]
            
            ax2.bar(deck_names, deck_counts, color='#2196f3')
            ax2.set_title('Cartões por Baralho (Top 5)')
            ax2.tick_params(axis='x', rotation=45)
            
            plt.tight_layout()
            
            # Adicionar gráfico ao tkinter
            canvas = FigureCanvasTkAgg(fig, stats_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.RIGHT, padx=10)
            
        except ImportError:
            # Se matplotlib não estiver disponível
            chart_label = tk.Label(stats_frame, 
                                  text="📈 Gráficos indisponíveis\n(instale matplotlib)", 
                                  font=("Arial", 12), bg=theme["bg"], fg=theme["fg"])
            chart_label.pack(side=tk.RIGHT, padx=10)
        
        # Botão voltar
        btn_back = tk.Button(self.main_frame, text="⬅️ Voltar", 
                            font=("Arial", self.font_size), bg="#9e9e9e", fg="white",
                            command=self.show_main_menu)
        btn_back.pack(pady=10)
    
    def show_settings(self):
        """Exibe configurações do aplicativo"""
        self.clear_frame()
        theme = self.themes[self.current_theme]
        
        title_label = tk.Label(self.main_frame, text="⚙️ Configurações", 
                              font=("Arial", 18, "bold"), bg=theme["bg"], fg=theme["fg"])
        title_label.pack(pady=10)
        
        # Frame de configurações
        config_frame = tk.Frame(self.main_frame, bg=theme["bg"])
        config_frame.pack(pady=20, fill="both", expand=True)
        
        # Seleção de tema
        theme_frame = tk.Frame(config_frame, bg=theme["bg"])
        theme_frame.pack(pady=10, fill="x")
        
        theme_label = tk.Label(theme_frame, text="🎨 Tema:", 
                              font=("Arial", self.font_size), bg=theme["bg"], fg=theme["fg"])
        theme_label.pack(side=tk.LEFT, padx=10)
        
        self.theme_var = tk.StringVar(value=self.current_theme)
        for theme_name in self.themes.keys():
            theme_radio = tk.Radiobutton(theme_frame, text=theme_name.title(), 
                                        variable=self.theme_var, value=theme_name,
                                        font=("Arial", self.font_size),
                                        bg=theme["bg"], fg=theme["fg"],
                                        command=self.change_theme)
            theme_radio.pack(side=tk.LEFT, padx=10)
        
        # Tamanho da fonte
        font_frame = tk.Frame(config_frame, bg=theme["bg"])
        font_frame.pack(pady=10, fill="x")
        
        font_label = tk.Label(font_frame, text="📝 Tamanho da fonte:", 
                             font=("Arial", self.font_size), bg=theme["bg"], fg=theme["fg"])
        font_label.pack(side=tk.LEFT, padx=10)
        
        self.font_var = tk.IntVar(value=self.font_size)
        font_scale = tk.Scale(font_frame, from_=10, to=16, orient=tk.HORIZONTAL,
                             variable=self.font_var, command=self.change_font_size,
                             bg=theme["bg"], fg=theme["fg"])
        font_scale.pack(side=tk.LEFT, padx=10)
        
        # Opções de revisão
        review_frame = tk.Frame(config_frame, bg=theme["bg"])
        review_frame.pack(pady=20, fill="x")
        
        review_label = tk.Label(review_frame, text="🔄 Configurações de Revisão:", 
                               font=("Arial", self.font_size, "bold"), 
                               bg=theme["bg"], fg=theme["fg"])
        review_label.pack(anchor="w", padx=10)
        
        self.bidirectional_var = tk.BooleanVar(value=self.bidirectional_mode)
        bidirectional_check = tk.Checkbutton(review_frame, 
                                           text="Revisão bidirecional (frente↔verso)",
                                           variable=self.bidirectional_var,
                                           font=("Arial", self.font_size),
                                           bg=theme["bg"], fg=theme["fg"],
                                           command=self.toggle_bidirectional)
        bidirectional_check.pack(anchor="w", padx=20, pady=5)
        
        # Backup e restauração
        backup_frame = tk.Frame(config_frame, bg=theme["bg"])
        backup_frame.pack(pady=20, fill="x")
        
        backup_label = tk.Label(backup_frame, text="💾 Backup e Restauração:", 
                               font=("Arial", self.font_size, "bold"), 
                               bg=theme["bg"], fg=theme["fg"])
        backup_label.pack(anchor="w", padx=10)
        
        btn_backup = tk.Button(backup_frame, text="💾 Fazer Backup", 
                              font=("Arial", self.font_size), bg="#4caf50", fg="white",
                              command=self.create_backup)
        btn_backup.pack(side=tk.LEFT, padx=10, pady=5)
        
        btn_restore = tk.Button(backup_frame, text="📥 Restaurar Backup", 
                               font=("Arial", self.font_size), bg="#ff9800", fg="white",
                               command=self.restore_backup)
        btn_restore.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Botão voltar
        btn_back = tk.Button(self.main_frame, text="⬅️ Voltar", 
                            font=("Arial", self.font_size), bg="#9e9e9e", fg="white",
                            command=self.show_main_menu)
        btn_back.pack(pady=20)
    
    def change_theme(self):
        """Muda o tema da aplicação"""
        self.current_theme = self.theme_var.get()
        self.apply_theme()
        self.save_data()
        self.show_settings()  # Recarregar para aplicar o tema
    
    def change_font_size(self, value):
        """Muda o tamanho da fonte"""
        self.font_size = int(value)
        self.save_data()
    
    def toggle_bidirectional(self):
        """Liga/desliga modo de revisão bidirecional"""
        self.bidirectional_mode = self.bidirectional_var.get()
        self.save_data()
    
    def create_backup(self):
        """Cria um backup dos dados"""
        file_path = filedialog.asksaveasfilename(
            title="Salvar Backup",
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            try:
                import shutil
                shutil.copy2("flashcards_data.json", file_path)
                messagebox.showinfo("Sucesso", "Backup criado com sucesso!")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao criar backup: {e}")
    
    def restore_backup(self):
        """Restaura dados de um backup"""
        file_path = filedialog.askopenfilename(
            title="Selecionar Backup",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if file_path:
            confirm = messagebox.askyesno("Confirmar Restauração", 
                                         "Isso substituirá todos os dados atuais. Continuar?")
            if confirm:
                try:
                    import shutil
                    shutil.copy2(file_path, "flashcards_data.json")
                    self.load_data()
                    messagebox.showinfo("Sucesso", "Backup restaurado com sucesso!")
                    self.show_main_menu()
                except Exception as e:
                    messagebox.showerror("Erro", f"Erro ao restaurar backup: {e}")
    
    def start_review(self):
        """Inicia a sessão de revisão com opção bidirecional"""
        self.clear_frame()
        theme = self.themes[self.current_theme]
        
        # Obter cartões do baralho atual
        deck_cards = self.get_deck_cards(self.current_deck)
        
        if not deck_cards:
            no_cards = tk.Label(self.main_frame, 
                               text="Nenhum flashcard neste baralho.", 
                               font=("Arial", 14), bg=theme["bg"], fg=theme["fg"])
            no_cards.pack(pady=20)
            
            btn_back = tk.Button(self.main_frame, text="⬅️ Voltar", 
                                font=("Arial", self.font_size), bg="#9e9e9e", fg="white",
                                command=self.show_main_menu)
            btn_back.pack(pady=10)
            return
        
        # Filtrar flashcards prontos para revisão
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cards_to_review = []
        
        for card_idx in deck_cards:
            if card_idx < len(self.flashcards):
                card = self.flashcards[card_idx]
                if not card["next_review"] or card["next_review"] <= current_date:
                    cards_to_review.append(card_idx)
        
        if not cards_to_review:
            no_review = tk.Label(self.main_frame, 
                                text=f"✅ Todos os flashcards do baralho '{self.current_deck}' foram revisados!", 
                                font=("Arial", 14), bg=theme["bg"], fg=theme["fg"])
            no_review.pack(pady=20)
            
            # Permitir revisão forçada
            force_btn = tk.Button(self.main_frame, text="🔄 Revisar Todos Mesmo Assim", 
                                 font=("Arial", self.font_size), bg="#ff9800", fg="white",
                                 command=lambda: self.show_card(deck_cards.copy()))
            force_btn.pack(pady=10)
            
            btn_back = tk.Button(self.main_frame, text="⬅️ Voltar", 
                                font=("Arial", self.font_size), bg="#9e9e9e", fg="white",
                                command=self.show_main_menu)
            btn_back.pack(pady=10)
        else:
            self.show_card(cards_to_review.copy())
    
    def show_card(self, cards_to_review):
        """Exibe um cartão para revisão com suporte bidirecional"""
        self.clear_frame()
        theme = self.themes[self.current_theme]
        
        if not cards_to_review:
            complete_label = tk.Label(self.main_frame, 
                                     text="🎉 Revisão completa!", 
                                     font=("Arial", 18, "bold"), bg=theme["bg"], fg=theme["fg"])
            complete_label.pack(pady=20)
            
            summary_text = f"Baralho '{self.current_deck}' revisado com sucesso!"
            summary_label = tk.Label(self.main_frame, text=summary_text,
                                    font=("Arial", 12), bg=theme["bg"], fg=theme["fg"])
            summary_label.pack(pady=10)
            
            btn_back = tk.Button(self.main_frame, text="🏠 Voltar ao Menu", 
                                font=("Arial", self.font_size), bg="#4caf50", fg="white",
                                command=self.show_main_menu)
            btn_back.pack(pady=10)
            return
        
        # Selecionar um cartão aleatório
        card_idx = random.choice(cards_to_review)
        cards_to_review.remove(card_idx)
        self.current_card = self.flashcards[card_idx]
        self.current_card_idx = card_idx
        
        # Determinar direção (bidirecional ou não)
        if self.bidirectional_mode and random.choice([True, False]):
            self.showing_front = False  # Mostrar verso primeiro
            question = self.current_card["back"]
            answer = self.current_card["front"]
            direction_indicator = "🔄 Verso → Frente"
        else:
            self.showing_front = True  # Mostrar frente primeiro
            question = self.current_card["front"]
            answer = self.current_card["back"]
            direction_indicator = "➡️ Frente → Verso"
        
        self.current_question = question
        self.current_answer = answer
        self.showing_answer = False
        
        # Informações da sessão
        info_frame = tk.Frame(self.main_frame, bg=theme["bg"])
        info_frame.pack(fill="x", padx=10, pady=5)
        
        info_left = tk.Label(info_frame, text=f"📚 {self.current_deck}",
                            font=("Arial", 10), bg=theme["bg"], fg=theme["fg"])
        info_left.pack(side=tk.LEFT)
        
        info_center = tk.Label(info_frame, text=direction_indicator,
                              font=("Arial", 10, "bold"), bg=theme["bg"], fg="#2196f3")
        info_center.pack(side=tk.LEFT, expand=True)
        
        info_right = tk.Label(info_frame, text=f"Restantes: {len(cards_to_review) + 1}",
                             font=("Arial", 10), bg=theme["bg"], fg=theme["fg"])
        info_right.pack(side=tk.RIGHT)
        
        # Frame para o cartão
        card_frame = tk.Frame(self.main_frame, bg=theme["card_bg"], 
                             highlightbackground="#ddd", highlightthickness=2,
                             relief=tk.RAISED, bd=2)
        card_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Título da seção
        question_label = tk.Label(card_frame, text="❓ Pergunta:", 
                                 font=("Arial", self.font_size, "bold"), 
                                 bg=theme["card_bg"], fg=theme["fg"])
        question_label.pack(pady=(20, 10))
        
        # Conteúdo do cartão
        content_text = tk.Text(card_frame, height=8, font=("Arial", self.font_size + 2),
                              wrap=tk.WORD, bg=theme["card_bg"], fg=theme["fg"], 
                              relief=tk.FLAT, cursor="arrow")
        content_text.pack(padx=20, pady=10, fill="both", expand=True)
        content_text.insert(tk.END, question)
        content_text.config(state=tk.DISABLED)
        
        # Frame para botões
        button_frame = tk.Frame(self.main_frame, bg=theme["bg"])
        button_frame.pack(pady=15)
        
        # Botão para mostrar resposta
        show_answer_btn = tk.Button(button_frame, text="💡 Mostrar Resposta", 
                                   font=("Arial", self.font_size), bg="#2196f3", fg="white",
                                   pady=10, width=20,
                                   command=lambda: self.show_answer(cards_to_review))
        show_answer_btn.pack()
        
        # Tecla Enter para mostrar resposta
        self.root.bind('<Return>', lambda e: self.show_answer(cards_to_review))
        self.root.focus_set()
    
    def show_answer(self, cards_to_review):
        """Mostra a resposta e botões de avaliação"""
        self.showing_answer = True
        self.clear_frame()
        theme = self.themes[self.current_theme]
        
        # Informações da sessão
        info_frame = tk.Frame(self.main_frame, bg=theme["bg"])
        info_frame.pack(fill="x", padx=10, pady=5)
        
        direction_indicator = "🔄 Verso → Frente" if not self.showing_front else "➡️ Frente → Verso"
        
        info_left = tk.Label(info_frame, text=f"📚 {self.current_deck}",
                            font=("Arial", 10), bg=theme["bg"], fg=theme["fg"])
        info_left.pack(side=tk.LEFT)
        
        info_center = tk.Label(info_frame, text=direction_indicator,
                              font=("Arial", 10, "bold"), bg=theme["bg"], fg="#2196f3")
        info_center.pack(side=tk.LEFT, expand=True)
        
        info_right = tk.Label(info_frame, text=f"Restantes: {len(cards_to_review) + 1}",
                             font=("Arial", 10), bg=theme["bg"], fg=theme["fg"])
        info_right.pack(side=tk.RIGHT)
        
        # Frame para o cartão
        card_frame = tk.Frame(self.main_frame, bg=theme["card_bg"], 
                             highlightbackground="#ddd", highlightthickness=2,
                             relief=tk.RAISED, bd=2)
        card_frame.pack(fill="both", expand=True, padx=20, pady=15)
        
        # Pergunta
        question_label = tk.Label(card_frame, text="❓ Pergunta:", 
                                 font=("Arial", self.font_size, "bold"), 
                                 bg=theme["card_bg"], fg=theme["fg"])
        question_label.pack(pady=(15, 5))
        
        question_text = tk.Text(card_frame, height=3, font=("Arial", self.font_size),
                               wrap=tk.WORD, bg=theme["card_bg"], fg=theme["fg"], 
                               relief=tk.FLAT, cursor="arrow")
        question_text.pack(padx=15, pady=5, fill="x")
        question_text.insert(tk.END, self.current_question)
        question_text.config(state=tk.DISABLED)
        
        # Separador
        separator = tk.Frame(card_frame, height=2, bg="#ddd")
        separator.pack(fill="x", padx=15, pady=10)
        
        # Resposta
        answer_label = tk.Label(card_frame, text="✅ Resposta:", 
                               font=("Arial", self.font_size, "bold"), 
                               bg=theme["card_bg"], fg="#4caf50")
        answer_label.pack(pady=(10, 5))
        
        answer_text = tk.Text(card_frame, height=3, font=("Arial", self.font_size),
                             wrap=tk.WORD, bg=theme["card_bg"], fg=theme["fg"], 
                             relief=tk.FLAT, cursor="arrow")
        answer_text.pack(padx=15, pady=5, fill="x")
        answer_text.insert(tk.END, self.current_answer)
        answer_text.config(state=tk.DISABLED)
        
        # Frame para avaliação
        rating_frame = tk.Frame(self.main_frame, bg=theme["bg"])
        rating_frame.pack(pady=20)
        
        rating_title = tk.Label(rating_frame, text="🎯 Como foi sua resposta?", 
                               font=("Arial", self.font_size + 1, "bold"), 
                               bg=theme["bg"], fg=theme["fg"])
        rating_title.pack(pady=(0, 15))
        
        # Botões de avaliação em duas linhas
        buttons_container = tk.Frame(rating_frame, bg=theme["bg"])
        buttons_container.pack()
        
        # Primeira linha - respostas negativas
        row1 = tk.Frame(buttons_container, bg=theme["bg"])
        row1.pack(pady=5)
        
        btn_again = tk.Button(row1, text="😵 Esqueci\nCompleto", 
                             font=("Arial", self.font_size - 1), bg="#f44336", fg="white", 
                             width=15, height=3,
                             command=lambda: self.process_answer(0, cards_to_review))
        btn_again.pack(side=tk.LEFT, padx=5)
        
        btn_hard = tk.Button(row1, text="😰 Difícil\nDemorei muito", 
                            font=("Arial", self.font_size - 1), bg="#ff9800", fg="white", 
                            width=15, height=3,
                            command=lambda: self.process_answer(1, cards_to_review))
        btn_hard.pack(side=tk.LEFT, padx=5)
        
        # Segunda linha - respostas positivas
        row2 = tk.Frame(buttons_container, bg=theme["bg"])
        row2.pack(pady=5)
        
        btn_good = tk.Button(row2, text="😊 Bom\nLembrei bem", 
                            font=("Arial", self.font_size - 1), bg="#4caf50", fg="white", 
                            width=15, height=3,
                            command=lambda: self.process_answer(2, cards_to_review))
        btn_good.pack(side=tk.LEFT, padx=5)
        
        btn_easy = tk.Button(row2, text="😎 Fácil\nImediato", 
                            font=("Arial", self.font_size - 1), bg="#2196f3", fg="white", 
                            width=15, height=3,
                            command=lambda: self.process_answer(3, cards_to_review))
        btn_easy.pack(side=tk.LEFT, padx=5)
        
        # Atalhos de teclado
        self.root.bind('1', lambda e: self.process_answer(0, cards_to_review))
        self.root.bind('2', lambda e: self.process_answer(1, cards_to_review))
        self.root.bind('3', lambda e: self.process_answer(2, cards_to_review))
        self.root.bind('4', lambda e: self.process_answer(3, cards_to_review))
        
        # Dica de atalhos
        shortcut_label = tk.Label(rating_frame, text="💡 Atalhos: 1=Esqueci, 2=Difícil, 3=Bom, 4=Fácil", 
                                 font=("Arial", 10), bg=theme["bg"], fg="#666")
        shortcut_label.pack(pady=(15, 0))
    
    def process_answer(self, quality, cards_to_review):
        """Processa a resposta com algoritmo SM-2 aprimorado"""
        self.root.unbind('<Return>')
        self.root.unbind('1')
        self.root.unbind('2')
        self.root.unbind('3')
        self.root.unbind('4')
        
        card = self.current_card
        
        # Atualizar dados de revisão
        card["last_review"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        card["total_reviews"] = card.get("total_reviews", 0) + 1
        
        # Algoritmo SM-2 aprimorado
        if quality >= 3:  # Resposta correta
            if card["repetitions"] == 0:
                card["interval"] = 1
            elif card["repetitions"] == 1:
                card["interval"] = 6
            else:
                card["interval"] = round(card["interval"] * card["ease_factor"])
            
            card["repetitions"] += 1
            card["correct_streak"] = card.get("correct_streak", 0) + 1
        else:  # Resposta incorreta
            card["repetitions"] = 0
            card["interval"] = 1
            card["correct_streak"] = 0
        
        # Atualizar fator de facilidade
        card["ease_factor"] = max(1.3, card["ease_factor"] + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)))
        
        # Ajustar intervalo baseado na qualidade
        if quality == 0:  # Esqueci
            card["interval"] = 1
        elif quality == 1:  # Difícil
            card["interval"] = max(1, round(card["interval"] * 1.2))
        elif quality == 3:  # Fácil
            card["interval"] = round(card["interval"] * 1.3)
        
        # Calcular próxima revisão
        next_review_date = datetime.datetime.now() + datetime.timedelta(days=card["interval"])
        card["next_review"] = next_review_date.strftime("%Y-%m-%d %H:%M:%S")
        
        # Salvar e continuar
        self.save_data()
        self.show_card(cards_to_review)
    
    def on_closing(self):
        """Confirmação ao fechar o aplicativo"""
        if messagebox.askokcancel("Sair", "Deseja realmente sair do aplicativo?"):
            self.save_data()  # Garantir que os dados sejam salvos
            self.root.destroy()

def main():
    try:
        root = tk.Tk()
        app = FlashcardApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Erro ao iniciar aplicativo: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()