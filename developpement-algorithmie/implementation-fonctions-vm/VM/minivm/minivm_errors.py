# Ici on a définit toutes les exceptions (erreurs) que peut provoquer la machine

class StopMachine(Exception):
    """
    Quand tous c'est bien passé et qu'on a atteint l'appel système SYSEXIT
    """
    pass

class InstructionFault(Exception):
    """
    Toute instruction qui ne peut s'executé car quelque chose ne va pas
    """
    pass

class StackOverflow(Exception):
    """
    Lorsque la pile est pleine
    """
    pass

class StackUnderflow(Exception):
    """
    Lorsque la pile est vide
    """
    pass

class StackFrameError(Exception):
    """
    Lorsqu'un index de fetch/store est au-delà de la taille de la stack frame
    """
    pass
