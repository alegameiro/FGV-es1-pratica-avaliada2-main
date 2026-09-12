# Questão 1: Engenharia de Requisitos — Sistema BiblioTech

## 1. Requisitos Funcionais (RF)

| ID | Descrição | Prioridade |
|----|-----------|------------|
| RF01 | O sistema deve permitir que o bibliotecário cadastre livros no acervo, informando título, autor, ISBN, categoria e quantidade de exemplares. | Alta |
| RF02 | O sistema deve permitir o cadastro de leitores, coletando nome, CPF, e-mail e telefone. | Alta |
| RF03 | O sistema deve permitir ao bibliotecário registrar empréstimos de livros para leitores cadastrados, definindo a data do empréstimo e a data prevista de devolução. | Alta |
| RF04 | O sistema deve permitir que leitores façam a reserva de um livro quando todos os exemplares do acervo estiverem emprestados. | Média |
| RF05 | O sistema deve notificar automaticamente por e-mail o primeiro leitor da fila de reservas assim que o exemplar for devolvido. | Média |
| RF06 | O sistema deve permitir a renovação do prazo de empréstimo de um livro para o leitor, desde que o livro não possua reservas ativas. | Média |
| RF07 | O sistema deve calcular e aplicar multas por atraso caso a devolução do livro ocorra após a data prevista. | Alta |
| RF08 | O sistema deve registrar a devolução de livros emprestados e atualizar o saldo de exemplares disponíveis no acervo. | Alta |
| RF09 | O sistema deve permitir a consulta e busca de livros no acervo por título, autor, ISBN ou categoria. | Média |
| RF10 | O sistema deve exibir o histórico de empréstimos, devoluções, reservas ativas e multas pendentes de cada leitor. | Média |

---

## 2. Requisitos Não-Funcionais (RNF)

| ID | Categoria | Descrição | Métrica |
|----|-----------|-----------|---------|
| RNF01 | Segurança | O sistema deve proteger os dados pessoais dos leitores (CPF, e-mail, telefone) e autenticar bibliotecários de forma segura. | Senhas armazenadas via hash SHA-256 e conformidade integral com as diretrizes da LGPD. |
| RNF02 | Desempenho | O sistema deve processar consultas de acervo e registros de empréstimos com baixo tempo de resposta sob carga diária. | 95% das operações de consulta e registro concluídas em tempo inferior a 1,5 segundo. |
| RNF03 | Usabilidade | A interface do sistema deve ser intuitiva, permitindo que bibliotecários e leitores realizem operações básicas sem complexidade. | Um bibliotecário deve conseguir registrar um empréstimo em menos de 3 cliques e após no máximo 20 minutos de treinamento. |
| RNF04 | Disponibilidade | O sistema deve manter alta taxa de operação para consultas e reservas online pelos leitores. | Disponibilidade de pelo menos 99,5% durante o horário de funcionamento e atendimento das bibliotecas. |
| RNF05 | Manutenibilidade | O código-fonte do backend deve seguir boas práticas de arquitetura e design limpo. | Cobertura de testes unitários mínima de 80% e aderência aos princípios SOLID. |

---

## 3. Regras de Negócio (RN)

| ID | Descrição |
|----|-----------|
| RN01 | O prazo padrão estipulado para a devolução de qualquer empréstimo é de exatamente 14 dias corridos a partir da data de retirada. |
| RN02 | A multa cobrada por atraso na devolução de um livro é de R$ 2,00 por dia de atraso decorrido. |
| RN03 | A renovação de um empréstimo só é permitida se não houver nenhuma reserva ativa registrada na fila para o mesmo livro. |
| RN04 | A reserva de um livro é permitida exclusivamente quando todos os exemplares cadastrados do livro estiverem ocupados (emprestados). |
| RN05 | Quando um livro com reservas ativas é devolvido, o direito de empréstimo do exemplar é atribuído estritamente ao primeiro leitor da fila de reservas (fila FIFO — *First In, First Out*). |

---

## 4. User Stories (Histórias de Usuário)

### US01 — Cadastrar Livro no Acervo
**Como** bibliotecário,  
**Quero** cadastrar novos livros e seus exemplares no acervo,  
**Para** disponibilizá-los para empréstimo aos leitores da biblioteca comunitária.

**Critérios de Aceitação:**
- [ ] O sistema deve validar e exigir os campos obrigatórios: Título, Autor, ISBN, Categoria e Quantidade de Exemplares.
- [ ] O sistema não deve permitir o cadastro de dois livros com o mesmo ISBN.
- [ ] A quantidade inicial de exemplares disponíveis deve ser igual à quantidade total informada no cadastro.

**Story Points:** 3

---

### US02 — Realizar Empréstimo de Livro
**Como** bibliotecário,  
**Quero** registrar o empréstimo de um livro disponível para um leitor cadastrado,  
**Para** controlar a saída de exemplares do acervo e definir a data de retorno.

**Critérios de Aceitação:**
- [ ] O leitor e o livro devem existir previamente no cadastro do sistema.
- [ ] O sistema deve calcular automaticamente a data de devolução prevista para 14 dias corridos após a data do empréstimo (RN01).
- [ ] O sistema deve decrementar a quantidade de exemplares disponíveis no acervo e impedir o empréstimo se a quantidade for zero.

**Story Points:** 5

---

### US03 — Reservar Livro Indisponível
**Como** leitor,  
**Quero** solicitar a reserva de um livro cujos exemplares estejam todos emprestados,  
**Para** garantir minha posição na fila de espera para leitura do livro.

**Critérios de Aceitação:**
- [ ] A reserva só deve ser permitida se todos os exemplares do livro estiverem emprestados (RN04).
- [ ] O sistema deve registrar o leitor no final da fila de reservas do livro respeitando a ordem cronológica.
- [ ] O sistema deve permitir que o leitor consulte a sua posição na fila de reservas.

**Story Points:** 5

---

### US04 — Renovar Empréstimo de Livro
**Como** leitor,  
**Quero** solicitar a renovação do meu empréstimo ativo,  
**Para** estender o prazo de leitura por mais 14 dias sem precisar ir à biblioteca.

**Critérios de Aceitação:**
- [ ] O sistema deve verificar se o livro possui reservas ativas; se houver reserva, a renovação deve ser negada (RN03).
- [ ] Em caso de sucesso, a nova data de devolução deve ser estendida para +14 dias a partir da data da renovação.
- [ ] O sistema deve negar a renovação se o empréstimo já estiver em atraso com multa pendente.

**Story Points:** 3

---

### US05 — Processar Devolução e Calcular Multa
**Como** bibliotecário,  
**Quero** registrar a devolução de um livro e verificar eventuais atrasos,  
**Para** atualizar o acervo e cobrar a multa devida pelo leitor quando aplicável.

**Critérios de Aceitação:**
- [ ] O sistema deve comparar a data atual com a data prevista de devolução.
- [ ] Se a devolução for em atraso, o sistema deve calcular o valor da multa multiplicando R$ 2,00 pelo número de dias de atraso (RN02).
- [ ] O status do exemplar devolvido deve mudar para "Disponível" e o estoque do acervo deve ser incrementado em 1 unidade.

**Story Points:** 5

---

### US06 — Notificar Leitor sobre Reserva Disponível
**Como** sistema / bibliotecário,  
**Quero** notificar por e-mail o primeiro leitor da fila de reserva assim que um livro for devolvido,  
**Para** que ele saiba que o exemplar está disponível para retirada na biblioteca.

**Critérios de Aceitação:**
- [ ] Ao concluir a devolução de um livro com reservas ativas, o sistema deve identificar o primeiro leitor da fila (RN05).
- [ ] Um e-mail de notificação deve ser gerado e enviado contendo o nome do leitor, título do livro e prazo para retirada.
- [ ] A reserva deve mudar de status para "Aguardando Retirada".

**Story Points:** 3
