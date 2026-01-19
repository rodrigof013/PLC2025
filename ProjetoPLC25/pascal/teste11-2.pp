program TestePerdaDados;
var
   NotaFinal : integer;
   NotaCalculada : real;
begin
   NotaCalculada := 15.5;
   { ERRO ESPERADO: Tipo incompatível. }
   NotaFinal := NotaCalculada; 
   
   writeln(NotaFinal);
end.