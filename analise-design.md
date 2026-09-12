# Questão 3: Análise de Design e Princípios SOLID — Sistema BiblioTech

---

## 1. Identificação das Violações dos Princípios SOLID

Ao analisar o código legado no arquivo `src/gerenciador_original.py`, constata-se que a classe `GerenciadorEmprestimoOriginal` opera como uma *God Class* (classe onipotente), acumulando responsabilidades heterogêneas e violando três princípios centrais do SOLID:

### a) Single Responsibility Principle (SRP) — Princípio da Responsabilidade Única
* **Violação:** A classe possui múltiplas razões independentes para mudar. Ela é responsável por:
  1. Conectar e executar comandos SQL diretos no banco de dados SQLite (`biblioteca.db`).
  2. Executar regras de negócio do empréstimo (verificar disponibilidade de livros e situação de leitores).
  3. Calcular valores de multas por atraso.
  4. Formatar e gerar relatórios em texto.
  5. Enviar notificações de e-mail e SMS aos leitores.
* **Impacto:** Alterações na tecnologia de banco de dados, no formato de envio de notificações ou na fórmula de multas forçam a modificação de uma mesma e única classe.

### b) Open/Closed Principle (OCP) — Princípio Aberto/Fechado
* **Violação:** A classe está fechada para extensões e aberta para modificações. Se a BiblioTech precisar adicionar uma nova forma de notificação (ex: WhatsApp) ou mudar a estratégia de cálculo de multas (ex: valor fixo por categoria), é necessário editar diretamente o código fonte do gerenciador.
* **Impacto:** Alto risco de introduzir regressões e *bugs* em funcionalidades de negócio que já estavam funcionando perfeitamente.

### c) Dependency Inversion Principle (DIP) — Princípio da Inversão de Dependências
* **Violação:** A classe de alto nível de negócio (`GerenciadorEmprestimoOriginal`) depende diretamente de detalhes de implementação de baixo nível (`sqlite3.connect('biblioteca.db')`).
* **Impacto:** Torna impossível realizar testes unitários isolados em memória (mocar o banco de dados) e impede a substituição da ferramenta de persistência por outro SGBD sem reescrever toda a classe de negócio.

---

## 2. Análise de Coesão e Acoplamento

* **Baixa Coesão:** A classe possui um baixo nível de coesão porque seus métodos e atributos não trabalham para um único propósito bem definido. Ela mistura persistência, regras de negócio, apresentação de relatórios e infraestrutura de comunicação.
* **Alto Acoplamento (Acoplamento Problemático):** Existe um acoplamento forte e concreto entre a regra de negócio e os comandos SQL (`INSERT`, `UPDATE`, `SELECT`) hardcoded no meio dos métodos de aplicação. Qualquer alteração no nome de uma coluna da tabela do banco de dados quebra diretamente a execução do fluxo de empréstimo.

---

## 3. Plano de Refatoração Proposto

Para corrigir estes problemas e atingir um design limpo e sustentável:
1. **Aplicar o SRP (Camada de Repositórios):** Isolar os comandos SQL em classes de repositório especializadas (`RepositorioLivro`, `RepositorioLeitor`, `RepositorioEmprestimo`) derivadas de uma interface abstrata `IRepositorio`.
2. **Aplicar o SRP (Camada de Serviços):** Extrair a lógica de envio de mensagens para `ServicoNotificacao`, a geração de relatórios para `ServicoRelatorio` e a regra de cobrança para `CalculadoraMulta`.
3. **Aplicar o DIP (Injeção de Dependências):** Injetar todos os repositórios e serviços através do método construtor `__init__` da classe `GerenciadorEmprestimo`, garantindo baixo acoplamento e alta testabilidade.
