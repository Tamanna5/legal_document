import re
import spacy
from transformers import pipeline

def extract_legal_entities(text):
    """Extract legal entities from text using SpaCy"""
    # Load SpaCy model
    nlp = spacy.load("en_core_web_lg")
    
    # Process the text
    doc = nlp(text)
    
    # Extract entities
    entities = {
        "PERSON": [],
        "ORG": [],
        "DATE": [],
        "MONEY": [],
        "LAW": [],
        "GPE": []  # Geopolitical entities
    }
    
    for ent in doc.ents:
        if ent.label_ in entities:
            if ent.text not in entities[ent.label_]:
                entities[ent.label_].append(ent.text)
    
    # Custom patterns for legal-specific entities
    legal_patterns = [
        (r"Article\s+(\d+|[IVX]+)", "ARTICLE"),
        (r"Section\s+(\d+\.\d+|\d+)", "SECTION"),
        (r"Clause\s+(\d+\.\d+|\d+)", "CLAUSE"),
        (r"Chapter\s+(\d+|[IVX]+)", "CHAPTER"),
    ]
    
    for pattern, label in legal_patterns:
        if label not in entities:
            entities[label] = []
            
        matches = re.finditer(pattern, text)
        for match in matches:
            if match.group(0) not in entities[label]:
                entities[label].append(match.group(0))
    
    return entities

def extract_key_clauses(text):
    """Extract key legal clauses using pattern matching and NLP"""
    # Define patterns for common legal clauses
    clause_patterns = {
        "indemnification": r"(?i)(indemnification|indemnify|hold\s+harmless).{1,200}?[.;]",
        "termination": r"(?i)(terminat(e|ion)).{1,200}?[.;]",
        "confidentiality": r"(?i)(confidential|confidentiality).{1,200}?[.;]",
        "liability": r"(?i)(limit(ation)?\s+of\s+liability).{1,200}?[.;]",
        "payment": r"(?i)(payment\s+terms|payment\s+schedule).{1,200}?[.;]",
        "warranty": r"(?i)(warrant(y|ies)|guarantees).{1,200}?[.;]",
        "governing_law": r"(?i)(governing\s+law|jurisdiction).{1,200}?[.;]",
        "force_majeure": r"(?i)(force\s+majeure).{1,200}?[.;]"
    }
    
    clauses = {}
    
    # Extract clauses based on patterns
    for clause_type, pattern in clause_patterns.items():
        matches = re.finditer(pattern, text)
        extracted = []
        
        for match in matches:
            # Get the sentence or paragraph containing the match
            extracted.append(match.group(0).strip())
        
        if extracted:
            clauses[clause_type] = extracted
    
    return clauses

def identify_legal_roles(text, nlp_model):
    """Identify legal roles (parties) in the document"""
    # Common terms for parties in legal documents
    party_indicators = [
        "party", "parties", "client", "contractor", "vendor", "customer",
        "employer", "employee", "lessor", "lessee", "licensor", "licensee",
        "buyer", "seller", "landlord", "tenant", "provider", "recipient"
    ]
    
    # Identify potential parties
    parties = {}
    
    # Look for organization entities near party terms
    for indicator in party_indicators:
        # Find all occurrences of the indicator
        pattern = re.compile(rf'\b{indicator}\b', re.IGNORECASE)
        for match in pattern.finditer(text):
            # Look at the text surrounding this match
            start = max(0, match.start() - 100)
            end = min(len(text), match.end() + 100)
            surrounding_text = text[start:end]
            
            # Process this text snippet
            surrounding_doc = nlp_model(surrounding_text)
            
            # Look for organizations or people
            for ent in surrounding_doc.ents:
                if ent.label_ in ["ORG", "PERSON"]:
                    role_key = f"{indicator}_{len(parties)}" if indicator not in parties else indicator
                    parties[role_key] = ent.text
    
    return parties

def extract_obligations_and_rights(text):
    """Extract obligations, rights, and duties from legal text"""
    # Patterns for obligations
    obligation_patterns = [
        r'(shall|must|is required to|is obligated to|is responsible for)([^.;:]+)[.;:]',
        r'(has a duty to|is duty-bound to|undertakes to)([^.;:]+)[.;:]'
    ]
    
    # Patterns for rights
    right_patterns = [
        r'(may|is entitled to|has the right to|is authorized to)([^.;:]+)[.;:]',
        r'(is permitted to|can|has the option to)([^.;:]+)[.;:]'
    ]
    
    # Extract obligations
    obligations = []
    for pattern in obligation_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            modal = match.group(1)
            action = match.group(2).strip()
            obligations.append({
                "modal": modal,
                "action": action,
                "text": modal + " " + action
            })
    
    # Extract rights
    rights = []
    for pattern in right_patterns:
        for match in re.finditer(pattern, text, re.IGNORECASE):
            modal = match.group(1)
            action = match.group(2).strip()
            rights.append({
                "modal": modal,
                "action": action,
                "text": modal + " " + action
            })
    
    return {
        "obligations": obligations,
        "rights": rights
    } 