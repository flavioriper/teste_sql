import pyodbc
import random
from library_auxiliar import *
'''Este script tem como finalidade inserir alguns registros numa base de dados SQL SERVER, depois disto executar uma verificação nos registros adicionados (e tambem
nos registros já existentes para retornar todos os valores que atendam uma condição específica, calculando uma média destes e mostrando uma listagem de todos os dados
utilizados para tal resultado.
Para o funcionamento deste script, é necessário algumas configurações no ambiente de trabalho: a instalação da base de dados SQL Server (foi utilizada a base de dados
SQL Server 2014), alem da instalação do driver de conexão PYODBC'''

#As próximas 7 linhas fazem a conexão com a base de dados através do PYODBC. Altere os valores para melhor atender seu ambiente de trabalho caso necessário
conn = pyodbc.connect(
    r'DRIVER={SQL Server};'
    r'SERVER=.;'
    r'DATABASE=master;'
    r'Trusted_Connection=yes;'
    )
cursor = conn.cursor()

cursor.execute("DROP TABLE tb_customer_account")
cursor.execute("IF OBJECT_ID ('tb_customer_account') IS NULL BEGIN CREATE TABLE tb_customer_account (id_customer INT PRIMARY KEY NOT NULL, cpf_cnpj VARCHAR(18) NOT NULL, nm_customer VARCHAR(30) NOT NULL, is_active VARCHAR(10) NOT NULL, vl_total INT NOT NULL); END;")
conn.commit() #Executa uma verificação na base de dados, caso a tabela alvo não exista o próprio script criará

check = 1
while check == 1:
    choose = input('Devo adicionar os registros automaticamente(S/N)? ')
    if choose == 'S' or choose == 's':
        auto_insert()
        print()
        check = 0
    elif choose == 'N' or choose == 'n':
        manual_insert()
        print()
        check = 0
    else:
        print('Opção inválida!')
        check = 1

'''A parte a seguir recebe os valores adicionados na base de dados e processa essas informações'''
media_list = []
media_count = 0
list_result = []
cursor.execute("SELECT * FROM tb_customer_account")
for i in cursor.fetchall(): #Laço responsável por receber apenas os valores da condição: vl_total > 560 e id_customer entre 1500 e 2700
    if i[4] > 560 and 1500 <= i[0] <= 2700:
        media_list.append(i[4])
        media_count = media_count + i[4]
        list_result.append(i)
        
list_result.sort(key=lambda x: x[4], reverse=True) #Organiza a lista de forma descendente usando como base o quinto item do array
for i in list_result:
    print(i)
if media_count > 0:
    print()
    print("A média de 'vl_total' é: {}R$.".format(round((media_count/len(media_list)),2))) #O round está limitando para apenas duas casas decimais o float da média
else:
    print('Não existem IDs entre 1500 e 2700 com salários maiores que 560,00R$')
print(' ')
data_erase() #Caso queira persistir os dados na base, exclua essa linha  
conn.close()
