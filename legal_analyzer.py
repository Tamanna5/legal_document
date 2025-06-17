from document_processor import load_document, preprocess_text, split_into_sections
from entity_extractor import (
    extract_legal_entities,
    extract_key_clauses,
    identify_legal_roles,
    extract_obligations_and_rights
)
from summarizer import summarize_text, summarize_sections
import spacy

def analyze_legal_document(file_path):
    """Main function to analyze legal documents"""
    # Load document
    print(f"Loading document: {file_path}")
    raw_text = load_document(file_path)
    
    # Preprocess text
    print("Preprocessing text...")
    cleaned_text = preprocess_text(raw_text)
    
    # Split into sections
    print("Identifying document structure...")
    sections = split_into_sections(cleaned_text)
    
    # Extract legal entities
    print("Extracting legal entities...")
    entities = extract_legal_entities(cleaned_text)
    
    # Extract key clauses
    print("Identifying key clauses...")
    clauses = extract_key_clauses(cleaned_text)
    
    # Generate document summary
    print("Generating document summary...")
    document_summary = summarize_text(cleaned_text, max_length=200, min_length=100)
    
    # Load SpaCy model for role identification
    print("Loading NLP model for advanced analysis...")
    nlp = spacy.load("en_core_web_lg")
    
    # Identify legal roles
    print("Identifying legal parties and roles...")
    legal_roles = identify_legal_roles(cleaned_text, nlp)
    
    # Extract obligations and rights
    print("Analyzing obligations and rights...")
    obligations_rights = extract_obligations_and_rights(cleaned_text)
    
    # Generate summaries for key sections
    print("Generating section summaries...")
    section_summaries = summarize_sections(sections)
    
    # Compile results
    analysis_results = {
        "document_summary": document_summary,
        "entities": entities,
        "key_clauses": clauses,
        "section_summaries": section_summaries,
        "legal_roles": legal_roles,
        "obligations_and_rights": obligations_rights
    }
    
    return analysis_results

def display_analysis(analysis_results):
    """Format and display the analysis results"""
    print("\n" + "=" * 80)
    print(" " * 25 + "LEGAL DOCUMENT ANALYSIS")
    print("=" * 80)
    
    print("\n**Document Summary:**")
    print("-" * 80)
    print(analysis_results["document_summary"])
    
    print("\n**Key Legal Parties:**")
    print("-" * 80)
    for role, party in analysis_results["legal_roles"].items():
        print(f"{role}: {party}")
    
    print("\n**Key Legal Entities:**")
    print("-" * 80)
    for entity_type, entities in analysis_results["entities"].items():

            print(f"{entity_type}:")
            for entity in entities[:5]:  # Limit to 5 entities per category
                print(f"  - {entity}")
            if len(entities) > 5:
                print(f"  - ... and {len(entities) - 5} more")
    
    print("\n**Key Clauses:**")
    print("-" * 80)
    for clause_type, clauses in analysis_results["key_clauses"].items():
        if clauses:
            print(f"{clause_type.upper().replace('_', ' ')}:")
            for clause in clauses[:2]:  # Limit to 2 examples per clause type
                print(f"  - {clause[:200]}..." if len(clause) > 200 else f"  - {clause}")
            if len(clauses) > 2:
                print(f"  - ... and {len(clauses) - 2} more instances")
            print()
    
    print("\n**Key Obligations:**")
    print("-" * 80)
    for obligation in analysis_results["obligations_and_rights"]["obligations"][:5]:
        print(f"  - {obligation['text']}")
    if len(analysis_results["obligations_and_rights"]["obligations"]) > 5:
        print(f"  - ... and {len(analysis_results['obligations_and_rights']['obligations']) - 5} more obligations")
    
    print("\n**Section Summaries:**")
    print("-" * 80)
    for section in analysis_results["section_summaries"]:
        print(f"{section['heading']}:")
        print(f"  {section['summary']}")
        print() 