print("Bem vindo ao seu banco!")

template = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair


=> """
saldo = 0
limite = 500
extrato = []
numero_saque = 0
LIMITE_SAQUE = 3


while True:
    opcao = input(template).lower()

    if opcao == "d":
        valor = int(input("Insira o valor a ser depositado: "))

        if (valor > 0):
            saldo += valor
            operacao = {"Operacao": "Deposito", "Valor": valor}
            extrato.append(operacao)
            print(f"Seu deposito foi feito com sucesso. \n \n \t R$ {valor:.2f}")
        
        else:
            print("Informe um valor válido!")

    elif opcao == "s":
        valor = int(input("Insira o valor a ser depositado: "))
        
        if (valor > 0):
            if (valor > saldo):
                print("Não é possível sacar o dinheiro por falta de saldo.")
                continue
            
            if (numero_saque >= LIMITE_SAQUE):
                print("Você excedeu o seu limite de saque diário.")
                continue
            
            if (valor > limite):
                print(f"Seu limite de saque é de R$ {limite:.2f}")
                continue
            
            saldo -= valor
            numero_saque += 1
            operacao = {"Operacao": "Saque", "Valor": valor}
            extrato.append(operacao)
            print(f"Saque efetuado com sucesso. \n \n \t R$ {valor:.2f}")
        else:
            print("Entre com um valor válido!")

    elif opcao == "e":
        print("\t Extrato")

        if (extrato):
            for operacao in extrato:
                print(f"""
                    Operação {operacao['Operacao'].upper()} ======================> Valor R$ {operacao['Valor']:.2f}
                """)
        else:
            print("\n \t Você não realizou nenhuma operação em sua conta")

    elif opcao == "q":
        print("Até mais!!")
        break

    else:
        print("Opção inválida, por favor selecione novamente a operação desejada.")