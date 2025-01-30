<h1>Armafa</h1>

<p>Um projeto no padrão MVC(model-view-controler) com 2KLOC feito exclusivamnete para windows que me foi requisitado pela empresa Armafa 
para armazenar e gerir seus produtos, clientes e pedidos com funcionalidades como criar PDFs.</p>
<hr>

<h2>Tecnologias 🛠</h2>
<ul>
    <li>Python 3.12</li>
    <li>Tkinter (GUI)</li>
    <li>SQLite3 (Banco de Dados)</li>
    <li>ReportLab (Geração de PDFs)</li>
</ul>
<hr>

<h2>Funcionalidades 📌</h2>
<p>Em Geral Armafa é um CRUD de Cliente, Produtos e Pedidos, no qual essas informações são armazenadas
em classes Repoditory(Singleton) no Padrão MVC(model-view-controler) que preza por uma separação clara entre
a logica de negocio e a GUI(Graphical-User-Interface) da aplicação por meio de controlers que serve como ponte 
entre eles.</p>
<hr>

<h2>Como Rodar 🚀 </h2>
```shell
# Clone o Repositorio
git clone https://github.com/Eurico149/Armafa
cd Armafa

# Instale as Dependencias
pip install -r requirementes.txt

# Inicie o main
python3 main.py
```
<h2>Criar Executavel 🔧</h2>
```shell
pyinstaller --name "Armafa" --windowed --icon="./src/data/afghanistan.ico" --add-data "src/data;src/data" main.py
```
<hr>

<h2>Estrutura 📁</h2>
```
Armafa/
├─── src/
│   ├─── controller/
│   ├─── data/
│   ├─── model/
│   └─── view/
├── main.py
├── .gitignore
├── README.md
├── Armafa
└── requirementes.txt
```
<hr>

<h2>Licença 📝</h2>
Este projeto está licenciado sob [MIT License](LICENSE)
