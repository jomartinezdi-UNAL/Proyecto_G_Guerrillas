"""
Implementacion Python del modelo de fragmentacion y fusion.
Codigo consolidado a partir del notebook simulacion_guerrilla_PY(2).ipynb.
ADVERTENCIA: ejecutar este archivo vuelve a correr las simulaciones
principales y el barrido de nu, que pueden tardar varias horas.
"""


# ===== Codigo de la celda 5 del notebook original =====
import numpy as np
import matplotlib.pyplot as plt
import time

N = 30_000
NU = 0.01
BARRIDOS = 300 # El número de barridos se toma según la estabilidad de las gráficas, observada empíricamente.
SEMILLA = 42 # Número para usar en la generación de números aleatorios.

rng = np.random.default_rng(SEMILLA)
print(f"N={N:,}, nu={NU}, barridos={BARRIDOS}, pasos={N*BARRIDOS:,}")


# ===== Codigo de la celda 7 del notebook original =====
def seleccionar_grupo(tamanos, rng):
    """Elige un grupo con probabilidad proporcional a su tamaño."""
    pesos = np.asarray(tamanos, dtype=float)
    probabilidades = pesos / pesos.sum()
    return int(rng.choice(len(tamanos), p=probabilidades))


def paso(tamanos, nu, rng):
    """Ejecuta un paso: La fragmentación ocurre con probabilidad nu, y ocurre fusión en otro caso."""
    tamanos = list(tamanos)
    i = seleccionar_grupo(tamanos, rng)
    si = tamanos.pop(i)
    if rng.random() < nu:
        # Fragmentación completa: s_i unidades nuevas de tamaño 1.
        tamanos.extend([1] * si)
    elif len(tamanos) == 0:
        # Caso límite: cuando solo hay un grupo, no existe otro con el cual fusionarlo.
        tamanos.append(si)
    else:
        # Fusión con otro grupo seleccionado proporcionalmente a su tamaño.
        j = seleccionar_grupo(tamanos, rng)
        sj = tamanos.pop(j)
        tamanos.append(si + sj)

    return tamanos


def contar_tamanos(tamanos, N):
    """Cuenta el numero de grupo de tamaño s"""
    n_s = np.zeros(N + 1, dtype=np.int64)
    valores, conteos = np.unique(tamanos, return_counts=True)
    n_s[valores] = conteos
    return n_s


# ===== Codigo de la celda 9 del notebook original =====
estado = [1] * N
historial_M = [] # Cantidad total de grupos
historial_n1 = [] # Cantidad de grupos de tamaño 1

inicio = time.time()
for b in range(BARRIDOS):
    for _ in range(N):
        estado = paso(estado, NU, rng)

    # Comprobación de la condición de la suma
    assert sum(estado) == N
    historial_M.append(len(estado))
    historial_n1.append(estado.count(1))

print(f"Tiempo transcurrido: {time.time()-inicio:.1f} s")
print(f"Grupos al final: {len(estado):,}")
print(f"Suma de tamaños: {sum(estado):,} (si es igual a {N:,}, todo nice)")


# ===== Codigo de la celda 11 del notebook original =====
barridos = np.arange(1, BARRIDOS + 1)
fig, ax = plt.subplots(1, 2, figsize=(12, 4))
ax[0].plot(barridos, np.array(historial_M) / N, lw=1)
ax[0].set_xlabel("Barrido (N pasos)")
ax[0].set_ylabel("Número de grupos / N")
ax[0].set_title("Evolución del número de grupos")
ax[1].plot(barridos, np.array(historial_n1) / N, lw=1)
ax[1].set_xlabel("Barrido (N pasos)")
ax[1].set_ylabel("Grupos de tamaño 1 / N")
ax[1].set_title("Evolución de los grupos unitarios")
for a in ax: a.grid(alpha=0.25)
plt.tight_layout()
plt.show()

# Comparación entre la evolución del número de grupos y los grupos unitarios. Se verifica que no tienen el mismo comportamiento.

M_norm = np.array(historial_M) / N
n1_norm = np.array(historial_n1) / N

plt.figure(figsize=(8, 4))
plt.plot(barridos, M_norm - n1_norm)
plt.axhline(0, color="black", lw=0.8)
plt.xlabel("Barrido (N pasos)")
plt.ylabel(r"$(M-n_1)/N$")
plt.title("Proporción de grupos no unitarios")
plt.grid(alpha=0.25)
plt.tight_layout()
plt.show()


# ===== Codigo de la celda 13 del notebook original =====
n_s = contar_tamanos(estado, N)
s = np.arange(1, N + 1)
mascara = n_s[1:] > 0

fig, ax = plt.subplots(figsize=(6.4, 6))

ax.loglog(
    s[mascara],
    n_s[1:][mascara] / n_s[1],
    "o",
    mfc="none",
    ms=4,
    color="k",
    label=f"Simulación (N={N:,}, ν={NU})"
)

sg = np.logspace(0, np.log10(2*N), 100)
ax.loglog(
    sg,
    sg**-2.5,
    "-",
    color="C3",
    lw=1.5,
    label=r"Pendiente $-2.5$"
)

ax.set_xlabel(r"$s$ (fuerza de ataque)")
ax.set_ylabel(r"$n_s/n_1$")
ax.set(
    xlim=(0.8, 2*N),
    ylim=(1e-10, 2),
    title="Distribución de tamaños de los grupos"
)

ax.legend()
plt.tight_layout()
plt.show()


# ===== Codigo de la celda 15 del notebook original =====
S_MIN = 2
S_MAX = 30

m = (s >= S_MIN) & (s <= S_MAX) & (n_s[1:] > 0)

if m.sum() >= 2:
    pendiente, intercepto = np.polyfit(
        np.log10(s[m]),
        np.log10(n_s[1:][m]),
        1
    )
    alpha = -pendiente

    print(f"Intervalo de ajuste: s entre {S_MIN} y {S_MAX}")
    print(f"Pendiente log-log = {pendiente:.3f}")
    print(f"Exponente exploratorio alpha = {alpha:.3f}")

    fig, ax = plt.subplots(figsize=(6.4, 6))

    ax.loglog(
        s[mascara],
        n_s[1:][mascara] / n_s[1],
        "o",
        mfc="none",
        ms=4,
        color="k",
        label="Simulación"
    )

    ax.loglog(
        s[m],
        10**intercepto * s[m]**pendiente / n_s[1],
        "-",
        color="C3",
        lw=1.5,
        label=fr"Ajuste: $\alpha={alpha:.2f}$"
    )

    ax.set_xlabel(r"$s$ (fuerza de ataque)")
    ax.set_ylabel(r"$n_s/n_1$")
    ax.set_title("Distribución de tamaños de los grupos")
    ax.legend()

    plt.tight_layout()
    plt.show()

else:
    print("No hay suficientes tamaños en el intervalo para realizar el ajuste. Revisa S_MIN y S_MAX.")


# ===== Codigo de la celda 17 del notebook original =====
def simular(N, nu, barridos, semilla):
    rng_local = np.random.default_rng(semilla)
    estado = [1] * N
    for _ in range(barridos):
        for _ in range(N):
            estado = paso(estado, nu, rng_local)
    return estado

BARRIDOS_NU = 20
VALORES_NU = [0.005, 0.01, 0.05, 0.1]

resultados_alpha = []

colores = plt.cm.viridis(np.linspace(0, 1, len(VALORES_NU)))
s_guia = np.logspace(0, np.log10(2*N), 100)

fig, ax = plt.subplots(figsize=(6.5, 5))

for k, nu in enumerate(VALORES_NU):
    estado_nu = simular(N, nu, BARRIDOS_NU, SEMILLA + k + 1)
    dist = contar_tamanos(estado_nu, N)

    ss = np.arange(1, N + 1)
    ok = dist[1:] > 0

    ax.loglog(
        ss[ok],
        dist[1:][ok] / dist[1],
        ".",
        ms=3,
        color=colores[k],
        label=fr"$\nu$={nu}"
    )

    intervalo = (
        (ss >= S_MIN) &
        (ss <= S_MAX) &
        (dist[1:] > 0)
    )

    if intervalo.sum() >= 2:
        p, _ = np.polyfit(
            np.log10(ss[intervalo]),
            np.log10(dist[1:][intervalo]),
            1
        )
        resultados_alpha.append((nu, -p))

ax.loglog(
    s_guia,
    s_guia**-2.5,
    "k-",
    lw=1.2,
    label=r"$s^{-2.5}$"
)

ax.set(
    xlim=(0.8, 2*N),
    ylim=(1e-10, 2),
    title=r"Distribuciones para distintos $\nu$"
)

ax.set_xlabel(r"$s$")
ax.set_ylabel(r"$n_s/n_1$")
ax.legend(fontsize=8.5, ncol=2, loc="upper right")

plt.tight_layout()
plt.show()

for nu, alpha in resultados_alpha:
    print(f"ν={nu:.3f}: α aproximado={alpha:.3f}")
