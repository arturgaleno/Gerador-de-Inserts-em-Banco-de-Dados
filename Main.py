'''
Created on 07/02/2012

@author: Artur Galeno Muniz
'''
import InsertEmTodoBanco
#from AssistenteDeDelecao import * #@UnusedWildImport
#import InsertEmTabela

if __name__ == '__main__':
    #for a in range(0,100):
        InsertEmTodoBanco.InsertEmTodoBanco(host='localhost',user='root',passwd='1n5p1r0n123',db='Tutor')
        #InsertEmTabela.InsertEmTabela(host='',user='',passwd='',db='')
        #assistente = AssistenteDeDelecao(host='localhost',user='root',passwd='1n5p1r0n123',db='DIGITEC')
        #assistente.limparBanco()