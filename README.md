# Simulación de un proceso de guerra de guerrillas

## Descripción del proyecto

Este proyecto desarrolla una simulación computacional de un modelo estocástico de fragmentación y fusión aplicado al estudio de un proceso de guerra de guerrillas.

El modelo representa un sistema compuesto por unidades de ataque que pueden fragmentarse o fusionarse mediante reglas probabilísticas. A partir de estas interacciones se estudia la distribución estadística de los tamaños de las unidades y su posible comportamiento mediante una ley de potencia.

El trabajo contempla dos implementaciones independientes, desarrolladas en **Python y C++**, cuyos resultados se comparan desde el punto de vista estadístico y computacional.

## Objetivos

- Implementar computacionalmente las reglas de selección, fragmentación y fusión.
- Estudiar la distribución de tamaños de las unidades del sistema.
- Estimar el exponente de la ley de potencia y contrastarlo con el valor teórico de referencia \(\alpha=2.5\).
- Analizar la influencia del parámetro de fragmentación \(\nu\).
- Comparar los resultados obtenidos mediante Python y C++.
- Evaluar y documentar el desempeño de ambas implementaciones.

## Modelo y parámetros

El sistema conserva una fuerza total \(N\), inicialmente distribuida en unidades de tamaño uno.

La probabilidad de seleccionar una unidad depende proporcionalmente de su tamaño. Posteriormente, esta puede fragmentarse con probabilidad \(\nu\) o participar en un proceso de fusión con probabilidad \(1-\nu\).

La distribución de tamaños se analiza mediante la expresión:

\[
n_s \propto s^{-\alpha}
\]

Para las simulaciones finales se utilizó:

| Parámetro | Valor |
|---|---:|
| Fuerza total \(N\) | 30 000 |
| Valores de \(\nu\) | 0.005, 0.01, 0.05 y 0.1 |
| Exponente teórico de referencia | 2.5 |

## Estructura del repositorio

Proyecto_G_Guerrillas/
│
├── figures/
│   └── Gráficas finales de las simulaciones.
│
├── notebooks/
│   └── Cuadernos Jupyter de simulación y análisis.
│
├── report/
│   └── Informe científico en LaTeX y bibliografía.
│
├── results/
│   └── Resultados numéricos y datos exportados.
│
├── src/
│   └── Código fuente de las implementaciones.
│
├── README.md
└── requirements.txt


## Tecnologías utilizadas

- **Python:** implementación y análisis numérico.
- **C++:** implementación computacional del modelo.
- **Jupyter Notebook:** desarrollo y documentación de las simulaciones.
- **NumPy:** operaciones numéricas y manipulación de datos.
- **Matplotlib:** generación de gráficas.
- **SciPy:** herramientas de análisis científico.
- **LaTeX / Overleaf:** elaboración del informe técnico.
- **GitHub:** almacenamiento, control de versiones y colaboración.

## Instalación de dependencias

Para instalar las bibliotecas necesarias de Python, ejecutar:

pip install -r requirements.txt

## Resultados

Las simulaciones permiten comparar las distribuciones de tamaños y los exponentes estimados mediante ambas implementaciones. Los resultados, las figuras y su interpretación se encuentran organizados en los directorios correspondientes.

## Trabajo colaborativo

El desarrollo del proyecto se realizó mediante distribución de actividades y seguimiento de responsabilidades utilizando Jira. GitHub se empleó como repositorio central para organizar y conservar los archivos del proyecto y sus versiones.

## Referencias

El modelo se basa en los trabajos de Johnson et al. sobre regularidades estadísticas en conflictos armados y procesos de fragmentación y fusión. Las referencias bibliográficas completas se encuentran en el directorio `report/`.
