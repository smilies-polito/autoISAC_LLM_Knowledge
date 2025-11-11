import json
from collections import Counter, defaultdict

def analyze_procedures_and_techniques(file_path):
    """
    Read a JSON file and analyze procedures and techniques comprehensively
    
    Args:
        file_path (str): Path to the JSON file
    
    Returns:
        dict: Dictionary with comprehensive analysis results
    """
    try:
        # Read the JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # Handle both single object and array of objects
        if isinstance(data, dict):
            data = [data]
        
        # Initialize counters and trackers
        procedure_title_counts = Counter()
        procedure_type_counts = Counter()
        technique_title_counts = Counter()
        weighted_procedure_counts = defaultdict(int)
        total_techniques_per_procedure = {}
        
        # Process each procedure
        for item in data:
            if not isinstance(item, dict):
                continue
                
            # Get procedure information
            procedure_title = item.get('title', 'No title')
            procedure_type = item.get('type', 'No type')
            procedure_id = item.get('id', 'No ID')
            
            # Count procedure titles and types
            procedure_title_counts[procedure_title] += 1
            procedure_type_counts[procedure_type] += 1
            
            # Process techniques within this procedure
            techniques = item.get('technique', [])
            if not isinstance(techniques, list):
                techniques = [techniques] if techniques else []
            
            num_techniques = len(techniques)
            total_techniques_per_procedure[procedure_id] = num_techniques
            
            # Count technique titles
            for technique in techniques:
                if isinstance(technique, dict):
                    technique_title = technique.get('title', 'No technique title')
                    technique_title_counts[technique_title] += 1
            
            # Calculate weighted count (procedure count * number of techniques)
            weighted_procedure_counts[procedure_title] += num_techniques
        
        return {
            'procedure_title_counts': dict(procedure_title_counts),
            'procedure_type_counts': dict(procedure_type_counts),
            'technique_title_counts': dict(technique_title_counts),
            'weighted_procedure_counts': dict(weighted_procedure_counts),
            'total_techniques_per_procedure': total_techniques_per_procedure
        }
    
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {e}")
        return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def print_analysis_results(results):
    """
    Print comprehensive analysis results in a formatted way
    """
    if not results:
        return
    
    print("COMPREHENSIVE PROCEDURE AND TECHNIQUE ANALYSIS")
    print("=" * 60)
    
    # 1. Procedure Title Counts (Simple count)
    print("\n1. PROCEDURE TITLE COUNTS (Simple Count)")
    print("-" * 45)
    procedure_counts = results['procedure_title_counts']
    sorted_procedures = sorted(procedure_counts.items(), key=lambda x: x[1], reverse=True)
    
    for title, count in sorted_procedures:
        print(f"'{title}': {count} procedure(s)")
    
    print(f"\nTotal unique procedure titles: {len(procedure_counts)}")
    print(f"Total procedure entries: {sum(procedure_counts.values())}")
    
    # 2. Procedure Type Counts
    print("\n2. PROCEDURE TYPE COUNTS")
    print("-" * 30)
    type_counts = results['procedure_type_counts']
    for proc_type, count in sorted(type_counts.items()):
        print(f"'{proc_type}': {count}")
    
    # 3. Technique Title Counts
    print("\n3. TECHNIQUE TITLE COUNTS")
    print("-" * 30)
    technique_counts = results['technique_title_counts']
    sorted_techniques = sorted(technique_counts.items(), key=lambda x: x[1], reverse=True)
    
    for title, count in sorted_techniques:
        print(f"'{title}': {count} technique(s)")
    
    print(f"\nTotal unique technique titles: {len(technique_counts)}")
    print(f"Total technique entries: {sum(technique_counts.values())}")
    
    # 4. Weighted Procedure Counts (Procedure * Techniques)
    print("\n4. WEIGHTED PROCEDURE COUNTS (Procedure × Number of Techniques)")
    print("-" * 65)
    weighted_counts = results['weighted_procedure_counts']
    sorted_weighted = sorted(weighted_counts.items(), key=lambda x: x[1], reverse=True)
    
    for title, weighted_count in sorted_weighted:
        simple_count = procedure_counts.get(title, 0)
        avg_techniques = weighted_count / simple_count if simple_count > 0 else 0
        print(f"'{title}':")
        print(f"  - Simple count: {simple_count}")
        print(f"  - Weighted count: {weighted_count}")
        print(f"  - Avg techniques per procedure: {avg_techniques:.1f}")
        print()
    
    # 5. Summary Statistics
    print("5. SUMMARY STATISTICS")
    print("-" * 25)
    total_procedures = sum(procedure_counts.values())
    total_techniques = sum(technique_counts.values())
    total_weighted = sum(weighted_counts.values())
    
    print(f"Total procedures: {total_procedures}")
    print(f"Total techniques: {total_techniques}")
    print(f"Total weighted count: {total_weighted}")
    print(f"Average techniques per procedure: {total_techniques/total_procedures:.2f}")
    print(f"Unique procedure titles: {len(procedure_counts)}")
    print(f"Unique technique titles: {len(technique_counts)}")
    
    # 6. Techniques per procedure breakdown
    print("\n6. TECHNIQUES PER PROCEDURE BREAKDOWN")
    print("-" * 40)
    techniques_per_proc = results['total_techniques_per_procedure']
    technique_distribution = Counter(techniques_per_proc.values())
    
    for num_techniques, count in sorted(technique_distribution.items()):
        print(f"Procedures with {num_techniques} technique(s): {count}")

def main():
    # Replace with your actual file path
    file_path = "procedures.json"
    
    print("Analyzing JSON file for procedures and techniques...")
    print("=" * 60)
    
    results = analyze_procedures_and_techniques(file_path)
    
    if results:
        print_analysis_results(results)
    else:
        print("Failed to process the file.")
        print("\nTroubleshooting tips:")
        print("1. Check if the file path is correct")
        print("2. Ensure the file contains valid JSON")
        print("3. Make sure the file is not empty")
        print("4. Check file permissions")
        print("5. Verify the JSON structure matches expected format")

if __name__ == "__main__":
    main()