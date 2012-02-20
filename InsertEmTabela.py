#*-* coding:utf-8 *-*
'''
Created on 07/02/2012

@author: Artur Galeno Muniz
'''

from GeradoresDeDados import * #@UnusedWildImport
from BD import * #@UnusedWildImport
import re

class InsertEmTabela(object):
    
    db = ''
    user = ''
    host = ''
    passwd = ''
    tabela = ''
        
    def __init__(self,host,user,passwd,db,tabela):
        self.user = user
        self.host = host
        self.passwd = passwd
        self.db = db
        self.tabela = tabela
        self.criarInsert()
    
    def criarInsert(self):        
        bd = BD(self.host,self.user,self.passwd,self.db)
        bd.fecharConexao()
                      
        values = []
        values1 = []
        
        print "Gerando Insert para Tabela: "+self.tabela
        
        bd = BD(self.host,self.user,self.passwd,self.db)
        colunas = bd.obterColunasDe(self.tabela)
        colunasChavesPrimarias = []
        chavesEstrangeiras = bd.relacionamentosDe(self.tabela,log=True)
        bd.fecharConexao()
        
        if chavesEstrangeiras != []:
            for relacao in chavesEstrangeiras:
                bd = BD(self.host,self.user,self.passwd,self.db) 
                rows1 = bd.retornarLinhas('SELECT '+relacao[5]+' FROM '+relacao[4])
                if (relacao[0]+'.'+relacao[1] == relacao[3]+'.'+relacao[4]) and rows1 == ():
                    pass
                else:    
                    if rows1 == ():
                        print "EROO!! Não há linhas na tabela: "+relacao[4]
                        print "Saindo da aplicação..."
                        sys.exit(0)
                    aux = random.randint(0,len(rows1)-1)
                    choosed = rows1[aux][0]
                    values1.append(relacao[2])
                    values.append(str(choosed))
        
        for row in colunas:                                
            if row[0] not in [relacao[2] for relacao in chavesEstrangeiras]:
                    values1.append(row[0])
                    if re.search(r'^varchar',row[1]) != None:
                        if row[3] == 'PRI':
                            colunasChavesPrimarias.append(row[0])
                            bd = BD(self.host,self.user,self.passwd,self.db)
                            chavesPrimarias = bd.retornarLinhas("SELECT "+row[0]+" FROM "+self.tabela)
                            controle = False
                            while controle == False:
                                gerador = GeradoresDeDados()
                                valor = gerador.gerarVarchar(row)
                                if (valor,) not in chavesPrimarias:
                                    values.append(valor)
                                    controle = True
                        else:
                            gerador = GeradoresDeDados()
                            values.append(gerador.gerarVarchar(row))
                        
                    if re.search(r'^date$',row[1]) != None:
                        if row[3] == 'PRI':
                           
                            colunasChavesPrimarias.append(row[0])
                            bd = BD(self.host,self.user,self.passwd,self.db)
                            chavesPrimarias = bd.retornarLinhas("SELECT "+row[0]+" FROM "+self.tabela)
                            controle = False
                            while controle == False:
                                gerador = GeradoresDeDados()
                                valor = gerador.gerarDate()
                                if (valor,) not in chavesPrimarias:
                                    values.append(valor)
                                    controle = True
                        else:
                            gerador = GeradoresDeDados()
                            values.append(gerador.gerarDate())
                        
                    if re.search(r'^int',row[1]) != None:
                        if row[3] == 'PRI':
                           
                            colunasChavesPrimarias.append(row[0])
                            bd = BD(self.host,self.user,self.passwd,self.db)
                            chavesPrimarias = bd.retornarLinhas("SELECT "+row[0]+" FROM "+self.tabela)
                            controle = False
                            while controle == False:
                                gerador = GeradoresDeDados()
                                valor = gerador.gerarInt()
                                if (long(valor),) not in chavesPrimarias:
                                    values.append(valor)
                                    controle = True
                        else:
                            gerador = GeradoresDeDados()
                            values.append(gerador.gerarInt())
                                
                    if re.search(r'^char',row[1]) != None:
                        if row[3] == 'PRI':
                            
                            colunasChavesPrimarias.append(row[0])
                            bd = BD(self.host,self.user,self.passwd,self.db)
                            chavesPrimarias = bd.retornarLinhas("SELECT "+row[0]+" FROM "+self.tabela)
                            controle = False
                            while controle == False:
                                gerador = GeradoresDeDados()
                                valor = gerador.gerarChar(row)
                                if (valor,) not in chavesPrimarias:
                                    values.append(valor)
                                    controle = True
                        else:
                            gerador = GeradoresDeDados()
                            values.append(gerador.gerarChar(row))
                                
                    if re.search(r'^decimal',row[1]) != None:
                        if row[3] == 'PRI':
                            
                            colunasChavesPrimarias.append(row[0])
                            bd = BD(self.host,self.user,self.passwd,self.db)
                            chavesPrimarias = bd.retornarLinhas("SELECT "+row[0]+" FROM "+self.tabela)
                            controle = False
                            while controle == False:
                                gerador = GeradoresDeDados()
                                valor = gerador.gerarDecimal(row)
                                if (valor,) not in chavesPrimarias:
                                    values.append(valor)
                                    controle = True
                        else:
                            gerador = GeradoresDeDados()
                            values.append(gerador.gerarDecimal(row))
                            
                    if re.search(r'^tinyint',row[1]) != None:
                        if row[3] == 'PRI':
                            
                            colunasChavesPrimarias.append(row[0])
                            bd = BD(self.host,self.user,self.passwd,self.db)
                            chavesPrimarias = bd.retornarLinhas("SELECT "+row[0]+" FROM "+self.tabela)
                            controle = False
                            while controle == False:
                                gerador = GeradoresDeDados()
                                valor = gerador.gerarTinyInt()
                                if (valor,) not in chavesPrimarias:
                                    values.append(valor)
                                    controle = True
                        else:
                            gerador = GeradoresDeDados()
                            values.append(gerador.gerarTinyInt())
                            
                    if re.search(r'^smallint',row[1]) != None:
                        if row[3] == 'PRI':
                            
                            colunasChavesPrimarias.append(row[0])
                            bd = BD(self.host,self.user,self.passwd,self.db)
                            chavesPrimarias = bd.retornarLinhas("SELECT "+row[0]+" FROM "+self.tabela)
                            controle = False
                            while controle == False:
                                gerador = GeradoresDeDados()
                                valor = gerador.gerarSmallInt()
                                if (valor,) not in chavesPrimarias:
                                    values.append(valor)
                                    controle = True
                        else:
                            gerador = GeradoresDeDados()
                            values.append(gerador.gerarSmallInt())
                            
                    if re.search(r'^mediumint',row[1]) != None:
                        if row[3] == 'PRI':
                            
                            colunasChavesPrimarias.append(row[0])
                            bd = BD(self.host,self.user,self.passwd,self.db)
                            chavesPrimarias = bd.retornarLinhas("SELECT "+row[0]+" FROM "+self.tabela)
                            controle = False
                            while controle == False:
                                gerador = GeradoresDeDados()
                                valor = gerador.gerarMediumInt()
                                if (valor,) not in chavesPrimarias:
                                    values.append(valor)
                                    controle = True
                        else:
                            gerador = GeradoresDeDados()
                            values.append(gerador.gerarMediumInt())
                    
                    if re.search(r'^bigint',row[1]) != None:
                        if row[3] == 'PRI':
                            
                            colunasChavesPrimarias.append(row[0])
                            bd = BD(self.host,self.user,self.passwd,self.db)
                            chavesPrimarias = bd.retornarLinhas("SELECT "+row[0]+" FROM "+self.tabela)
                            controle = False
                            while controle == False:
                                gerador = GeradoresDeDados()
                                valor = gerador.gerarBigInt()
                                if (valor,) not in chavesPrimarias:
                                    values.append(valor)
                                    controle = True
                        else:
                            gerador = GeradoresDeDados()
                            values.append(gerador.gerarBigInt())
                    
                    if re.search(r'^float',row[1]) != None:
                        if row[3] == 'PRI':
                            
                            colunasChavesPrimarias.append(row[0])
                            bd = BD(self.host,self.user,self.passwd,self.db)
                            chavesPrimarias = bd.retornarLinhas("SELECT "+row[0]+" FROM "+self.tabela)
                            controle = False
                            while controle == False:
                                gerador = GeradoresDeDados()
                                valor = gerador.gerarFloat(row)
                                if (valor,) not in chavesPrimarias:
                                    values.append(valor)
                                    controle = True
                        else:
                            gerador = GeradoresDeDados()
                            values.append(gerador.gerarFloat(row))
                            
                    if re.search(r'^double',row[1]) != None:
                        if row[3] == 'PRI':
                            
                            colunasChavesPrimarias.append(row[0])
                            bd = BD(self.host,self.user,self.passwd,self.db)
                            chavesPrimarias = bd.retornarLinhas("SELECT "+row[0]+" FROM "+self.tabela)
                            controle = False
                            while controle == False:
                                gerador = GeradoresDeDados()
                                valor = gerador.gerarDouble(row)
                                if (valor,) not in chavesPrimarias:
                                    values.append(valor)
                                    controle = True
                        else:
                            gerador = GeradoresDeDados()
                            values.append(gerador.gerarDouble(row))
                    
                    if re.search(r'^datetime$',row[1]) != None:
                        if row[3] == 'PRI':
                            
                            colunasChavesPrimarias.append(row[0])
                            bd = BD(self.host,self.user,self.passwd,self.db)
                            chavesPrimarias = bd.retornarLinhas("SELECT "+row[0]+" FROM "+self.tabela)
                            controle = False
                            while controle == False:
                                gerador = GeradoresDeDados()
                                valor = gerador.gerarDateTime()
                                if (valor,) not in chavesPrimarias:
                                    values.append(valor)
                                    controle = True
                        else:
                            gerador = GeradoresDeDados()
                            values.append(gerador.gerarDateTime())
                            
                    if re.search(r'^timestamp$',row[1]) != None:
                        if row[3] == 'PRI':
                            
                            colunasChavesPrimarias.append(row[0])
                            bd = BD(self.host,self.user,self.passwd,self.db)
                            chavesPrimarias = bd.retornarLinhas("SELECT "+row[0]+" FROM "+self.tabela)
                            controle = False
                            while controle == False:
                                gerador = GeradoresDeDados()
                                valor = gerador.gerarTimeStamp()
                                if (valor,) not in chavesPrimarias:
                                    values.append(valor)
                                    controle = True
                        else:
                            gerador = GeradoresDeDados()
                            values.append(gerador.gerarTimeStamp())
                    
                    if re.search(r'^time$',row[1]) != None:
                        if row[3] == 'PRI':
                            
                            colunasChavesPrimarias.append(row[0])
                            bd = BD(self.host,self.user,self.passwd,self.db)
                            chavesPrimarias = bd.retornarLinhas("SELECT "+row[0]+" FROM "+self.tabela)
                            controle = False
                            while controle == False:
                                gerador = GeradoresDeDados()
                                valor = gerador.gerarTime()
                                if (valor,) not in chavesPrimarias:
                                    values.append(valor)
                                    controle = True
                        else:
                            gerador = GeradoresDeDados()
                            values.append(gerador.gerarTime())
                            
                    if re.search(r'^year',row[1]) != None:
                        if row[3] == 'PRI':
                            
                            colunasChavesPrimarias.append(row[0])
                            bd = BD(self.host,self.user,self.passwd,self.db)
                            chavesPrimarias = bd.retornarLinhas("SELECT "+row[0]+" FROM "+self.tabela)
                            controle = False
                            while controle == False:
                                gerador = GeradoresDeDados()
                                valor = gerador.gerarYear()
                                if (valor,) not in chavesPrimarias:
                                    values.append(valor)
                                    controle = True
                        else:
                            gerador = GeradoresDeDados()
                            values.append(gerador.gerarYear())
                            
                            
        string1 = ''
        c = '\''       
        for y in range(0, len(values) ):
            string1 = string1 + (c + values[y] + c) + ','
        
        string2 = ''              
        for y in range(0, len(values1) ):
            string2 = string2 + (values1[y]) + ','
        
        try:
            bd = BD(self.host,self.user,self.passwd,self.db) 
            insert = "INSERT INTO " + self.tabela +" (" +string2[:len(string2)-1]+ ")" +" VALUES (" + string1[:len(string1)-1] + ")"
            bd.inserir(insert)
            values = []
            values1 = []
        except:
            print "Saindo da aplicação..."