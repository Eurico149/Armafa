import tkinter as tk

def item_duplo_clique(event):
    # Pega o índice do item clicado
    selecionado = listbox.curselection()
    if selecionado:
        item = listbox.get(selecionado)
        print(f"Você clicou duas vezes no item: {item}")
        # Aqui você pode adicionar a lógica do que acontece quando clica duas vezes

root = tk.Tk()

# Cria a Listbox
listbox = tk.Listbox(root)
listbox.pack()

# Adiciona alguns itens
listbox.insert(tk.END, "Item 1")
listbox.insert(tk.END, "Item 2")
listbox.insert(tk.END, "Item 3")

# Associa o evento de duplo clique
listbox.bind("<Double-1>", item_duplo_clique)

root.mainloop()
