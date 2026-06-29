use std::fmt;

/// Type d'erreur spécifique à l'analyseur réseau
#[derive(Debug)]
pub enum ScannerError {
    /// Argument fourni invalide
    InvalidArgument(String),
    /// Erreur d'entrée/sortie
    IoError(std::io::Error),
    /// Échec d'une opération réseau
    NetworkError(String),
    /// Erreur d'analyse
    ParseError(String),
    /// Permission refusée (privilèges root requis)
    PermissionDenied(String),
}

impl fmt::Display for ScannerError {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        match self {
            ScannerError::InvalidArgument(msg) => write!(f, "Argument invalide : {}", msg),
            ScannerError::IoError(err) => write!(f, "Erreur d'E/S : {}", err),
            ScannerError::NetworkError(msg) => write!(f, "Erreur réseau : {}", msg),
            ScannerError::ParseError(msg) => write!(f, "Erreur d'analyse : {}", msg),
            ScannerError::PermissionDenied(msg) => write!(f, "Permission refusée : {}", msg),
        }
    }
}

impl std::error::Error for ScannerError {}

impl From<std::io::Error> for ScannerError {
    fn from(err: std::io::Error) -> Self {
        ScannerError::IoError(err)
    }
}

impl From<std::net::AddrParseError> for ScannerError {
    fn from(err: std::net::AddrParseError) -> Self {
        ScannerError::ParseError(err.to_string())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn display_invalid_argument() {
        let e = ScannerError::InvalidArgument("mauvais_arg".to_string());
        assert_eq!(format!("{}", e), "Argument invalide\u{00A0}: mauvais_arg");
    }

    #[test]
    fn display_io_error_contains_message() {
        let ioerr = std::io::Error::new(std::io::ErrorKind::Other, "erreur disque");
        let e: ScannerError = ioerr.into();
        let s = format!("{}", e);
        assert!(s.starts_with("Erreur d'E/S"));
        assert!(s.contains("erreur disque"));
    }

    #[test]
    fn display_network_and_parse_and_permission() {
        let n = ScannerError::NetworkError("timeout".to_string());
        assert_eq!(format!("{}", n), "Erreur réseau\u{00A0}: timeout");

        let p = ScannerError::ParseError("format invalide".to_string());
        assert_eq!(
            format!("{}", p),
            "Erreur d'analyse\u{00A0}: format invalide"
        );

        let perm = ScannerError::PermissionDenied("root requis".to_string());
        assert_eq!(
            format!("{}", perm),
            "Permission refusée\u{00A0}: root requis"
        );
    }

    #[test]
    fn from_addrparseerror_uses_parse_error_variant() {
        // Provokes an AddrParseError by parsing an invalid IP
        let parse_err = "not_an_ip".parse::<std::net::IpAddr>().unwrap_err();
        let e: ScannerError = parse_err.into();
        let s = format!("{}", e);
        assert!(s.starts_with("Erreur d'analyse"));
    }
}
