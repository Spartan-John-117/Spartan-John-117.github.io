import functools
import inspect

def checktypes(func):
    
    sig = inspect.signature(func)                                               # Le module signature de inspect permet
                                                                                # permet de récupérer plusieurs informations
                                                                                # sur la fonction dont le type des paramètres...

    @functools.wraps(func)
    def wrapper(*args, **kwargs):                                               # Cette fonction peut prendre n'importe quel
                                                                                # type d'arguments       
        bound_arguments = sig.bind(*args, **kwargs)                             # Permet d'associer les arguments passés avec
                                                                                # le nom des paramètres définis
        bound_arguments.apply_defaults()                                        # Ajoute les valeurs par défaut si aucune
                                                                                # n'est renseignée

        for param_name, param_value in bound_arguments.arguments.items():       # Parcours le dictionnaire "bound_argument" 
                                                                                # contenant les paires "nom d'argument" et "valeur"
            if param_name in sig.parameters:                                    # Vérifie si le paramètre est dans la signature
                expected_type = sig.parameters[param_name].annotation           # Si oui, récupère le type attendu, s'il n'y a 
                                                                                # rien, le type est "empty"
                if expected_type is not inspect.Parameter.empty \
                    and not isinstance(param_value, expected_type):             # Vérifie si la value correspond au expected type
                    raise TypeError(
                        f"{func.__name__}: wrong type of '{param_name}' " 
                        f"argument, '{expected_type.__name__}' expected, got "
                        f"'{type(param_value).__name__}'"
                    )
        
        result = func(*args, **kwargs)                                          # Appelle la fonction décorée après la vérif

        expected_return_type = sig.return_annotation                            # Récupère le type de retour attendu
        if expected_return_type is not inspect.Signature.empty \
            and not isinstance(result, expected_return_type):                   # Même vérif que pour "expected_type"
            raise TypeError(
                f"{func.__name__}: wrong return type, "
                f"'{expected_return_type.__name__}' expected, got "
                f"'{type(result).__name__}'"
            )

        return result

    return wrapper
