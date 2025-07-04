module AST where

data Term
  = Abs Char Term
  | App Term Term
  | Var Char
  deriving (Show)