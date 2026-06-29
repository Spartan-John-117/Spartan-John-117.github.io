use crate::error::ScannerError;
use crate::packet::NetworkPacket;
use serde_json;
use std::fs::File;
use std::io::Write;

/// Formats de sortie pour le débug
#[derive(Debug, Clone)]
pub enum DebugFormat {
    Json,
    Pcap,
}

impl DebugFormat {
    pub fn from_str(s: &str) -> Result<Self, ScannerError> {
        match s.to_lowercase().as_str() {
            "json" => Ok(DebugFormat::Json),
            "pcap" => Ok(DebugFormat::Pcap),
            _ => Err(ScannerError::InvalidArgument(format!(
                "Format de débogage invalide : {}",
                s
            ))),
        }
    }
}

/// Gestionnaire de traces chargé d'exporter les informations des paquets.
///
/// # Exemple
///
/// ```rust,ignore
/// use net_scanner::debug::{DebugFormat, DebugWriter};
/// use net_scanner::packet::NetworkPacket;
///
/// // `packet` provient généralement de `NetworkScanner::create_packet`.
/// # fn exemple(mut packet: NetworkPacket) -> Result<(), Box<dyn std::error::Error>> {
/// let mut writer = DebugWriter::new(DebugFormat::Json, "./trace.json".into());
/// writer.add_packet(packet.clone());
/// writer.write_to_file()?;
/// # Ok(())
/// # }
/// ```
pub struct DebugWriter {
    format: DebugFormat,
    file_path: String,
    packets: Vec<NetworkPacket>,
}

impl DebugWriter {
    pub fn new(format: DebugFormat, file_path: String) -> Self {
        Self {
            format,
            file_path,
            packets: Vec::new(),
        }
    }

    /// Ajoute un paquet à écrire dans le fichier de traces
    pub fn add_packet(&mut self, packet: NetworkPacket) {
        self.packets.push(packet);
    }

    /// Écrit tous les paquets collectés dans le fichier de traces
    pub fn write_to_file(&self) -> Result<(), ScannerError> {
        match self.format {
            DebugFormat::Json => self.write_json(),
            DebugFormat::Pcap => self.write_pcap(),
        }
    }

    /// Écrit les paquets au format JSON
    fn write_json(&self) -> Result<(), ScannerError> {
        let mut file = File::create(&self.file_path)?;

        let json_output = serde_json::json!({
            "packets": self.packets,
            "count": self.packets.len(),
            "format_version": "1.0"
        });

        let json_string = serde_json::to_string_pretty(&json_output).map_err(|e| {
            ScannerError::IoError(std::io::Error::new(
                std::io::ErrorKind::InvalidData,
                format!("Erreur de sérialisation JSON : {}", e),
            ))
        })?;

        file.write_all(json_string.as_bytes())?;
        Ok(())
    }

    /// Écrit les paquets au format PCAP
    fn write_pcap(&self) -> Result<(), ScannerError> {
        let mut file = File::create(&self.file_path)?;

        // Écriture de l'en-tête global PCAP
        self.write_pcap_global_header(&mut file)?;

        // Écriture de chaque paquet
        for packet in &self.packets {
            self.write_pcap_packet(&mut file, packet)?;
        }

        Ok(())
    }

    /// Écrit l'en-tête global PCAP (24 octets)
    fn write_pcap_global_header(&self, file: &mut File) -> Result<(), ScannerError> {
        let header = [
            0xD4, 0xC3, 0xB2, 0xA1, // Nombre magique (endianness little)
            0x02, 0x00, // Version majeure
            0x04, 0x00, // Version mineure
            0x00, 0x00, 0x00, 0x00, // Décalage de fuseau horaire
            0x00, 0x00, 0x00, 0x00, // Précision du timestamp
            0xFF, 0xFF, 0x00, 0x00, // Longueur maximale (65535)
            0x01, 0x00, 0x00, 0x00, // Type de lien (Ethernet)
        ];

        file.write_all(&header)?;
        Ok(())
    }

    /// Écrit une trame PCAP (16 octets d'en-tête + données)
    fn write_pcap_packet(
        &self,
        file: &mut File,
        packet: &NetworkPacket,
    ) -> Result<(), ScannerError> {
        let packet_data = packet.to_bytes();
        let packet_len = packet_data.len() as u32;

        // Récupère l'horodatage (actuellement fictif)
        let ts_sec = 0u32;
        let ts_usec = 0u32;

        // Écrit l'en-tête de trame (16 octets)
        file.write_all(&ts_sec.to_le_bytes())?; // Secondes
        file.write_all(&ts_usec.to_le_bytes())?; // Microsecondes
        file.write_all(&packet_len.to_le_bytes())?; // Longueur capturée
        file.write_all(&packet_len.to_le_bytes())?; // Longueur originale

        // Écrit les données du paquet
        file.write_all(&packet_data)?;

        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_debug_format_from_str() {
        assert!(matches!(
            DebugFormat::from_str("json"),
            Ok(DebugFormat::Json)
        ));
        assert!(matches!(
            DebugFormat::from_str("pcap"),
            Ok(DebugFormat::Pcap)
        ));
        assert!(matches!(
            DebugFormat::from_str("JSON"),
            Ok(DebugFormat::Json)
        ));
        assert!(matches!(
            DebugFormat::from_str("PCAP"),
            Ok(DebugFormat::Pcap)
        ));
        assert!(DebugFormat::from_str("invalide").is_err());
    }

    #[test]
    fn test_debug_writer_creation() {
        let writer = DebugWriter::new(DebugFormat::Json, "test.json".to_string());
        assert_eq!(writer.packets.len(), 0);
    }
}
