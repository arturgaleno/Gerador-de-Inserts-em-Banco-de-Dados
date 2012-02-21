#*-* coding:utf-8 *-*
'''
Created on 07/02/2012

@author: Artur Galeno Muniz
'''

from GeradoresDeDados import * #@UnusedWildImport
from BD import * #@UnusedWildImport
import InsertEmTabela

class InsertEmTodoBanco(object):
    
    db = ''
    user = ''
    host = ''
    passwd = ''
        
    def __init__(self,host,user,passwd,db):
        self.user = user
        self.host = host
        self.passwd = passwd
        self.db = db
        if host == '' or user == '' or passwd == '' or db == '':
            print "Parâmetros de conexão inválidos"
            sys.exit(0)
        self.criarInsert()
    
    def criarInsert(self):        
        bd = BD(self.host,self.user,self.passwd,self.db)
        tabelas = bd.todosRelacionamentos()
        bd.fecharConexao()

        for tabela_ in tabelas:
            InsertEmTabela.InsertEmTabela(host=self.host, user=self.user, passwd=self.passwd, db=self.db, tabela=tabela_)