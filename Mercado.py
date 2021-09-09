from typing import List,Dict
from utils.helper import formata_float_str_moeda
from Models.produto import Produto
from time import sleep

produtos: List[Produto] = []
carrinho: List[Dict[str, int]] = []

def main() -> None:
   menu()

def menu() -> None:
    print('********************************')
    print('*********** Menu ***************')
    print('********** Mercado **************')
    print('*********************************')

    print('Selecione algumas das opções abaixo')
    print('1 - Cadastrar produto')
    print('2 - Listar produto')
    print('3 - Comprar produto')
    print('4 - Visualizar produto')
    print('5 - Fechar pedido')
    print('6 - Sair do sistema')

    op = int(input())

    if op ==1:
        cadastrar_prouto()
    elif op == 2:
        listar_produto()
    elif op == 3:
        comprar_produto()
    elif op == 4:
        visualizar_carrinho()
    elif op == 5:
        fechar_pedido()
    elif op == 6:
        print('Volte sempre!')
        sleep(2)
        exit(0)
    else:
        print('Opçãõ não válida. Digite de novo. por favor.')
        sleep(2)
        menu()

def cadastrar_prouto() -> None:
    print('Cadastro do produto.')
    print('********************')

    nome: str = input('Nome do produto ')
    preço: float =float(input('Preço do produto'))

    produto: Produto = Produto(nome, preço)

    produtos.append(produto)

    print(f'Produto {produto.nome} foi cadastrado com sucesso.')
    sleep(2)
    menu()

def listar_produto() -> None:
    if len(produtos) > 0:
        print('Listagem de produto')
        print('---------------')
        for produto in produtos:
            print(f'{produto}')
            print('---------------')
            sleep(1)
    else:
        print('Não tem produtos cadastrado.')
        sleep(2)
        menu()


def comprar_produto() -> None:
     if len(produtos) > 0:
         print('Informe o codigo do produto para adicionar no carrinho.')
         print('*******************************************************')
         print('********* Produtos disponíveis')

         for produto in produtos:
             print(produto)
             print('----------------')
             sleep(1)
         codigo: int = int(input())

         produto: Produto = pega_produto_por_codigo(codigo)

         if produto:
             if len(carrinho)  > 0:
                tem_no_carrinho: bool =False
                for item in carrinho:
                    quant: int = item.get(produto)
                    if quant:
                        item[produto] = quant+1
                        print(f'O produto {produto.nome} possui {quant +1} unnidades no carrinho.')
                        tem_no_carrinho=True
                        sleep(2)
                        menu()

                if not tem_no_carrinho:
                    prod = {produto:1}
                    carrinho.append(prod)
                    print(f'O produto {produto.nome} foi adicionado no carrinho.')
                    sleep(2)
                    menu()
             else:
                 item = {produto : 1}
                 carrinho.append(item)
                 print(f'O produto {produto.nome} foi adicionado ao carrinho.')
                 sleep(2)
                 menu()
         else:
             print('Produto não encontrado.')
             sleep(2)
             menu()
     else:
         print('Ainda não tem produtos para vender.')
     sleep(2)
     menu()

def visualizar_carrinho() ->None:
    if len(carrinho) > 0:
       print('Produtos do carrinho.')

       for item in carrinho:
           for dados in item.items():
               print(dados[0])
               print(f'Quantidade: {dados[1]}')
               print('-----------------')
               sleep(2)
               menu()
    else:
        print('Ainda não tem produto no carrinho.')
    sleep(2)
    menu()
def fechar_pedido() -> None:
    if len(carrinho) > 0:
        valor_total: float = 0

        print('Produto do carrinho')
        for item in carrinho:
            for dados in item.items():
                print(dados[0])
                print(f'Quantidades de produtos {dados[1]}')
                valor_total+=dados[0].preço*dados[1]
                print('-----------------------')
                sleep(1)
        print(f'Sua factura é {formata_float_str_moeda(valor_total)}')
        print('Volte sempre')
        carrinho.clear()
        sleep(5)
    else:
        print('Ainda não tem produto!')
        sleep(2)
        menu()

def pega_produto_por_codigo(codigo: int) -> Produto:

    p: Produto =None
    for produto in produtos:
        if produto.codigo == codigo:
             p = produto
    return  p


if __name__=='__main__':
    main()