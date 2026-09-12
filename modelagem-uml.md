# Questão 2: Modelagem UML — Sistema BiblioTech

---

## a) Diagrama de Classes

O Diagrama de Classes abaixo representa a estrutura estática do sistema BiblioTech, mapeando as entidades de domínio, seus atributos, métodos e os relacionamentos com multiplicidade.

```mermaid
classDiagram
    class Livro {
        -String titulo
        -String autor
        -String isbn
        -String categoria
        -int qtdExemplaresDisponiveis
        +cadastrarLivro() bool
        +buscarPorIsbn(String isbn) Livro
        +verificarDisponibilidade() bool
    }

    class Exemplar {
        -int idExemplar
        -int numeroTombo
        -String status
        +emprestar() void
        +devolver() void
    }

    class Leitor {
        -int idLeitor
        -String nome
        -String cpf
        -String email
        -double debitoMulta
        +cadastrarLeitor() bool
        +consultarHistorico() List
        +verificarSituacao() bool
    }

    class Emprestimo {
        -int idEmprestimo
        -Date dataEmprestimo
        -Date dataDevolucaoPrevista
        -Date dataDevolucaoReal
        -String status
        +registrarEmprestimo() bool
        +renovarEmprestimo() bool
        +finalizarEmprestimo() void
    }

    class Reserva {
        -int idReserva
        -Date dataReserva
        -int posicaoFila
        -String status
        +solicitarReserva() bool
        +notificarDisponibilidade() void
    }

    class Bibliotecario {
        -int idBibliotecario
        -String nome
        -String matricula
        +registrarEmprestimo() void
        +processarDevolucao() void
    }

    class Multa {
        -int idMulta
        -double valor
        -Date dataGeracao
        -boolean paga
        +calcularValor(int diasAtraso) double
        +quitarMulta() void
    }

    Livro "1" --> "*" Exemplar : possui
    Leitor "1" --> "*" Emprestimo : realiza
    Exemplar "1" --> "*" Emprestimo : objeto_de
    Leitor "1" --> "*" Reserva : solicita
    Livro "1" --> "*" Reserva : possui_fila
    Emprestimo "1" --> "0..1" Multa : gera
    Bibliotecario "1" --> "*" Emprestimo : gerencia
```

---

## b) Diagrama de Sequência: Cenário "Realizar Empréstimo de um Livro"

O Diagrama de Sequência abaixo ilustra o aspecto dinâmico da aplicação durante a execução do caso de uso de registro de empréstimo, demonstrando a verificação da situação do leitor, a checagem do acervo e a criação do registro de empréstimo.

```mermaid
sequenceDiagram
    autonumber
    actor B as Bibliotecario
    participant S as Sistema
    participant U as Leitor
    participant L as Livro
    participant E as Emprestimo

    B->>S: solicitarEmprestimo(idLeitor, isbn)
    activate S

    S->>U: verificarSituacao(idLeitor)
    activate U
    U-->>S: leitorRegular (sem multas/atrasos)
    deactivate U

    S->>L: verificarDisponibilidade(isbn)
    activate L
    L-->>S: exemplarDisponivel (qtdExemplares > 0)
    deactivate L

    alt Leitor Regular e Livro Disponível
        S->>L: decrementarEstoque()
        activate L
        L-->>S: estoqueAtualizado
        deactivate L

        S->>E: criarEmprestimo(idLeitor, idExemplar, dataPrevista)
        activate E
        E-->>S: novoEmprestimoRegistrado
        deactivate E

        S-->>B: Empréstimo realizado com sucesso!
    else Leitor Irregular ou Livro Indisponível
        S-->>B: Empréstimo Negado (motivo informado)
    end
    deactivate S
```

---

## c) Diagrama de Atividades: Cenário "Devolver Livro e Processar Reservas"

O Diagrama de Atividades abaixo especifica o fluxo de controle para o processo de devolução de um livro, englobando a apuração de multas por atraso, a checagem da fila de reservas e a notificação do próximo leitor.

```mermaid
flowchart TD
    Start([Início: Leitor entrega o exemplar]) --> RegDev[Registrar data e hora da devolução]
    RegDev --> CheckAtraso{Devolução em atraso?}

    CheckAtraso -- Sim --> CalcMulta[Calcular multa: R\$ 2,00 por dia de atraso]
    CalcMulta --> RegMulta[Registrar multa pendente no perfil do leitor]
    RegMulta --> CheckReserva

    CheckAtraso -- Não --> CheckReserva{Existem reservas ativas para o livro?}

    CheckReserva -- Sim --> GetPrimeiro[Identificar 1º leitor da fila de reserva - FIFO]
    GetPrimeiro --> NotifLeitor[Enviar e-mail de notificação de disponibilidade]
    NotifLeitor --> UpdateReserva[Atualizar status da reserva para 'Aguardando Retirada']
    UpdateReserva --> EndReserva([Fim: Exemplar reservado e leitor notificado])

    CheckReserva -- Não --> IncEstoque[Incrementar exemplares disponíveis no acervo]
    IncEstoque --> EndNormal([Fim: Exemplar devolvido ao acervo disponível])
```