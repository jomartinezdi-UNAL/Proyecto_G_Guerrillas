# Resultados de la simulación

Esta carpeta contiene tablas en formato CSV con los valores numéricos reportados
en el informe del proyecto. Los archivos organizan resultados ya obtenidos;
no ejecutan simulaciones ni generan datos nuevos.

## Archivos

- `exponentes_alpha.csv`: exponentes estimados para cada valor de `nu` en las
  implementaciones C++ y Python, junto con la diferencia porcentual reportada.
- `parametros_simulacion.csv`: parámetros y métricas de las ejecuciones
  principales, incluidos tamaño del sistema, probabilidad de fragmentación,
  número de pasos/eventos y tiempo registrado.

## Consideraciones para interpretar los datos

1. La referencia teórica usada para comparar el exponente es `alpha = 2.5`.
2. La diferencia porcentual entre implementaciones está calculada respecto al
   resultado de Python, tal como se indica en el informe.
3. Las ejecuciones de C++ y Python no son estrictamente equivalentes: C++
   acumula 120 000 muestras durante la ejecución, mientras que Python analiza
   el estado final. Por ello, los tiempos reportados son los de esas ejecuciones
   particulares y no una comparación controlada del costo por evento.
4. En Python se reportaron 15 729 grupos al final y una suma de tamaños de
   30 000, consistente con la conservación de la fuerza total.
5. Los campos marcados como `No reportado` o `No aplica` no deben interpretarse
   como cero ni como resultados faltantes que se hayan estimado.

## Unidades y columnas

- `nu`: parámetro de fragmentación, adimensional.
- `alpha_cpp`, `alpha_python`: exponentes estimados.
- `diferencia_porcentual`: diferencia porcentual reportada.
- `tiempo`: segundos.
- `pasos_eventos`: cantidad de pasos o eventos de la simulación principal.
