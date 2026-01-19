program BinarioParaInteiro;

type
    string = packed array [1..50] of char;

function Length(s: string): integer;
var
    i: integer;
begin
    i := 1;
    while (i <= 50) and (s[i] <> ' ') do
    begin
        i := i + 1;
    end;
    Length := i - 1;
end;

function BinToInt(bin: string): integer;
var  
    i, valor, potencia: integer;
begin  
    valor := 0;  
    potencia := 1;
    
    for i := Length(bin) downto 1 do 
    begin 
        if bin[i] = '1' then      
            valor := valor + potencia;    
        potencia := potencia * 2;
    end;  
    
    BinToInt := valor;
end;

var  
    bin: string;  
    valor: integer;
begin  
    writeln('Introduza uma string binária:');  
    readln(bin);  
    
    valor := BinToInt(bin);  
    
    writeln('O valor inteiro correspondente é: ', valor);
end.