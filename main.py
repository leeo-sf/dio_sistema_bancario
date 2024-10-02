from datetime import datetime
from abc import ABC, abstractproperty


def menu():
    template = """\n
==========================MENU==========================

[d] Depositar
[s] Sacar
[e] Extrato
[nu] Novo usuário
[nc] Nova conta
[q] Sair


=> """
    return input(template).lower()


def depositar(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtra_usuario(cpf, clientes)

    if not cliente:
        print("\n \t Cliente não encontrado")
        return
    
    valor = float(input("Informe o valor do deposito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)


def sacar(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtra_usuario(cpf, clientes)

    if not cliente:
        print("\n \t Cliente não encontrado")
        return
    
    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    cliente.realizar_transacao(conta, transacao)


def exibir_extrato(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtra_usuario(cpf, clientes)

    if not cliente:
        print("\n \t Cliente não encontrado")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n====================EXTRATO====================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foi realizada nenhuma movimentção."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"
    
    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtra_usuario(cpf, clientes)

    if cliente:
        print("\n \tJá existe cliente com esse CPF!")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe e data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)

    print("==== \nCliente criado com sucesso =)")


def filtra_usuario(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None


def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n \tCliente não possui conta!")
        return
    
    return cliente.contas[0]


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(self, cliente, numero):
        return self(numero, cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    def sacar(self, valor):
        saldo = self.saldo

        if (valor > saldo):
            print("Não é possível sacar o dinheiro por falta de saldo.")
            return False

        self._saldo -= valor
        print(f"Saque efetuado com sucesso. \n \n \t R$ {valor:.2f}")
        return True
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"Seu deposito foi feito com sucesso. \n \n \t R$ {valor:.2f}")
        else:
            print("Informe um valor válido!")


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saque=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saque = limite_saque

    def sacar(self, valor):
        numero_saque = len(
            [transacao for transacao in self.historico.transacao if transacao["tipo"] == Saque.__name__]
        )

        if valor > self.limite:
            print(f"Seu limite de saque é de R$ {self.limite:.2f}")
            return False
        
        elif numero_saque >= self.limite_saque:
            print("Você excedeu o seu limite de saque diário.")
            return False
        
        else:
            return super().sacar(valor)


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractproperty
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor
    
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF (somente números): ")
    cliente = filtra_usuario(cpf, clientes)

    if not cliente:
        print("\n \t Cliente não encontrado")
        return
    
    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)
    cliente.contas.append(conta)

    print("Conta criada com sucesso!!")



def main():
    clientes = []
    contas = []
    
    while True:
        opcao = menu()

        if opcao == "d":
            depositar(clientes)

        elif opcao == "s":
            sacar(clientes)

        elif opcao == "e":
            exibir_extrato(clientes)

        elif opcao == "nu":
            criar_cliente(clientes)
        
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)

        elif opcao == "q":
            print("Até mais!!")
            break

        else:
            print("Opção inválida, por favor selecione novamente a operação desejada.")


main()