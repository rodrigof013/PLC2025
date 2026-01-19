import subprocess
dici={
'1': [
    'pascal/teste1.pp',
    'pascal/teste2.pp',
    'pascal/teste3.pp',
    'pascal/teste4.pp',
    'pascal/teste5-2.pp'
]
,
'2': [
    'pascal/teste7.pp',
    'pascal/teste8.pp',
    'pascal/teste9.pp',
    'pascal/teste11.pp',
    'pascal/teste11-3.pp',
    'pascal/teste12.pp',
    'pascal/teste14.pp'
]
,
'3':[
    'pascal/teste5.pp',
    'pascal/teste8-2.pp',
    'pascal/teste8-3.pp',
    'pascal/teste8-4.pp',
    'pascal/teste11-2.pp'
]
}

lista = dici.get(input('1- Testes Enunciado\n2- Testes Funcionais Extra\n3- Testes com Erros\n>>>'),[])

for t in lista:
    subprocess.run(['python','.\src\pcprogram.py',t,'-q'])
    r=input('Avançar (S/N):')
    if r.lower() not in ['s','y']:
        break