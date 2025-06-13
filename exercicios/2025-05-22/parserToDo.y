{
module ParserToDo where
import Data.Char
}

%name parserlamb
%tokentype { Token }
%error { parseError }

%token
	lam { TokenLam } 
	var { TokenVar $$ }
	'.' { TokenPoint }
	'(' { TokenOB }
	')' { TokenCB }
	
%%

-- regras de producao da gramatica

CalcLamb : lam var '.' CalcLamb               { Abs $2 ( $4 ) }
         | lam var '.' '('CalcLamb')'         { Abs $2 ( $5 ) }
	   | '(' lam var '.' '('CalcLamb')' ')' { ( Abs $3 ( $6 ) ) }
	   | CalcLamb CalcLamb                  { ( App $1 $2 ) }
	   | '(' CalcLamb CalcLamb ')'          { ( App $2 $3 ) }
	   | '(' CalcLamb ')' '(' CalcLamb ')'  { ( App $2 $5 ) }
	   | var                                { Var $1 }

{

parseError :: [Token] -> a
parseError b = error "Parse Error"

data Term 
		= Abs Char Term
		| App Term Term
		| Var Char
	deriving Show

data Token 
		= TokenVar Char
		| TokenPoint
		| TokenOB
		| TokenCB
		| TokenLam 
	deriving Show

-- ToDo: implementar a função lexer abaixo
lexer :: String -> [Token]
lexer [] = []
lexer (c:cs)
	| isSpace c = lexer cs
	| isAlpha c = TokenVar c : lexer cs
lexer ('.':cs) = TokenPoint : lexer cs
lexer ('(':cs) = TokenOB : lexer cs
lexer (')':cs) = TokenCB : lexer cs
lexer ('\\':cs) = TokenLam : lexer cs

main = getContents >>= print . parserlamb .lexer

}
