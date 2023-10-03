import random
import math


def read_input_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        k, n, t, c = map(int, lines[0].split())
        v = list(map(int, lines[1].split(',')))
        w = list(map(int, lines[2].split(',')))
    return k, n, t, c, v, w


# Funkcja wyżarzania
def simulated_annealing_knapsack(k, n, t, c, v, w):
    # Funkcja sumująca wartości i wagi w danych kombinacjach
    def objective_function(combination):
        total_value = sum(v[i] for i in range(n) if combination[i])
        total_weight = sum(w[i] for i in range(n) if combination[i])
        return total_value, total_weight

    # Funkcja perturbacji dokonująca losowej zmiany jednego bitu wektora
    def perturbation(combination):
        # Zamiana randomowej wartości w kombinacji bitów, 0 na 1, 1 na 0
        combination[random.randint(0, n - 1)] = 1 - combination[random.randint(0, n - 1)]

    # Inicjalizacja wektora binarnego o randomowej wartości i długości n
    combination = [random.randint(0, 1) for _ in range(n)]

    # Inicjalizacja zmiennych
    best_combination = []
    best_value, best_weight = objective_function(combination)
    temperature = t
    iterations = 0

    while temperature > 0:
        # Perturbacja w celu wprowadzenia losowej zmiennej w wartościach zmiennej combination
        perturbation(combination)
        # Obliczenie zsumowanej wartości new_value, new_weight
        new_value, new_weight = objective_function(combination)
        # Wewnetrzna pętla ma na celu kontynuowanie perturbacji i obliczanie wartości funkcji celu,
        # dopóki waga kombinacji nie przekracza kombinacji plecaka. Dopiero gdy zostanie znaleziona kombinacja
        # o wadze mniejszej lub równej pojemności plecaka, zostaje wykonany kolejny warunek if new_weight <= k
        # i dalsza ocena tej kombinacji w celu znalezienia lepszego rozwiązania.
        # Petla iterująca dopóki temperatura nie osiągnie wartości ujemnej
        while new_weight > k:
            # Perturbacja w celu wprowadzenia losowej zmiany
            perturbation(combination)
            # Obliczanie wartości funkcji celu new_value i wagi new_weight dla nowo zaktualizowanej kombinacji
            new_value, new_weight = objective_function(combination)
            if new_weight <= k:
                # Sprawdzenie czy nowa wartość jest lepsza o dotychczasowej lub
                # czy wylosowana liczba losowa jest mniejsza od ujemnej wartości wykładniczej
                # różnicy miedzy nowa wartosci a najlepsza wartoscia
                # Im większa różnica tym mniejsza szansa ze to rozwiazanie zostanie zaakceptowane
                if new_value > best_value or random.random() < math.exp(-((new_value - best_value) / temperature)):
                    best_combination = combination
                    best_value = new_value
                    best_weight = new_weight

        temperature -= c
        iterations += 1

        print(f"Iteration number: {iterations}, Best value: {new_value}, Best weight: {best_weight}, Best combination: {best_combination}")

    return best_combination, best_weight, best_value, iterations


# Wczytanie ścieżki do pliku
while True:
    try:
        file_path = input("Type file path: ")
        k, n, t, c, v, w = read_input_file(file_path)
        break
    except FileNotFoundError:
        print("File not found. The path was incorrect. Try once again.")

best_combination, weight, value, num_iterations = simulated_annealing_knapsack(k, n, t, c, v, w)

# Wynik, czyli najlepsza kombinacja w postaci wektoru, suma wartości i wag
print("\nResult:")
print("Best solution found:", best_combination)
print("Total weight:", weight)
print("Total value:", value)