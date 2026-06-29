use serde::Serialize;
use std::net::Ipv4Addr;

/// En-tête de trame Ethernet (14 octets)
#[derive(Debug, Clone, Serialize)]
pub struct EthernetHeader {
    pub dst_mac: [u8; 6],
    pub src_mac: [u8; 6],
    pub ethertype: u16, // 0x0800 pour IPv4
}

impl EthernetHeader {
    pub fn new(src_mac: [u8; 6], dst_mac: [u8; 6]) -> Self {
        Self {
            dst_mac,
            src_mac,
            ethertype: 0x0800, // IPv4
        }
    }

    pub fn to_bytes(&self) -> Vec<u8> {
        let mut bytes = Vec::with_capacity(14);
        bytes.extend_from_slice(&self.dst_mac);
        bytes.extend_from_slice(&self.src_mac);
        bytes.extend_from_slice(&self.ethertype.to_be_bytes());
        bytes
    }
}

/// En-tête IPv4 (20 octets minimum)
#[derive(Debug, Clone, Serialize)]
pub struct Ipv4Header {
    pub version_ihl: u8, // Version (4 bits) + IHL (4 bits)
    pub dscp_ecn: u8,    // DSCP (6 bits) + ECN (2 bits)
    pub total_length: u16,
    pub identification: u16,
    pub flags_fragment: u16, // Flags (3 bits) + décalage de fragment (13 bits)
    pub ttl: u8,
    pub protocol: u8, // 6 = TCP, 17 = UDP
    pub header_checksum: u16,
    pub src_ip: Ipv4Addr,
    pub dst_ip: Ipv4Addr,
}

impl Ipv4Header {
    pub fn new(src_ip: Ipv4Addr, dst_ip: Ipv4Addr, protocol: u8, payload_length: u16) -> Self {
        let total_length = 20 + payload_length; // 20 octets pour l'en-tête IP + la charge utile

        Self {
            version_ihl: 0x45, // Version 4, IHL 5 (20 octets)
            dscp_ecn: 0,
            total_length,
            identification: 0x1234, // Identifiant arbitraire
            flags_fragment: 0x4000, // Drapeau "ne pas fragmenter"
            ttl: 64,
            protocol,
            header_checksum: 0, // Calculé ultérieurement
            src_ip,
            dst_ip,
        }
    }

    pub fn apply_bitfield(&mut self, bitfield: u8) {
        // Applique le champ sur les 8 bits de poids fort de flags_fragment
        let current = self.flags_fragment;
        let new_flags = (bitfield as u16) << 8;
        let fragment_offset = current & 0x1FFF; // Conserve les 13 bits de poids faible
        self.flags_fragment = new_flags | fragment_offset;
    }

    pub fn calculate_checksum(&mut self) {
        self.header_checksum = 0;
        let bytes = self.to_bytes();
        self.header_checksum = calculate_ip_checksum(&bytes);
    }

    pub fn to_bytes(&self) -> Vec<u8> {
        let mut bytes = Vec::with_capacity(20);
        bytes.push(self.version_ihl);
        bytes.push(self.dscp_ecn);
        bytes.extend_from_slice(&self.total_length.to_be_bytes());
        bytes.extend_from_slice(&self.identification.to_be_bytes());
        bytes.extend_from_slice(&self.flags_fragment.to_be_bytes());
        bytes.push(self.ttl);
        bytes.push(self.protocol);
        bytes.extend_from_slice(&self.header_checksum.to_be_bytes());
        bytes.extend_from_slice(&self.src_ip.octets());
        bytes.extend_from_slice(&self.dst_ip.octets());
        bytes
    }
}

/// En-tête UDP (8 octets)
#[derive(Debug, Clone, Serialize)]
pub struct UdpHeader {
    pub src_port: u16,
    pub dst_port: u16,
    pub length: u16,
    pub checksum: u16,
}

impl UdpHeader {
    pub fn new(src_port: u16, dst_port: u16, payload_length: u16) -> Self {
        Self {
            src_port,
            dst_port,
            length: 8 + payload_length, // 8 octets pour l'en-tête UDP + la charge utile
            checksum: 0,                // Calculé ultérieurement
        }
    }

    pub fn calculate_checksum(&mut self, src_ip: Ipv4Addr, dst_ip: Ipv4Addr, payload: &[u8]) {
        self.checksum = 0;
        let header_bytes = self.to_bytes();
        self.checksum = calculate_udp_checksum(src_ip, dst_ip, &header_bytes, payload);
    }

    pub fn to_bytes(&self) -> Vec<u8> {
        let mut bytes = Vec::with_capacity(8);
        bytes.extend_from_slice(&self.src_port.to_be_bytes());
        bytes.extend_from_slice(&self.dst_port.to_be_bytes());
        bytes.extend_from_slice(&self.length.to_be_bytes());
        bytes.extend_from_slice(&self.checksum.to_be_bytes());
        bytes
    }
}

/// En-tête TCP (20 octets minimum)
#[derive(Debug, Clone, Serialize)]
pub struct TcpHeader {
    pub src_port: u16,
    pub dst_port: u16,
    pub seq_num: u32,
    pub ack_num: u32,
    pub data_offset_flags: u16, // Offset données (4 bits) + réservé (3 bits) + flags (9 bits)
    pub window_size: u16,
    pub checksum: u16,
    pub urgent_pointer: u16,
}

impl TcpHeader {
    pub fn new(src_port: u16, dst_port: u16) -> Self {
        Self {
            src_port,
            dst_port,
            seq_num: 0x12345678,
            ack_num: 0,
            data_offset_flags: 0x5002, // Offset 5 (20 octets) + drapeau SYN
            window_size: 8192,
            checksum: 0, // Calculé ultérieurement
            urgent_pointer: 0,
        }
    }

    pub fn calculate_checksum(&mut self, src_ip: Ipv4Addr, dst_ip: Ipv4Addr, payload: &[u8]) {
        self.checksum = 0;
        let header_bytes = self.to_bytes();
        self.checksum = calculate_tcp_checksum(src_ip, dst_ip, &header_bytes, payload);
    }

    pub fn to_bytes(&self) -> Vec<u8> {
        let mut bytes = Vec::with_capacity(20);
        bytes.extend_from_slice(&self.src_port.to_be_bytes());
        bytes.extend_from_slice(&self.dst_port.to_be_bytes());
        bytes.extend_from_slice(&self.seq_num.to_be_bytes());
        bytes.extend_from_slice(&self.ack_num.to_be_bytes());
        bytes.extend_from_slice(&self.data_offset_flags.to_be_bytes());
        bytes.extend_from_slice(&self.window_size.to_be_bytes());
        bytes.extend_from_slice(&self.checksum.to_be_bytes());
        bytes.extend_from_slice(&self.urgent_pointer.to_be_bytes());
        bytes
    }
}

/// Paquet réseau complet.
///
/// # Exemple
///
/// ```rust,ignore
/// use net_scanner::packet::{NetworkPacket, TransportHeader};
/// use std::net::Ipv4Addr;
///
/// let src_mac = [0x00, 0x11, 0x22, 0x33, 0x44, 0x55];
/// let dst_mac = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF];
/// let payload = b"Bonjour".to_vec();
///
/// let packet = NetworkPacket::new_udp(
///     src_mac,
///     dst_mac,
///     Ipv4Addr::new(192, 168, 1, 10),
///     Ipv4Addr::new(192, 168, 1, 1),
///     54321,
///     80,
///     payload,
/// );
///
/// assert!(matches!(packet.transport, TransportHeader::Udp(_)));
/// ```
#[derive(Debug, Clone, Serialize)]
pub struct NetworkPacket {
    pub ethernet: EthernetHeader,
    pub ipv4: Ipv4Header,
    pub transport: TransportHeader,
    pub payload: Vec<u8>,
}

#[derive(Debug, Clone, Serialize)]
#[serde(tag = "type")]
pub enum TransportHeader {
    Udp(UdpHeader),
    Tcp(TcpHeader),
}

impl NetworkPacket {
    pub fn new_udp(
        src_mac: [u8; 6],
        dst_mac: [u8; 6],
        src_ip: Ipv4Addr,
        dst_ip: Ipv4Addr,
        src_port: u16,
        dst_port: u16,
        payload: Vec<u8>,
    ) -> Self {
        let ethernet = EthernetHeader::new(src_mac, dst_mac);
        let mut udp = UdpHeader::new(src_port, dst_port, payload.len() as u16);
        let mut ipv4 = Ipv4Header::new(src_ip, dst_ip, 17, udp.length); // 17 = UDP

        // Calcul des sommes de contrôle
        udp.calculate_checksum(src_ip, dst_ip, &payload);
        ipv4.calculate_checksum();

        Self {
            ethernet,
            ipv4,
            transport: TransportHeader::Udp(udp),
            payload,
        }
    }

    pub fn new_tcp(
        src_mac: [u8; 6],
        dst_mac: [u8; 6],
        src_ip: Ipv4Addr,
        dst_ip: Ipv4Addr,
        src_port: u16,
        dst_port: u16,
        payload: Vec<u8>,
    ) -> Self {
        let ethernet = EthernetHeader::new(src_mac, dst_mac);
        let mut tcp = TcpHeader::new(src_port, dst_port);
        let mut ipv4 = Ipv4Header::new(src_ip, dst_ip, 6, 20 + payload.len() as u16); // 6 = TCP

        // Calcul des sommes de contrôle
        tcp.calculate_checksum(src_ip, dst_ip, &payload);
        ipv4.calculate_checksum();

        Self {
            ethernet,
            ipv4,
            transport: TransportHeader::Tcp(tcp),
            payload,
        }
    }

    pub fn apply_ip_bitfield(&mut self, bitfield: u8) {
        self.ipv4.apply_bitfield(bitfield);
        self.ipv4.calculate_checksum(); // Recalcul après modification
    }

    pub fn to_bytes(&self) -> Vec<u8> {
        let mut bytes = Vec::new();

        // En-tête Ethernet
        bytes.extend_from_slice(&self.ethernet.to_bytes());

        // En-tête IP
        bytes.extend_from_slice(&self.ipv4.to_bytes());

        // En-tête de transport
        match &self.transport {
            TransportHeader::Udp(udp) => bytes.extend_from_slice(&udp.to_bytes()),
            TransportHeader::Tcp(tcp) => bytes.extend_from_slice(&tcp.to_bytes()),
        }

        // Charge utile
        bytes.extend_from_slice(&self.payload);

        bytes
    }
}

/// Calcule la somme de contrôle de l'en-tête IP
fn calculate_ip_checksum(header: &[u8]) -> u16 {
    let mut sum: u32 = 0;

    // Addition de tous les mots 16 bits de l'en-tête
    for chunk in header.chunks_exact(2) {
        let word = u16::from_be_bytes([chunk[0], chunk[1]]);
        sum += word as u32;
    }

    // Ajout des retenues
    while (sum >> 16) > 0 {
        sum = (sum & 0xFFFF) + (sum >> 16);
    }

    // Complément à un
    !sum as u16
}

/// Calcule la somme de contrôle UDP
fn calculate_udp_checksum(
    src_ip: Ipv4Addr,
    dst_ip: Ipv4Addr,
    header: &[u8],
    payload: &[u8],
) -> u16 {
    let mut sum: u32 = 0;

    // Pseudo-en-tête
    let src_octets = src_ip.octets();
    let dst_octets = dst_ip.octets();

    // IP source
    sum += u16::from_be_bytes([src_octets[0], src_octets[1]]) as u32;
    sum += u16::from_be_bytes([src_octets[2], src_octets[3]]) as u32;

    // IP de destination
    sum += u16::from_be_bytes([dst_octets[0], dst_octets[1]]) as u32;
    sum += u16::from_be_bytes([dst_octets[2], dst_octets[3]]) as u32;

    // Protocole (17 pour UDP)
    sum += 17;

    // Longueur UDP
    let udp_length = header.len() + payload.len();
    sum += udp_length as u32;

    // En-tête UDP
    for chunk in header.chunks_exact(2) {
        let word = u16::from_be_bytes([chunk[0], chunk[1]]);
        sum += word as u32;
    }

    // Charge utile
    for chunk in payload.chunks_exact(2) {
        let word = u16::from_be_bytes([chunk[0], chunk[1]]);
        sum += word as u32;
    }

    // Gestion d'une longueur impaire
    if payload.len() % 2 == 1 {
        sum += (payload[payload.len() - 1] as u32) << 8;
    }

    // Ajout des retenues
    while (sum >> 16) > 0 {
        sum = (sum & 0xFFFF) + (sum >> 16);
    }

    // Complément à un
    !sum as u16
}

/// Calcule la somme de contrôle TCP (similaire à UDP)
fn calculate_tcp_checksum(
    src_ip: Ipv4Addr,
    dst_ip: Ipv4Addr,
    header: &[u8],
    payload: &[u8],
) -> u16 {
    let mut sum: u32 = 0;

    // Pseudo-en-tête
    let src_octets = src_ip.octets();
    let dst_octets = dst_ip.octets();

    // IP source
    sum += u16::from_be_bytes([src_octets[0], src_octets[1]]) as u32;
    sum += u16::from_be_bytes([src_octets[2], src_octets[3]]) as u32;

    // IP de destination
    sum += u16::from_be_bytes([dst_octets[0], dst_octets[1]]) as u32;
    sum += u16::from_be_bytes([dst_octets[2], dst_octets[3]]) as u32;

    // Protocole (6 pour TCP)
    sum += 6;

    // Longueur TCP
    let tcp_length = header.len() + payload.len();
    sum += tcp_length as u32;

    // En-tête TCP
    for chunk in header.chunks_exact(2) {
        let word = u16::from_be_bytes([chunk[0], chunk[1]]);
        sum += word as u32;
    }

    // Charge utile
    for chunk in payload.chunks_exact(2) {
        let word = u16::from_be_bytes([chunk[0], chunk[1]]);
        sum += word as u32;
    }

    // Gestion d'une longueur impaire
    if payload.len() % 2 == 1 {
        sum += (payload[payload.len() - 1] as u32) << 8;
    }

    // Ajout des retenues
    while (sum >> 16) > 0 {
        sum = (sum & 0xFFFF) + (sum >> 16);
    }

    // Complément à un
    !sum as u16
}

/// Analyse une adresse MAC au format "aa:bb:cc:dd:ee:ff"
pub fn parse_mac_address(mac_str: &str) -> Result<[u8; 6], String> {
    let parts: Vec<&str> = mac_str.split(':').collect();
    if parts.len() != 6 {
        return Err("Une adresse MAC doit comporter 6 segments séparés par ':'".to_string());
    }

    let mut mac = [0u8; 6];
    for (i, part) in parts.iter().enumerate() {
        mac[i] = u8::from_str_radix(part, 16)
            .map_err(|_| format!("Chiffre hexadécimal invalide dans l'adresse MAC : {}", part))?;
    }

    Ok(mac)
}
