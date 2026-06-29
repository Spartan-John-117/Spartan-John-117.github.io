#include <fcntl.h>
#include <unistd.h>
#include <errno.h>

int my_cat(const char *const filename) {
    int fd;
    char buffer[1024];
    ssize_t bytes_read;

                                                                            // Si le fichier est NULL
    if (filename == NULL) {                                                 // lire depuis l'entrée standard (file descriptor 0)
        fd = 0; // file descriptor pour stdin
    } else {
                                                                            // Ouvrir le fichier en mode lecture seule
        fd = open(filename, O_RDONLY);
        if (fd < 0) {
            return 1;                                                       // Erreur lors de l'ouverture du fichier
        }
    }

                                                                            // Lire le fichier et écrire dans 
    while ((bytes_read = read(fd, buffer, sizeof(buffer))) > 0) {           // stdout (file descriptor 1)
        if (write(1, buffer, bytes_read) < 0) {
            if (fd != 0) close(fd);
            return 1;                                                       // Erreur lors de l'écriture
        }
    }

                                                                            // Vérifier si une erreur est survenue 
    if (bytes_read < 0) {                                                   // pendant la lecture
        if (fd != 0) close(fd);
        return 1;
    }

                                                                            // Fermer le fichier si ce n'est pas stdin
    if (fd != 0) {
        if (close(fd) < 0) {
            return 1;                                                       // Erreur lors de la fermeture du fichier
        }
    }

    return 0;
}