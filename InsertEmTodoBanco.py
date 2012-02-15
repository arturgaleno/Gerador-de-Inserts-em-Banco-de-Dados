#*-* coding:utf-8 *-*
'''
Created on 07/02/2012

@author: Artur Galeno Muniz
'''

from GeradoresDeDados import * #@UnusedWildImport
from BD import * #@UnusedWildImport

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
        self.criarInsert()
    
    def relacionamentosDe(self,tabela):
        bd = BD(self.host,self.user,self.passwd,'information_schema')
        rows = bd.retornarLinhas("SELECT * FROM information_schema.KEY_COLUMN_USAGE WHERE TABLE_SCHEMA = \'%s\' AND TABLE_NAME = \'%s\' AND REFERENCED_TABLE_NAME IS NOT NULL;" %(self.db,tabela))
        listaDeRelacionamentos = []
        for row in rows:
            aux = (row[4],row[5],row[6],row[9],row[10],row[11])
            listaDeRelacionamentos.append(aux)
        return listaDeRelacionamentos
    
    def obterColunasDe(self, tabela):
        bd = BD(self.host,self.user,self.passwd,self.db)
        colunas = bd.retornarLinhas("DESC "+tabela)
        return colunas
        
    def todosRelacionamentos(self):
        bd = BD(self.host,self.user,self.passwd,self.db)
        tabelas = bd.retornarLinhas("SHOW TABLES")
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
                    bd = BD(self.host,self.user,self.passwd,self.db) 
                    rows1 = bd.retornarLinhas('SELECT '+relacao[5]+' FROM '+relacao[4])
                    aux = random.randint(0,len(rows1)-1)
                    choosed = rows1[aux-1][0]
                    values1.append(relacao[2])
                    values.append(str(choosed))
                                                
            colunas = self.obterColunasDe(tabela)
            
            for row in colunas:                                
                if row[0] not in [relacao[2] for relacao in self.relacionamentosDe(tabela)]:
                    values1.append(row[0])
                    if row[1][0:7] == 'varchar':
                        gerador = GeradoresDeDados()
                        values.append(gerador.gerarVarchar(row))
                        
                    if row[1][0:4] == 'date':
                        gerador = GeradoresDeDados()
                        values.append(gerador.gerarDate())
                        
                    if row[1][0:3] == 'int':
                        gerador = GeradoresDeDados()
                        values.append(gerador.gerarInt())
                        ''
                    if row[1][0:4] == 'char':
                        gerador = GeradoresDeDados()
                        values.append(gerador.gerarChar(row))
                        
                    if row[1][0:7] == 'decimal':
                        gerador = GeradoresDeDados()
                        values.append(gerador.gerarDecimal(row))
            
            string1 = ''
            c = '\''       
            for y in range(0, len(values) ):
                string1 = string1 + (c + values[y] + c) + ','
            
            string2 = ''              
            for y in range(0, len(values1) ):
                string2 = string2 + (values1[y]) + ','
            
            try:
                bd = BD(self.host,self.user,self.passwd,self.db) 
                insert = "INSERT INTO " + tabela +" (" +string2[:len(string2)-1]+ ")" +" VALUES (" + string1[:len(string1)-1] + ")"
                bd.inserir(insert)
                values = []
                values1 = []
            except:
                print "Saindo da aplicação..."
                break