module Lexer where

import Data.Char

data Token
  = TokenVar Char
  | TokenPoint
  | TokenOB
  | TokenCB
  | TokenLam
  deriving (Show)

lexer :: String -> [Token]
lexer [] = []
lexer ('.' : cs) = TokenPoint : lexer cs
lexer ('(' : cs) = TokenOB : lexer cs
lexer (')' : cs) = TokenCB : lexer cs
lexer ('λ' : cs) = TokenLam : lexer cs
lexer (c : cs)
  | isSpace c = lexer cs
  | isAlpha c = lexVar (c : cs)
  | otherwise = error $ "Unknown character: " ++ [c]

lexVar :: String -> [Token]
lexVar cs =
  case span isAlpha cs of
    ("lam", rest) -> TokenLam : lexer rest
    (var, rest) -> TokenVar (head var) : lexer rest
