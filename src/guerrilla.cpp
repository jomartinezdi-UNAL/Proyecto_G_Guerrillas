#include <chrono>
#include <cstdio>
#include <cstdlib>
#include <map>
#include <random>
#include <string>

// total = suma de s * L[s] sobre el mapa actual y nos devuelve la fuerza s de la unidad elegida.
// nsteps es el número total de pasos del algoritmo.

using Partition = std::map<int, long long>;                                            // aquí fuerza s -> numero de unidades

static int pick_size_biased(const Partition& L, long long total, std::mt19937_64& rng){
    std::uniform_int_distribution<long long> U(0, total - 1);
    long long r = U(rng), cum = 0;                                                     // r que es un entero uniforme en [0,N)
    for (const auto& kv : L){                                                          // va recorriendo el mapa acumulando s * L[s]
        cum += static_cast<long long>(kv.first) * kv.second;
        if (r < cum) return kv.first;                                                  // en el caso de que r caiga en el tramo de la fuerza s
    }
    return L.rbegin()->first;                                                          // no deberia ocurrir (ojalá)
}


static void remove_one(Partition& L, int s){                                           // Aquí se quita una unidad de fuerza s del mapa (se borra la entrada si queda en 0).
    auto it = L.find(s);
    if (--(it->second) == 0) L.erase(it);
}


int main(int argc, char** argv){
    if (argc < 6){
        std::fprintf(stderr, "Uso: %s N nu nsteps seed out_prefix\n", argv[0]);
        return 1;
    }

    const long long N = std::atoll(argv[1]);                                       // Es la fuerza total (la conservada)
    const double nu = std::atof(argv[2]);                                          // Es la probabilidad de fragmentación
    const long long nsteps = std::atoll(argv[3]);                                  // Son los pasos totales
    const unsigned long long seed = std::strtoull(argv[4], nullptr, 10);
    const std::string prefix = argv[5];

    std::mt19937_64 rng(seed);                                                     // Para los números aleatorios
    std::uniform_real_distribution<double> U01(0.0, 1.0);

    Partition L;                                                                   // La condición inicial es N unidades de fuerza 1
    L[1] = N;

    Partition acc;                                                                 // Es el acumulador de L[s] sobre las muestras
    long long nsamples = 0;                                                        // Es el número de muestras acumuladas
    const long long sample_every = N / 4;                                          // Se muestrea 4 veces cada N pasos


    const auto t0 = std::chrono::steady_clock::now();                              // Aquí ya va el algoritmo y como queremos ver el tiempo, se contabiliza desde acá


    for (long long step = 0; step < nsteps; ++step){                               // Elegimos una unidad i proporcional a s_i y la sacamos del sistema
        int si = pick_size_biased(L, N, rng);
        remove_one(L, si);

        if (U01(rng) < nu){                                                        // Es la fragmentacion, i a s_i unidades de fuerza 1
            L[1] += si;
        }
        else{                                                                      // Coalescencia con otra unidad, j proporcional a s_j (j != i)
            long long rest = N - si;                                               // fuerza total sin contar a i
            if (rest == 0) {                                                       // i era la unica unidad y no hay con quien fusionarse
                L[si] += 1;
            }
            else{
                int sj = pick_size_biased(L, rest, rng);
                remove_one(L, sj);
                L[si + sj] += 1;                                                   // Es la nueva unidad de fuerza s_i + s_j
            }
        }

        if ((step % sample_every) == 0) {                                          // Se acumula el histograma L[s] para promediarlo después
            for (const auto& kv : L) acc[kv.first] += kv.second;
            ++nsamples;
        }
    }                                                                              // Hasta aquí llega el algoritmo


    const double dt = std::chrono::duration<double>(std::chrono::steady_clock::now() - t0).count();


    FILE* fh = std::fopen((prefix + "_hist.txt").c_str(), "w");                                       // Para guardar el histograma promediado <n_s>
    std::fprintf(fh, "# s  <n_s>   (N=%lld nu=%g muestras=%lld)\n", N, nu, nsamples);
    for (const auto& kv : acc)
        std::fprintf(fh, "%d %.8g\n", kv.first, static_cast<double>(kv.second) / nsamples);
    std::fclose(fh);

    std::printf("[C++] N=%lld nu=%g | %lld pasos | muestras=%lld | "
                "TIEMPO DE EJECUCION DEL ALGORITMO = %.3f s\n",
                N, nu, nsteps, nsamples, dt);
    return 0;
}
