# *-* coding:utf-8 *-*
'''
Created on 15/02/2012

@author: artur
'''

import MySQLdb, sys

class BD(object):
    
    con = None
        
    def __init__(self,host,user,passwd,db):
        try:
            self.con = MySQLdb.connect(host,user,passwd,db)
        except:
            print "Conexão com o banco NÃO realizada. Seguindo paramêtros de conexão: Servidor: %s, Usuário: %s, Senha: %s, Banco de Dados: %s" %(host,user,passwd,db)
            sys.exit(0)
    
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
        
    