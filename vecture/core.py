"""
Vecture Redact Core Logic
-------------------------
Implements the primary bifurcation protocols.
Responsible for pattern recognition, integrity verification, and the generation
of 'Vecture Keys'—the tether between the public void and the private truth.

Origin: VECTURE LABORATORIES
"""

import re
import hashlib
import json
import zlib
import base64
from typing import List, Tuple, Optional, Dict
from pathlib import Path

class VectureRedactor:
    """
    The engine for data bifurcation.
    
    Responsible for:
    1. Scanning text for sensitive entities (IPv4, Dates, Emails, Custom).
    2. Generating a sanitized version of the text.
    3. Constructing a cryptographic restoration key.
    4. Validating and reintegrating redacted data to restore the original state.
    """
    def __init__(self):
        # Pattern Recognition Matrix
        self.ipv4_pattern = r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
        # Temporal Coordinates: YYYY-MM-DD, DD.MM.YYYY, MM/DD/YYYY
        self.date_pattern = r'\b(?:\d{4}-\d{2}-\d{2}|\d{2}\.\d{2}\.\d{4}|\d{2}/\d{2}/\d{4})\b'
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        
    def _find_matches(self, text: str, custom_words: List[str], redact_caps: bool) -> List[Tuple[int, int, str]]:
        """
        Returns a list of (start, end, text) tuples to be redacted.
        """
        matches = []
        
        # Phase 1: Standard Entity Detection
        for pattern in [self.ipv4_pattern, self.date_pattern, self.email_pattern]:
            for m in re.finditer(pattern, text):
                matches.append((m.start(), m.end(), m.group()))
                
        # Phase 2: Targeted Entity Suppression
        for word in custom_words:
            if not word: continue
            # Normalize casing for detection
            escaped_word = re.escape(word)
            try:
                for m in re.finditer(r'\b' + escaped_word + r'\b', text, re.IGNORECASE):
                    matches.append((m.start(), m.end(), m.group()))
            except re.error:
                continue 
                
        # Phase 3: Heuristic Analysis (Capitalization)
        if redact_caps:
            # Detect Capitalized Entities
            for m in re.finditer(r'\b[A-Z][a-z]+\b', text):
                matches.append((m.start(), m.end(), m.group()))

        # Conflict Resolution: Eliminate Redundancy
        # Linear Alignment
        matches.sort(key=lambda x: x[0])
        
        cleaned_matches = []
        if not matches:
            return []
            
        # Resolve Overlapping Realities
        curr_start, curr_end, curr_text = matches[0]
        
        cleaned_matches.append(matches[0])
        
        for i in range(1, len(matches)):
            m_start, m_end, m_text = matches[i]
            last_start, last_end, last_text = cleaned_matches[-1]
            
            if m_start < last_end:
                # Overlap detected. Prioritize existing match.
                continue
            else:
                cleaned_matches.append(matches[i])
                
        return cleaned_matches

    def redact(self, text: str, style: str = "CLASSIC", custom_words: List[str] = [], redact_caps: bool = False) -> Tuple[str, Dict]:
        """
        Executes the redaction protocol on the provided text.

        Scans the input for defined patterns and replaces them according to the specified style.
        Simultaneously generates a 'Vecture Key' containing the original data and its
        positional coordinates, anchored by a SHA-256 hash of the final redacted output.

        Args:
            text (str): The raw input text to be processed.
            style (str): The visual style of redaction (CLASSIC, BLACKOUT, VECTURE_NOISE).
            custom_words (List[str]): A list of specific keywords to target for removal.
            redact_caps (bool): If True, enables heuristic scanning for capitalized entities.

        Returns:
            Tuple[str, Dict]: A tuple containing the (Redacted Text, Key Data).
        """
        matches = self._find_matches(text, custom_words, redact_caps)
        
        result_text = []
        key_restorations = []
        
        current_idx = 0
        
        for start, end, original in matches:
            # Preserve Antecedent Reality
            result_text.append(text[current_idx:start])
            
            # Select Obfuscation Method
            if style == "BLACKOUT":
                replacement = "█" * len(original)
            elif style == "VECTURE_NOISE":
                import random
                chars = "XJ9#kL@!%&?"
                replacement = "".join(random.choice(chars) for _ in range(len(original)))
            else: # CLASSIC
                replacement = "[REDACTED]"
            
            # Log Displacement Coordinates
            # Position is current length of result_text stream
            current_len = sum(len(s) for s in result_text)
            
            key_restorations.append({
                "pos": current_len,
                "text": original,
                "len": len(replacement) # Track length of silence
            })
            
            # Inject Silence
            result_text.append(replacement)
            
            current_idx = end
            
        # Preserve Remaining Reality
        result_text.append(text[current_idx:])
        
        final_redacted_text = "".join(result_text)
        
        # Generate Cryptographic Anchor (SHA-256)
        file_hash = hashlib.sha256(final_redacted_text.encode('utf-8')).hexdigest()
        
        key_data = {
            "version": "1.0",
            "hash": file_hash,
            "restorations": key_restorations
        }
        
        return final_redacted_text, key_data

    def restore(self, redacted_text: str, key_data: Dict) -> str:
        """
        Reconstructs the original reality from the redacted text and key data.

        Verifies the integrity of the redacted text against the hash stored in the key.
        If valid, it injects the hidden data back into their original positions.

        Args:
            redacted_text (str): The public, sanitized text.
            key_data (Dict): The dictionary containing restoration artifacts and hash.

        Returns:
            str: The fully restored original text.

        Raises:
            ValueError: If the hash does not match (integrity violation) or key data is corrupt.
        """
        # Verify Integrity Protocol
        current_hash = hashlib.sha256(redacted_text.encode('utf-8')).hexdigest()
        if current_hash != key_data.get("hash"):
            raise ValueError("Integrity Violation: Key file does not match the provided redacted file.")
            
        restorations = key_data.get("restorations", [])
        # Restore from the terminus to prevent coordinate drift
        restorations.sort(key=lambda x: x["pos"], reverse=True)
        
        result = redacted_text
        
        for item in restorations:
            pos = item["pos"]
            original = item["text"]
            replacement_len = item["len"]
            
            # Validate Coordinate Bounds
            if pos < 0 or pos + replacement_len > len(result):
                raise ValueError(f"Corrupt Key: Index {pos} out of bounds.")
                
            # Reintegrate
            before = result[:pos]
            after = result[pos + replacement_len:]
            result = before + original + after
            
        return result

    @staticmethod
    def obfuscate_key(key_data: Dict) -> str:
        """Compress and Base64 encode the key."""
        json_str = json.dumps(key_data)
        compressed = zlib.compress(json_str.encode('utf-8'))
        encoded = base64.b64encode(compressed).decode('ascii')
        return "VECTURE_KEY:" + encoded

    @staticmethod
    def deobfuscate_key(key_content: str) -> Dict:
        """Decode and decompress the key."""
        if key_content.startswith("VECTURE_KEY:"):
            key_content = key_content.replace("VECTURE_KEY:", "")
            try:
                decoded = base64.b64decode(key_content)
                decompressed = zlib.decompress(decoded)
                return json.loads(decompressed)
            except Exception as e:
                raise ValueError(f"Invalid Obfuscated Key: {e}")
        else:
            # Assume plain JSON
            try:
                return json.loads(key_content)
            except json.JSONDecodeError:
                raise ValueError("Invalid Key File: Not JSON or VECTURE_KEY.")
