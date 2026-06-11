import tkinter as tk
from tkinter import font as tkfont

# ════════════════════════════════════════
#  CONFIGURAÇÕES
# ════════════════════════════════════════

CORES = {
    "bg": "#0f0f13",
    "surface": "#1a1a24",
    "border": "#2a2a3a",
    "accent": "#7c6cfc",
    "accent_hover": "#9588ff",
    "correct": "#3ddc84",
    "wrong": "#ff5c5c",
    "text": "#e8e8f0",
    "muted": "#7a7a9a",
}

PERGUNTAS = [
    {
        "pergunta": "Qual é a capital do Brasil?",
        "alternativas": ["São Paulo", "Rio de Janeiro", "Brasília", "Salvador"],
        "correta": 2,
    },
    {
        "pergunta": "Quantos países fazem parte da América do Sul?",
        "alternativas": ["10", "12", "14", "8"],
        "correta": 1,
    },
    {
        "pergunta": "Qual planeta é conhecido como o Planeta Vermelho?",
        "alternativas": ["Vênus", "Júpiter", "Saturno", "Marte"],
        "correta": 3,
    },
    {
        "pergunta": "Em que ano o Brasil foi descoberto pelos portugueses?",
        "alternativas": ["1492", "1500", "1498", "1510"],
        "correta": 1,
    },
    {
        "pergunta": "Qual é o maior oceano do mundo?",
        "alternativas": ["Atlântico", "Índico", "Ártico", "Pacífico"],
        "correta": 3,
    },
    {
        "pergunta": "Quem escreveu 'Dom Casmurro'?",
        "alternativas": ["José de Alencar", "Machado de Assis", "Carlos Drummond", "Clarice Lispector"],
        "correta": 1,
    },
    {
        "pergunta": "Qual é o elemento químico representado pelo símbolo 'O'?",
        "alternativas": ["Ouro", "Ósmio", "Oxigênio", "Olívio"],
        "correta": 2,
    },
    {
        "pergunta": "Em qual continente fica o Egito?",
        "alternativas": ["Ásia", "Europa", "África", "Oceania"],
        "correta": 2,
    },
    {
        "pergunta": "Quantos lados tem um hexágono?",
        "alternativas": ["5", "7", "8", "6"],
        "correta": 3,
    },
    {
        "pergunta": "Qual é o menor país do mundo?",
        "alternativas": ["Mônaco", "San Marino", "Vaticano", "Liechtenstein"],
        "correta": 2,
    },
]

LETRAS = ["A", "B", "C", "D"]


# ════════════════════════════════════════
#  CLASSE PRINCIPAL
# ════════════════════════════════════════

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz — Cultura Geral")
        self.root.configure(bg=CORES["bg"])
        self.root.resizable(True, True)

        # Centraliza a janela
        largura, altura = 700, 620
        x = (self.root.winfo_screenwidth() - largura) // 2
        y = (self.root.winfo_screenheight() - altura) // 2
        self.root.geometry(f"{largura}x{altura}+{x}+{y}")
        self.root.minsize(480, 520)

        # Fontes
        self.font_titulo = tkfont.Font(family="Segoe UI", size=28, weight="bold")
        self.font_subtitulo = tkfont.Font(family="Segoe UI", size=12)
        self.font_pergunta = tkfont.Font(family="Segoe UI", size=15, weight="bold")
        self.font_opcao = tkfont.Font(family="Segoe UI", size=13)
        self.font_btn = tkfont.Font(family="Segoe UI", size=13, weight="bold")
        self.font_counter = tkfont.Font(family="Segoe UI", size=11)
        self.font_resultado_num = tkfont.Font(family="Segoe UI", size=40, weight="bold")
        self.font_resultado_titulo = tkfont.Font(family="Segoe UI", size=22, weight="bold")
        self.font_resultado_item = tkfont.Font(family="Segoe UI", size=11)

        # Estado
        self.atual = 0
        self.respostas_usuario = []
        self.selecionada = tk.IntVar(value=-1)

        # Container principal
        self.container = tk.Frame(root, bg=CORES["bg"])
        self.container.pack(fill="both", expand=True, padx=30, pady=20)

        self.tela_inicio()

    # ──────────────────────────────────
    #  TELA INICIAL
    # ──────────────────────────────────
    def tela_inicio(self):
        self.limpar()

        spacer = tk.Frame(self.container, bg=CORES["bg"])
        spacer.pack(expand=True)

        centro = tk.Frame(self.container, bg=CORES["bg"])
        centro.pack(expand=True)

        # Badge
        badge = tk.Label(
            centro, text="🧠  CULTURA GERAL", font=self.font_counter,
            bg=CORES["surface"], fg=CORES["accent"],
            padx=16, pady=6
        )
        badge.pack(pady=(0, 20))

        # Titulo
        tk.Label(
            centro, text="Quanto você sabe?", font=self.font_titulo,
            bg=CORES["bg"], fg=CORES["text"]
        ).pack(pady=(0, 12))

        # Subtitulo
        tk.Label(
            centro, text="10 perguntas para testar seus conhecimentos.\nEscolha a alternativa e veja o resultado no final.",
            font=self.font_subtitulo, bg=CORES["bg"], fg=CORES["muted"], justify="center"
        ).pack(pady=(0, 36))

        # Botão começar
        self.criar_botao(centro, "Começar o Quiz →", self.iniciar_quiz, destaque=True)

        spacer2 = tk.Frame(self.container, bg=CORES["bg"])
        spacer2.pack(expand=True)

    # ──────────────────────────────────
    #  INICIAR QUIZ
    # ──────────────────────────────────
    def iniciar_quiz(self):
        self.atual = 0
        self.respostas_usuario = []
        self.mostrar_pergunta()

    # ──────────────────────────────────
    #  TELA DA PERGUNTA
    # ──────────────────────────────────
    def mostrar_pergunta(self):
        self.limpar()
        self.selecionada.set(-1)

        q = PERGUNTAS[self.atual]
        total = len(PERGUNTAS)

        # Barra de progresso
        barra_frame = tk.Frame(self.container, bg=CORES["border"], height=6)
        barra_frame.pack(fill="x", pady=(0, 20))
        barra_frame.pack_propagate(False)

        progresso = (self.atual / total)
        barra = tk.Frame(barra_frame, bg=CORES["accent"])
        barra.place(relx=0, rely=0, relwidth=progresso, relheight=1)

        # Counter e info
        info_frame = tk.Frame(self.container, bg=CORES["bg"])
        info_frame.pack(fill="x", pady=(0, 16))

        tk.Label(
            info_frame, text=f"Pergunta {self.atual + 1} de {total}",
            font=self.font_counter, bg=CORES["bg"], fg=CORES["muted"]
        ).pack(side="left")

        tk.Label(
            info_frame, text=f"Respondidas: {len(self.respostas_usuario)}",
            font=self.font_counter, bg=CORES["surface"], fg=CORES["accent"],
            padx=12, pady=4
        ).pack(side="right")

        # Card da pergunta
        card = tk.Frame(self.container, bg=CORES["surface"], padx=24, pady=24)
        card.pack(fill="x", pady=(0, 20))

        tk.Label(
            card, text=q["pergunta"], font=self.font_pergunta,
            bg=CORES["surface"], fg=CORES["text"],
            wraplength=580, justify="left", anchor="w"
        ).pack(fill="x")

        # Opções como radiobuttons estilizados
        self.opcoes_frames = []
        for i, alt in enumerate(q["alternativas"]):
            frame_opcao = tk.Frame(self.container, bg=CORES["surface"], padx=16, pady=14, cursor="hand2")
            frame_opcao.pack(fill="x", pady=4)

            letra = tk.Label(
                frame_opcao, text=LETRAS[i], font=self.font_btn,
                bg=CORES["border"], fg=CORES["muted"],
                width=3, height=1
            )
            letra.pack(side="left", padx=(0, 14))

            rb = tk.Radiobutton(
                frame_opcao, text=alt, variable=self.selecionada, value=i,
                font=self.font_opcao, bg=CORES["surface"], fg=CORES["text"],
                activebackground=CORES["surface"], activeforeground=CORES["text"],
                selectcolor=CORES["surface"], indicatoron=False,
                relief="flat", bd=0, anchor="w",
                command=lambda idx=i: self.selecionar_opcao(idx)
            )
            rb.pack(side="left", fill="x", expand=True)

            # Clique no frame inteiro seleciona
            frame_opcao.bind("<Button-1>", lambda e, idx=i: self.clicar_opcao(idx))
            letra.bind("<Button-1>", lambda e, idx=i: self.clicar_opcao(idx))

            self.opcoes_frames.append((frame_opcao, letra))

        # Botão próxima
        btn_frame = tk.Frame(self.container, bg=CORES["bg"])
        btn_frame.pack(fill="x", pady=(20, 0))

        texto_btn = "Finalizar Quiz →" if self.atual == total - 1 else "Próxima →"
        self.criar_botao(btn_frame, texto_btn, self.proxima_pergunta, destaque=True, side="right")

    def clicar_opcao(self, idx):
        self.selecionada.set(idx)
        self.selecionar_opcao(idx)

    def selecionar_opcao(self, idx):
        for i, (frame, letra) in enumerate(self.opcoes_frames):
            if i == idx:
                frame.configure(bg="#252540")
                letra.configure(bg=CORES["accent"], fg="#fff")
                for child in frame.winfo_children():
                    if isinstance(child, tk.Radiobutton):
                        child.configure(bg="#252540")
            else:
                frame.configure(bg=CORES["surface"])
                letra.configure(bg=CORES["border"], fg=CORES["muted"])
                for child in frame.winfo_children():
                    if isinstance(child, tk.Radiobutton):
                        child.configure(bg=CORES["surface"])

    def proxima_pergunta(self):
        if self.selecionada.get() == -1:
            return  # Não selecionou nada

        self.respostas_usuario.append(self.selecionada.get())
        self.atual += 1

        if self.atual >= len(PERGUNTAS):
            self.mostrar_resultado()
        else:
            self.mostrar_pergunta()

    # ──────────────────────────────────
    #  TELA DE RESULTADO
    # ──────────────────────────────────
    def mostrar_resultado(self):
        self.limpar()

        total = len(PERGUNTAS)
        acertos = sum(
            1 for i, q in enumerate(PERGUNTAS)
            if self.respostas_usuario[i] == q["correta"]
        )
        erros = total - acertos
        pct = int((acertos / total) * 100)

        # Scroll frame para os resultados
        canvas = tk.Canvas(self.container, bg=CORES["bg"], highlightthickness=0)
        scrollbar = tk.Scrollbar(self.container, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=CORES["bg"])

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Scroll com mouse
        def on_mouse(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        canvas.bind_all("<MouseWheel>", on_mouse)

        # ── Conteúdo ──

        # Pontuação grande
        cor_nota = CORES["correct"] if pct >= 70 else (CORES["accent"] if pct >= 40 else CORES["wrong"])

        tk.Label(
            scroll_frame, text=f"{acertos}/{total}", font=self.font_resultado_num,
            bg=CORES["bg"], fg=cor_nota
        ).pack(pady=(10, 4))

        tk.Label(
            scroll_frame, text=f"{pct}% de acerto", font=self.font_counter,
            bg=CORES["bg"], fg=CORES["muted"]
        ).pack(pady=(0, 8))

        # Titulo
        if pct == 100:
            titulo = "Perfeito! 🏆"
        elif pct >= 70:
            titulo = "Muito bem! 🎉"
        elif pct >= 40:
            titulo = "Quase lá! 😅"
        else:
            titulo = "Continue tentando! 💪"

        tk.Label(
            scroll_frame, text=titulo, font=self.font_resultado_titulo,
            bg=CORES["bg"], fg=CORES["text"]
        ).pack(pady=(0, 8))

        # Resumo
        tk.Label(
            scroll_frame, text=f"✓ {acertos} acerto{'s' if acertos != 1 else ''}    ✗ {erros} erro{'s' if erros != 1 else ''}",
            font=self.font_counter, bg=CORES["bg"], fg=CORES["muted"]
        ).pack(pady=(0, 24))



        # Espaço extra e botões
        btn_frame = tk.Frame(scroll_frame, bg=CORES["bg"])
        btn_frame.pack(pady=(24, 16))

        self.criar_botao(btn_frame, "Jogar de Novo →", self.iniciar_quiz, destaque=True, side="left")

        # Pack canvas e scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # ──────────────────────────────────
    #  UTILITÁRIOS
    # ──────────────────────────────────
    def limpar(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def criar_botao(self, parent, texto, comando, destaque=False, side=None):
        bg = CORES["accent"] if destaque else CORES["surface"]
        fg = "#fff" if destaque else CORES["text"]
        hover_bg = CORES["accent_hover"] if destaque else CORES["border"]

        btn = tk.Label(
            parent, text=texto, font=self.font_btn,
            bg=bg, fg=fg, padx=28, pady=12, cursor="hand2"
        )

        if side:
            btn.pack(side=side)
        else:
            btn.pack()

        btn.bind("<Enter>", lambda e: btn.configure(bg=hover_bg))
        btn.bind("<Leave>", lambda e: btn.configure(bg=bg))
        btn.bind("<Button-1>", lambda e: comando())

        return btn


# ════════════════════════════════════════
#  INICIAR
# ════════════════════════════════════════

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
