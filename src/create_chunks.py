import json

# Load procedures.json (full list of entries)
with open("procedures.json", "r", encoding="utf-8") as f:
    all_procedures = json.load(f)

# Define group titles based on balanced content-based chunks (~15 weight each)
group_titles = {
    "group_1": [  # Tesla Core Security Research (Weight: 16)
        'Free-fall: Hacking Tesla from wireless to CAN bus'
    ],
    "group_2": [  # Tesla Model-Specific Attacks (Weight: 14)
        'Hacking a Tesla Model S: What we found and what we learned',
        'NFC Relay Attack on Tesla Model Y',
        'Unlocking the Drive: Exploiting Tesla Model 3'
    ],
    "group_3": [  # Tesla Wireless & Advanced Exploits (Weight: 15)
        'OVER-THE-AIR: HOW WE REMOTELY COMPROMISED THE GATEWAY, BCM, AND AUTOPILOT ECUS OF TESLA CARS',
        'Exploiting Wi-Fi Stack on Tesla Model S',
        "New Example: Jailbreaking an Electric Vehicle in 2023 or What It Means to Hotwire Tesla's x86-Based Seat Heater"
    ],
    "group_4": [  # CAN Bus & Message Injection (Weight: 17 - split as needed)
        'CAN Message Injection'
    ],
    "group_5": [  # Comprehensive Attack Surface Analysis (Weight: 16 - split as needed)
        'Comprehensive Experimental Analyses of Automotive Attack Surfaces'
    ],
    "group_6": [  # Network & Control Unit Analysis (Weight: 15 - subset)
        'Adventures in Automotive Networks and Control Units'
    ],
    "group_7": [  # BMW Security Assessment (Weight: 15)
        'Experimental Security Assessment of BMW Cars: A Summary Report'
    ],
    "group_8": [  # Remote Exploitation Techniques (Weight: 14)
        'Remote Exploitation of an Unaltered Passenger Vehicle'
    ],
    "group_9": [  # Modern Automobile Analysis (Weight: 15)
        'Experimental Security Analysis of a Modern Automobile',
        'Experimental Security Analysis of a Modern Automobile '
    ],
    "group_10": [  # Lexus & Multi-Brand Research (Weight: 14)
        'Tencent Keen Security Lab: Experimental Security Assessment on Lexus Cars',
        'Drift with Devil: Security of Multi-Sensor Fusion based Localization in High-Level Autonomous Driving under GPS Spoofing'
    ],
    "group_11": [  # IoT & Firmware Security (Weight: 14)
        'IoT backdoors in cars',
        'There Will Be Glitches Extracting and Analyzing Automotive Firmware Efficiently'
    ],
    "group_12": [  # Wireless & PHY Layer Attacks (Weight: 13)
        'Evaluating Physical-Layer BLE Location Tracking Attacks on Mobile Devices',
        'Losing the Car Keys: Wireless PHY-Layer Insecurity in EV Charging'
    ],
    "group_13": [  # Specialized Attack Research Part 1 (Weight: 13)
        'Security and Privacy Vulnerabilities of In-Car Wireless Networks: A Tire Pressure Monitoring System Case Study',
        'Drive it like you hacked it',
        'Driving Down the Rabbit Hole'
    ],
    "group_14": [  # Specialized Attack Research Part 2 (Weight: 2)
        'Extracting SecOC secrets from an ECU'
    ]
}

# Initialize empty lists for each group
grouped_procedures = {group: [] for group in group_titles}

# Helper to find group for a given title
def get_group_for_title(title):
    for group, titles in group_titles.items():
        if title.strip() in titles:
            return group
    return None

# Sort procedures into the appropriate groups
for proc in all_procedures:
    group = get_group_for_title(proc['title'])
    if group:
        grouped_procedures[group].append(proc)

# Write each group to its own file
for group, procedures in grouped_procedures.items():
    with open(f"{group}.json", "w") as f:
        json.dump(procedures, f, indent=4)

print("✅ All groups have been successfully saved into separate JSON files.")
print(f"Created {len(group_titles)} group files:")
for group in group_titles:
    print(f"  - {group}.json")