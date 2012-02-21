# *-* coding:utf-8 *-*
'''
Created on 15/02/2012

@author: artur
'''

import MySQLdb, sys

class BD(object):
    
    con = None
    db = ''
    user = ''
    host = ''
    passwd = ''
        
    def __init__(self,host,user,passwd,db):
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        try:
            self.con = MySQLdb.connect(host,user,passwd,db)
        except:
            print "Conexão com o banco NÃO realizada. Seguindo paramêtros de conexão: Servidor: %s, Usuário: %s, Senha: %s, Banco de Dados: %s" %(host,user,passwd,db)
            sys.exit(0)
    
    def fecharConexao(self):
        try:
            self.con.close()
            self.con = None
        except:
            print "Não há conexão aberta."
                
    def retornarLinhas(self,query=''):
        try:
            cursor = self.con.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            del cursor
            self.con.close()
            self.con = None
            return rows
        except Exception, detail:
            print "Não foi possível executar a query:"
            print query
            print "Foi gerado um erro: ",detail
            print ''
            raise Exception
            
    def inserir(self,query=''):
        try:
            cursor = self.con.cursor()
            cursor.execute(query)
            cursor.close()
            self.con.commit()
            del cursor
            self.con.close()
            self.con = None
            print query
            print "1 row affected"
            print ''
        except Exception, detail:
            print "Não foi possível executar a query:"
            print query
            print "Foi gerado um erro: ",detail
            print ''
            raise Exception
        
    def relacionamentosDe(self,tabela,log=False):
        bd = BD(self.host,self.user,self.passwd,'information_schema')
        rows = bd.retornarLinhas("SELECT * FROM information_schema.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA = \'%s\' AND TABLE_NAME = \'%s\' AND REFERENCED_TABLE_NAME IS NOT NULL;" %(self.db,tabela))
        tmp_listaDeRelacionamentos = []
        listaDeRelacionamentos = []
        for row in rows:
            aux = (row[4],row[5],row[6],row[9],row[10],row[11])
            tmp_listaDeRelacionamentos.append(aux)
        for relacao in tmp_listaDeRelacionamentos:
            num = tmp_listaDeRelacionamentos.count(relacao)
            if num != 1 and log == True and (relacao not in listaDeRelacionamentos):
                print "----CUIDADO!!! A relação na ----"
                print "Tabela: %s Coluna: %s" %(relacao[1],relacao[2])
                print "Com estrangeirismo na tabela: %s Coluna: %s" %(relacao[4],relacao[5])
                print "Aparece %s veses. Verifique se esse tipo de relação é mesmo necessário." %(str(num))
                print "Pois há referêcias ambíguas com 'CONSTRAINTS' diferentes."
                print "Isso não indica necessariamente um erro no banco de dados. Mas se essa"
                print "situação não foi proposital, é aconselhavel que seja verificada."
                print ""
            if relacao not in listaDeRelacionamentos:
                listaDeRelacionamentos.append(relacao)
        return listaDeRelacionamentos
    
    def obterColunasDe(self, tabela):
        bd = BD(self.host,self.user,self.passwd,self.db)
        colunas = bd.retornarLinhas("DESC "+tabela)
        return colunas
        
    def todosRelacionamentos(self):
        bd = BD(self.host,self.user,self.passwd,self.db)
        tabelas = bd.retornarLinhas("SHOW TABLES")
        pilha = []
        tmp_pilha  = []
        for tabela in tabelas:
            relacoes = self.relacionamentosDe(tabela[0])
            if relacoes == []:
                pilha.append(tabela[0])
        for tabela in tabelas:
            if tabela[0] not in pilha and tabela[0] not in tmp_pilha:
                tmp_pilha.append(tabela[0])
                relacoes = self.relacionamentosDe(tabela[0])
                while relacoes != []:
                    relacao = relacoes.pop(0)
                    if relacao[4] not in pilha and relacao[4] not in tmp_pilha:
                        tmp_pilha.append(relacao[4])
                        relacoes = self.relacionamentosDe(relacao[4])
                tmp_pilha.reverse()
                pilha.extend(tmp_pilha)
                tmp_pilha = []
        return pilha