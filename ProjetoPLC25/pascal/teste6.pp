program SomaNumeros;
var 
    N, N1, N2: integer;
    R: real;
    fa : array[1..10,1..20] of integer;
    epst : array[1..10] of integer;
    aluno : RECORD
              numero : integer;
              nota   : real;
           END;
const
    N3 = 'JoseNegro';
begin
    write('Introduza um numero: ');
    readln(N1);
    write('Introduz outro: ');
    readln(N2);
    N := N1 + N2;
    epst[1] := 1;
    fa[1][1]:= epst[1];
    epst[2]:=fa[1][1];
end.