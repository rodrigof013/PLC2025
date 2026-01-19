program AdivinhaNumero;
var
  secreto, palpite: Integer;
begin
  secreto := 42;

  writeln('--- Jogo da Adivinhação ---');

  repeat
    write('Tenta adivinhar o número secreto: ');
    readln(palpite);

    if palpite < secreto then
      writeln('É maior!')
    else if palpite > secreto then
      writeln('É menor!');

  until (palpite = secreto); { O ciclo só para quando esta condição for VERDADE }

  writeln('Parabéns! Acertaste.');
end.