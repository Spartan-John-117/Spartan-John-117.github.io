use crate::debug::{DebugFormat, DebugWriter};
use crate::error::ScannerError;
use crate::packet::{parse_mac_address, NetworkPacket};
use crate::Args;
#[cfg(target_os = "linux")]
use libc::{AF_PACKET, ETH_P_ALL, SOCK_RAW};
use std::net::Ipv4Addr;
use std::thread;
use std::time::Duration;

#[cfg(target_os = "linux")]
use nix::errno::Errno;

/// Structure principale de l'analyseur réseau.
///
/// # Exemple
///
/// ```rust,ignore
/// use net_scanner::scanner::NetworkScanner;
/// use net_scanner::Args;
///
/// let args = Args::parse_from([
///     "net_scanner",
///     "--src_ip=192.168.1.10",
///     "--dst_ip=192.168.1.1",
///     "--dest_port=443",
///     "--dry_run",
///     "--debug_file=trace.json",
///     "--debug_format=json",
/// ]);
///
/// let mut scanner = NetworkScanner::new(args)?;
/// scanner.run()?;
/// # Ok::<(), net_scanner::error::ScannerError>(())
/// ```
pub struct NetworkScanner {
    config: ScannerConfig,
    debug_writer: Option<DebugWriter>,
}

/// Configuration de l'analyseur réseau
#[derive(Debug)]
struct ScannerConfig {
    src_ip: Option<Ipv4Addr>,
    dst_ip: Option<Ipv4Addr>,
    dest_port: Option<u16>,
    src_mac: Option<[u8; 6]>,
    dst_mac: Option<[u8; 6]>,
    l4_protocol: Option<Protocol>,
    timeout_ms: Option<u64>,
    ip_bitfield: Option<u8>,
    interface: Option<String>,
    dry_run: bool,
    payload: Option<Vec<u8>>,
}

#[derive(Debug, Clone)]
enum Protocol {
    Udp,
    Tcp,
}

impl Protocol {
    fn from_str(s: &str) -> Result<Self, ScannerError> {
        match s.to_lowercase().as_str() {
            "udp" => Ok(Protocol::Udp),
            "tcp" => Ok(Protocol::Tcp),
            _ => Err(ScannerError::InvalidArgument(format!(
                "Protocole invalide : {}",
                s
            ))),
        }
    }
}

impl NetworkScanner {
    /// Crée un nouvel analyseur réseau à partir des arguments CLI
    pub fn new(args: Args) -> Result<Self, ScannerError> {
        let config = Self::parse_config(&args)?;
        let debug_writer = Self::create_debug_writer(&args)?;

        Ok(Self {
            config,
            debug_writer,
        })
    }

    /// Analyse la configuration fournie en arguments
    fn parse_config(args: &Args) -> Result<ScannerConfig, ScannerError> {
        let src_mac = if let Some(ref mac_str) = args.src_mac {
            Some(parse_mac_address(mac_str).map_err(|e| ScannerError::ParseError(e))?)
        } else {
            None
        };

        let dst_mac = if let Some(ref mac_str) = args.dst_mac {
            Some(parse_mac_address(mac_str).map_err(|e| ScannerError::ParseError(e))?)
        } else {
            None
        };

        let l4_protocol = if let Some(ref protocol_str) = args.l4_protocol {
            Some(Protocol::from_str(protocol_str)?)
        } else {
            None
        };

        let ip_bitfield = if let Some(ref bitfield_str) = args.ip_bitfield {
            Some(Self::parse_hex_u8(bitfield_str)?)
        } else {
            None
        };

        let payload = args.payload.clone().map(|s| s.into_bytes());

        Ok(ScannerConfig {
            src_ip: args.src_ip,
            dst_ip: args.dst_ip,
            dest_port: args.dest_port,
            src_mac,
            dst_mac,
            l4_protocol,
            timeout_ms: args.timeout_ms,
            ip_bitfield,
            interface: args.interface.clone(),
            dry_run: args.dry_run,
            payload,
        })
    }

    /// Crée l'écrivain de traces si les options associées sont présentes
    fn create_debug_writer(args: &Args) -> Result<Option<DebugWriter>, ScannerError> {
        match (&args.debug_file, &args.debug_format) {
            (Some(file_path), Some(format_str)) => {
                let format = DebugFormat::from_str(format_str)?;
                Ok(Some(DebugWriter::new(format, file_path.clone())))
            }
            (Some(_), None) => Err(ScannerError::InvalidArgument(
                "--debug_file nécessite --debug_format".to_string(),
            )),
            (None, Some(_)) => Err(ScannerError::InvalidArgument(
                "--debug_format nécessite --debug_file".to_string(),
            )),
            (None, None) => Ok(None),
        }
    }

    /// Convertit une chaîne hexadécimale en `u8`
    fn parse_hex_u8(hex_str: &str) -> Result<u8, ScannerError> {
        let cleaned = if hex_str.starts_with("0x") || hex_str.starts_with("0X") {
            &hex_str[2..]
        } else {
            hex_str
        };

        u8::from_str_radix(cleaned, 16).map_err(|_| {
            ScannerError::ParseError(format!("Valeur hexadécimale invalide : {}", hex_str))
        })
    }

    /// Exécute l'analyse
    pub fn run(&mut self) -> Result<(), ScannerError> {
        // Crée un paquet représentatif en fonction de la configuration
        let packet = self.create_packet()?;

        // Ajoute le paquet à l'écrivain de traces si demandé
        if let Some(ref mut debug_writer) = self.debug_writer {
            debug_writer.add_packet(packet.clone());
        }

        // Envoie le paquet si une interface est fournie et que l'on n'est pas en mode simulation.
        let should_send = !self.config.dry_run && self.config.interface.is_some();
        if should_send {
            if let Some(interface) = self.config.interface.as_ref() {
                self.send_packet(interface, &packet)?;
            }
        }

        // Applique un délai éventuel entre les tentatives
        if let Some(timeout_ms) = self.config.timeout_ms {
            thread::sleep(Duration::from_millis(timeout_ms));
        }

        // Écrit les informations de débogage si demandé
        if let Some(ref debug_writer) = self.debug_writer {
            debug_writer.write_to_file()?;
        }

        Ok(())
    }

    /// Construit un paquet réseau conforme à la configuration
    fn create_packet(&self) -> Result<NetworkPacket, ScannerError> {
        // Utilise des valeurs par défaut si nécessaire
        let src_ip = self
            .config
            .src_ip
            .unwrap_or_else(|| Ipv4Addr::new(192, 168, 1, 100));
        let dst_ip = self
            .config
            .dst_ip
            .unwrap_or_else(|| Ipv4Addr::new(192, 168, 1, 1));
        let dest_port = self.config.dest_port.unwrap_or(80);
        let src_port = 12345; // Port source fixe pour simplifier

        // Adresses MAC par défaut si non fournies
        let src_mac = self
            .config
            .src_mac
            .unwrap_or([0x00, 0x11, 0x22, 0x33, 0x44, 0x55]);
        let dst_mac = self
            .config
            .dst_mac
            .unwrap_or([0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]);

    // Charge utile : valeur fournie via --payload ou message par défaut
    let payload = self
        .config
        .payload
        .clone()
        .unwrap_or_else(|| String::from("Si tu vois ce message, c'est que normalement ça marche").into_bytes());

        let mut packet = match self.config.l4_protocol.as_ref().unwrap_or(&Protocol::Udp) {
            Protocol::Udp => NetworkPacket::new_udp(
                src_mac, dst_mac, src_ip, dst_ip, src_port, dest_port, payload,
            ),
            Protocol::Tcp => NetworkPacket::new_tcp(
                src_mac, dst_mac, src_ip, dst_ip, src_port, dest_port, payload,
            ),
        };

        // Applique le champ IPv4 si nécessaire
        if let Some(bitfield) = self.config.ip_bitfield {
            packet.apply_ip_bitfield(bitfield);
        }

        Ok(packet)
    }

    /// Émet le paquet via un socket brut lorsque c'est possible
    fn send_packet(&self, interface: &str, packet: &NetworkPacket) -> Result<(), ScannerError> {
        let bytes = packet.to_bytes();

        #[cfg(target_os = "linux")]
        {
            send_raw_packet_linux(interface, &bytes, &packet.ethernet.dst_mac)
        }

        #[cfg(not(target_os = "linux"))]
        {
            let _ = interface;
            let _ = bytes;
            Err(ScannerError::NetworkError(
                "L'émission via socket brut n'est prise en charge que sous Linux".to_string(),
            ))
        }
    }
}

#[cfg(target_os = "linux")]
fn send_raw_packet_linux(
    interface: &str,
    packet: &[u8],
    dst_mac: &[u8; 6],
) -> Result<(), ScannerError> {
    use libc::{c_void, close, sendto, sockaddr_ll};
    use std::ffi::CString;
    use std::mem;
    use std::os::fd::RawFd;

    // Création du socket brut
    let protocol = (ETH_P_ALL as u16).to_be();
    let fd: RawFd = unsafe { libc::socket(AF_PACKET, SOCK_RAW, protocol as i32) };

    if fd < 0 {
        let err = Errno::last();
        return Err(match err {
            Errno::EPERM => ScannerError::PermissionDenied(
                "Les privilèges root sont requis pour ouvrir un socket brut".to_string(),
            ),
            _ => {
                ScannerError::NetworkError(format!("Échec de l'ouverture du socket brut : {}", err))
            }
        });
    }

    // Résolution de l'index d'interface
    let if_name = CString::new(interface).map_err(|_| {
        ScannerError::InvalidArgument(format!("Nom d'interface invalide : {}", interface))
    })?;

    let if_index = unsafe { libc::if_nametoindex(if_name.as_ptr()) } as i32;
    if if_index == 0 {
        unsafe { close(fd) };
        return Err(ScannerError::NetworkError(format!(
            "Interface réseau inconnue : {}",
            interface
        )));
    }

    // Préparation de l'adresse de destination
    let mut addr: sockaddr_ll = unsafe { mem::zeroed() };
    addr.sll_family = AF_PACKET as u16;
    addr.sll_protocol = protocol;
    addr.sll_ifindex = if_index;
    addr.sll_halen = 6;
    addr.sll_addr[..6].copy_from_slice(dst_mac);

    // Envoi du paquet
    let result = unsafe {
        sendto(
            fd,
            packet.as_ptr() as *const c_void,
            packet.len(),
            0,
            &addr as *const _ as *const libc::sockaddr,
            mem::size_of::<sockaddr_ll>() as libc::socklen_t,
        )
    };

    let send_result = if result < 0 {
        Err(Errno::last())
    } else {
        Ok(())
    };

    unsafe { close(fd) };

    match send_result {
        Ok(()) => Ok(()),
        Err(err) => Err(ScannerError::NetworkError(format!(
            "Échec de l'envoi du paquet : {}",
            err
        ))),
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::packet::TransportHeader;
    use serde_json::Value;
    use std::env;
    use std::fs;
    use std::time::{SystemTime, UNIX_EPOCH};

    #[test]
    fn test_protocol_from_str() {
        assert!(matches!(Protocol::from_str("udp"), Ok(Protocol::Udp)));
        assert!(matches!(Protocol::from_str("tcp"), Ok(Protocol::Tcp)));
        assert!(matches!(Protocol::from_str("UDP"), Ok(Protocol::Udp)));
        assert!(matches!(Protocol::from_str("TCP"), Ok(Protocol::Tcp)));
        assert!(Protocol::from_str("invalide").is_err());
    }

    #[test]
    fn test_parse_hex_u8() {
        assert_eq!(NetworkScanner::parse_hex_u8("0x04").unwrap(), 4);
        assert_eq!(NetworkScanner::parse_hex_u8("0xFF").unwrap(), 255);
        assert_eq!(NetworkScanner::parse_hex_u8("04").unwrap(), 4);
        assert_eq!(NetworkScanner::parse_hex_u8("FF").unwrap(), 255);
        assert!(NetworkScanner::parse_hex_u8("invalide").is_err());
        assert!(NetworkScanner::parse_hex_u8("0x100").is_err()); // Trop grand pour un u8
    }

    #[test]
    fn test_create_packet_uses_defaults() {
        let args = Args {
            src_ip: None,
            dst_ip: None,
            dest_port: None,
            src_mac: None,
            dst_mac: None,
            l4_protocol: None,
            timeout_ms: None,
            debug_file: None,
            debug_format: None,
            ip_bitfield: None,
            interface: None,
            payload: None,
            dry_run: true,
        };

        let scanner = NetworkScanner::new(args).expect("initialisation de base réussie");
        let packet = scanner
            .create_packet()
            .expect("création du paquet par défaut");

        assert_eq!(packet.ipv4.src_ip, Ipv4Addr::new(192, 168, 1, 100));
        assert_eq!(packet.ipv4.dst_ip, Ipv4Addr::new(192, 168, 1, 1));
    assert_eq!(packet.payload, "Si tu vois ce message, c'est que normalement ça marche".as_bytes());

        match &packet.transport {
            TransportHeader::Udp(udp) => {
                assert_eq!(udp.dst_port, 80);
                assert_eq!(udp.src_port, 12345);
                assert_eq!(udp.length as usize, 8 + packet.payload.len());
            }
            _ => panic!("Le protocole par défaut doit être UDP"),
        }
    }

    #[test]
    fn test_run_writes_json_in_dry_run_mode() {
        let mut path = env::temp_dir();
        let unique = format!(
            "net_scanner_test_{}_{}.json",
            std::process::id(),
            SystemTime::now()
                .duration_since(UNIX_EPOCH)
                .expect("horloge système valide")
                .as_nanos()
        );
        path.push(unique);

        let file_path_str = path.to_string_lossy().to_string();

        let args = Args {
            src_ip: None,
            dst_ip: None,
            dest_port: None,
            src_mac: None,
            dst_mac: None,
            l4_protocol: None,
            timeout_ms: None,
            debug_file: Some(file_path_str),
            debug_format: Some("json".to_string()),
            ip_bitfield: None,
            interface: None,
            payload: None,
            dry_run: true,
        };

        let mut scanner = NetworkScanner::new(args).expect("initialisation avec debug JSON");
        scanner.run().expect("exécution du scanner en dry run");

        let contents = fs::read_to_string(&path).expect("lecture du fichier JSON");
        let json: Value = serde_json::from_str(&contents).expect("JSON valide");

        assert_eq!(json["count"].as_u64(), Some(1));
        let packets = json["packets"].as_array().expect("tableau de paquets");
        assert_eq!(packets.len(), 1);
        assert_eq!(packets[0]["ipv4"]["src_ip"], "192.168.1.100");
        assert_eq!(packets[0]["ipv4"]["dst_ip"], "192.168.1.1");

        let _ = fs::remove_file(&path);
    }
}
