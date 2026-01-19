program ErroIf;
var
   X : integer;
begin
   X := 10;
   { X + 5 dá 15 (Integer), não dá Boolean! }
   { Erro Esperado: "A condição do IF deve ser booleana" }
   if (X + 5) then
      writeln('Isto não deve compilar');
end.