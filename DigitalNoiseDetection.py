import tkinter as tk
from tkinter import messagebox
import random

# ============================================================
# DIGITAL NOISE DETECTION AND ERROR DEMONSTRATOR
# (7,4) HAMMING BLOCK CODE
# ============================================================

BG = "#0b1220"
PANEL = "#111c2e"
PANEL2 = "#17253a"
TEXT = "#f4f7fb"
MUTED = "#aab7c8"
ACCENT = "#4da3ff"
SUCCESS = "#35d07f"
ERROR = "#ff5c6c"
GOLD = "#ffd166"
WHITE = "#ffffff"


def bits_to_string(bits):
    return "".join(str(b) for b in bits)


def valid_bits(value, length):
    return len(value) == length and all(c in "01" for c in value)


# -------------------- HAMMING (7,4) -------------------------

def encode_hamming(data):
    # Positions: P1 P2 D1 P4 D2 D3 D4

    d1, d2, d3, d4 = map(int, data)

    p1 = d1 ^ d2 ^ d4
    p2 = d1 ^ d3 ^ d4
    p4 = d2 ^ d3 ^ d4

    return [p1, p2, d1, p4, d2, d3, d4]


def calculate_syndrome(received):

    r1, r2, r3, r4, r5, r6, r7 = received

    s1 = r1 ^ r3 ^ r5 ^ r7
    s2 = r2 ^ r3 ^ r6 ^ r7
    s4 = r4 ^ r5 ^ r6 ^ r7

    position = s1 + (2 * s2) + (4 * s4)

    # Syndrome displayed as S4 S2 S1
    syndrome = f"{s4}{s2}{s1}"

    return syndrome, position


def decode_hamming(received):

    syndrome, position = calculate_syndrome(received)

    corrected = received.copy()

    # Correct the detected single-bit error
    if position != 0:
        corrected[position - 1] ^= 1

    # Extract original data bits
    decoded = [
        corrected[2],
        corrected[4],
        corrected[5],
        corrected[6]
    ]

    return syndrome, position, corrected, decoded


# ============================================================
# GUI APPLICATION
# ============================================================

class HammingApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Digital Noise Detection & Error Demonstrator"
        )

        self.root.geometry("1150x760")
        self.root.minsize(1000, 680)
        self.root.configure(bg=BG)

        self.original_codeword = None
        self.received_codeword = None
        self.corrected_codeword = None

        self.build_ui()


    # ---------------- UI HELPERS ----------------

    def make_label(
        self,
        parent,
        text,
        size=11,
        bold=False,
        color=TEXT
    ):

        font = (
            "Segoe UI",
            size,
            "bold" if bold else "normal"
        )

        return tk.Label(
            parent,
            text=text,
            bg=parent.cget("bg"),
            fg=color,
            font=font
        )


    def panel(self, parent, title):

        frame = tk.Frame(
            parent,
            bg=PANEL,
            highlightthickness=1,
            highlightbackground="#263851"
        )

        title_label = tk.Label(
            frame,
            text=title,
            bg=PANEL,
            fg=GOLD,
            font=("Segoe UI", 13, "bold")
        )

        title_label.pack(
            anchor="w",
            padx=18,
            pady=(14, 8)
        )

        return frame


    def entry(self, parent, width=18):

        e = tk.Entry(
            parent,
            width=width,
            bg="#0a1424",
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            font=("Consolas", 16, "bold"),
            justify="center"
        )

        e.configure(
            highlightthickness=1,
            highlightbackground="#31445f",
            highlightcolor=ACCENT
        )

        return e


    def button(self, parent, text, command, width=20):

        return tk.Button(
            parent,
            text=text,
            command=command,
            width=width,
            bg=ACCENT,
            fg=WHITE,
            activebackground="#3187d8",
            activeforeground=WHITE,
            relief="flat",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            padx=8,
            pady=8
        )


    # ========================================================
    # BUILD GUI
    # ========================================================

    def build_ui(self):

        # ---------------- HEADER ----------------

        header = tk.Frame(
            self.root,
            bg=BG
        )

        header.pack(
            fill="x",
            padx=25,
            pady=(20, 5)
        )

        tk.Label(
            header,
            text="DIGITAL NOISE DETECTION & ERROR DEMONSTRATOR",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 21, "bold")
        ).pack()

        tk.Label(
            header,
            text="(7,4) HAMMING BLOCK CODE  •  ERROR DETECTION & CORRECTION",
            bg=BG,
            fg=ACCENT,
            font=("Segoe UI", 10, "bold")
        ).pack(pady=(3, 0))


        # ---------------- SCROLL AREA ----------------

        canvas = tk.Canvas(
            self.root,
            bg=BG,
            highlightthickness=0
        )

        scrollbar = tk.Scrollbar(
            self.root,
            orient="vertical",
            command=canvas.yview
        )

        self.content = tk.Frame(
            canvas,
            bg=BG
        )

        self.content.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window(
            (0, 0),
            window=self.content,
            anchor="nw"
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(20, 0),
            pady=10
        )

        scrollbar.pack(
            side="right",
            fill="y",
            padx=(0, 12),
            pady=10
        )


        # Mouse-wheel scrolling

        canvas.bind_all(
            "<MouseWheel>",
            lambda e:
            canvas.yview_scroll(
                int(-e.delta / 120),
                "units"
            )
        )


        # ====================================================
        # TWO COLUMN SECTION
        # ====================================================

        top = tk.Frame(
            self.content,
            bg=BG
        )

        top.pack(
            fill="x",
            pady=5
        )


        # ---------------- TRANSMITTER ----------------

        left = self.panel(
            top,
            "1. TRANSMITTER — INPUT MESSAGE"
        )

        left.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 8)
        )


        # ---------------- NOISE CHANNEL ----------------

        right = self.panel(
            top,
            "2. NOISE CHANNEL — RECEIVED DATA"
        )

        right.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(8, 0)
        )


        top.grid_columnconfigure(
            0,
            weight=1
        )

        top.grid_columnconfigure(
            1,
            weight=1
        )


        # ====================================================
        # TRANSMITTER
        # ====================================================

        tk.Label(
            left,
            text="Enter 4-bit message:",
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(pady=(4, 3))


        self.message_entry = self.entry(
            left,
            12
        )

        self.message_entry.pack(
            pady=4
        )


        self.button(
            left,
            "GENERATE HAMMING CODE",
            self.generate_code,
            25
        ).pack(pady=10)


        tk.Label(
            left,
            text="Generated (7,4) Codeword",
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(pady=(7, 2))


        self.codeword_var = tk.StringVar(
            value="—"
        )

        tk.Label(
            left,
            textvariable=self.codeword_var,
            bg="#0a1424",
            fg=GOLD,
            font=("Consolas", 22, "bold"),
            width=16,
            pady=8
        ).pack(
            pady=(2, 15)
        )


        # ====================================================
        # NOISE CHANNEL
        # ====================================================

        tk.Label(
            right,
            text="Noise / error mode:",
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(pady=(4, 3))


        self.noise_var = tk.StringVar(
            value="No Error"
        )


        self.noise_menu = tk.OptionMenu(
            right,
            self.noise_var,
            "No Error",
            "1-Bit Error",
            "Random Noise"
        )


        self.noise_menu.config(
            bg="#0a1424",
            fg=TEXT,
            activebackground="#203451",
            activeforeground=TEXT,
            relief="flat",
            font=("Segoe UI", 10),
            width=18
        )


        self.noise_menu["menu"].config(
            bg="#0a1424",
            fg=TEXT,
            activebackground=ACCENT,
            activeforeground=WHITE
        )


        self.noise_menu.pack(
            pady=4
        )


        self.button(
            right,
            "SIMULATE NOISE",
            self.simulate_noise,
            25
        ).pack(pady=9)


        tk.Label(
            right,
            text="OR manually enter received codeword:",
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(pady=(5, 3))


        self.received_entry = self.entry(
            right,
            12
        )

        self.received_entry.pack(
            pady=3
        )


        self.button(
            right,
            "USE MANUAL CODEWORD",
            self.use_manual,
            25
        ).pack(
            pady=(8, 15)
        )


        # ====================================================
        # ERROR ANALYSIS
        # ====================================================

        analysis = self.panel(
            self.content,
            "3. ERROR ANALYSIS"
        )

        analysis.pack(
            fill="x",
            pady=12
        )


        info = tk.Frame(
            analysis,
            bg=PANEL
        )

        info.pack(
            fill="x",
            padx=18,
            pady=(2, 15)
        )


        self.syndrome_var = tk.StringVar(
            value="—"
        )

        self.error_var = tk.StringVar(
            value="—"
        )

        self.position_var = tk.StringVar(
            value="—"
        )

        self.received_var = tk.StringVar(
            value="—"
        )


        self.info_box(
            info,
            "SYNDROME",
            self.syndrome_var,
            0
        )

        self.info_box(
            info,
            "ERROR STATUS",
            self.error_var,
            1
        )

        self.info_box(
            info,
            "ERROR POSITION",
            self.position_var,
            2
        )

        self.info_box(
            info,
            "RECEIVED CODEWORD",
            self.received_var,
            3
        )


        # ---------------- BIT VISUALIZATION ----------------

        tk.Label(
            analysis,
            text="BIT-BY-BIT TRANSMISSION VIEW",
            bg=PANEL,
            fg=MUTED,
            font=("Segoe UI", 10, "bold")
        ).pack(
            pady=(3, 5)
        )


        self.bits_frame = tk.Frame(
            analysis,
            bg=PANEL
        )

        self.bits_frame.pack(
            pady=(0, 18)
        )


        self.bit_labels = []


        for i in range(7):

            box = tk.Frame(
                self.bits_frame,
                bg=PANEL2,
                highlightthickness=1,
                highlightbackground="#31445f"
            )

            box.grid(
                row=0,
                column=i,
                padx=5
            )


            label = tk.Label(
                box,
                text="—",
                width=3,
                height=1,
                bg=PANEL2,
                fg=TEXT,
                font=("Consolas", 18, "bold")
            )

            label.pack(
                padx=5,
                pady=(6, 2)
            )


            tk.Label(
                box,
                text=f"Bit {i+1}",
                bg=PANEL2,
                fg=MUTED,
                font=("Segoe UI", 8)
            ).pack(
                padx=5,
                pady=(0, 5)
            )


            self.bit_labels.append(
                label
            )


        # ====================================================
        # ERROR CORRECTION
        # ====================================================

        correction = self.panel(
            self.content,
            "4. ERROR CORRECTION & OUTPUT"
        )

        correction.pack(
            fill="x",
            pady=(0, 12)
        )


        grid = tk.Frame(
            correction,
            bg=PANEL
        )

        grid.pack(
            fill="x",
            padx=18,
            pady=5
        )


        self.corrected_var = tk.StringVar(
            value="—"
        )

        self.original_var = tk.StringVar(
            value="—"
        )

        self.decoded_var = tk.StringVar(
            value="—"
        )

        self.status_var = tk.StringVar(
            value="WAITING FOR INPUT"
        )


        self.output_box(
            grid,
            "TRANSMITTED CODEWORD",
            self.codeword_var,
            0,
            0
        )


        self.output_box(
            grid,
            "CORRECTED CODEWORD",
            self.corrected_var,
            0,
            1
        )


        self.output_box(
            grid,
            "ORIGINAL MESSAGE",
            self.original_var,
            1,
            0
        )


        self.output_box(
            grid,
            "DECODED MESSAGE",
            self.decoded_var,
            1,
            1
        )


        self.status_label = tk.Label(
            correction,
            textvariable=self.status_var,
            bg="#0a1424",
            fg=MUTED,
            font=("Segoe UI", 15, "bold"),
            pady=12
        )


        self.status_label.pack(
            fill="x",
            padx=18,
            pady=(10, 18)
        )


        # ====================================================
        # EXPLANATION
        # ====================================================

        explain = self.panel(
            self.content,
            "5. HOW HAMMING (7,4) WORKS"
        )

        explain.pack(
            fill="x",
            pady=(0, 20)
        )


        explanation = (
            "Bit positions:   1    2    3    4    5    6    7\n"
            "                 P1   P2   D1   P4   D2   D3   D4\n\n"
            "P1 checks positions 1, 3, 5, 7\n"
            "P2 checks positions 2, 3, 6, 7\n"
            "P4 checks positions 4, 5, 6, 7\n\n"
            "The syndrome identifies the position of a single-bit error.\n"
            "A syndrome of 000 means that no single-bit error is detected."
        )


        tk.Label(
            explain,
            text=explanation,
            bg=PANEL,
            fg=MUTED,
            justify="left",
            font=("Consolas", 10),
            padx=18,
            pady=5
        ).pack(
            anchor="w"
        )


        self.button(
            explain,
            "CLEAR / RESET",
            self.reset,
            20
        ).pack(
            pady=15
        )


    # ========================================================
    # INFORMATION BOX
    # ========================================================

    def info_box(
        self,
        parent,
        title,
        variable,
        column
    ):

        frame = tk.Frame(
            parent,
            bg=PANEL2,
            highlightthickness=1,
            highlightbackground="#263851"
        )


        frame.grid(
            row=0,
            column=column,
            padx=5,
            sticky="nsew"
        )


        parent.grid_columnconfigure(
            column,
            weight=1
        )


        tk.Label(
            frame,
            text=title,
            bg=PANEL2,
            fg=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(
            padx=12,
            pady=(9, 3)
        )


        tk.Label(
            frame,
            textvariable=variable,
            bg=PANEL2,
            fg=TEXT,
            font=("Consolas", 13, "bold"),
            wraplength=180
        ).pack(
            padx=10,
            pady=(0, 10)
        )


    # ========================================================
    # OUTPUT BOX
    # ========================================================

    def output_box(
        self,
        parent,
        title,
        variable,
        row,
        column
    ):

        frame = tk.Frame(
            parent,
            bg=PANEL2,
            highlightthickness=1,
            highlightbackground="#263851"
        )


        frame.grid(
            row=row,
            column=column,
            padx=5,
            pady=5,
            sticky="nsew"
        )


        parent.grid_columnconfigure(
            column,
            weight=1
        )


        tk.Label(
            frame,
            text=title,
            bg=PANEL2,
            fg=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(
            pady=(8, 2)
        )


        tk.Label(
            frame,
            textvariable=variable,
            bg=PANEL2,
            fg=GOLD,
            font=("Consolas", 16, "bold")
        ).pack(
            pady=(0, 8)
        )


    # ========================================================
    # PROJECT FUNCTIONS
    # ========================================================

    def generate_code(self):

        data = self.message_entry.get().strip()


        if not valid_bits(data, 4):

            messagebox.showerror(
                "Invalid Message",
                "Please enter exactly 4 binary bits.\n"
                "Example: 1011"
            )

            return


        codeword = encode_hamming(
            data
        )


        self.original_codeword = codeword


        self.codeword_var.set(
            bits_to_string(codeword)
        )


        self.original_var.set(
            data
        )


        self.status_var.set(
            "CODEWORD GENERATED — READY FOR TRANSMISSION"
        )


        self.status_label.config(
            fg=ACCENT
        )


        self.received_entry.delete(
            0,
            tk.END
        )


        self.clear_analysis()


        self.update_bits(
            codeword,
            None
        )


    # ========================================================
    # SIMULATE NOISE
    # ========================================================

    def simulate_noise(self):

        if self.original_codeword is None:

            messagebox.showwarning(
                "Generate Code First",
                "Enter a 4-bit message and generate "
                "the Hamming codeword first."
            )

            return


        transmitted = self.original_codeword.copy()

        mode = self.noise_var.get()


        if mode == "No Error":

            received = transmitted.copy()


        elif mode == "1-Bit Error":

            position = random.randint(
                0,
                6
            )

            received = transmitted.copy()

            received[position] ^= 1


        else:

            # Random Noise

            received = transmitted.copy()

            