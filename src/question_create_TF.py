import json
from openai import OpenAI
import re

# Prepare the full input string
def build_master_prompt(entries):
    prompt_intro = """# Cybersecurity Question Generator

                        You'll need to read the prompt and generate MAX 5 high-quality T/F questions
                        based on the provided Auto-ISAC procedure data that could test the knowledge of a person over the dataset.
                        The data provided represents only a subset of the complete Auto-ISAC database.
                        Auto-ISAC database present the most most common attacks in the automotive domain.

                        ## Data Structure
                        - **Procedures**: Real automotive attack scenarios
                        - **Techniques**: Specific attack methods within procedures (also with mitreId identifiers)
                        - **Scope**: You have only a subset of the complete database - focus solely on provided data

                        ## Question and options Requirements
                        The scenario in the question needs to be described carefully and with details. Add anything you think is relevant to precisely and univocally describe the scenario.

                        ### Content Focus:
                        - **Prompt Specific**: The text of the question, the options and the various explanations should be based ONLY on the text provided in the prompt (procedures descriptions and techniques)
                        - **Specific to details**: Both in the question and in the options ask for details cited in the techniques and procedures.
                        - **Clarity**: Ensure questions are clear, it can take multiple sentences to create a clear question
                        - Do not create trivial questions, create challenging T/F questions that test the exact knowledge in the dataset.

                        ### Quality Standards:
                        - Explicit all the acronyms in the question text and options
                        - In "source_procedures" field, include all procedures that were used to create the question
                        - Create 50/50 split between True and False questions
                        - False quesitons shohuld mismatch techniques and procedures in a way that is not trivial, but still based on the text provided in the prompt
                        

                        ### Avoid:
                        - Specific procedure names, research studies, or vehicle models
                        - Frequency/prevalence language ("commonly," "typically," "most likely")
                        - Direct copying of procedure names or techniques
                        - Using options that are too far from the correct answer
                        - Directly repeating verbs, nouns, or phrases from the question text in the options
                        - "What did researchers do" style questions
                        - Avoid directly asking for the procedure name or technique name, instead focus on the details and implications of the techniques and procedures

                        ## Output Format: onli gave me a list of questions in JSON format
                        - Provide MAX 5 T/F questions in the following format:
                        [
                            {
                                "question": "Question text",
                                "options": {
                                    "T": "True option text",
                                    "F": "False option text"
                                },
                                "correct_answer": "T/F",
                                "Explanation": {
                                    "T": "Explanation for why T is correct/incorrect",
                                    "F": "Explanation for why F is correct/incorrect",
                                },
                                "source_procedures": ["ATM-020202", ...]
                            }
                        ]

                        ---

                        **Dataset begins below:**
                    """
    

    prompt_data = json.dumps(entries, indent=2)
    prompt_end = "--- End dataset ---"

    return prompt_intro + prompt_data + "\n" + prompt_end

# Call GPT to generate questions
def generate_mcqs_from_all_data(entries):
    prompt = build_master_prompt(entries)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.9,
        # max_tokens=4000  # You can go higher if needed
    )

    content = response.choices[0].message.content

    # Remove triple backticks and optional language tags (like ```json)
    cleaned_content = re.sub(r"```(?:json)?\n?(.*?)```", r"\1", content, flags=re.DOTALL)

    return cleaned_content.strip()


# Run and save
if __name__ == "__main__":

    # Initialize the OpenAI client
    client = OpenAI(
        api_key=""
    )

    chunks = [
        "chunks/group_1.json",
        "chunks/group_2.json",
        "chunks/group_3.json",
        "chunks/group_4.json",
        "chunks/group_4_1.json",
        "chunks/group_5.json",
        "chunks/group_5_1.json",
        "chunks/group_6.json",
        "chunks/group_6_1.json",
        "chunks/group_7.json",
        "chunks/group_8.json",
        "chunks/group_9.json",
        "chunks/group_10.json",
        "chunks/group_11.json",
        "chunks/group_12.json",
        "chunks/group_13.json",
        "chunks/group_14.json",
    ]

    for chunk in chunks:
        with open(chunk, "r", encoding="utf-8") as f:
            entries = json.load(f)
            questions_output = generate_mcqs_from_all_data(entries)

            # Save the output to a file
            output_file = f"questions_tf/mcqs_{chunk.split('/')[-1]}"
            with open(output_file, "w", encoding="utf-8") as out_f:
                out_f.write(questions_output)

            print(f"✅ Multiple-choice questions generated and saved to {output_file}")