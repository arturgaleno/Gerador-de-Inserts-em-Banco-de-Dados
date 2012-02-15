#*-* coding:utf-8 *-*
'''
Created on 15/02/2012

@author: artur
'''
import random, string

class GeradoresDeDados(object):
        
    def gerarVarchar(self,row):
        ''' Gera um varchar. Utiliza como entrada uma determinada linha retornada no comando SQL "DESBRIBE <TABELA>; '''
        tam = row[1][8:]
        tam = tam[:-1]
        
        z = ''.join(random.choice(string.ascii_uppercase + string.digits) for a in range(0,int(tam))) #@UnusedVariable
        return z
    
    def gerarDate(self,de=2000,ate=2011):
        ''' Gera um campo Date. Utiliza como entrada os valores inteiros "de" e "ate". "de" eh o ano o qual você deseja que os valores
        aleatórios partam, e "ate" é o ano limite dos valores aleatórios. "ate" tem que ser maior que "de", e ambos devem ser
        valores válidos ao SGBD'''
        z = ('' + str(random.randint(de,ate)) + '-' + str(random.randint(01, 12)) + '-' + str(random.randint(01, 24)) + '')
        return z
    
    def gerarInt(self,de=1,ate=100):
        z = str(random.randint(de, ate))
        return z
    
    def gerarChar(self,row):
        tam = row[1][5:]
        tam = tam[:-1]
        z = ''.join(random.choice(string.ascii_uppercase) for a in range(0,int(tam))) #@UnusedVariable
        return z
    
    def gerarDecimal(self,row):
        tam = row[1][8:]
        tam = tam[:-1]
        tam = tam.split(',')
        tmp_parteDecimal = (int(tam[1]))
        tmp_parteInteira = int(tam[0]) - tmp_parteDecimal
        aux = '9'
        parteInteira = ''.join(aux for i in range(0,tmp_parteInteira)) #@UnusedVariable
        parteDecimal = ''.join(aux for i in range (0,tmp_parteDecimal))  #@UnusedVariable  
        z = str(random.randint(0, int(parteInteira)))
        z = z+'.'+str(random.randint(0, int(parteDecimal)))
        return z