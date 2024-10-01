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


def depositar(saldo, extrato, valor):
    saldo += valor
    operacao = {"Operacao": "Deposito".center(10), "Valor": valor}
    extrato.append(operacao)
    print(f"Seu deposito foi feito com sucesso. \n \n \t R$ {valor:.2f}")
    return saldo, extrato


def sacar(*, valor, saldo, extrato, limite_saque_diario, numero_saque, limite_saque):
    if (valor > saldo):
        print("Não é possível sacar o dinheiro por falta de saldo.")
        return saldo, extrato

    if (numero_saque >= limite_saque_diario):
        print("Você excedeu o seu limite de saque diário.")
        return saldo, extrato

    if (valor > limite_saque):
        print(f"Seu limite de saque é de R$ {limite_saque:.2f}")
        return saldo, extrato

    saldo -= valor
    numero_saque += 1
    operacao = {"Operacao": "Saque".center(10), "Valor": valor}
    extrato.append(operacao)
    print(f"Saque efetuado com sucesso. \n \n \t R$ {valor:.2f}")
    return saldo, extrato


def obter_extrato(saldo, /, *, extrato):
    print("\t Extrato")

    if (extrato):
        for operacao in extrato:
            print(f"""
            Operação {operacao['Operacao'].upper()} ======================> Valor R$ {operacao['Valor']:.2f}
            """)
        
        print(f"\t Saldo R$ {saldo:.2f}")
    else:
        print("\n \t Você não realizou nenhuma operação em sua conta")


def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtra_usuario(cpf, usuarios)

    if usuario:
        print("\n \t Já existe um usuário com esse CPF!")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})

    print("\n \t Usuário criado com sucesso")


def filtra_usuario(cpf, usuarios):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None


def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtra_usuario(cpf, usuarios)

    if usuario:
        print("\n \t Conta criada com sucesso!")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\n \t Usuário não encontrado! Verifique os dados informados.")



def main():
    saldo = 0
    limite = 500
    extrato = []
    usuarios = []
    contas = []
    numero_saque = 0
    LIMITE_SAQUE = 3
    AGENCIA = "0001"
    
    while True:
        opcao = menu()

        if opcao == "d":
            valor = int(input("Insira o valor a ser depositado: "))

            if (valor > 0):
                saldo, extrato = depositar(saldo, extrato, valor)
            
            else:
                print("Informe um valor válido!")

        elif opcao == "s":
            valor = int(input("Insira o valor a ser depositado: "))
            
            if (valor > 0):
                saldo, extrato = sacar(valor=valor, saldo=saldo, extrato=extrato, 
                                       limite_saque_diario=LIMITE_SAQUE, numero_saque=numero_saque, 
                                       limite_saque=limite)
                
            else:
                print("Entre com um valor válido!")

        elif opcao == "e":
            obter_extrato(saldo, extrato=extrato)    

        elif opcao == "nu":
            criar_usuario(usuarios)
        
        elif opcao == "nc":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        elif opcao == "q":
            print("Até mais!!")
            break

        else:
            print("Opção inválida, por favor selecione novamente a operação desejada.")


main()