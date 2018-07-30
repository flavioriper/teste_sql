import random
import pyodbc

conn = pyodbc.connect(
    r'DRIVER={SQL Server};'
    r'SERVER=.;'
    r'DATABASE=master;'
    r'Trusted_Connection=yes;'
    )
cursor = conn.cursor()

def cpf_generate():
    '''Cria um número de CPF ou CNPJ aleatório para inserção na base de dados'''
    sort = random.randint(0,1) #Variável responsável por sortear entre CPF ou CNPJ gerado
    if sort == 1:
        list1 = ['1','2','3','4','5','6','7','8','9','0']
        list2 = ['.']
        list3 = ['-']
        delimiter = ''
        num_gen = []
        cpf_list = []
        for i in range(14): #laço para criação do cpf
            if i == 3:
                cpf_list.append(list2[0])
            elif i == 7:
                cpf_list.append(list2[0])
            elif i == 11:
                cpf_list.append(list3[0])
            else:
                num_gen = random.sample(list1, 1)
                cpf_list.append(num_gen[0])
        cpf = delimiter.join(cpf_list)
        return cpf
    else:
        list1 = ['1','2','3','4','5','6','7','8','9','0']
        delimiter = ''
        num_gen = []
        cpf_list = []
        for i in range(18): #laço para criação do cnpj
            if i == 2:
                cpf_list.append('.')
            elif i == 6:
                cpf_list.append('.')
            elif i == 10:
                cpf_list.append('/')
            elif i > 10 and i < 14:
                cpf_list.append('0')
            elif i == 15:
                cpf_list.append('-')
            else:
                num_gen = random.sample(list1, 1)
                cpf_list.append(num_gen[0])
        cnpj = delimiter.join(cpf_list)
        return cnpj

def name_generate():
    '''Gera um nome aleatório da lista a seguir para inserção na base de dados'''
    
    list1 = ['Alice','Miguel','Sophia','Arthur','Júlia','Davi','Laura','Pedro','Isabella','Bernardo','Manuela','Gabriel','Luiza',
             'Lucas','Helena','Matheus','Valentina','Heitor','Giovanna','Rafael','MariaEduarda','Enzo','Beatriz','Nicolas','MariaClara',
             'Lorenzo','MariaLuiza','Guilherme','Heloísa','Samuel','Mariana','Theo','Lara','Felipe','Lívia','Gustavo','Lorena','Henrique',
             'AnaClara','JoãoPedro','Isadora','JoãoLucas','Rafaela','Daniel','Sarah','Murilo','Yasmin','Vitor','Ana Luiza','Pedro Henrique',
             'Letícia','Eduardo','Nicole','Leonardo','Gabriela','Pietro','Isabelly','Benjamin','Melissa','Isaac','Cecília','João','Esther',
             'Joaquim','Ana Júlia','Lucca','Emanuelly','Caio','Clara','Vinicius','Marina','Cauã','Rebeca','Bryan','Vitória','João','Miguel',
             'Isis','Vicente','Lavínia','Francisco','Maria','Antônio','Bianca','Benício','Ana Beatriz','João Vitor','Larissa','Enzo Gabriel',
             'Maria Fernanda','Davi Lucas','Catarina','Davi Lucca','Alícia','Thiago','Maria Alice','Thomas','Amanda','Emanuel','Ana','Enrico']
    s = random.sample(list1, 1)
    return s[0]

def pk_generate(x):
    '''Esta função tem como objetivo criar um padrão para a chave primária no campo 'ID_CUSTOMER'.
    Ela serve apenas como apoio e nao deve ser usada sem o auxílio de outras funções'''

    db_list = []
    list1 = []
    cursor.execute("SELECT id_customer FROM tb_customer_account")
    for i in cursor.fetchall():
        db_list.append(i[0])
    while len(list1) != x:
        r = random.randint(0,(5000))
        if r not in db_list:
            list1.append(r)
    return list1

def data_select():
    '''Solicita os dados da base de dados e retorna os registros de forma visual'''

    cursor.execute("SELECT * FROM tb_customer_account;")
    for i in cursor.fetchall():
        print(i)

def data_erase():
    '''Limpa a base de dados com um truncate no SQL'''
    cursor.execute("TRUNCATE TABLE tb_customer_account;")
    conn.commit()

def auto_insert():
    '''Função para inserir as informações na base de dados específicas para o scrip gerando todos os valores automaticamente.'''
    choice = int(input('Digite quantos registros devo adicionar automáticamente: '))
    for i in range(choice):
        pk = pk_generate(choice)
        s = random.randint(0,1)
        if s == 0:
            s = 'Ativo'
        else:
            s = 'Inativo'
        r = random.randint(0,1000)
        cursor.execute("INSERT INTO tb_customer_account VALUES ({}, '{}', '{}', '{}', {});".format(pk[i], cpf_generate(), name_generate(), s, r))
        conn.commit()

def manual_insert():
    '''Função para inserir as informações na base de dados uma por uma.'''
    choice = int(input('Quantos registros adicionarei?: '))
    for i in range(choice):
        db_list = []
        cursor.execute("SELECT id_customer FROM tb_customer_account")
        for i in cursor.fetchall(): #Armazena a chave primária numa lista
            db_list.append(i[0])
        checker = 1
        while checker == 1: #Condição que consulta se a chave primária já existe no banco de dados para evitar duplicidade
            sql = int(input('Digite o ID: '))
            if sql in db_list:
                print('Esta chave primária já existe!')
                checker = 1
            else:
                checker = 0
        while checker == 0:
            sql1 = input('Digite o cpf/cnpj(com traços): ')
            if len(sql1) != 14 and len(sql1) != 18: #Valida o número de CPF ou CNPJ para que não seja inserido um número inválido
                print('Por favor, insira um valor válido de CPF/CNPJ')
                checker = 0
            else:
                checker = 1
        sql2 = input('Digite o nome: ')
        sql3 = input('Está ativo?(S/N) ')
        if sql3 == 'S' or 's':
            sql3 = 'Ativo'
        elif sql3 == 'N' or 'n':
            sql3 = 'Inativo'
        else:
            print('Opção inválida')
            sql3 = input('Está ativo?(S/N) ')
        sql4 = int(input('Digite o saldo: '))
        cursor.execute("INSERT INTO tb_customer_account VALUES ({}, '{}', '{}', '{}', {});".format(sql, sql1, sql2, sql3, sql4))
        conn.commit()
