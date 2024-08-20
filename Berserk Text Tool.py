import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import codecs
from tkinter import Scrollbar
from PIL import Image, ImageTk
from PIL import Image, ImageTk, ImageDraw, ImageFont
import webbrowser
from tkinter import ttk
import json
from tkinter import Button
from pytube import YouTube
import os


current_language = "Português do Brasil" 

scroll_speed_factor = 0.001


# Função para sincronizar a rolagem do mouse
def sync_scroll(event):
    delta = event.delta * scroll_speed_factor
    original_text_box.yview_scroll(int(-1 * delta), "units")
    original_text_box.update_idletasks()
    # Calcula a proporção do scroll do texto original e aplica à caixa de números de linhas
    fraction = original_text_box.yview()[0]
    line_numbers_box.yview_moveto(fraction)

# Configurar o scrollbar para usar a função de sincronização


dark_theme = {
    'bg': 'black',
    'fg': 'white',
    'highlightbackground': 'black',
    'highlightcolor': 'white',
    'selectbackground': 'white',
    'selectforeground': 'black',
    'insertbackground': 'white',
    'insertwidth': 2,
    'font': ('Arial', 12),
}




def load_translations(language):
    global current_language
    current_language = language
    
    with open("translations.json", "r", encoding="utf-8") as file:
        translations = json.load(file)
        return translations.get(language, translations["English"])
    
def update_interface_text():
    translations = load_translations(current_language)
    
    
    original_text_label.config(text=translations["OriginalText"])
    translated_text_label.config(text=translations["TranslatedText"])
    load_table_button.config(text=translations["OpenTable"])
    load_translated_button.config(text=translations["OpenTextExtract"])
    load_original_button.config(text=translations["OpenSTBFile"])
    extrair_button.config(text=translations["ExtractSTB"])
    inserir_button.config(text=translations["InsertText"])
    clear_button.config(text=translations["ClearText"])
    save_button.config(text=translations["SaveText"])
    exibir_creditos_button.config(text=translations["About"])
    language_label.config(text=translations["SelectLanguage"])
   # english_button.config(text=translations["LanguageEnglish"])
   # portuguese_button.config(text=translations["LanguagePortuguese"])
    exibir_creditos_button.config(text=translations["Credits"])
    text_label.config(text=translations["Label"])
    line_label.config(text=translations["Lines"])
    window.title(f"Berserk Text Editor - Developed By Sora Leon")
    


def set_english_language():
    change_language("English")

def set_portuguese_language():
    change_language("Português do Brasil")

def set_spanish_language():
    change_language("Español")

def change_language(language):
    global current_language
    current_language = language
   
    update_interface_text()
    update_image()




hex_table={}



def credits():
    message = ("Programado por Sora Leon\nDesenvolvido em Python\nVersão 3.0.1\nFerramenta Para Edição dos Textos do Jogo: Berserk: Millennium Falcon Hen Seima Senki no Shō")
    messagebox.showinfo('Creditos', message)
    webbrowser.open("https://www.youtube.com/@SoraLeon")
    webbrowser.open("https://digi-translations.blogspot.com/")
    

    
def update_line_numbers(event=None):
    # Obtém o texto atual do campo de texto original
    text = original_text_box.get("1.0", "end-1c")
    # Divide o texto em linhas e conta o número de linhas
    line_count = len(text.split("\n"))
    # Atualiza a caixa de texto de contagem de linhas
    line_numbers_box.config(state=tk.NORMAL)
    line_numbers_box.delete(1.0, tk.END)
    line_numbers_box.insert(tk.END, "\n".join(str(i) for i in range(1, line_count + 1)))
    line_numbers_box.config(state=tk.DISABLED)




def insert_newlines(text, max_line_length=36):
    lines = text.split('\n')
    new_lines = []
    for line in lines:
        if "{0a}" in line:
            parts = line.split("{0a}")
            for part in parts:
                while len(part) > max_line_length:
                    new_lines.append(part[:max_line_length])
                    part = part[max_line_length:]
                if part:
                    new_lines.append(part)
        else:
            while len(line) > max_line_length:
                new_lines.append(line[:max_line_length])
                line = line[max_line_length:]
            if line:
                new_lines.append(line)
    return '\n'.join(new_lines)

def update_image():
    text = text_entry.get('1.0', 'end-1c')
    
    # Limita o número de linhas a 3
    lines = text.split('\n')[:3]

    # Limita cada linha a 29 caracteres e insere {0a} para quebrar linhas
    for i, line in enumerate(lines):
        lines[i] = insert_newlines(line)

    text = "\n".join(lines)
    
    # Substitui {0a} por quebra de linha
    text = text.replace("{0a}", "\n")
    text = text.replace("{0A}", "\n")  # Considera {0A} como quebra de linha também
    
    image = Image.open("previewer.png")
    
    # Determina o tamanho necessário da imagem com base no texto
    target_width = 400
    w_percent = (target_width / float(image.size[0]))
    h_size = int((float(image.size[1]) * float(w_percent)) * 3)
    image = image.resize((target_width, h_size), Image.BICUBIC)
    
    # Configura a posição e tamanho do texto com base nas dimensões da imagem
    text_x = 65  # Convertendo cm para pixels (21 pixels = 1 cm)
    text_y = 50  # Convertendo cm para pixels (29.7 pixels = 1 cm)

    draw = ImageDraw.Draw(image)
    font_size = 16 # Tamanho da fonte (ajustado para caber 3 linhas de 29 caracteres)
    font = ImageFont.truetype("msgothic.ttc", font_size)

    lines = text.split('\n')[:3]
    for i, line in enumerate(lines):
        draw.text((text_x, text_y + i * (font_size + 4)), line, fill="white", font=font)

    photo = ImageTk.PhotoImage(image)

    preview_label.configure(image=photo)
    preview_label.image = photo
# Atualize a função load_stb_text para exibir a contagem de linhas
def load_stb_text():
    file_path = filedialog.askopenfilename(title="Escolha o arquivo STB",
                                           filetypes=[("Arquivos STB", "*.stb")])
    if file_path:
        try:
            with open(file_path, 'rb') as file:
                data = file.read()
                comeco_texto = int.from_bytes(data[0x20:0x24], byteorder='little')
                texto_utf8 = data[comeco_texto:].decode("latin-1")
                linhas = texto_utf8.split('\x00')
                stb_text = '\n'.join(line.strip() for line in linhas if line.strip())
                original_text_box.config(state=tk.NORMAL)
                original_text_box.delete(1.0, tk.END)
                original_text_box.insert(tk.END, stb_text)
                original_text_box.config(state=tk.DISABLED)

                # Exiba a contagem de linhas na caixa de texto de contagem de linhas
                line_count = len(linhas)
                line_numbers_box.config(state=tk.NORMAL)
                line_numbers_box.delete(1.0, tk.END)
                line_numbers_box.insert(tk.END, '\n'.join(str(i) for i in range(1, line_count + 1)))
                line_numbers_box.config(state=tk.DISABLED)
                update_line_numbers()
        except FileNotFoundError:
            original_text_box.config(state=tk.NORMAL)
            original_text_box.delete(1.0, tk.END)
            original_text_box.insert(tk.END, "Arquivo STB não pôde ser lido.")
            original_text_box.config(state=tk.DISABLED)
            



def load_translated_text():
    file_path = filedialog.askopenfilename(title="Escolha o arquivo de texto editado",
                                           filetypes=[("Arquivos de texto", "*.txt")])
    if file_path:
        try:
            with codecs.open(file_path, 'r', encoding='utf-8') as file:
                translated_text = file.read()
                translated_text_box.delete(1.0, tk.END)
                translated_text_box.insert(tk.END, translated_text)
        except FileNotFoundError:
            translated_text_box.delete(1.0, tk.END)




def load_hex_table():
    global hex_table
    file_path = filedialog.askopenfilename(title="Escolha o arquivo de tabela",
                                           filetypes=[("Arquivos de texto", "*.txt")])
    if file_path:
        try:
            with codecs.open(file_path, 'r', encoding='utf-8') as file:
                hex_table = {}
                for line in file:
                    line = line.strip()  # Remove espaços em branco no início e no final da linha
                    if '=' in line:
                        char, value = line.split('=', 1)  # Divida a linha na primeira ocorrência do "="
                        hex_table[char] = value
                messagebox.showinfo("Alerta Berserk!", "Tabela carregada com sucesso!")
        except FileNotFoundError:
            pass

def save_translated_text():
    translated_text = translated_text_box.get('1.0', 'end-1c')  # Obtém o texto traduzido

    for char, value in hex_table.items():
        translated_text = translated_text.replace(char, value)

    file_path = filedialog.asksaveasfilename(title="Salvar Texto Traduzido", defaultextension=".txt",
                                             filetypes=[("Arquivos de texto", "*.txt")])

    if file_path:
        with codecs.open(file_path, 'w', encoding='utf-8') as file:
            file.write(translated_text)


def all_replace():
    file_paths = filedialog.askopenfilenames(title="Escolha os arquivos .txt para substituição",
                                            filetypes=[("Arquivos de texto", "*.txt")])

    for file_path in file_paths:
        with codecs.open(file_path, 'r', encoding='utf-8') as file:
            original_text = file.read()
        
        # Aplica a substituição usando a tabela hex_table
        translated_text = original_text
        for char, value in hex_table.items():
            translated_text = translated_text.replace(char, value)
        
        with codecs.open(file_path, 'w', encoding='utf-8') as file:
            file.write(translated_text)
            message = ("Substituição de todos caracteres concluída!")
            messagebox.showinfo("Completo!", message)



def clear_text():
    original_text_box.config(state=tk.NORMAL)
    original_text_box.delete(1.0, tk.END)
    original_text_box.config(state=tk.DISABLED)
    line_numbers_box.config(state=tk.NORMAL)
    line_numbers_box.delete(1.0, tk.END)
    line_numbers_box.config(state=tk.DISABLED)
    update_line_numbers()
    translated_text_box.delete(1.0, tk.END)


def extrair_all_stb():
    stb_paths = filedialog.askopenfilenames(title="Selecionar arquivos .STB para extração", filetypes=[("Arquivos .STB", "*.stb")])

    if stb_paths:
        for stb_path in stb_paths:
            output_path = os.path.splitext(stb_path)[0] + ".txt"
            extrair_texto(stb_path, output_path)
        
        messagebox.showinfo("Aviso", "Extração concluída para todos os arquivos .STB selecionados.")

def inserir_all_txt():
    stb_paths = filedialog.askopenfilenames(title="Selecionar arquivos .STB para atualização", filetypes=[("Arquivos .STB", "*.stb")])
    txt_paths = filedialog.askopenfilenames(title="Selecionar arquivos de texto para inserir", filetypes=[("Arquivos .TXT", "*.txt")])

    if stb_paths and txt_paths:
        for i, stb_path in enumerate(stb_paths):
            if i < len(txt_paths):
                txt_path = txt_paths[i]
                output_path = os.path.splitext(stb_path)[0] + "_atualizado.stb"
                inserir_texto(stb_path, txt_path, output_path)
            else:
                messagebox.showinfo("Aviso", "Não há arquivos .txt suficientes para adicionar a todos os arquivos .STB selecionados.")
                return

        messagebox.showinfo("Aviso", f"Inserção concluída para todos os arquivos .STB selecionados com {len(txt_paths)} arquivos de texto.")


def extrair_texto(stb_path, output_path):
    with open(stb_path, "rb") as file:
        data = file.read()
        comeco_texto = int.from_bytes(data[0x14:0x18], byteorder='little')
        texto_utf8 = data[comeco_texto:].decode("latin-1")
        linhas = texto_utf8.split('\x00')
        texto_corrigido = '\n'.join(line.strip().replace('\n', '{0a}') for line in linhas if line.strip())

        with open(output_path, "w", encoding="latin-1") as output_file:
            output_file.write(texto_corrigido)

        print(f"Extração concluída para {output_path}")

        with open("stb_extraido.txt", "w", encoding="utf-8") as aviso_file:
            aviso_file.write("STB extraído com sucesso!")

        messagebox.showinfo("Aviso", "STB extraído com sucesso!")


def inserir_texto(stb_path, txt_path, output_path):
    with open(stb_path, "rb") as file:
        data = file.read()

        with open(txt_path, "r", encoding="latin-1") as input_file:
            texto_utf8 = input_file.read()
            texto_utf8 = texto_utf8.replace('\n', '\x00')
            texto_utf8 = texto_utf8.replace('{0a}', '\x0a')
            comeco_texto = int.from_bytes(data[0x14:0x18], byteorder='little')
            data = data[:comeco_texto] + texto_utf8.encode("latin-1") + data[comeco_texto + len(texto_utf8):]

        with open(txt_path, "r", encoding="latin-1") as input_file:
            lines = input_file.readlines()
            total_charcount = 0
            primeiro_ponteiro = 0

            for line_count, line in enumerate(lines, start=1):
                charcount = len(line.strip())

                if line_count == 1:
                    primeiro_ponteiro = (charcount + 1) * 1

                if '{0a}' in line:
                    charcount -= line.count('{0a}') * 3

                total_charcount += (charcount + 1) * 1
                hex_value = hex(total_charcount + comeco_texto)[2:].upper()

                print(f"{hex_value} {line_count}")

            hex_total = hex(total_charcount)[2:].upper()
            hex_primeiro_ponteiro = hex(primeiro_ponteiro)[2:].upper()

            print(f"Total Charcount: 0x{hex_total}")
            print(f"Primeiro Ponteiro: 0x{hex_primeiro_ponteiro}")

            posicao_ponteiro = 0x2C
            incrementos_count = 0

            for line_count, line in enumerate(lines, start=1):
                charcount = len(line.strip())
                if "{0a}" in line:
                    charcount -= line.count('{0a}') * 3
                if line_count != 1:
                    charcount += (charcount_anterior + 1) * 1
                charcount_anterior = charcount

                charcount_bytes = (charcount + 1) * 1 + comeco_texto
                data = data[:posicao_ponteiro] + charcount_bytes.to_bytes(4, byteorder='little') + data[posicao_ponteiro + 4:]
                posicao_ponteiro += 8

                incrementos_count += 1
                print(incrementos_count)
                if posicao_ponteiro > comeco_texto:
                    break

        with open(output_path, "wb") as output_file:
            output_file.write(data)
            print(f"Inserção concluída para {output_path}")

            with open("texto_inserido.txt", "w", encoding="utf-8") as aviso_file:
                aviso_file.write("Texto inserido com sucesso em STB")

            messagebox.showinfo("Aviso", "Texto inserido com sucesso em STB")




window = tk.Tk()
window.title("Berserk Text Editor - Desenvolvido Por Sora Leon")



load_table_button = tk.Button(window, text="Abrir Tabela")
load_table_button.grid(row=0, column=0)
load_table_button.config(command=load_hex_table)

load_original_button = tk.Button(window, text="Abrir arquivo STB")
load_original_button.grid(row=0, column=1)
load_original_button.config(command=load_stb_text)

load_translated_button = tk.Button(window, text="Abrir Texto Extraído")
load_translated_button.grid(row=0, column=2)
load_translated_button.config(command=load_translated_text)

clear_button = tk.Button(window, text="Limpar Texto")
clear_button.grid(row=0, column=3)
clear_button.config(command=clear_text)

save_button = tk.Button(window, text="Salvar")
save_button.grid(row=0, column=4)
save_button.config(command=save_translated_text)

extrair_button = tk.Button(window, text="Extrair STB")
extrair_button.grid(row=0, column=5)
extrair_button.config(command=extrair_texto)

inserir_button = tk.Button(window, text="Inserir Texto")
inserir_button.grid(row=0, column=6)
inserir_button.config(command=inserir_texto)

extrair_all_stb_button = tk.Button(window, text="EXTRAIR ALL STB", command=extrair_all_stb)
extrair_all_stb_button.grid(row=0, column=5)

inserir_all_txt_button = tk.Button(window, text="INSERIR ALL .TXT", command=inserir_all_txt)
inserir_all_txt_button.grid(row=0, column=6)

all_replace_button = tk.Button(window, text="All Replace", command=all_replace)
all_replace_button.grid(row=0, column=7)

exibir_creditos_button = tk.Button(window, text="Sobre")
exibir_creditos_button.grid(row=0, column=8)
exibir_creditos_button.config(command=credits)

original_text_label = tk.Label(window, text="Texto Original")
original_text_label.grid(row=1, column=0, columnspan=3, sticky="n")
original_text_label.config(anchor="center")

translated_text_label = tk.Label(window, text="Texto Editado")
translated_text_label.grid(row=1, column=3, columnspan=4, sticky="n")
translated_text_label.config(anchor="center")


text_frame = tk.Frame(window)
text_frame.grid(row=2, column=0, columnspan=10, sticky="n")


line_numbers_box = tk.Text(text_frame, wrap=tk.WORD, width=4, height=20)
line_numbers_box.grid(row=0, column=0, sticky="n")
line_numbers_box.config(state=tk.DISABLED)

original_text_box = tk.Text(text_frame, wrap=tk.WORD, width=36, height=20)
original_text_box.grid(row=0, column=1, columnspan=4)
original_text_box.config(state=tk.DISABLED)
original_text_box.config(selectbackground='blue')


translated_text_box = tk.Text(text_frame, wrap=tk.WORD, width=40, height=20)
translated_text_box.grid(row=0, column=5, columnspan=5)
translated_text_box.config(selectbackground='blue')


text_scrollbar = Scrollbar(text_frame, command=original_text_box.yview)
text_scrollbar.grid(row=0, column=10, sticky="ns")


original_text_box.config(yscrollcommand=text_scrollbar.set)
translated_text_box.config(yscrollcommand=text_scrollbar.set)


line_numbers_frame = tk.Frame(text_frame)
line_numbers_frame.grid(row=0, column=0, sticky="n")

line_label = tk.Label(line_numbers_frame, text="Linhas:")
line_label.grid(row=0, column=0, sticky="n")

line_numbers_box = tk.Text(line_numbers_frame, wrap=tk.NONE, width=4, height=20)
line_numbers_box.grid(row=0, column=1, sticky="n")
line_numbers_box.config(state=tk.DISABLED)





window.iconbitmap(r'guts.img')
image_frame = tk.Frame(window)
image_frame.grid(row=2, column=10, rowspan=10, padx=20, pady=20, sticky="n")

image = Image.open("previewer.png")
target_width = 400  # Largura desejada para o retângulo
w_percent = (target_width / float(image.size[0]))
h_size = int((float(image.size[1]) * float(w_percent)) * 3)
image = image.resize((target_width, h_size), Image.BICUBIC)
preview_image = ImageTk.PhotoImage(image)

preview_label = tk.Label(image_frame, image=preview_image)
preview_label.grid(row=0, column=0)

# Crie a caixa de diálogo para inserir texto na imagem
text_frame = tk.Frame(window)
text_frame.grid(row=3, column=10, padx=20, pady=20, sticky="n")

text_label = tk.Label(text_frame, text="Preview - Digite para Visualizar")
text_label.grid(row=0, column=0, sticky="n")

text_entry = tk.Text(text_frame, width=40, height=3)
text_entry.grid(row=1, column=0, sticky="n")
text_entry.bind("<KeyRelease>", lambda event: update_image())
text_entry.config(selectbackground='blue')



background_image = tk.PhotoImage(file="BB.img")

canvas = tk.Canvas(window, width=800, height=600)  
canvas.grid(row=3, column=0, columnspan=10)
canvas.create_image(0, 0, anchor=tk.NW, image=background_image)

# Elementos da interface para seleção de idioma
language_label = tk.Label(text_frame, text="Seleção de Idioma:")
language_label.grid(row=15, column=0, columnspan=1, pady=(1, 0))

# Substitua os botões de seleção de idioma por uma barra seletiva
s = ttk.Style()  # Crie um objeto de estilo

# Após a criação do Combobox, configure a cor do texto para a cor desejada, por exemplo, preta (black).
language_slider = ttk.Combobox(text_frame, values=["Português do Brasil", "English", "Español", "日本語", "Italiano", "Português de Portugal","Russian"])
language_slider.set(current_language)
language_slider.grid(row=16, column=0, columnspan=2, sticky="n")

# Configure a cor do texto (foreground) para preto.
language_slider.config(foreground="black")
language_slider.config(background="black")

language_slider.bind("<<ComboboxSelected>>", lambda event: change_language(language_slider.get()))





window.tk_setPalette(background=dark_theme['bg'], foreground=dark_theme['fg'])
original_text_box.config(bg=dark_theme['bg'], fg=dark_theme['fg'], insertbackground=dark_theme['insertbackground'], font=dark_theme['font'])
translated_text_box.config(bg=dark_theme['bg'], fg=dark_theme['fg'], insertbackground=dark_theme['insertbackground'], font=dark_theme['font'])
line_numbers_box.config(bg=dark_theme['bg'], fg=dark_theme['fg'], insertbackground=dark_theme['insertbackground'], font=dark_theme['font'])
preview_label.config(bg=dark_theme['bg'], fg=dark_theme['fg'])
text_label.config(bg=dark_theme['bg'], fg=dark_theme['fg'])
text_entry.config(bg=dark_theme['bg'], fg=dark_theme['fg'], insertbackground=dark_theme['insertbackground'], font=dark_theme['font'])
canvas.config(bg=dark_theme['bg'])

text_scrollbar.config(bg=dark_theme['bg'], troughcolor=dark_theme['bg'], activebackground=dark_theme['bg'])

# Configurar o seletor de idioma com cores personalizadas
language_slider.config(style="Dark.TCombobox")
s = ttk.Style()
s.theme_create("dark", parent="alt", settings={
    "TCombobox": {
        "configure": {
            "selectbackground": dark_theme['selectbackground'],
            "fieldbackground": dark_theme['bg'],
            "background": dark_theme['bg'],
            "foreground": dark_theme['fg'],
            "font": dark_theme['font'],
        },
    }
})

original_text_box.bind("<MouseWheel>", sync_scroll)
line_numbers_box.bind("<MouseWheel>", sync_scroll)



window.mainloop()
