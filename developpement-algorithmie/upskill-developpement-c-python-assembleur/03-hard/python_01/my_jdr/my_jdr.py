import random
import itertools

class AddExpr:                                                                  # Classe pour gérer les additions
    def __init__(self, lhs, rhs):
        self.lhs = lhs                                                          # lhs correspond au côté gauche de l'opération
        self.rhs = rhs                                                          # rhs correspond au côté droit de l'opération
        self.result = 0                                                         # Exemple : lhs + rhs

    def __repr__(self) -> str:
        return repr(self.lhs) + ' + ' + repr(self.rhs)

    def throw(self) -> int:
        if self.result == 0:
            a = self.lhs.throw()
            b = self.rhs.throw()
            self.result = a + b
        return self.result

class SubExpr:                                                                  # Classe pour gérer les soustractions
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.result = 0

    def __repr__(self) -> str:
        return repr(self.lhs) + ' - ' + repr(self.rhs)

    def throw(self) -> int:
        if self.result == 0:
            a = self.lhs.throw()
            b = self.rhs.throw()
            self.result = a - b
        return self.result

class MulExpr:                                                                  # Classe pour gérer les multiplications
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.results = []                                                       # Le résultat des différents lancés est stocké 
                                                                                # dans une liste
    def __repr__(self) -> str:
        return f"{self.lhs}D{repr(self.rhs)}"

    def throw(self):
        if not self.results:
            self.results = [self.rhs.throw() for _ in range(self.lhs)]          # On lance le type de dés indiqué par rhs autant de fois
        return sum(self.results)                                                # que mentionné par lhs

    def show(self):
        return ", ".join(map(str, self.results))

class Pool:                                                                     # Classe pour gérer les opérations sur les dés
    def __init__(self, op):
        self.op = op

    def throw(self):
        return self.op.throw()

    def show(self):
        if hasattr(self.op, "show"):
            return self.op.show()
        return str(self.op.throw())

    def __add__(self, rhs):
        if type(rhs) is int:
            rhs = FrozenDice(rhs)
        return Pool(AddExpr(self, rhs))

    def __radd__(self, lhs):
        if isinstance(lhs, int):
            return Pool(AddExpr(lhs, self))
        return NotImplemented 

    def __sub__(self, rhs):
        if type(rhs) is int:
            rhs = FrozenDice(rhs)
        return Pool(SubExpr(self, rhs))

    def __rsub__(self, lhs):
        if isinstance(lhs, int): 
            return Pool(SubExpr(lhs, self)) 
        return NotImplemented 

    def __mul__(self, lhs):
        if type(lhs) is int:
            return Pool(MulExpr(lhs, self))
        raise ValueError("lhs is not integer")

    def __rmul__(self, lhs):
        return self.__mul__(lhs)

    def __repr__(self) -> str:
        return repr(self.op)

    def roll(self):                                                             # Génère toutes les combinaisons possible pour calculer
        if isinstance(self.op, AbstractResult):
            for val in range(1, self.op.max + 1):
                yield (val,)

        elif isinstance(self.op, Pool):
            yield from self.op.roll()
        
        def roll_helper(op):                                                    # les chances de succès
            if isinstance(op, MulExpr):                                         # vérifie que l'opération est bien une multiplication
                ranges = [range(1, op.rhs.max + 1) for _ in range(op.lhs)]      # Génère le range pour chaque dés range d6 = (1, 7)
                                                                                # Le "_" dans la boucle for indique que l'itérateur n'a pas 
                                                                                # de nom car on ne s'en sert pas dans la boucle
                for combo in itertools.product(*ranges):                        # Génère toutes les combinaisons de résultats de l'opération
                    yield combo                                                 # Permet de retourner les valeurs une par une au lieu de
                                                                                # retourner le résultat complet en un seul bloc (plus léger)
            elif isinstance(op, AddExpr):
                for l in roll_helper(op.lhs):                                   # Calcule toutes les valeurs possible à gauche
                    for r in roll_helper(op.rhs):                               # Calcule toutes les valeurs possible à droite
                        yield l + (r if isinstance(r, tuple) else (r,))         # Retourne le résultat sous forme de tuple pour chaque combinaison
            elif isinstance(op, SubExpr):
                for l in roll_helper(op.lhs):
                    for r in roll_helper(op.rhs):
                        yield l + (-r if isinstance(r, tuple) else (-r,))
            else:
                raise ValueError(f"Unsupported operation type: {type(op)}")

        yield from roll_helper(self.op)

    def success(self, lamb) -> float:                                          # Calcule les chance de succès en fonction de la lambda fournie
        all_outcomes = list(self.roll())                                        # Place tous les résultats de roll dans une liste
        successes = sum(1 for outcome in all_outcomes if lamb(outcome))         # Pour chaque résultat, vérifie s'il satisfait la lambda et ajoute 1
        return (successes / len(all_outcomes)) * 100                            # Fournit le résultat sous forme de pourcentage

    darkness = lambda rolls: sum(1 for roll in rolls if roll >= 5) >= 4         # Variable pour la lambda Darkness


class AbstractResult(Pool):                                                     # Classe de base qui définit le comportement d'un dés (générique)
    min = 1
    max = 1                                                                     # Le maximum varie en fonction du type de dés
    def __init__(self):
        self.result = 0

    def __repr__(self):
        return type(self).__name__

    def throw(self):                                                            # Le lancé est simulé par l'obtention d'un nombre
        if self.result == 0:                                                    # aléatoire comprit entre 1 et le max du type de dés
            self.result = random.randint(type(self).min, type(self).max)
        return self.result

    def seed(s):                                                                # Permet de définir la seed en dur pour pouvoir reproduire
        random.seed(s)                                                          # les résultats

class FrozenDice(AbstractResult):                                               # Création d'une constante, le lancé de dés n'est plus
    def __init__(self, v):                                                      # aléatoire mais est fixé par la valeur de v
        self.result = v
        self.min = v
        self.max = v

    def __repr__(self):
        return str(self.result)

    def throw(self):
        return self.result

                                                                                # Définition des classes pour chaque type de dés
class D4(AbstractResult):
    max=4

class D6(AbstractResult):
    max = 6

class D8(AbstractResult):
    max = 8

class D10(AbstractResult):
    max = 10

class D12(AbstractResult):
    max = 12

class D20(AbstractResult):
    max = 20

                                                                                # Instances standards pour chaque type de dés
d4 = D4()
d6 = D6()
d8 = D8()
d10 = D10()
d12 = D12()
d20 = D20()
