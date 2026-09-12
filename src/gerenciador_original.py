import sqlite3
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Tuple


# ============================================================================
# 1. ABSTRAÇÕES DE PERSISTÊNCIA (DIP - Dependency Inversion Principle)
# ============================================================================

class IRepositorio(ABC):
    """Interface abstrata para operações de persistência de dados."""
    
    @abstractmethod
    def buscar(self, id_chave: str):
        pass
    
    @abstractmethod
    def salvar(self, entidade) -> bool:
        pass


# ============================================================================
# 2. REPOSITÓRIOS ESPECÍFICOS (SRP - Single Responsibility Principle)
# ============================================================================

class RepositorioLivro(IRepositorio):
    """Responsável exclusivamente por operações com livros no banco de dados SQLite."""
    
    def __init__(self, db_path: str = "biblioteca.db"):
        self.db_path = db_path

    def buscar(self, isbn: str) -> Optional[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT isbn, titulo, autor, categoria, exemplares_disponiveis FROM livros WHERE isbn = ?", (isbn,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "isbn": row,
                "titulo": row,
                "autor": row,
                "categoria": row,
                "exemplares_disponiveis": row
            }
        return None

    def salvar(self, livro: Dict) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE livros SET exemplares_disponiveis = ? WHERE isbn = ?",
            (livro["exemplares_disponiveis"], livro["isbn"])
        )
        conn.commit()
        conn.close()
        return True


class RepositorioLeitor(IRepositorio):
    """Responsável exclusivamente por operações com leitores no banco de dados SQLite."""
    
    def __init__(self, db_path: str = "biblioteca.db"):
        self.db_path = db_path

    def buscar(self, cpf: str) -> Optional[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT cpf, nome, email, telefone FROM leitores WHERE cpf = ?", (cpf,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "cpf": row,
                "nome": row,
                "email": row,
                "telefone": row
            }
        return None

    def salvar(self, leitor: Dict) -> bool:
        # Método para atualização de cadastros de leitores
        return True


class RepositorioEmprestimo(IRepositorio):
    """Responsável exclusivamente por operações com empréstimos e multas no banco SQLite."""
    
    def __init__(self, db_path: str = "biblioteca.db"):
        self.db_path = db_path

    def buscar(self, id_emprestimo: int) -> Optional[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, livro_isbn, leitor_cpf, data_emprestimo, data_devolucao_prevista, data_devolucao "
            "FROM emprestimos WHERE id = ?", (id_emprestimo,)
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return {
                "id": row,
                "livro_isbn": row,
                "leitor_cpf": row,
                "data_emprestimo": row,
                "data_devolucao_prevista": row,
                "data_devolucao": row
            }
        return None

    def salvar(self, emprestimo: Dict) -> bool:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO emprestimos (livro_isbn, leitor_cpf, data_emprestimo, data_devolucao_prevista) "
            "VALUES (?, ?, ?, ?)",
            (
                emprestimo["livro_isbn"],
                emprestimo["leitor_cpf"],
                emprestimo["data_emprestimo"],
                emprestimo["data_devolucao_prevista"]
            )
        )
        conn.commit()
        conn.close()
        return True


# ============================================================================
# 3. SERVIÇOS ESPECIALIZADOS (SRP e OCP)
# ============================================================================

class ServicoNotificacao:
    """Responsável isoladamente pelo envio de notificações aos usuários."""
    
    def enviar_email(self, destinatario: str, assunto: str, mensagem: str) -> bool:
        print(f"[E-mail para {destinatario}] {assunto}: {mensagem}")
        return True

    def enviar_sms(self, telefone: str, mensagem: str) -> bool:
        print(f"[SMS para {telefone}] {mensagem}")
        return True


class ServicoRelatorio:
    """Responsável isoladamente pela geração e formatação de relatórios."""
    
    def gerar_comprovante_emprestimo(self, livro: Dict, leitor: Dict, data_devolucao: str) -> str:
        return (
            f"=== COMPROVANTE DE EMPRÉSTIMO — BIBLIOTECH ===\n"
            f"Leitor: {leitor['nome']} (CPF: {leitor['cpf']})\n"
            f"Livro: {livro['titulo']} (ISBN: {livro['isbn']})\n"
            f"Data Prevista para Devolução: {data_devolucao}\n"
            f"================================================"
        )


class CalculadoraMulta:
    """Responsável isoladamente pela lógica de cálculo de multas por atraso."""
    
    VALOR_DIARIA: float = 2.00

    def calcular(self, data_prevista_str: str, data_real_str: str) -> float:
        formato = "%Y-%m-%d"
        data_prevista = datetime.strptime(data_prevista_str, formato)
        data_real = datetime.strptime(data_real_str, formato)
        
        if data_real > data_prevista:
            dias_atraso = (data_real - data_prevista).days
            return dias_atraso * self.VALOR_DIARIA
        return 0.0


# ============================================================================
# 4. GERENCIADOR PRINCIPAL (Orquestrador com Injeção de Dependências)
# ============================================================================

class GerenciadorEmprestimo:
    """Orquestra o fluxo de empréstimo desacoplado, recebendo serviços via construtor (DIP)."""
    
    def __init__(
        self, 
        repo_livro: RepositorioLivro,
        repo_leitor: RepositorioLeitor,
        repo_emprestimo: RepositorioEmprestimo,
        servico_notificacao: ServicoNotificacao,
        servico_relatorio: ServicoRelatorio,
        calculadora_multa: CalculadoraMulta
    ):
        self.repo_livro = repo_livro
        self.repo_leitor = repo_leitor
        self.repo_emprestimo = repo_emprestimo
        self.servico_notificacao = servico_notificacao
        self.servico_relatorio = servico_relatorio
        self.calculadora_multa = calculadora_multa

    def realizar_emprestimo(self, livro_isbn: str, leitor_cpf: str) -> Tuple[bool, str]:
        """Realiza a validação de regras de negócio e efetiva o empréstimo."""
        # 1. Validar leitor
        leitor = self.repo_leitor.buscar(leitor_cpf)
        if not leitor:
            return False, "Erro: Leitor não encontrado no cadastro."

        # 2. Validar e verificar disponibilidade do livro
        livro = self.repo_livro.buscar(livro_isbn)
        if not livro:
            return False, "Erro: Livro não encontrado no acervo."

        if livro["exemplares_disponiveis"] <= 0:
            return False, "Erro: Não há exemplares disponíveis para empréstimo."

        # 3. Calcular datas (Regra de Negócio: 14 dias de prazo)
        hoje = datetime.now()
        data_emprestimo_str = hoje.strftime("%Y-%m-%d")
        data_devolucao_str = (hoje + timedelta(days=14)).strftime("%Y-%m-%d")

        # 4. Registrar Empréstimo e Atualizar Estoque do Livro
        novo_emprestimo = {
            "livro_isbn": livro_isbn,
            "leitor_cpf": leitor_cpf,
            "data_emprestimo": data_emprestimo_str,
            "data_devolucao_prevista": data_devolucao_str
        }
        self.repo_emprestimo.salvar(novo_emprestimo)

        livro["exemplares_disponiveis"] -= 1
        self.repo_livro.salvar(livro)

        # 5. Notificar Leitor e Gerar Comprovante
        self.servico_notificacao.enviar_email(
            destinatario=leitor["email"],
            assunto="Empréstimo Confirmado - BiblioTech",
            mensagem=f"Seu empréstimo do livro '{livro['titulo']}' foi realizado. Devolução até {data_devolucao_str}."
        )

        comprovante = self.servico_relatorio.gerar_comprovante_emprestimo(
            livro=livro, leitor=leitor, data_devolucao=data_devolucao_str
        )

        return True, comprovante
    