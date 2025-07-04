{
module Parser where

import AST
import Lexer
}

%name parseLamb
%tokentype { Token }
%error { parseError }

%token
	lam { TokenLam } 
	var { TokenVar $$ }
	'.' { TokenPoint }
	'(' { TokenOB }
	')' { TokenCB }
%%

AppTerm : AppTerm Atom { App $1 $2 }
        | Atom         { $1 }

Atom : lam var '.' AppTerm { Abs $2 $4 }
     | var                 { Var $1 }
     | '(' AppTerm ')'     { $2 }

{
parseError :: [Token] -> a
parseError b = error "Parse error"
}
