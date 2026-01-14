### Грамматика

- path    := ('/' | '//')? step (('/' | '//') step)*
- step    := '.' | '..' | IDENT | '*'
- filter  := '[' ( '@'? IDENT '=' literal ) ']'
- literal := STRING | NUMBER | BOOLEAN | NULL