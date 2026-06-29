//! # Analyseur réseau à socket brut
//!
//! Cette application assemble manuellement les couches Ethernet (L2), IPv4 (L3) et UDP/TCP (L4)
//! afin de produire des trames que vous pouvez soit écrire sur disque, soit émettre réellement
//! sur une interface Linux disposant des privilèges nécessaires.
//!
//! ## Exemple rapide
//!
//! ```rust,no_run
//! use std::process::Command;
//!
//! Command::new("cargo")
//!     .args([
//!         "run",
//!         "--",
//!         "--src_ip=192.168.1.100",
//!         "--dst_ip=192.168.1.1",
//!         "--dest_port=80",
//!         "--debug_file=trace.json",
//!         "--debug_format=json",
//!         "--dry_run",
//!     ])
//!     .status()
//!     .expect("Impossible d'exécuter le scanner");
//! ```
//!
//! ## Raccourci de génération de documentation
//!
//! ```text
//! cargo doc --no-deps --open
//! ```

use clap::Parser;
use std::net::Ipv4Addr;
use std::process;

mod debug;
mod error;
mod packet;
mod scanner;

use crate::error::ScannerError;
use crate::scanner::NetworkScanner;

/// Analyseur réseau basé sur un socket brut
#[derive(Parser, Debug)]
#[command(author, version, about, long_about = None)]
struct Args {
    /// Adresse IPv4 source écrite dans l'en-tête IP
    #[arg(long = "src_ip")]
    src_ip: Option<Ipv4Addr>,

    /// Adresse IPv4 de destination pour l'en-tête IP
    #[arg(long = "dst_ip")]
    dst_ip: Option<Ipv4Addr>,

    /// Port de destination (couche 4)
    #[arg(long = "dest_port")]
    dest_port: Option<u16>,

    /// Adresse MAC source utilisée dans l'en-tête Ethernet
    #[arg(long = "src_mac")]
    src_mac: Option<String>,

    /// Adresse MAC de destination utilisée dans l'en-tête Ethernet
    #[arg(long = "dst_mac")]
    dst_mac: Option<String>,

    /// Choix du protocole de couche 4 pour la sonde
    #[arg(long = "l4_protocol", value_parser = ["udp", "tcp"])]
    l4_protocol: Option<String>,

    /// Délai entre les tentatives (en millisecondes)
    #[arg(long = "timeout_ms")]
    timeout_ms: Option<u64>,

    /// Chemin du fichier de traces
    #[arg(long = "debug_file")]
    debug_file: Option<String>,

    /// Format du fichier de traces : json ou pcap
    #[arg(long = "debug_format", value_parser = ["json", "pcap"])]
    debug_format: Option<String>,

    /// Valeur brute (8 bits) à injecter dans l'octet Flags/Fragment de l'en-tête IPv4
    #[arg(long = "ip_bitfield")]
    ip_bitfield: Option<String>,

    /// Interface réseau à utiliser pour l'envoi réel (optionnelle)
    #[arg(long = "interface")]
    interface: Option<String>,

    /// N'envoie pas les paquets sur le réseau et se contente d'écrire dans le fichier de traces
    #[arg(long = "dry_run")]
    dry_run: bool,

    /// Contenu (texte) de la payload du paquet
    #[arg(long = "payload")]
    payload: Option<String>,
}

fn main() {
    let args = Args::parse();

    let result = run_scanner(args);
    match result {
        Ok(_) => process::exit(0),
        Err(e) => {
            eprintln!("Erreur : {}", e);
            process::exit(1);
        }
    }
}

fn run_scanner(args: Args) -> Result<(), ScannerError> {
    let mut scanner = NetworkScanner::new(args)?;
    scanner.run()
}
