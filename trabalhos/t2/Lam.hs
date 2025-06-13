-- Código 10/06/2025
module Main where

import Data.Maybe as Maybe
import Data.List as List

--exemplo
-- AST do Calculo-lambda
data TLam = Var Char
          | Abs Char TLam
          | App TLam TLam
        deriving (Eq, Show)

data TNameL = VarN Int
            | AbsN TNameL
            | AppN TNameL TNameL
            deriving (Eq, Show)
        
exC0 :: TLam
exC0 = Abs 's' (Abs 'z' (Var 'z'))

exC1 :: TLam
exC1 = Abs 's' (Abs 'z' (App (Var 's') (Var 'z')))

exC2 :: TLam
exC2 = Abs 's' (Abs 'z' (App (Var 's') (App (Var 's') (Var 'z'))))

exPlus :: TLam
exPlus = Abs 'm' (Abs 'n' (Abs 's' (Abs 'z' (App (App (Var 'm') (Var 's')) (App (App (Var 'n') (Var 's')) (Var 'z'))))))

exC1PlusC0 :: TLam
exC1PlusC0 = App (App exPlus exC1) exC0

exC1PlusC1 :: TLam
exC1PlusC1 = App (App exPlus exC1) exC1

type Gamma = [Char]

-- encontra as variáveis livres de um termo
freeVariables :: TLam -> [Char]
freeVariables (Var x) = [x]
freeVariables (Abs x t) = List.delete x (freeVariables t)
freeVariables (App t1 t2) = freeVariables t1 `union` freeVariables t2

-- substitui as variáveis por índices de bruijin
removeNames :: Gamma -> TLam -> TNameL
removeNames gamma (Var x) = VarN (Maybe.fromJust (List.elemIndex x gamma))
removeNames gamma (Abs x t) = AbsN (removeNames (x:gamma) t)
removeNames gamma (App t1 t2) = AppN (removeNames gamma t1) (removeNames gamma t2)

-- restaura os nomes das variáveis a partir dos índices de bruijin
restoreNames :: Gamma -> TNameL -> TLam
restoreNames gamma (VarN x) = Var (gamma !! x)
restoreNames gamma (AbsN t) = let x = head (filter (`notElem` gamma) ['a'..'z'])
                              in Abs x (restoreNames (x:gamma) t)
restoreNames gamma (AppN t1 t2) = App (restoreNames gamma t1) (restoreNames gamma t2)

-- desloca as variáveis de um termo t por d se d >= c
shift :: Int -> Int -> TNameL -> TNameL
shift d c (VarN x) = if x >= c then VarN (x + d) else VarN x
shift d c (AbsN t) = AbsN (shift d (c + 1) t)
shift d c (AppN t1 t2) = AppN (shift d c t1) (shift d c t2)

-- substitui a variável x por s no termo t
subst :: Int -> TNameL -> TNameL -> TNameL
subst x s (VarN y) = if x == y then s else VarN y
subst x s (AbsN t) = AbsN (subst (x + 1) (shift 1 0 s) t)
subst x s (AppN t1 t2) = AppN (subst x s t1) (subst x s t2)

-- verifica se o termo é um valor, ou seja, não é uma aplicação
isValue :: TNameL -> Bool
isValue (VarN _) = True
isValue (AbsN _) = True
isValue (AppN _ _) = False

-- avalia um termo, aplicando a semântica operacional call-by-value
eval :: TNameL -> TNameL
eval (AppN (AbsN t12) t2)
    | isValue t2 = shift (-1) 0 (subst 0 (shift 1 0 t2) t12)
eval (AppN t1 t2)
    | isValue t1 = AppN t1 (eval t2)
    | otherwise = AppN (eval t1) t2
eval (AbsN t) = AbsN (eval t)
eval (VarN x) = VarN x

-- avalia um termo até que não haja mais redex
evalAll :: TNameL -> TNameL
evalAll t =
    let t' = eval t
    in if t' == t then t else evalAll t'

-- executa a avaliação de um termo, restaurando os nomes das variáveis
run :: TLam -> TLam
run term = 
    let gamma = freeVariables term
        namelessTerm = removeNames gamma term
        evaluatedTerm = evalAll namelessTerm
    in restoreNames gamma evaluatedTerm

main :: IO()
main = do
    let result = run exC1PlusC1
    print result
