int my_get_nbr_recurs(char const str[])
{
    static int signe = 1;								// Le "static" permet de déclarer une variable qui ne peut pas
														// être remise à 0 à chaque itération
	static int number = 0;
	static int i = 0;
 
    if (str[i] == '-')									// Vérifie s'il y'a un caractère négatif au début de la chaîne
    {
        signe = -1;
        i += 1;
    }
 
    if (str[i] >= '0' && str[i] <= '9')					// Si le caractère est compris entre 0 et 9
    {
        number = number * 10 + (str[i] - '0');			// Vérifie 
		i += 1;
        return my_get_nbr_recurs(str);
    }
 
    if (str[i] == '\0')
	{
        return number * signe;
    }
    return 0;
}

