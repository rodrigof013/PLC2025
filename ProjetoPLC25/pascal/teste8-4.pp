program ErroCola;
var
   X:integer;
begin
   X := 10;
   { 'Ifthen' vira uma variável nova, não são keywords! }
   { Erro Esperado: "Erro de Sintaxe: esperava 'then', recebeu 'writeln'" ou "Variável Ifthen não declarada" }
   if(X>5)Ifthen
      writeln('Ola');
end.