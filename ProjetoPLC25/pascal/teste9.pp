program RegistoAluno;

type
   TAluno = record
      Numero : integer; { Trocamos 'Nome' (string) por 'Numero' (integer) }
      Nota : real;
      Aprovado : boolean;
   end;

var
   Turma : array[1..30] of TAluno;
   UmAluno : TAluno;

begin
   { Acesso aos campos do registo usando o ponto . }
   UmAluno.Numero := 202301;
   UmAluno.Nota := 15.5;
   UmAluno.Aprovado := true;
   
   { Atribuição a uma posição do array }
   Turma[1] := UmAluno;
   
   if Turma[1].Nota > 9.5 then
      writeln('O aluno numero ', Turma[1].Numero, ' passou.');
end.