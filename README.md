# VECTURE REDACT

> **CLASSIFICATION: PUBLIC RELEASE**  
> **ORIGIN: VECTURE LABORATORIES**

## // OVERVIEW

In the architecture of modern data, visibility is a variable, not a constant. 

**Vecture Redact** is a precision instrument designed to bifurcate a document into two states: the **Public Narrative** and the **Hidden Truth**. Unlike standard sanitization tools which destroy information, Redact displaces it into a cryptographic shadow—the **Vecture Key**.

To the unauthorized observer, the document appears complete, merely redacted. To the Keyholder, the original reality can be summoned at will.

## // INITIALIZATION

Python 3.8+ environment required. Do not proceed on compromised systems.

```bash
pip install -r requirements.txt
```

## // OPERATIONAL DIRECTIVES

The system recognizes two primary states of operation: **SEVER** (Redact) and **REINTEGRATE** (Restore).

### 1. SEVER (REDACT)

Scans the target asset for sensitive patterns (IPv4, Dates, Emails, Custom Entities) and excises them.

```bash
python -m vecture.main redact <TARGET_ASSET> [OPTIONS]
```

**Parameters:**
*   `--style [CLASSIC|BLACKOUT|VECTURE_NOISE]`: Choose the visual signature of the omission.
    *   `CLASSIC`: The standard `[REDACTED]` marker.
    *   `BLACKOUT`: Total visual negation (████).
    *   `VECTURE_NOISE`: Randomized alphanumeric obfuscation. Matches original length to preserve document flow.
*   `--words <FILE>`: Ingest a suppression list from an external `.txt` source.
*   `--capitals`: Engage heuristic scanning for capitalized entities. Use with caution.
*   `--obfuscate-key`: Encrypts the generated Key File. **Mandatory for sensitive operations.**

**Output Artifacts:**
*   The **Sanitized Asset** (e.g., `doc_redacted.md`): Safe for public dissemination.
*   The **Vecture Key** (`.vecture`): The displaced reality.

### 2. REINTEGRATE (RESTORE)

Reconstructs the original asset by fusing the Sanitized Asset with its Vecture Key. The system enforces a cryptographic handshake to ensure the timelines match.

```bash
python -m vecture.main restore <SANITIZED_ASSET> <KEY_FILE>
```

**Integrity Protocol:**
The Key File contains a SHA-256 hash of the sanitized state. If the public document has been altered by a third party, the system will reject the reintegration to prevent data corruption.

## // TRAINING SIMULATION

To acclimate new operators to the bifurcation process, a Level 1 simulation package is included in the repository.

**Target Assets:**
*   `example_report.md`: A sensitive field report.
*   `targets.txt`: A list of known entities to suppress.

### PHASE 1: EXECUTE PROTOCOL
Run the following directive to sever the sensitive data using the "BLACKOUT" signature and obfuscated key storage.

```bash
python -m vecture.main redact example_report.md \
    --words targets.txt \
    --style BLACKOUT \
    --capitals \
    --obfuscate-key
```

**Outcome:** The system generates `example_report_redacted.md` (Sanitized) and `example_report_redacted.md.vecture` (The Key).

### PHASE 2: OBSERVE THE VOID
Inspect the redacted file. Note that all names, dates, IPs, and specific targets have been negated.

### PHASE 3: RESTORE REALITY
Use the generated key to reconstruct the original timeline.

```bash
python -m vecture.main restore \
    example_report_redacted.md \
    example_report_redacted.md.vecture
```

**Outcome:** The original document is restored as `example_report_restored.md`.

## // ASSET MANAGEMENT: THE KEY

The `.vecture` file is the only bridge back to the original truth. 

*   **Status:** LEVEL 5 ASSET.
*   **Handling:** If this file is lost, the redacted information is mathematically unrecoverable. 
*   **Security:** If obfuscated, the key appears as static. Do not mistake it for corruption.

## // LIABILITY

Vecture Laboratories provides tools for those who shape reality. We assume no responsibility for the timelines you create or the data you choose to omit.

*Silence is engineered.*