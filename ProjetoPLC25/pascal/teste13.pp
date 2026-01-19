program Teste13;

label
    999,888;

const
    Pi = 3.14159;
    MaxCount = 100;
    Greeting = 'Hello World';

type
    Age = 0..10;
    Initial = char;
    Status = (Active, Inactive, Suspended);
    TVetor = ARRAY [1..10] OF integer;
    TYPE
   TData = RECORD
      dia : 1..31;
      mes : 1..12;
      ano : integer;
   END;

   TPessoa = RECORD
      id : integer;
      dataNasc : TData; { Record dentro de record }
   END;

var
    UserAge : Age;
    UserInitial : Initial;
    CurrentStatus : Status;
    Counter : integer;
    vetor : ARRAY [1..5, 1..5] OF integer;
    nome : PACKED ARRAY [1..20] OF char;
    nota : 0..20;
    cor : (vermelho, verde, azul);
    aluno : RECORD
              numero : integer;
              nota   : real;
           END;

begin
999:
    writeln('Ola, Mundo!');
888:
end.