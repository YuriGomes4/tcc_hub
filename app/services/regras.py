from app.controllers import crud_regras, crud_produto
from app.services import ml_api

def match_tabela(tabela):

    match tabela:
        case "produtos":
            crud = crud_produto
        case _:
            print("Tabela inexistente")
            crud = None

    return crud

def match_coluna(query, coluna):

    try:
        match coluna:
            case "id":
                column = query.id
            case "category_id":
                column = query.category_id
            case "cost":
                column = query.cost
            case "price":
                column = query.price
            case "title":
                column = query.title
            case "listing_type_id":
                column = query.listing_type_id
            case "free_shipping":
                column = query.free_shipping
            case "shipping_free_cost":
                column = query.shipping_free_cost
            case "sale_fee":
                column = query.sale_fee
            case "sales":
                column = query.sales
            case "invoicing":
                column = query.invoicing
            case "seller":
                column = query.seller
            case "json":
                column = query.json
            case _:
                None  # Chave não reconhecida
    except KeyError:
        column = None  # Chave não encontrada

    return column

def match_crud(regra):

    print(regra.tabela_obj)
    crud = match_tabela(regra.tabela_obj)

    #crud = match_coluna(tabela, regra.coluna_obj)

    return crud

###################################################################

def alterar_produto(item_id, update):
    ml_api.alterar_produto(item_id, update)

###################################################################

def verificar():
    regras = crud_regras.read_multi()
    
    for regra in regras:
            
        if regra.feito == False:

            crud = match_crud(regra)
            query_args = {"id": regra.ref_id_obj}
            query = crud.read(**query_args)

            #print(query)

            operador = regra.operador

            def contem_apenas_numeros(texto):
                for caractere in texto:
                    if not (caractere.isdigit() or caractere == '.' or caractere == ','):
                        return False
                return True
            
            if contem_apenas_numeros(regra.valor_obj):
                valor1 = float(match_coluna(query, regra.coluna_obj))
                valor2 = float(regra.valor_obj)
            else:
                valor1 = match_coluna(query, regra.coluna_obj)
                valor2 = regra.valor_obj

            # Use uma instrução condicional para verificar a operação
            if operador == ">=":
                resultado = valor1 >= valor2
            elif operador == ">":
                resultado = valor1 > valor2
            elif operador == "<=":
                resultado = valor1 <= valor2
            elif operador == "<":
                resultado = valor1 < valor2
            elif operador == "==":
                resultado = valor1 == valor2
            elif operador == "!=":
                resultado = valor1 != valor2
            else:
                raise ValueError("Operador não reconhecido")
            
            if resultado:
                funcao = globals().get(regra.funcao)
                if funcao:
                    match regra.funcao:
                        case "alterar_produto":
                            update = {
                                f'{regra.coluna_new}': regra.valor_new
                            }
                            
                            funcao(regra.ref_id_new, update)

                            regra.feito = 1
                            crud_regras.update(regra)
                        case _:
                            print("Função não mapeada")
                else:
                    print(f"A função {regra.funcao} não foi encontrada.")


            
            print(resultado, valor1, valor2)
        else:
            print("Regra já utilizada")

