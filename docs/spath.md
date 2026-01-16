### Грамматика

- path    := (SLASH | DOUBLE_SLASH)? step ( (SLASH | DOUBLE_SLASH) step )*
- step    := DOT | IDENT filter*
- filter  := '[' (':'? IDENT) (EQ | NEQ) literal ']'
- literal := STRING | NUMBER | BOOLEAN | NULL