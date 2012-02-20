#*-* coding:utf-8 *-*
'''
Created on 19/02/2012

@author: artur
'''

import MySQLdb, sys #@UnusedImport
from BD import *

class AssistenteDeDelecao(object):
    
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

    def limparBanco(self):
        bd = BD(self.host,self.user,self.passwd,self.db)
        ordemDeTabelas = bd.todosRelacionamentos()
        bd.fecharConexao()
        ordemDeTabelas.reverse()
        for tabela in ordemDeTabelas:
            bd = BD(self.host,self.user,self.passwd,self.db)
            relacoes = bd.relacionamentosDe(tabela)
            bd.fecharConexao()
            if relacoes != ():
                for relacao in relacoes:
                    if (relacao[0]+'.'+relacao[1] == relacao[3]+'.'+relacao[4]):
                        bd = BD(self.host,self.user,self.passwd,self.db)                            
                        aux = bd.retornarLinhas("SELECT "+relacao[5]+" FROM "+tabela+" WHERE "+relacao[5]+" NOT IN (SELECT "+relacao[2]+" FROM "+tabela+" WHERE "+relacao[2]+" IS NOT NULL)")
                        while len(aux) != 0:
                            for row in aux:
                                cursor = self.con.cursor()
                                try:
                                    cursor.execute("DELETE FROM "+tabela+" WHERE "+relacao[5]+"="+"'"+row[0]+"'")
                                except: print "Não foi possivel executar a operação: "+"DELETE FROM "+tabela+" WHERE "+relacao[5]+"="+"'"+row[0]+"'"
                                cursor.close()
                                cursor = None
                                self.con.commit()
                            bd = BD(self.host,self.user,self.passwd,self.db)
                            aux = bd.retornarLinhas("SELECT "+relacao[5]+" FROM "+tabela+" WHERE "+relacao[5]+" NOT IN (SELECT "+relacao[2]+" FROM "+tabela+" WHERE "+relacao[2]+" IS NOT NULL)")
            try:
                cursor = self.con.cursor()
                print "DELETANDO ITENS DA TABELA: "+tabela
                cursor.execute("DELETE FROM "+tabela)
                print "ITENS DELETADOS"
                cursor.close()
                cursor = None
                self.con.commit()
            except:
                print "Não foi possível deletar itens da tabela: "+tabela
                if self.con != None: self.con.close()
                self.con = None
                sys.exit(0)
        self.con.close()
        self.con = None
        print "Tabelas do banco %s limpas" %(self.db)
        
    def limparTabela(self,tabela):
        bd = BD(self.host,self.user,self.passwd,self.db)
        relacoes = bd.relacionamentosDe(tabela)
        bd.fecharConexao()
        if relacoes != ():
            for relacao in relacoes:
                if (relacao[0]+'.'+relacao[1] == relacao[3]+'.'+relacao[4]):
                    bd = BD(self.host,self.user,self.passwd,self.db)                            
                    aux = bd.retornarLinhas("SELECT "+relacao[5]+" FROM "+tabela+" WHERE "+relacao[5]+" NOT IN (SELECT "+relacao[2]+" FROM "+tabela+" WHERE "+relacao[2]+" IS NOT NULL)")
                    while len(aux) != 0:
                        for row in aux:
                            cursor = self.con.cursor()
                            try:
                                cursor.execute("DELETE FROM "+tabela+" WHERE "+relacao[5]+"="+"'"+row[0]+"'")
                            except: print "Não foi possivel executar a operação: "+"DELETE FROM "+tabela+" WHERE "+relacao[5]+"="+"'"+row[0]+"'"
                            cursor.close()
                            cursor = None
                            self.con.commit()
                        bd = BD(self.host,self.user,self.passwd,self.db)
                        aux = bd.retornarLinhas("SELECT "+relacao[5]+" FROM "+tabela+" WHERE "+relacao[5]+" NOT IN (SELECT "+relacao[2]+" FROM "+tabela+" WHERE "+relacao[2]+" IS NOT NULL)")
        try:
            cursor = self.con.cursor()
            print "DELETANDO ITENS DA TABELA: "+tabela
            cursor.execute("DELETE FROM "+tabela)
            print "ITENS DELETADOS"
            cursor.close()
            cursor = None
            self.con.commit()
        except:
            print "Não foi possível deletar itens da tabela: "+tabela
            if self.con != None: self.con.close()
            self.con = None
            sys.exit(0)
        self.con.close()
        self.con = None
        print "Tabela %s do banco %s limpa" %(tabela,self.db)
    