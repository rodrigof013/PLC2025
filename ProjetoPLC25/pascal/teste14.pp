program FibonacciRecursivo;

var
   n, resultado: integer;

function Fibonacci(x: integer): integer;
begin
   if x <= 1 then
      Fibonacci := x
   else
      Fibonacci := Fibonacci(x - 1) + Fibonacci(x - 2);
end;

begin
   writeln('Digite o valor de n:');
   readln(n);
   resultado := Fibonacci(n);
   writeln('Fibonacci(', n, ') = ', resultado);
end.