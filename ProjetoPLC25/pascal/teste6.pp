program SomaNumeros;
var 
    N, N1, N2: integer;
    R: real;
    fa : array[1..10,1..20] of integer;
    epst : array[1..10] of real;
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
    epst[1] := 1.2;
    fa[1][fa[1][1]]:= 1;
    aluno.numero:=2;
    aluno.nota:=10.2;
    write(N1, ' + ', N2, ' é igual a ', N);
end.