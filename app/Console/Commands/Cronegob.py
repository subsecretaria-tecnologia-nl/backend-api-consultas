import time
from Searchdata import *
from Savedata import *

# Cronometro de tiempo / inicio
t1_start = time.time()

egob = consulta_egob()

if egob['error'] == 1:
    print(egob['msg'])
else:
    data = egob['data']
    guardado = inserta_data(data)
    if(guardado['error'] == 1):
        print(guardado['msg'])
    else:
        print("Elementos procesados: ",len(data))

t1_stop = time.time()


print("Tiempo transcurrido durante el proceso (segundos): ", round(t1_stop-t1_start,4))


