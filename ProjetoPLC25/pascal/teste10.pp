program TesteLogico;
var
   A, B : boolean;
begin
   A := true;
   B := false;
   
   (* Este e um comentario antigo *)
   if (A or B) and not (A and B) then
      writeln('XOR logico simulado');
      
   { Comentario no meio da linha } A := false; // Comentario ate ao fim
   
   if A <> B then
      writeln('Diferentes');
end.