# Sistema de Gerenciamento e Emissão de Certificados API

Este projeto consiste no desenvolvimento de um sistema completo para gerenciamento e emissão de certificados de cursos de extensão. A aplicação permite o cadastro de cursos, alunos, e emissões de certificados, bem como a geração do certificado em PDF, com validação de autenticidade por código único. O projeto integra conhecimentos da disciplina de Desenvolvimento Frontend e serve como avaliação para a mesma.

## Funcionalidades Principais

* **Autenticação de Usuário:** Cadastro (via `flask shell`) e login seguro para administradores do sistema.
* **Gerenciamento de Cursos:** CRUD (Criar, Ler, Atualizar, Deletar) completo para cursos de extensão.
    * Atributos do curso: Nome, carga horária, descrição, data de realização.
* **Gerenciamento de Alunos:** CRUD completo para alunos.
    * Atributos do aluno: Nome completo, e-mail, CPF.
* **Emissão de Certificados:**
    * Associação de alunos a cursos para registrar a conclusão.
    * Geração de certificados em formato PDF contendo dados do aluno, curso, carga horária, data de emissão e um código único de validação.
* **Validação de Certificados:** Endpoint público para verificar a autenticidade de um certificado através do seu código único.
* **Dashboard Administrativo (API):** Endpoint para fornecer métricas como número de certificados emitidos, alunos cadastrados e cursos ativos.

## Tecnologias Utilizadas

* **Linguagem:** Python 3.13+
* **Framework Backend:** Flask
* **Banco de Dados:** SQLite (para desenvolvimento e implantação no PythonAnywhere)
* **ORM:** Flask-SQLAlchemy
* **Geração de PDF:** FPDF2
* **Autenticação:** Sessões Flask
* **CORS:** Flask-CORS para permitir requisições do frontend
* **Variáveis de Ambiente:** python-dotenv
* **Servidor WSGI (para produção):** Gunicorn (recomendado, PythonAnywhere usa seu próprio)

## Configuração e Instalação (Desenvolvimento Local)

Siga os passos abaixo para configurar o ambiente de desenvolvimento local.

### Pré-requisitos

* Python 3.13 ou superior instalado.
* `pip` (gerenciador de pacotes Python).
* Git (para clonar o repositório).

### Passos

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/desatinar/back-sistema-emissao-certificado.git
    cd back-sistema-emissao-certificado
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    # No Windows
    venv\Scripts\activate
    # No macOS/Linux
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    * Crie um arquivo chamado `.env` na raiz do projeto.
    * Adicione as seguintes variáveis (substitua pelos seus valores):
        ```env
        SECRET_KEY='chave_secreta'
        DATABASE_URL='sqlite:///site.db'
        ```

5.  **Execute a aplicação localmente:**
    ```bash
    python run.py
    ```
    A API estará disponível em `http://127.0.0.1:5000`.

6.  **Crie um usuário administrador inicial (via Flask Shell):**
    * Com o ambiente virtual ativo e na pasta do projeto, execute:
        ```bash
        flask shell
        ```
    * No shell do Flask, execute o seguinte script Python:
        ```python
        from app import db
        from app.models.user import User # Ou o caminho correto para seu modelo User

        admin_email = 'admin@email.com'
        admin_password = 'suaSenha'

        existing_user = User.query.filter_by(email=admin_email).first()
        if not existing_user:
            new_admin = User(email=admin_email)
            new_admin.set_password(admin_password)
            db.session.add(new_admin)
            db.session.commit()
            print(f"Usuário '{admin_email}' criado com sucesso!")
        else:
            print(f"Usuário '{admin_email}' já existe.")
        exit()
        ```

## Implantação (PythonAnywhere)

Esta API foi configurada e testada para implantação na plataforma PythonAnywhere utilizando SQLite. Os passos principais para a implantação incluem:

1.  Criar um Web App Flask no PythonAnywhere.
2.  Clonar o repositório para o servidor do PythonAnywhere.
3.  Configurar um ambiente virtual e instalar as dependências do `requirements.txt`.
4.  Ajustar o arquivo WSGI para apontar para a função `create_app` da aplicação.
5.  Configurar as variáveis de ambiente (`SECRET_KEY`, `DATABASE_URL` com caminho absoluto para o SQLite) na aba "Web" do PythonAnywhere ou no arquivo WSGI (se a seção da UI não for encontrada).
6.  Definir o "Working directory".
7.  Recarregar o Web App.
8.  Criar o usuário administrador no servidor via `flask shell` no PythonAnywhere.

A URL da API implantada é: `http://desatinar.pythonanywhere.com`.

## Documentação da API

A seguir, a descrição dos endpoints disponíveis na API.

**Prefixo base para endpoints de admin:** `/api/admin`
**Prefixo base para endpoints de autenticação:** `/api/auth`
**Prefixo base para endpoints públicos:** `/api/public`

---

### Autenticação

#### 1. Login de Administrador
* **Método:** `POST`
* **URL:** `/api/auth/login`
* **Protegido:** Não
* **Corpo da Requisição (JSON):**
    ```json
    {
        "email": "admin_email",
        "password": "admin_password"
    }
    ```
* **Resposta de Sucesso (200 OK):**
    ```json
    {
        "message": "Sucesso!",
        "user": {
            "id": 1,
            "username": "seu_admin_username"
        }
    }
    ```
* **Resposta de Erro (401 Unauthorized):**
    ```json
    {
        "message": "Credenciais inválidas"
    }
    ```

#### 2. Logout de Administrador
* **Método:** `POST`
* **URL:** `/api/auth/logout`
* **Protegido:** Sim (requer estar logado)
* **Corpo da Requisição:** Vazio
* **Resposta de Sucesso (200 OK):**
    ```json
    {
        "message": "Logout"
    }
    ```

#### 3. Status da Sessão
* **Método:** `GET`
* **URL:** `/api/auth/status`
* **Protegido:** Não
* **Resposta de Sucesso (Logado) (200 OK):**
    ```json
    {
        "logged_in": true,
        "admin_id": 1,
        "username": "seu_admin_username"
    }
    ```
* **Resposta de Sucesso (Não Logado) (200 OK):**
    ```json
    {
        "logged_in": false
    }
    ```

---

### Gerenciamento de Cursos (Admin)
*Todos os endpoints abaixo requerem autenticação de administrador.*

#### 1. Criar Novo Curso
* **Método:** `POST`
* **URL:** `/api/admin/courses`
* **Corpo da Requisição (JSON):**
    ```json
    {
        "name": "Nome do Curso",
        "workload": 40, // Carga horária em horas (inteiro)
        "description": "Descrição detalhada do curso.",
        "course_date": "AAAA-MM-DD" // Data de realização ou referência do curso
    }
    ```
* **Resposta de Sucesso (201 Created):** Retorna o objeto do curso criado.

#### 2. Listar Todos os Cursos
* **Método:** `GET`
* **URL:** `/api/admin/courses`
* **Resposta de Sucesso (200 OK):** Retorna uma lista de objetos de curso.

#### 3. Atualizar um Curso Existente
* **Método:** `PUT`
* **URL:** `/api/admin/courses/<int:course_id>`
* **Corpo da Requisição (JSON):** Campos a serem atualizados.
* **Resposta de Sucesso (200 OK):** Retorna o objeto do curso atualizado.

#### 4. Deletar um Curso
* **Método:** `DELETE`
* **URL:** `/api/admin/courses/<int:course_id>`
* **Resposta de Sucesso (200 OK):**
    ```json
    {
        "message": "Curso deletado com sucesso!"
    }
    ```

---

### Gerenciamento de Alunos (Admin)
*Todos os endpoints abaixo requerem autenticação de administrador.*

#### 1. Criar Novo Aluno
* **Método:** `POST`
* **URL:** `/api/admin/students`
* **Corpo da Requisição (JSON):**
    ```json
    {
        "full_name": "Nome Completo do Aluno",
        "email": "aluno@email.com",
        "cpf": "123.456.789-00"
    }
    ```
* **Resposta de Sucesso (201 Created):** Retorna o objeto do aluno criado.

#### 2. Listar Todos os Alunos
* **Método:** `GET`
* **URL:** `/api/admin/students`
* **Resposta de Sucesso (200 OK):** Retorna uma lista de objetos de aluno.

#### 3. Atualizar um Aluno Existente
* **Método:** `PUT`
* **URL:** `/api/admin/students/<int:student_id>`
* **Corpo da Requisição (JSON):** Campos a serem atualizados.
* **Resposta de Sucesso (200 OK):** Retorna o objeto do aluno atualizado.

#### 4. Deletar um Aluno
* **Método:** `DELETE`
* **URL:** `/api/admin/students/<int:student_id>`
* **Resposta de Sucesso (200 OK):**
    ```json
    {
        "message": "Estudante excluído com sucesso!"
    }
    ```

---

### Certificados

#### 1. Emitir Novo Certificado (Admin)
* **Método:** `POST`
* **URL:** `/api/admin/certificates/issue`
* **Protegido:** Sim
* **Corpo da Requisição (JSON):**
    ```json
    {
        "student_id": 1,
        "course_id": 1
    }
    ```
* **Resposta de Sucesso (201 Created):** Objeto do certificado emitido.

#### 2. Download do PDF do Certificado (Público)
* **Método:** `GET`
* **URL:** `/api/public/certificates/download/<string:unique_validation_code>`
* **Protegido:** Não
* **Resposta de Sucesso:** Download do arquivo PDF.

#### 3. Validar Certificado (Público)
* **Método:** `GET`
* **URL:** `/api/public/certificates/validate/<string:unique_validation_code>`
* **Protegido:** Não
* **Resposta de Sucesso (200 OK - Certificado Válido):**
    ```json
    {
        "valid": true,
        "student_name": "Nome do Aluno",
        "course_name": "Nome do Curso",
        "course_workload": 40,
        "issue_date": "AAAA-MM-DD",
        "validation_code": "uuid-do-certificado"
    }
    ```
* **Resposta de Sucesso (404 Not Found - Certificado Inválido):**
    ```json
    {
        "valid": false,
        "message": "Certificado não encontrado"
    }
    ```

---

### Dashboard Administrativo (API)

#### 1. Obter Métricas do Dashboard (Admin)
* **Método:** `GET`
* **URL:** `/api/admin/dashboard/metrics`
* **Protegido:** Sim
* **Resposta de Sucesso (200 OK):**
    ```json
    {
        "certificates_issued": 0,
        "students_registered": 0,
        "courses_active": 0
    }
    ```
    *(Você precisará implementar a lógica para calcular essas métricas).*

---

## Estrutura do Projeto (Visão Geral)

```
/back-sistema-emissao-certificado/
|-- /app/
|   |-- /models/
|   |-- /routes/
|   |-- /services/
|   |-- __init__.py
|-- .env
|-- .gitignore
|-- config.py
|-- run.py
|-- requirements.txt
|-- README.md
```