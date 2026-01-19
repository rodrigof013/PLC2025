program TesteAtribuicaoCorreta;
var
   Area : real;
   Lado : integer;
begin
   Lado := 5;
   Area := Lado;
   Area := 10;
   
   writeln('Area: ', Area);
end.