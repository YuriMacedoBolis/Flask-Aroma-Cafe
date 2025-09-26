# Aroma & Café: Sistema de Gestão de Estoque e E-commerce

## ☕ Sobre o Projeto

O Aroma & Café é uma aplicação web completa desenvolvida com **Python** e o framework **Flask**. O projeto simula uma cafeteria, oferecendo um sistema de gestão de estoque para a equipe interna e uma vitrine de e-commerce para os clientes.

O objetivo principal foi construir uma aplicação funcional que demonstrasse o ciclo completo de desenvolvimento, desde a modelagem do banco de dados até a implementação de funcionalidades de front-end e autenticação segura.

##  Funcionalidades

- **Autenticação de Usuário:** Sistema de login, registro e logout com senhas seguras (hashing com **Flask-Bcrypt**).
- **Controle de Acesso:** Rotas exclusivas para funcionários (`@funcionario_required`) para gerenciar o estoque.
- **Gestão de Estoque (CRUD):**
    - **Visualizar:** Tabela dinâmica de produtos.
    - **Adicionar:** Formulário para cadastrar novos itens.
    - **Editar:** Formulário para atualizar dados de produtos existentes.
    - **Excluir:** Funcionalidade para remover produtos do banco de dados.
- **Simulação de E-commerce:**
    - **Cardápio:** Página pública que exibe os produtos em formato de cartão.
    - **Carrinho de Compras:** Sistema de sessão para adicionar e remover itens.
    - **Histórico de Pedidos:** Página para usuários visualizarem suas compras passadas.

##  Como Rodar o Projeto

Siga os passos abaixo para configurar e rodar a aplicação em sua máquina.

### **Pré-requisitos**

Certifique-se de ter o **Python 3.8+** e o **Git** instalados.

### **Instalação**

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/YuriMacedoBolis/Flask-Aroma-Cafe.git](https://github.com/YuriMacedoBolis/Flask-Aroma-Cafe.git)
    cd Flask-Aroma-Cafe
    ```

2.  **Crie e ative o ambiente virtual:**
    ```bash
    # Windows
    python -m venv venv
    venv\Scripts\activate

    # macOS / Linux
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Crie o arquivo de ambiente (.env):**
    Na raiz do projeto, crie um arquivo chamado `.env` com as seguintes variáveis:
    ```
    DATABASE_URI = 'sqlite:///instance/aroma.db'
    SECRET_KEY = 'sua-chave-secreta-forte-aqui'
    ```
    (Você pode gerar uma chave secreta Python aleatória usando `os.urandom(24)`.)

### **Configuração do Banco de Dados**

Para criar as tabelas e popular o banco de dados, execute os comandos abaixo na ordem:

1.  **Inicialize as migrações:**
    ```bash
    flask db init
    ```
2.  **Crie as tabelas:**
    ```bash
    flask db migrate -m "Criação de tabelas iniciais"
    ```
3.  **Aplique a migração:**
    ```bash
    flask db upgrade
    ```

4.  **Crie um usuário funcionário:**
    Para ter acesso ao painel de estoque, crie um usuário admin executando o script `crie_funcionario.py`
    ```bash
    python crie_funcionario.py
    ```
    (A senha padrão está definida no próprio script, então você precisará alterá-la se quiser uma diferente.)

### **Rodando a Aplicação**

Execute o comando abaixo para iniciar o servidor web do Flask:
```bash
python run.py
