import os

def parse_structure(input_structure):
    """
    Parse the input structure and return a dictionary of directories and files.
    """
    structure_dict = {}
    lines = input_structure.strip().split('\n')
    parent = ""

    for line in lines:
        if '├── ' in line or '└── ' in line:
            # It's a file or directory
            name = line.strip('├── ').strip('└── ')
            if not name.endswith('/'):
                # It's a file
                structure_dict[os.path.join(parent, name)] = 'file'
            else:
                # It's a directory
                structure_dict[name.rstrip('/')] = 'dir'
                parent = name.rstrip('/')
        elif '│   ' in line:
            # It's a subdirectory or file
            name = line.strip('│   ')
            if '└── ' in name or '├── ' in name:
                name = name.strip('├── ').strip('└── ')
                if not name.endswith('/'):
                    # It's a file
                    structure_dict[os.path.join(parent, name)] = 'file'
                else:
                    # It's a directory
                    structure_dict[os.path.join(parent, name.rstrip('/'))] = 'dir'
                    parent = os.path.join(parent, name.rstrip('/'))
        elif '│       ' in line:
            # It's a sub-subdirectory or file
            name = line.strip('│       ')
            if '└── ' in name or '├── ' in name:
                name = name.strip('├── ').strip('└── ')
                structure_dict[os.path.join(parent, name.rstrip('/') if name.endswith('/') else name)] = 'file' if not name.endswith('/') else 'dir'
                if name.endswith('/'):
                    parent = os.path.join(parent, name.rstrip('/'))

    return structure_dict

def create_files_and_directories(structure_dict):
    """
    Create directories and files from the parsed structure dictionary.
    """
    for path, type in structure_dict.items():
        if type == 'dir':
            os.makedirs(path, exist_ok=True)
        elif type == 'file':
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, 'w').close()

# User input for directory structure
input_structure = """
personal_assistant/
│
├── src/
│   ├── main.py                 
│   ├── gui/                    
│   │   ├── __init__.py
│   │   ├── main_window.py      
│   │   ├── chatgpt_ui.py       
│   │   └── gpt_model_ui.py    
│   │
│   ├── api/                   
│   │   ├── __init__.py
│   │   ├── openai_client.py   
│   │   └── api_utils.py       
│   │
│   ├── core/                  
│   │   ├── __init__.py
│   │   ├── user_session.py    
│   │   └── settings.py        
│   │
│   ├── utils/                 
│   │   ├── __init__.py
│   │   ├── logger.py          
│   │   └── error_handling.py  
│   │
│   └── models/                
│       ├── __init__.py
│       └── gpt_models.py      
│
├── tests/                     
│   ├── __init__.py
│   ├── test_gui.py
│   ├── test_api.py
│   └── test_core.py
│
├── docs/                      
│   └── README.md
│
├── configs/                   
│   └── config.ini             
│
├── resources/                 
│
├── .env                       
└── requirements.txt          
"""

structure_dict = parse_structure(input_structure)
create_files_and_directories(structure_dict)
print("The directory structure has been created.")

