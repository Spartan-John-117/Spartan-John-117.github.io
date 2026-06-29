from abc import ABC, abstractmethod
from math import sqrt

class Vehicule:                                 # Définition d'une classe 
    def __init__(self, porte=2):                # 2 portes si pas de valeur renseignée
        self.porte = porte


class Animal:
    def __init__(self, patte=4, queue=False):   # Par défaut 4 pattes et pas de queue
        self.patte = patte
        self.queue = queue


class Deplacement(ABC):
    @property
    @abstractmethod
    def x(self):
        pass    
    @x.setter                                   # Définition des getter et setter
    @abstractmethod
    def x(self, value):
        pass

    @property
    @abstractmethod
    def y(self):
        pass

    @y.setter
    @abstractmethod
    def y(self, value):
        pass

    @property
    @abstractmethod
    def z(self):
        pass
    
    @z.setter
    @abstractmethod
    def z(self, value):
        pass

    @abstractmethod
    def move_to(self, x: float, y: float, z: float, zone: str):
        pass

class Volant(Deplacement):
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
    
    

    def move_to(self, x: float, y: float, z: float, zone: str):
        if z < 0:
            raise ValueError("Ne peut pas voler")
        self.x, self.y, self.z = x, y, z
        return f"se déplace vers {x}, {y}, {z} en volant"


class Courant(Deplacement):
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

    def move_to(self, x: float, y: float, z: float, zone: str):
        if z != 0 or zone != 'terre':
            raise ValueError("Ne peut pas courir.")
        self.x, self.y, self.z = x, y, z
        return f"se déplace vers {x}, {y} en courant"


class Marchant(Deplacement):
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
    

    def move_to(self, x: float, y: float, z: float, zone: str):
        if z != 0 or zone != 'terre':
            raise ValueError("Ne peut pas marcher.")
        self.x, self.y, self.z = x, y, z
        return f"se déplace vers {x}, {y} en marchant"


class Roulant(Deplacement):
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

    def move_to(self, x: float, y: float, z: float, zone: str):
        if z != 0 or zone != 'terre':
            raise ValueError("Ne peut rouler.")
        self.x, self.y, self.z = x, y, z
        return f"se déplace vers {x}, {y} en roulant"


class Flottant(Deplacement):
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

    def move_to(self, x: float, y: float, z: float, zone: str):
        if z != 0 or zone != 'mer':
            raise ValueError("Ne peut pas flotter.")
        self.x, self.y, self.z = x, y, z
        return f"se déplace vers {x}, {y} en flottant"


class Nageant(Deplacement):
    def __init__(self):
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0

    def move_to(self, x: float, y: float, z: float, zone: str):
        if z >= 0 or zone != 'mer':
            raise ValueError("Ne peut pas nager.")
        self.x, self.y, self.z = x, y, z
        return f"se déplace vers {x}, {y}, {z} en nageant"


class Humain(Animal, Marchant, Courant, Flottant, Nageant):
    def __init__(self):
        super().__init__(patte=2, queue=False)
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def z(self):
        return self._z
    
    @z.setter
    def z(self, value):
        self._z = value

    def move_to(self, x: float, y: float, z: float, zone: str):
        distance =  sqrt((x - self.x) ** 2 + (y - self.y) ** 2 + (z - self.z) ** 2)
        if 2 <= distance <= 10:
            try:
                return Courant.move_to(self, x, y, z, zone)
            except ValueError:
                pass
        try:
            return Marchant.move_to(self, x, y, z, zone)
        except ValueError:
            pass
        try:
            return Nageant.move_to(self, x, y, z, zone)
        except ValueError:
            pass
        try:
            return Flottant.move_to(self, x, y, z, zone)
        except ValueError as e:
            raise ValueError("Déplacement de humain impossible.") from e


class VoitureSansPermis(Vehicule, Roulant):
    def __init__(self):
        super().__init__(porte=2)
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def z(self):
        return self._z
    
    @z.setter
    def z(self, value):
        self._z = value

class Berline(Vehicule, Roulant):
    def __init__(self):
        super().__init__(porte=5)
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def z(self):
        return self._z
    
    @z.setter
    def z(self, value):
        self._z = value

class Moto(Vehicule, Roulant):
    def __init__(self):
        super().__init__(porte=0)
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def z(self):
        return self._z
    
    @z.setter
    def z(self, value):
        self._z = value


class Hors_Bord(Vehicule, Flottant):
    def __init__(self):
        super().__init__(porte=0)
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def z(self):
        return self._z
    
    @z.setter
    def z(self, value):
        self._z = value


class Spitfire(Vehicule, Volant):
    def __init__(self):
        super().__init__(porte=0)
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def z(self):
        return self._z
    
    @z.setter
    def z(self, value):
        self._z = value

class Cygne(Animal, Flottant, Volant):
    def __init__(self):
        super().__init__(patte=2, queue=True)
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def z(self):
        return self._z
    
    @z.setter
    def z(self, value):
        self._z = value

    def move_to(self, x: float, y: float, z: float, zone: str):
        try:
            return Flottant.move_to(self, x, y, z, zone)
        except ValueError:
            pass
        try:
            return Volant.move_to(self, x, y, z, zone)
        except ValueError as e:
            raise ValueError("Déplacement de signe impossible.") from e


class Canard(Animal, Marchant, Courant, Flottant, Volant, Nageant):
    def __init__(self):
        super().__init__(patte=2, queue=True)
        self.x = 0.0
        self.y = 0.0
        self.z = 0.0
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def z(self):
        return self._z
    
    @z.setter
    def z(self, value):
        self._z = value

    def move_to(self, x: float, y: float, z: float, zone: str):
        distance = sqrt((x - self._x) ** 2 + (y - self._y) ** 2)
        print(distance)
        if 2 <= distance <= 10:
            try:
                return Courant.move_to(self, x, y, z, zone)
            except ValueError:
                pass
        try:
            return Marchant.move_to(self, x, y, z, zone)
        except ValueError:
            pass
        try:
            return Nageant.move_to(self, x, y, z, zone)
        except ValueError:
            pass
        try:
            return Flottant.move_to(self, x, y, z, zone)
        except ValueError:
            pass
        try:
            return Volant.move_to(self, x, y, z, zone)
        except ValueError as e:
            raise ValueError("Déplacement de canard impossible.") from e


class Poisson(Animal, Nageant):
    def __init__(self):
        super().__init__(patte=0, queue=True)
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

    @property
    def z(self):
        return self._z
    
    @z.setter
    def z(self, value):
        self._z = value
