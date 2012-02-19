#*-* coding:utf-8 *-*
'''
Created on 07/02/2012

@author: Artur Galeno Muniz
'''

from GeradoresDeDados import * #@UnusedWildImport
from BD import * #@UnusedWildImport
import re

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

            colunas = self.obterColunasDe(tabela)
            colunasChavesPrimarias = []
            chavesEstrangeiras = self.relacionamentosDe(tabela,log=True)
            
            if chavesEstrangeiras != []:
                for relacao in chavesEstrangeiras:
                    bd = BD(self.host,self.user,self.passwd,self.db) 
                    rows1 = bd.retornarLinhas('SELECT '+relacao[5]+' FROM '+relacao[4])
                    aux = random.randint(0,len(rows1)-1)
                    choosed = rows1[aux][0]
                    values1.append(relacao[2])
                    values.append(str(choosed))
            
            for row in colunas:                                
                if row[0] not in [relacao[2] for relacao in self.relacionamentosDe(tabela)]:
                        values1.append(row[0])
                        if re.search(r'^varchar',row[1]) != None:
                            if row[3] == 'PRI':
                                colunasChavesPrimarias.append(row[0])
                                bd = BD(self.host,self.user,self.passwd,self.db)
                                chavesPrimarias = bd.retornarLinhas("SELECT "+row[0]+" FROM "+tabela)
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
                                chavesPrimarias = bd.retornarLinhas("SELECT "+row[0]+" FROM "+tabela)
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
                                chavesPrimarias = bd.retornarLinhas("SELECT "+row[0]+" FROM "+tabela)
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
                                chavesPrimarias = bd.retornarLinhas("SELECT "+row[0]+" FROM "+tabela)
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
                                chavesPrimarias = bd.retornarLinhas("SELECT "+row[0]+" FROM "+tabela)
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
                                chavesPrimarias = bd.retornarLinhas("SELECT "+row[0]+" FROM "+tabela)
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
                                chavesPrimarias = bd.retornarLinhas("SELECT "+row[0]+" FROM "+tabela)
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
                                chavesPrimarias = bd.retornarLinhas("SELECT "+row[0]+" FROM "+tabela)
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
                                chavesPrimarias = bd.retornarLinhas("SELECT "+row[0]+" FROM "+tabela)
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
                                chavesPrimarias = bd.retornarLinhas("SELECT "+row[0]+" FROM "+tabela)
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
                                chavesPrimarias = bd.retornarLinhas("SELECT "+row[0]+" FROM "+tabela)
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
                                chavesPrimarias = bd.retornarLinhas("SELECT "+row[0]+" FROM "+tabela)
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
                                chavesPrimarias = bd.retornarLinhas("SELECT "+row[0]+" FROM "+tabela)
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
                                chavesPrimarias = bd.retornarLinhas("SELECT "+row[0]+" FROM "+tabela)
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
                                chavesPrimarias = bd.retornarLinhas("SELECT "+row[0]+" FROM "+tabela)
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
                insert = "INSERT INTO " + tabela +" (" +string2[:len(string2)-1]+ ")" +" VALUES (" + string1[:len(string1)-1] + ")"
                bd.inserir(insert)
                values = []
                values1 = []
            except:
                print "Saindo da aplicação..."
                break