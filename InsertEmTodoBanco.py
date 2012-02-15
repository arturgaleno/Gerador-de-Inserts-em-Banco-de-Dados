#*-* coding:utf-8 *-*
'''
Created on 07/02/2012

@author: Artur Galeno Muniz
'''

import MySQLdb, random, string

class InsertEmTodoBanco(object):
    
    con = None
    db = ''
    user = ''
    host = ''
    passwd = ''
        
    def __init__(self,host,user,passwd,db):
        self.user = user
        self.host = host
        self.passwd = passwd
        self.db = db
        self.criarInsert()
    
    def conectar(self,db='information_schema'):
        try:
            self.con = MySQLdb.connect(self.host,self.user,self.passwd,db)
        except:
            print "Conexão com o banco NÃO realizada. Seguindo paramêtros de conexão: Servidor: %s, Usuário: %s, Senha: ****, Banco de Dados: %s" %(self.host,self.user,self.bd)
    
    def relacionamentosDe(self,tabela):
        self.conectar()
        cursor = self.con.cursor()
        cursor.execute("SELECT * FROM information_schema.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s AND REFERENCED_TABLE_NAME IS NOT NULL;",(self.db,tabela))
        rows = cursor.fetchall()
        cursor.close()
        del cursor
        self.con.close()
        self.con = None
        listaDeRelacionamentos = []
        for row in rows:
            aux = (row[4],row[5],row[6],row[9],row[10],row[11])
            listaDeRelacionamentos.append(aux)
        return listaDeRelacionamentos
    
    def obterColunasDe(self, tabela):
        self.conectar(self.db)
        cursor = self.con.cursor()
        cursor.execute("DESC "+tabela)
        colunas = cursor.fetchall()
        cursor.close()
        del cursor
        self.con.close()
        self.con = None
        return colunas
        
    def todosRelacionamentos(self):
        self.conectar(self.db)
        cursor = self.con.cursor()
        cursor.execute("SHOW TABLES")
        tabelas = cursor.fetchall()
        cursor.close()
        del cursor
        self.con.close()
        self.con = None
        pilha = []
        for tabela in tabelas:
            if tabela[0] not in pilha:
                aux = self.relacionamentosDe(tabela[0])  
                if aux != None:
                    for relacionamento in aux:
                        if relacionamento[4] not in pilha:
                            pilha.append(relacionamento[4])
            if tabela[0] not in pilha: pilha.append(tabela[0])
        return pilha
        
    def criarInsert(self):        

        tabelas = self.todosRelacionamentos()
                      
        values = []
        values1 = []
        
        for tabela in tabelas:
            print "Gerando Insert para Tabela: "+tabela

            rows = self.relacionamentosDe(tabela)
            
            if rows != []:
                for relacao in rows: 
                    self.conectar(self.db)                   
                    cursor = self.con.cursor()
                    cursor.execute('SELECT '+relacao[5]+' FROM '+relacao[4])
                    rows1 = cursor.fetchall()
                    cursor.close()
                    del(cursor)
                    self.con.close()
                    self.con = None
                    aux = random.randint(1,len(rows1))
                    choosed = rows1[aux-1][0]
                    values1.append(relacao[2])
                    values.append(str(choosed))
                    
            colunas = self.obterColunasDe(tabela)

            for row in colunas:                                
                if row[0] not in [relacao[2] for relacao in self.relacionamentosDe(tabela)]:
                    values1.append(row[0])
                    if row[1][0:7] == 'varchar':
                        tam = row[1][8:]
                        tam = tam[:-1]
                        z = ''.join(random.choice(string.ascii_uppercase + string.digits) for a in range(0,int(tam)))
                        values.append(z)
                        
                    if row[1][0:4] == 'date':
                        values.append('' + str(random.randint(2000, 2011)) + '-' + str(random.randint(01, 12)) + '-' + str(random.randint(01, 24)) + '')
                        
                    if row[1][0:3] == 'int':
                        values.append(str(random.randint(1, 100)))
                        ''
                    if row[1][0:4] == 'char':
                        tam = row[1][5:]
                        tam = tam[:-1]
                        z = ''.join(random.choice(string.ascii_uppercase) for a in range(0,int(tam)))
                        values.append(z)
                        
                    if row[1][0:7] == 'decimal':
                        tam = row[1][8:]
                        tam = tam[:-1]
                        tam = tam.split(',')
                        tmp_parteDecimal = (int(tam[1]))
                        tmp_parteInteira = int(tam[0]) - tmp_parteDecimal
                        aux = '9'
                        parteInteira = ''.join(aux for i in range(0,tmp_parteInteira))
                        parteDecimal = ''.join(aux for i in range (0,tmp_parteDecimal))    
                        z = str(random.randint(0, int(parteInteira)))
                        z = z+'.'+str(random.randint(0, int(parteDecimal)))
                        values.append(z)
        
            string1 = ''
            c = '\''       
            for y in range(0, len(values) ):
                string1 = string1 + (c + values[y] + c) + ','
            
            string2 = ''              
            for y in range(0, len(values1) ):
                string2 = string2 + (values1[y]) + ','
                
        
            try:
                self.conectar(self.db)
                print "INSERT INTO " + tabela + " (" +string2[:len(string2)-1]+ ")" +" VALUES (" + string1[:len(string1)-1] + ")"
                cursor = self.con.cursor()
                cursor.execute("INSERT INTO " + tabela +" (" +string2[:len(string2)-1]+ ")" +" VALUES (" + string1[:len(string1)-1] + ")")
                cursor.close()
                del(cursor)
                self.con.commit()
                self.con.close()
                self.con = None
                values = []
                values1 = []
                print "1 row affected"
            except:
                print "Erro ao Inserir na Tabela: "+tabela
                print "Saindo da aplicação..."
                break