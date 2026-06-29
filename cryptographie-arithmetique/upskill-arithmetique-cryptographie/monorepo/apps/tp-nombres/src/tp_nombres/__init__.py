# Aucun n'import ne doit être fait dans ce fichier


from operator import add


def nombre_entier(n: int) -> str:
    return "S" * n + "0"


def S(n: str) -> str:
    return "S" + n


def addition(a: str, b: str) -> str:
    if a == "0":
        return b
    n = a[1:]
    return S(addition(n, b))


def multiplication(a: str, b: str) -> str:
    if a == "0":
        return "0"
    n= a[1:]
    tmp = multiplication(n, b)
    return addition(tmp, b)
    
def facto_ite(n: int) -> int:
    if n == 0:
        return 1
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def facto_rec(n: int) -> int:
    if n == 0:
        return 1
    return n * facto_rec(n - 1)


def fibo_rec(n: int) -> int:
    if n == 0:
        return 0
    elif n == 1:
        return 1
    return fibo_rec(n - 1) + fibo_rec(n - 2)


def fibo_ite(n: int) -> int:
    if n == 0:
        return 0
    elif n == 1:
        return 1
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def golden_phi(n: int) -> float:
    if n < 1:
        raise ValueError("n must be an integer >= 1")
    if n == 1:
        return 0.0
    return fibo_ite(n) / fibo_ite(n - 1)


def sqrt5(n: int) -> float:
    if n < 1:
        raise ValueError("n must be an integer >= 1")
    x = 1e-10
    for _ in range(n):
        x = 0.5 * (x + 5 / x)
    return x


def my_pow(a: float, n: int) -> float:
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    result = 1.0
    for _ in range(n):
        result *= a
    return result


if __name__ == "__main__":
    # Vous pouvez tester votre code manuellement ici, lancer depuis VSCode, poser des breakpoints en debug, ...
    print(nombre_entier(8) == "SSSSSSSS0")