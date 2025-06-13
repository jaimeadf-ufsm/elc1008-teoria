-- Código 10/06/2025
module Lam where

import Data.List


--exemplo
data Color = Red | Blue | Green deriving (Show, Eq, Ord)


-- AST do Calculo-lambda

data TLam = Var Char -- variavel
          | Abs Char TLam -- abstracao
          | App TLam TLam -- aplicacao 



-- ToDo: Implementar a funcao abaixo: recebe um termo e retorna uma 
-- lista de variaveis livres.

freeVars :: TLam -> [Char]          
freeVars (Var x)     = undefined
freeVars (Abs x t)   = undefined
freeVars (App t1 t2) = undefined


-- ToDo: Implementar a função de substituição
subs :: Char -> TLam -> TLam -> TLam
subs x s (Var y) = if (x == y) then s else (Var y)
subs x s (Abs y t12) = undefined
subs x s (App t1 t2) = undefined

-- ToDo: Implementar a função isVal: recebe um termo lambda e 
-- retorna True se é um valor, i.e, se não é aplicação.

isVal :: TLam -> Bool
isVal (Var x) = True
isVal _       = undefined
-- ToDo: Implementar a semântica operacional call-by-value: um 
-- passo de beta redução

eval :: TLam -> TLam
eval (Var x) = Var x 
eval (Abs x t) = Abs x t
eval (App (Abs x t12) t2) = if (isVal t2) then (subs x t2 t12)
                                          else let t2' = eval t2
                                               in (App (Abs x t12) t2')
eval _ = undefined                                               

-- aplicando varios passos do eval até que não tenha mais redex: 
--eval recursivo
--evaluation :: TLam -> TLam

-- Teremos uma representacao para termos sem nome
data TNameL = VarN Int 
            | AbsN TNameL
            | AppN TNameL TNameL deriving (Eq, Show)


-- Contexto Gamma de variáveis livres

type Gamma =  [(Char, Int)]
gamma1 :: Gamma 
gamma1 = [('x',4),('y',3),('z',2),('a',1),('b',0)]

--ToDo
-- Definir uma função removeNames, que recebe um contexto de nomes 
-- gamma e um termo lambda com nomes, tal que as variaveis livres do 
-- termo devem estar em gamma. A função deve retornar o termo 
-- nameless correspondente

removeNames :: Gamma -> TLam -> TNameL
removeNames = undefined

-- ToDo
-- Definir uma função restoreNames, que recebe um termo lambda sem 
-- nomes e um contexto gamma e produz um termo lambda com nome.
-- Para fazer isso, precisamos escolher nomes para as variáveis ligadas.
-- Podemos inicialmente escolher qualquer nome que não aparece em gamma.

restoreNames :: Gamma -> TNameL -> TLam
restoreNames = undefined