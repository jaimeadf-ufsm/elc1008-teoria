module Main where

import Data.List as List
import Data.Maybe as Maybe

import AST
import Lexer
import Parser

data TermNameL
  = VarN Int
  | AbsN TermNameL
  | AppN TermNameL TermNameL
  deriving (Eq, Show)

type Gamma = [Char]

-- encontra as variáveis livres de um termo
freeVariables :: Term -> [Char]
freeVariables (Var x) = [x]
freeVariables (Abs x t) = List.delete x (freeVariables t)
freeVariables (App t1 t2) = freeVariables t1 `union` freeVariables t2

-- substNitui as variáveis por índices de bruijin
removeNames :: Gamma -> Term -> TermNameL
removeNames gamma (Var x) = VarN (Maybe.fromJust (List.elemIndex x gamma))
removeNames gamma (Abs x t) = AbsN (removeNames (x : gamma) t)
removeNames gamma (App t1 t2) = AppN (removeNames gamma t1) (removeNames gamma t2)

-- restaura os nomes das variáveis a partir dos índices de bruijin
restoreNames :: Gamma -> TermNameL -> Term
restoreNames gamma (VarN x) = Var (gamma !! x)
restoreNames gamma (AbsN t) =
  let x = head (filter (`notElem` gamma) ['a' .. 'z'])
   in Abs x (restoreNames (x : gamma) t)
restoreNames gamma (AppN t1 t2) = App (restoreNames gamma t1) (restoreNames gamma t2)

-- desloca as variáveis de um termo t por d se d >= c
shift :: Int -> Int -> TermNameL -> TermNameL
shift d c (VarN x) = if x >= c then VarN (x + d) else VarN x
shift d c (AbsN t) = AbsN (shift d (c + 1) t)
shift d c (AppN t1 t2) = AppN (shift d c t1) (shift d c t2)

-- substitui a variável x por s no termo t
substN :: Int -> TermNameL -> TermNameL -> TermNameL
substN x s (VarN y) = if x == y then s else VarN y
substN x s (AbsN t) = AbsN (substN (x + 1) (shift 1 0 s) t)
substN x s (AppN t1 t2) = AppN (substN x s t1) (substN x s t2)

-- verifica se o termo é um valor, ou seja, não é uma aplicação
isValueN :: TermNameL -> Bool
isValueN (VarN _) = True
isValueN (AbsN _) = True
isValueN (AppN _ _) = False

-- avalia um termo, aplicando a semântica operacional call-by-value
evalN :: TermNameL -> TermNameL
evalN (AppN (AbsN t12) t2)
  | isValueN t2 = shift (-1) 0 (substN 0 (shift 1 0 t2) t12) -- E-APPABS
evalN (AppN t1 t2)
  | isValueN t1 = AppN t1 (evalN t2) -- E-APP2
  | otherwise = AppN (evalN t1) t2 -- E-APP1
evalN (AbsN t) = AbsN t
evalN (VarN x) = VarN x

-- avalia um termo até que não haja mais redex
evalAllN :: TermNameL -> TermNameL
evalAllN t =
  let t' = evalN t
   in if t' == t then t else evalAllN t'

-- executa a avaliação de um termo, restaurando os nomes das variáveis
evalAll :: Term -> Term
evalAll term =
  let gamma = freeVariables term
      namelessTerm = removeNames gamma term
      evaluatedTerm = evalAllN namelessTerm
   in restoreNames gamma evaluatedTerm

-- formata o termo avaliado para uma string
formatLamb :: Term -> String
formatLamb (Var x) = [x]
formatLamb (Abs x t) = "(λ" ++ [x] ++ "." ++ formatLamb t ++ ")"
formatLamb (App t1 t2) = "(" ++ formatLamb t1 ++ " " ++ formatLamb t2 ++ ")"

main :: IO ()
main = getContents >>= putStrLn . formatLamb . evalAll . parseLamb . lexer
-- main = getContents >>= putStrLn . formatLamb . parseLamb . lexer
-- main = putStrLn (formatLamb exC1PlusC1)