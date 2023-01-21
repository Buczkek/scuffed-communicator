import subprocess
from time import sleep



def factorial_task(n:int):
    proc = subprocess.Popen(f'echo \'{n}\' | ./a.out', stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()
    mes = out.decode()
    sleep(10)
    print(f'Odp to {mes}')
    return mes