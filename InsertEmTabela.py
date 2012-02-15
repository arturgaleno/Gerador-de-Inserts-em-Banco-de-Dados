#*-* coding:utf-8 *-*
'''
Created on 07/02/2012

@author: Artur Galeno Muniz
'''

import MySQLdb, random, string

class InsertEmTabela(object):
    
    con = None #VARIAVEL CONEXAO
    tebelaNome = '' #NOME DA TABELA QUE SERA FEITA A INSERSÃO
    excluso = '' #CAMPO DA TABELA QUE DEVERA SER IGNORADO NA INSERSAO
    chartam = 1 #TAMANHO DO TIPO CHAR SE HOUVER NA TABELA
    fk = {} #DICIONARIO QUE DEVERA CONTER A {CHAVE_ESTRANGEIRA_DA_TABELA_EM_QUESTÃO:NOME_DA_TABELA_QUE_A_CHAVE_ESTRANGEIRA_FAZ_REFERENCIA, ...}
    
    def __init__(self,host,user,passwd,db,tabelaNome,excluso='',chartam=1,fk={}):
        self.con = MySQLdb.connect(host, user, passwd, db)
        self.tabelaNome = tabelaNome
        self.excluso = excluso
        self.chartam = chartam
        self.fk = fk
        self.criarInsert()
    def criarInsert(self):        
        
        ############################# TRECHO 1 ############################################
        #ESSE TRECHO IRÁ CRIAR O CURSOR PARA MANIPULAR OS COMDANDOS SQL,
        #ACHARA NO BANCO ESPEFICICADO A TABELA INDICADA NO PARAMETRO DA FUNCAO INIT
        #PEGARA A DESCRICAO DESSA TABELA APARTIR DO BANCO DE DADOS
        #
        
        cursor = self.con.cursor()
        cursor.execute("SHOW TABLES")
        tabelas = cursor.fetchall()
        i = 0
        tabela = ''
        for nome in tabelas:
            if(nome[i] == self.tabelaNome):
                tabela = nome[i]
                break
        cursor.execute("desc " + tabela)
        rows = cursor.fetchall()
        ############# FIM TRECHO 1##########################################
        
        values = [] #VALUES E VALUES1 SAO VARIAVEIS QUE GUARDAM OS VALORES DOS CAMPOS DA TABELA
        values1 = []#ATE QUE AS STRINGS DE INSERÇÃO SEJAM MONTADAS
        
        ################## TRECHO 2 ###########################################
        for row in rows: #PARA CADA LINHA DA DESCRIÇÃO DA TABELA QUE SERA POPULADA...
            
            if self.excluso in self.fk: self.escluso = ''
        #ESSA LINHA LOGO ACIMA VERIFICA SE EXCLUSO ESTA CONTIDO NO DICIONARIO DAS FK, SE SIM,
        # ELE VAI SER ESCLUSO COMO STRING VAZIA. E DAR PRIORIDADE A ESSE CAMPO TRANTANDO COMO FK
        
            for fk_nome in self.fk:             #O FOR DESSA LINHA MAIS O IF LOGO ABAICXO VERIFICA SE ESSA                       
                        if row[0] == fk_nome:   #LINHA É UMA FOREIGN KEY 
                            #SE FOR UMA FK UM CURSOR AUXILIAR SERA CRIADO
                            #SERA BUSCADO TODOS OS VALORES EM QUE A FK FAZ REFERENCIA NA TABELA REFERENCIADA
                            #ENTÃO ESCOLHE UM VALOR RANDOMICAMENTE PARA SER INSERIDO NO CAMPO FK, E ASSIM PERMITIR CONSISTENCIA
                            #DE DADO
                            cursor1 = self.con.cursor()
                            cursor1.execute("SELECT "+fk_nome+" FROM "+self.fk.get(fk_nome))
                            rows1 = cursor1.fetchall()
                            aux = random.randint(1,len(rows1))
                            choosed = rows1[aux][0];
                            values1.append(row[0])
                            values.append(str(choosed))
                            
            if (row[0] != self.excluso) & (row[0] not in self.fk): #SE A ESSA LINHA NÃO FOR UM CAMPO QUE DEVERA FICAR DE FORA E NEM UMA FK
                #VALORES RANDOMICOS SERÃO ESCOLHIDOS DE ACORDO COM SEU TIPO DE CAMPO
                values1.append(row[0])
                if row[1][0:7] == 'varchar':
                    z = ''.join(random.choice(string.ascii_uppercase + string.digits) for a in range(10)) #@UnusedVariable
                    values.append(z)
                    
                if row[1][0:4] == 'date':
                    values.append('' + str(random.randint(2000, 2011)) + '-' + str(random.randint(01, 12)) + '-' + str(random.randint(01, 24)) + '')
                    
                if row[1][0:3] == 'int':
                    values.append(str(random.randint(1, 100)))
                    
                if row[1][0:4] == 'char':
                    z = ''.join(random.choice(string.ascii_uppercase + string.digits) for a in range(self.chartam)) #@UnusedVariable
                    values.append(z)
                    
                if row[1][0:7] == 'decimal':
                    z = str(random.randint(100, 5000))
                    z = z+'.'+str(random.randint(0, 99))
                    values.append(z)
        ################################## FIM TRECHO 2 ################################################                  
        
        
        ################################## TRECHO 3 ####################################################
        #ESSE TRECHO É RESPONSAVEL POR MONTAR AS STRINGS PARA INSERSAO, APARTIR DA VARIAVEIS VALUES
        #DECLARADAS ENTRE O FIM DO TRECHO 1 E O INICIO DO TRECHO 2            
        string1 = ''
        c = '\''       
        for y in range(0, len(values) ):
            string1 = string1 + (c + values[y] + c) + ','
        
        string2 = ''              
        for y in range(0, len(values1) ):
            string2 = string2 + (values1[y]) + ','
            
        ################################## FIM TRECHO 3 ##################################################
        
        ############################# MONTAGEM DAS STRINGS DE INSERÇÃO ###################################
        
        try:
            print "INSERT INTO " + tabela + " (" +string2[:len(string2)-1]+ ")" +" VALUES (" + string1[:len(string1)-1] + ")"
            cursor.execute("INSERT INTO " + tabela +" (" +string2[:len(string2)-1]+ ")" +" VALUES (" + string1[:len(string1)-1] + ")")
            self.con.commit()
            self.con.close()
            print "1 row affected"
        except:
            self.con.close()
            print "Erro. Conexão fechada."
        
        ############################ FIM DA MONTAGEM DAS STRINGS DE INSERÇÃO #############################