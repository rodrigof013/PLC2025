program TesteStandardLabels;

label
   10, 20, 99;

var
   contador: integer;

begin
   contador := 0;

   writeln('A iniciar contagem com GOTO...');

10:
begin
   writeln('Contagem: ', contador);
   contador := contador + 1;

   if contador <= 3 then
      goto 10; { Salta para cima (Loop) }

   goto 20; { Salta o código seguinte }

   writeln('Esta linha nunca vai ser escrita!');
end;

20:
begin
   writeln('Ciclo terminado.');
   goto 99;
end;

99:
   writeln('Fim do programa.');
end.