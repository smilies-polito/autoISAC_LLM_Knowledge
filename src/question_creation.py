import json
import random
from openai import OpenAI 
from typing import List, Dict, Any
import time
from dataclasses import dataclass
from enum import Enum
import os

class EntityType(Enum):
    TACTIC = "tactic"
    TECHNIQUE = "technique"
    PROCEDURE = "procedure"

@dataclass
class MCQQuestion:
    """Data class to represent a multiple choice question"""
    entity_id: str
    entity_title: str
    entity_type: str
    question_type: str
    question: str
    options: List[str]
    correct_answer: str
    explanation: str

class ISACMCQGenerator:
    """
    Generator for multiple choice questions based on auto ISAC attack data.
    Handles tactics, techniques, and procedures with specialized prompts for each.
    """
    
    def __init__(self, api_key: str, model: str = "gpt-4"):
        """
        Initialize the MCQ generator with OpenAI API key and model.
        
        Args:
            api_key: OpenAI API key
            model: GPT model to use (default: gpt-4)
                    Common options: "gpt-4", "gpt-4-turbo", "gpt-3.5-turbo", etc.
        """
        self.client = OpenAI(api_key=api_key)  # Updated to use new client
        self.model = model
        self.question_styles = ["Factual Recall MCQ", "Scenario-Based", "Diagnostic MCQ"]
        print(f"Initialized ISACMCQGenerator with model: {model}")
        
    def get_tactic_system_prompt(self) -> str:
        """System prompt for generating questions from tactic data"""
        return """You are an expert cybersecurity educator specializing in automotive security and MITRE ATT&CK frameworks. Your task is to generate high-quality multiple choice questions based on auto ISAC tactic data.
                    You select the best question style.
        
                    You will receive JSON data containing:
                    - A tactic with its description and context
                    - Multiple techniques within that tactic, each with detailed descriptions

                    For each technique within the tactic, generate ONE multiple choice question using one of these three styles:

                    1. **Factual Recall MCQ**: Tests direct knowledge of facts, definitions, or specific details
                    2. **Scenario-Based**: Presents a realistic automotive security scenario requiring application of knowledge
                    3. **Diagnostic MCQ**: Tests ability to identify, analyze, or troubleshoot security issues

                    ## Critical Requirements:

                    **TACTIC INTEGRATION**: Each question MUST prominently integrate information from the tactic description to create questions that demonstrate the relationship between the overarching tactic and the specific technique. Questions should:
                    - Reference the tactic's purpose, goals, or methodology described in the tactic description
                    - Show how the specific technique serves the broader tactic objectives
                    - Connect the technique to the tactic's context within automotive attack scenarios
                    - Use terminology and concepts from BOTH the tactic and technique descriptions

                    **QUESTION LENGTH**: Questions should be **medium length** - clear and comprehensive but concise. Aim for 2-3 sentences maximum that efficiently convey the scenario or concept without unnecessary detail.

                    ## Additional Requirements:
                    - Generate exactly ONE question per technique within the tactic
                    - Randomly select question style for each technique
                    - Include 4 answer options (A, B, C, D)
                    - Provide clear explanation for the correct answer that references both tactic and technique context
                    - Focus on automotive/vehicle security context
                    - Ensure questions are challenging
                    - Make incorrect options plausible but clearly wrong to experts
                    - Demonstrate understanding of how techniques fit within the larger tactic framework

                    ## Output format:
                    Return a JSON array with one object per technique:
                    json
                    [
                    {
                        "technique_id": "technique ID from input",
                        "technique_title": "technique title",
                        "question_type": "Factual Recall MCQ|Scenario-Based|Diagnostic MCQ",
                        "question": "the question text that integrates tactic context",
                        "options": {
                        "A": "option A text",
                        "B": "option B text", 
                        "C": "option C text",
                        "D": "option D text"
                        },
                        "correct_answer": "A|B|C|D",
                        "explanation": "detailed explanation referencing both tactic purpose/context and technique specifics"
                    }
                    ]

                    ## Complete Example: Input and Expected Output

                    **Example Input JSON:**
                    json
                    {
                        "title": "Credential Access",
                        "type": "tactic",
                        "description": "<p>The adversary is trying to steal vehicle network credentials.</p><p>Credential Access consists of techniques for stealing vehicle network credentials like cryptographic tokens, keys, and passwords. Techniques used to get credentials include credential dumping and collecting unsecured credentials stored on ECU file systems. Using legitimate credentials can give adversaries access to vehicle systems and make them harder to detect.</p>",
                        "technique": [
                            {
                                "title": "Network Sniffing",
                                "type": "technique",
                                "description": "<p>Adversaries may sniff vehicle network traffic to capture information about an environment, including authentication material passed over the vehicle network. Network sniffing refers to using the network interface on a system to monitor or capture information sent over a wired or wireless vehicle network connection.</p>",
                                "id": "ATM-T0038"
                            },
                            {
                                "title": "Input Capture",
                                "type": "technique", 
                                "description": "<p>Adversaries may capture user input to obtain credentials or other information from the user through various methods. Malware may masquerade as a legitimate third-party keyboard to record user keystrokes.</p>",
                                "id": "ATM-T0036"
                            }
                        ]
                    }
                    

                    **Expected Output:**
                    json
                    [
                        {
                            "technique_id": "ATM-T0038",
                            "technique_title": "Network Sniffing",
                            "question_type": "Scenario-Based",
                            "question": "An adversary wants to steal vehicle network credentials like cryptographic tokens to gain system access. Which method best supports this credential access tactic by passively capturing authentication data?",
                            "options": {
                                "A": "Performing a denial-of-service attack on the CAN bus",
                                "B": "Network sniffing to monitor vehicle network traffic",
                                "C": "Physically disconnecting ECU connections",
                                "D": "Installing malware that deletes authentication logs"
                            },
                            "correct_answer": "B",
                            "explanation": "Network sniffing directly supports credential access by passively monitoring vehicle network traffic to capture authentication material like cryptographic tokens and passwords, enabling adversaries to steal vehicle network credentials for system access."
                        },
                        {
                            "technique_id": "ATM-T0036", 
                            "technique_title": "Input Capture",
                            "question_type": "Diagnostic MCQ",
                            "question": "You discover that vehicle network passwords are being stolen through keystroke recording. What technique is most likely being used to support this credential access attack?",
                            "options": {
                                "A": "Malicious third-party keyboard application capturing input",
                                "B": "Physical tampering with the vehicle's steering controls",
                                "C": "Wireless signal jamming of vehicle communications",
                                "D": "Overheating ECU processors to cause malfunctions"
                            },
                            "correct_answer": "A",
                            "explanation": "Input capture through malicious keyboard applications enables adversaries to record user keystrokes when entering passwords, directly supporting the credential access tactic's goal of stealing vehicle network credentials like passwords and tokens."
                        }
                    ]
                    

                    Remember to:
                    - **PRIORITIZE tactic-technique integration**: Every question should clearly demonstrate understanding of how the technique serves the broader tactic
                    - **Keep questions medium length**: 2-3 sentences maximum, clear but concise
                    - Use automotive security context in all questions
                    - Make questions practical and applicable to real-world automotive cybersecurity scenarios
                    - Ensure technical accuracy based on the provided tactic AND technique descriptions
                    - Create plausible but incorrect distractors that test understanding of the tactic-technique relationship
                    - Reference the tactic's strategic context when explaining why techniques are used
                    - Follow the example patterns shown above to integrate tactic purpose with technique specifics
                    - Put the right answer in the correct_answer field as "A", "B", "C", or "D"
                    - Randomly select question style for each technique to ensure variety: Factual Recall MCQ, Scenario-Based or Diagnostic MCQ
                    """

    def get_technique_system_prompt(self) -> str:
        """System prompt for generating questions from individual technique data"""
        return """You are an expert cybersecurity educator specializing in automotive security and MITRE ATT&CK frameworks. Your task is to generate high-quality multiple choice questions based on individual auto ISAC technique data.
                    You select the best question style.
                    You will receive JSON data containing a single technique with its detailed description.

                    Generate ONE multiple choice question using one of these three styles:

                    1. **Factual Recall MCQ**: Tests direct knowledge of facts, definitions, or specific details about the technique
                    2. **Scenario-Based**: Presents a realistic automotive security scenario where this technique would be applied
                    3. **Diagnostic MCQ**: Tests ability to identify, analyze, or troubleshoot issues related to this technique

                    ## Requirements:
                    - Generate exactly ONE question for the technique
                    - Randomly select question style
                    - Include 4 answer options (A, B, C, D)
                    - Provide clear explanation for the correct answer
                    - Focus deeply on the specific technique provided
                    - Use automotive/vehicle security context
                    - **Keep questions medium length**: 2-3 sentences maximum, clear but concise
                    - Ensure questions are challenging
                    - Make incorrect options plausible but clearly wrong to experts

                    ## Output format:
                    json
                    {
                    "technique_id": "technique ID from input",
                    "technique_title": "technique title",
                    "question_type": "Factual Recall MCQ|Scenario-Based|Diagnostic MCQ",
                    "question": "the question text",
                    "options": {
                        "A": "option A text",
                        "B": "option B text", 
                        "C": "option C text",
                        "D": "option D text"
                    },
                    "correct_answer": "A|B|C|D",
                    "explanation": "detailed explanation of why the answer is correct"
                    }


                    ## Examples:

                    **Example 1 Input**:
                    json
                    {
                        "title": "Abuse UDS for Collection",
                        "type": "technique",
                        "description": "<p>The adversary can attempt to abuse UDS 'read' capabilities, such as 'read memory by address' to access customer information from an ECU's storage or memory.</p>",
                        "createdAt": "2023-08-09T09:51:19.125Z",
                        "mitreId": "T0055",
                        "technique": [],
                        "updatedAt": "2024-08-30T19:17:20.377Z",
                        "id": "ATM-T0055",
                        "lastModifiedAt": "2024-08-30T19:17:20.377Z"
                    }


                    **Example 1 Output**:
                    json
                    {
                    "technique_id": "ATM-T0055",
                    "technique_title": "Abuse UDS for Collection",
                    "question_type": "Scenario-Based",
                    "question": "A security researcher discovers that an attacker has been sending UDS requests to various ECUs in a connected vehicle. Which UDS service would most likely be exploited to extract stored customer data from ECU memory?",
                    "options": {
                        "A": "Service 0x27 - Security Access to unlock protected diagnostic functions",
                        "B": "Service 0x23 - Read Memory by Address to access specific memory locations",
                        "C": "Service 0x22 - Read Data by Identifier to read predefined data parameters",
                        "D": "Service 0x31 - Routine Control to execute diagnostic routines"
                    },
                    "correct_answer": "B",
                    "explanation": "Service 0x23 (Read Memory by Address) is the primary UDS service that allows direct access to ECU memory locations, making it the most effective method for adversaries to extract customer information stored in ECU memory. While other services have legitimate diagnostic purposes, Read Memory by Address provides the raw memory access capability specifically mentioned in this attack technique."
                    }



                    **Example 2 Input**:
                    json
                    {
                        "title": "Location Tracking",
                        "type": "technique",
                        "description": "<p>An adversary could use a malicious or exploited application to surreptitiously track the vehicle's physical location through use of standard operating system APIs.</p><p>This technique's description was adapted from <a href=\"https://attack.mitre.org/techniques/T1430/\">MITRE ATT&amp;CK</a>.</p>",
                        "createdAt": "2023-08-09T09:51:19.131Z",
                        "mitreId": "T0043",
                        "technique": [],
                        "updatedAt": "2024-08-30T19:15:24.474Z",
                        "id": "ATM-T0043",
                        "lastModifiedAt": "2024-08-30T19:15:24.474Z"
                    }


                    **Example 2 Output**:
                    json
                    {
                    "technique_id": "ATM-T0043",
                    "technique_title": "Location Tracking",
                    "question_type": "Diagnostic MCQ",
                    "question": "A vehicle owner reports unusual data usage from their infotainment system despite minimal user interaction. Which indicator would most strongly suggest a malicious application is performing unauthorized location tracking?",
                    "options": {
                        "A": "Increased cellular data consumption during stationary periods with GPS API calls logged",
                        "B": "Frequent system updates being downloaded automatically by the infotainment unit",
                        "C": "Higher than normal CPU usage during media playback operations",
                        "D": "Periodic Bluetooth scanning for nearby devices while driving"
                    },
                    "correct_answer": "A",
                    "explanation": "Increased cellular data consumption during stationary periods combined with GPS API calls strongly indicates unauthorized location tracking. A malicious application would continuously collect location data and transmit it externally, resulting in unexplained data usage even when the vehicle isn't being actively used. The other options represent normal system behaviors that wouldn't specifically indicate location tracking abuse."
                    }



                    Remember to:
                    - Focus specifically on the single technique provided
                    - **Keep questions medium length**: 2-3 sentences maximum, clear but concise
                    - Use realistic automotive scenarios and technical details
                    - Create questions that test deep understanding of the technique
                    - Ensure all distractors are related but clearly incorrect
                    - Put the right answer in the correct_answer field as "A", "B", "C", or "D"
                    - Randomly select question style for each technique to ensure variety: Factual Recall MCQ, Scenario-Based or Diagnostic MCQ
                    """

    def get_procedure_system_prompt(self) -> str:
        """System prompt for generating questions from procedure data"""
        return """You are an expert cybersecurity educator specializing in automotive security and MITRE ATT&CK frameworks. Your task is to generate high-quality multiple choice questions based on auto ISAC procedure data.

                You will receive JSON data containing:
                - A procedure with its title and detailed description of a real-world attack scenario
                - Associated techniques that are used within this procedure

                Procedures represent specific implementations or real-world examples of how techniques are combined and executed in actual attack scenarios.

                Generate 2-3 multiple choice questions for the procedure using these styles:

                1. **Factual Recall MCQ**: Tests knowledge of specific facts, steps, or details from the procedure
                2. **Scenario-Based**: Tests understanding of how the procedure would work in similar contexts
                3. **Diagnostic MCQ**: Tests ability to identify, analyze, or respond to this type of attack procedure

                ## Requirements:
                - Generate 2-3 questions total for the procedure (you decide based on complexity)
                - Use different question styles for variety
                - Include 4 answer options (A, B, C, D) for each question
                - Provide clear explanation for each correct answer
                - Focus on the specific attack procedure described
                - Use automotive/vehicle security context
                - Connect the procedure to its associated techniques when relevant
                - Make questions practical for security professionals

                ## Output format:
                Return a JSON array with 2-3 question objects:
                ```json
                [
                {
                    "procedure_id": "procedure ID from input",
                    "procedure_title": "procedure title",
                    "question_type": "Factual Recall MCQ|Scenario-Based|Diagnostic MCQ",
                    "question": "the question text",
                    "options": {
                    "A": "option A text",
                    "B": "option B text", 
                    "C": "option C text",
                    "D": "option D text"
                    },
                    "correct_answer": "A|B|C|D",
                    "explanation": "detailed explanation of why the answer is correct"
                }
                ]
                ```

                ## Example:

                **Input procedure**: "CAN Message Injection"
                **Description**: Researchers discussed activating brakes through collision prevention system in ABS for Jeep Cherokee by disabling ACC and Front Facing Camera Module, then replaying collision event messages.

                **Example Output**:
                ```json
                [
                {
                    "procedure_id": "ATM-P0034",
                    "procedure_title": "CAN Message Injection",
                    "question_type": "Factual Recall MCQ",
                    "question": "In the documented CAN Message Injection procedure targeting a Jeep Cherokee's braking system, which components must be disabled before replaying collision event messages?",
                    "options": {
                    "A": "Electronic Stability Control and Traction Control System",
                    "B": "Adaptive Cruise Control and Front Facing Camera Module", 
                    "C": "Anti-lock Braking System and Electronic Brake Distribution",
                    "D": "Parking Assist System and Blind Spot Monitoring"
                    },
                    "correct_answer": "B",
                    "explanation": "According to the documented procedure, attackers must first disable both the Adaptive Cruise Control (ACC) and Front Facing Camera Module before they can successfully replay the collision event messages to activate the brakes through the collision prevention system."
                },
                {
                    "procedure_id": "ATM-P0034", 
                    "procedure_title": "CAN Message Injection",
                    "question_type": "Diagnostic MCQ",
                    "question": "A security analyst detects unusual CAN bus activity where collision prevention messages are being replayed while the ACC and camera systems show as disabled. What type of attack procedure is most likely being executed?",
                    "options": {
                    "A": "ECU firmware manipulation to alter braking algorithms",
                    "B": "Physical tampering with brake line sensors",
                    "C": "CAN Message Injection to trigger unintended brake activation", 
                    "D": "Wireless jamming of vehicle-to-vehicle communications"
                    },
                    "correct_answer": "C",
                    "explanation": "The pattern of disabled ACC/camera systems followed by replayed collision messages is characteristic of the CAN Message Injection procedure, which manipulates the collision prevention system to activate brakes by replaying legitimate collision event messages at inappropriate times."
                }
                ]
                ```

                Remember to:
                - Focus on the specific real-world attack procedure described
                - Generate questions that help security professionals understand and identify these procedures
                - Use technical details from the procedure description
                - Create realistic scenarios based on the documented attack method"""

    def identify_entity_type(self, json_data: Dict[str, Any]) -> EntityType:
        """
        Identify the type of entity from JSON data.
        
        Args:
            json_data: The parsed JSON data
            
        Returns:
            EntityType enum value
        """
        entity_type = json_data.get('type', '').lower()
        
        if entity_type == 'tactic':
            return EntityType.TACTIC
        elif entity_type == 'procedure':
            return EntityType.PROCEDURE
        elif entity_type == 'technique':
            return EntityType.TECHNIQUE
        else:
            # Fallback: if it has technique array, it's probably a tactic
            if 'technique' in json_data and isinstance(json_data['technique'], list) and len(json_data['technique']) > 0:
                return EntityType.TACTIC
            else:
                return EntityType.TECHNIQUE

    def extract_entities_from_json(self, json_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extract entity information based on the type detected.
        
        Args:
            json_data: The parsed JSON data
            
        Returns:
            List of entity dictionaries
        """
        entity_type = self.identify_entity_type(json_data)
        entities = []
        
        if entity_type == EntityType.TACTIC:
            # For tactics, create entries for each technique
            tactic_info = {
                'tactic_title': json_data.get('title', ''),
                'tactic_description': json_data.get('description', ''),
                'tactic_id': json_data.get('id', json_data.get('mitreId', ''))
            }
            
            for technique in json_data.get('technique', []):
                technique_data = {
                    'entity_id': technique.get('id', technique.get('mitreId', '')),
                    'entity_title': technique.get('title', ''),
                    'entity_type': 'technique',
                    'entity_description': technique.get('description', ''),
                    'parent_tactic': tactic_info
                }
                entities.append(technique_data)
                
        elif entity_type == EntityType.PROCEDURE:
            # For procedures, create a single entry
            procedure_data = {
                'entity_id': json_data.get('id', json_data.get('mitreId', '')),
                'entity_title': json_data.get('title', ''),
                'entity_type': 'procedure',
                'entity_description': json_data.get('description', ''),
                'associated_techniques': json_data.get('technique', [])
            }
            entities.append(procedure_data)
            
        elif entity_type == EntityType.TECHNIQUE:
            # For individual techniques, create a single entry
            technique_data = {
                'entity_id': json_data.get('id', json_data.get('mitreId', '')),
                'entity_title': json_data.get('title', ''),
                'entity_type': 'technique',
                'entity_description': json_data.get('description', ''),
                'sub_techniques': json_data.get('technique', [])  # In case it has sub-techniques
            }
            entities.append(technique_data)
            
        return entities

    def generate_mcq_for_entity(self, entity_data: Dict[str, Any]) -> List[MCQQuestion]:
        """
        Generate MCQ(s) for a given entity using the appropriate system prompt.
        
        Args:
            entity_data: Dictionary containing entity information
            
        Returns:
            List of MCQQuestion objects
        """
        entity_type = entity_data['entity_type']
        
        # Select appropriate system prompt
        if entity_type == 'technique' and 'parent_tactic' in entity_data:
            # Technique within a tactic
            system_prompt = self.get_tactic_system_prompt()
            user_prompt = self._create_tactic_user_prompt(entity_data)
        elif entity_type == 'technique':
            # Individual technique
            system_prompt = self.get_technique_system_prompt()
            user_prompt = self._create_technique_user_prompt(entity_data)
        elif entity_type == 'procedure':
            # Procedure
            system_prompt = self.get_procedure_system_prompt()
            user_prompt = self._create_procedure_user_prompt(entity_data)
        else:
            raise ValueError(f"Unknown entity type: {entity_type}")

        try:
            # Updated to use new OpenAI client
            response = self.client.chat.completions.create(
                model=self.model,  # Now properly uses the specified model
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Parse response based on expected format
            if entity_type == 'procedure':
                # Procedures return arrays of questions
                return self._parse_procedure_response(response_text, entity_data)
            else:
                # Techniques return single questions
                return [self._parse_technique_response(response_text, entity_data)]
                
        except Exception as e:
            print(f"Error generating MCQ for {entity_type} {entity_data['entity_title']}: {str(e)}")
            return []

    def _create_tactic_user_prompt(self, entity_data: Dict[str, Any]) -> str:
        """Create user prompt for tactic-based technique"""
        tactic = entity_data['parent_tactic']
        return f"""Generate a multiple choice question for the following technique within its tactic context:

                **Tactic Context:**
                - Title: {tactic['tactic_title']}
                - Description: {tactic['tactic_description']}

                **Technique Details:**
                - ID: {entity_data['entity_id']}
                - Title: {entity_data['entity_title']}
                - Description: {entity_data['entity_description']}

                Please generate exactly one question following the specified format and requirements."""

    def _create_technique_user_prompt(self, entity_data: Dict[str, Any]) -> str:
        """Create user prompt for individual technique"""
        return f"""Generate a multiple choice question for the following technique:
                **Technique Details:**
                - ID: {entity_data['entity_id']}
                - Title: {entity_data['entity_title']}
                - Description: {entity_data['entity_description']}
                Please generate exactly one question following the specified format and requirements."""

    def _create_procedure_user_prompt(self, entity_data: Dict[str, Any]) -> str:
        """Create user prompt for procedure"""
        techniques_info = ""
        if entity_data.get('associated_techniques'):
            techniques_info = "\n**Associated Techniques:**\n"
            for tech in entity_data['associated_techniques']:
                techniques_info += f"- {tech.get('title', '')}: {tech.get('description', '')}\n"
        
        return f"""Generate 2-3 multiple choice questions for the following procedure:
                    **Procedure Details:**
                    - ID: {entity_data['entity_id']}
                    - Title: {entity_data['entity_title']}
                    - Description: {entity_data['entity_description']}
                    {techniques_info}
                    Please generate 2-3 questions following the specified format and requirements."""

    def _parse_technique_response(self, response_text: str, entity_data: Dict[str, Any]) -> MCQQuestion:
        """Parse response for single technique question"""
        # Extract JSON from response
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        
        if start_idx != -1 and end_idx != -1:
            json_str = response_text[start_idx:end_idx]
            question_data = json.loads(json_str)
            
            return MCQQuestion(
                entity_id=question_data.get('technique_id', entity_data['entity_id']),
                entity_title=question_data.get('technique_title', entity_data['entity_title']),
                entity_type=entity_data['entity_type'],
                question_type=question_data['question_type'],
                question=question_data['question'],
                options=list(question_data['options'].values()),
                correct_answer=question_data['correct_answer'],
                explanation=question_data['explanation']
            )
        else:
            raise ValueError("Could not parse JSON from GPT response")

    def _parse_procedure_response(self, response_text: str, entity_data: Dict[str, Any]) -> List[MCQQuestion]:
        """Parse response for procedure questions (multiple questions)"""
        # Extract JSON array from response
        start_idx = response_text.find('[')
        end_idx = response_text.rfind(']') + 1
        
        if start_idx != -1 and end_idx != -1:
            json_str = response_text[start_idx:end_idx]
            questions_data = json.loads(json_str)
            
            mcqs = []
            for question_data in questions_data:
                mcq = MCQQuestion(
                    entity_id=question_data.get('procedure_id', entity_data['entity_id']),
                    entity_title=question_data.get('procedure_title', entity_data['entity_title']),
                    entity_type=entity_data['entity_type'],
                    question_type=question_data['question_type'],
                    question=question_data['question'],
                    options=list(question_data['options'].values()),
                    correct_answer=question_data['correct_answer'],
                    explanation=question_data['explanation']
                )
                mcqs.append(mcq)
            return mcqs
        else:
            raise ValueError("Could not parse JSON array from GPT response")

    def generate_all_mcqs(self, json_file_path: str, output_file_path: str = None) -> List[MCQQuestion]:
        """
        Generate MCQs for all entities in the provided JSON file.
        
        Args:
            json_file_path: Path to the auto ISAC JSON file
            output_file_path: Optional path to save results as JSON
            
        Returns:
            List of MCQQuestion objects
        """
        # Load JSON data
        with open(json_file_path, 'r', encoding='utf-8') as file:
            json_data = json.load(file)
        
        # Handle both single objects and arrays
        if isinstance(json_data, list):
            # If it's an array, process each item separately
            all_mcqs = []
            print(f"Found array with {len(json_data)} items to process...")
            
            for i, item in enumerate(json_data, 1):
                print(f"\nProcessing item {i}/{len(json_data)}")
                entities = self.extract_entities_from_json(item)
                entity_type = self.identify_entity_type(item)
        
                print(f"Detected entity type: {entity_type.value}")
                print(f"Found {len(entities)} entities in this item...")
                
                # Generate MCQs for this item
                for j, entity in enumerate(entities, 1):
                    print(f"Processing {entity['entity_type']} {j}/{len(entities)}: {entity['entity_title']}")
                    
                    mcqs = self.generate_mcq_for_entity(entity)
                    if mcqs:
                        all_mcqs.extend(mcqs)
                        print(f"✓ Generated {len(mcqs)} question(s)")
                        for mcq in mcqs:
                            print(f"  - {mcq.question_type}")
                    else:
                        print("✗ Failed to generate MCQs")
                    
                    # Add delay to respect API rate limits
                    time.sleep(1)
        else:
            # Original logic for single object
            entities = self.extract_entities_from_json(json_data)
            entity_type = self.identify_entity_type(json_data)
            
            print(f"Detected entity type: {entity_type.value}")
            print(f"Found {len(entities)} entities to process...")
            
            # Generate MCQs
            all_mcqs = []
            for i, entity in enumerate(entities, 1):
                print(f"Processing {entity['entity_type']} {i}/{len(entities)}: {entity['entity_title']}")
                
                mcqs = self.generate_mcq_for_entity(entity)
                if mcqs:
                    all_mcqs.extend(mcqs)
                    print(f"✓ Generated {len(mcqs)} question(s)")
                    for mcq in mcqs:
                        print(f"  - {mcq.question_type}")
                else:
                    print("✗ Failed to generate MCQs")
                
                # Add delay to respect API rate limits
                time.sleep(1)
        
        print(f"\nGenerated {len(all_mcqs)} MCQs successfully!")
        
        # Save to file if specified
        if output_file_path:
            self.save_mcqs_to_file(all_mcqs, output_file_path)
        
        return all_mcqs

    def save_mcqs_to_file(self, mcqs: List[MCQQuestion], file_path: str):
        """Save generated MCQs to a JSON file."""
        mcqs_data = []
        for mcq in mcqs:
            mcq_dict = {
                'entity_id': mcq.entity_id,
                'entity_title': mcq.entity_title,
                'entity_type': mcq.entity_type,
                'question_type': mcq.question_type,
                'question': mcq.question,
                'options': {
                    'A': mcq.options[0] if len(mcq.options) > 0 else '',
                    'B': mcq.options[1] if len(mcq.options) > 1 else '',
                    'C': mcq.options[2] if len(mcq.options) > 2 else '',
                    'D': mcq.options[3] if len(mcq.options) > 3 else ''
                },
                'correct_answer': mcq.correct_answer,
                'explanation': mcq.explanation
            }
            mcqs_data.append(mcq_dict)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(mcqs_data, file, indent=2, ensure_ascii=False)
        
        print(f"MCQs saved to {file_path}")

    def print_mcqs(self, mcqs: List[MCQQuestion]):
        """Print MCQs in a readable format."""
        for i, mcq in enumerate(mcqs, 1):
            print(f"\n{'='*80}")
            print(f"QUESTION {i}")
            print(f"{mcq.entity_type.title()}: {mcq.entity_title} ({mcq.entity_id})")
            print(f"Type: {mcq.question_type}")
            print(f"{'='*80}")
            print(f"\n{mcq.question}")
            print()
            
            options_labels = ['A', 'B', 'C', 'D']
            for j, option in enumerate(mcq.options):
                marker = "✓" if options_labels[j] == mcq.correct_answer else " "
                print(f"  {options_labels[j]}. {option} {marker}")
            
            print(f"\nCorrect Answer: {mcq.correct_answer}")
            print(f"Explanation: {mcq.explanation}")


# Example usage
def main():
    """Example usage of the ISACMCQGenerator with model specification"""
    API_KEY = os.getenv("")  # Better to use environment variable
    
    # You can now specify different models:
    # generator = ISACMCQGenerator(API_KEY, model="gpt-4")           # GPT-4 (default)
    # generator = ISACMCQGenerator(API_KEY, model="gpt-4-turbo")     # GPT-4 Turbo
    # generator = ISACMCQGenerator(API_KEY, model="gpt-3.5-turbo")   # GPT-3.5 Turbo
    # generator = ISACMCQGenerator(API_KEY, model="gpt-4o")          # GPT-4o
    
    # generator = ISACMCQGenerator(API_KEY, model="gpt-4-turbo")  # Example with GPT-4 Turbo
    generator = ISACMCQGenerator(API_KEY, model="gpt-4o")  # Example with GPT-4o
    
    # Generate MCQs from your JSON file
    json_file = "test.json"  # Replace with your JSON file path
    output_file = "questions_test.json"
    
    try:
        # Generate all MCQs
        mcqs = generator.generate_all_mcqs(json_file, output_file)
        
        # Print the results
        generator.print_mcqs(mcqs)
        
        # Print summary statistics
        question_types = {}
        entity_types = {}
        for mcq in mcqs:
            question_types[mcq.question_type] = question_types.get(mcq.question_type, 0) + 1
            entity_types[mcq.entity_type] = entity_types.get(mcq.entity_type, 0) + 1
        
        print(f"\n{'='*80}")
        print("SUMMARY")
        print(f"{'='*80}")
        print(f"Total questions generated: {len(mcqs)}")
        print(f"Model used: {generator.model}")
        print("\nBy Question Type:")
        for q_type, count in question_types.items():
            print(f"  {q_type}: {count}")
        print("\nBy Entity Type:")  
        for e_type, count in entity_types.items():
            print(f"  {e_type}: {count}")
            
    except FileNotFoundError:
        print(f"Error: Could not find the JSON file '{json_file}'")
        print("Please make sure the file path is correct.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()