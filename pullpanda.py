import git
import requests
import os
import json
import time
import webbrowser
from collections import deque

CONFIG_FILE = "config.txt"

YELLOW = '\033[33m'
RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'

def get_diff(repo_path):
    """
    Calculate and print the differences (diff) between the current branch and the main branch of a Git repository.

    Args:
        repo_path (str): The file path to the Git repository.
    """
    # Open the Git repository
    repo = git.Repo(repo_path)

    # Access the current branch
    current_branch = repo.active_branch

    # Access the remote repository (origin)
    origin = repo.remotes.origin

    # Update the references from the remote repository
    origin.fetch()

    # Access the main branch
    main_branch = repo.refs[target_branch]  # Assuming 'develop' as the main branch, modify as needed

    # Calculate the diff between the two branches
    diff = repo.git.diff(main_branch.commit, current_branch.commit)

    # Split the diff into chunks of maximum 4 files
    diff_chunks = [diff_chunk.strip() for diff_chunk in diff.split('diff --git')[1:]]

    # Queue for API calls
    api_call_queue = deque()

    # Iterate through diff chunks
    for chunk in diff_chunks:
        # Send diff for code review to Gemini API
        api_call_queue.append(chunk)

    # Process API calls from the queue
    process_api_calls(api_call_queue)


def process_api_calls(api_call_queue):
    """
    Process API calls from the queue.

    Args:
        api_call_queue (deque): A deque containing diff chunks.
    """
    # Markdown text variable
    markdown_text = ""

    # API endpoint for ChatGPT
    api_endpoint = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={}".format(token)

    # Iterate through the API call queue
    while api_call_queue:
        # Pop the diff chunk from the queue
        diff_chunk = api_call_queue.popleft()

        first_line = diff_chunk.split('\n')[0]

        file_path = first_line.split(' ')[0][2:]

        print(f"\n{BLUE}Reviewing: {RESET}{file_path}")

        # Prepare data for the API request
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": """Give me suggestions for improvements to the code focusing only on the lines that were added to the code and give me exemple of suggestion code if is pertinent:

                            Follow this pattern to create the suggestion: 

                            File: 

                            Suggestion: 

                            Code example:
                            """ + diff_chunk
                        }
                    ]
                }
            ]
        }

        # Send POST request to ChatGPT API
        response = requests.post(api_endpoint, json=data)

        if response.status_code == 200:
            # Convert the JSON response to a Python dictionary
            response_json = response.json()

            # Check if 'text' is present in the response dictionary
            if 'text' in response_json['candidates'][0]['content']['parts'][0]:
                # Get the Markdown text from the response
                markdown_chunk = response_json['candidates'][0]['content']['parts'][0]['text']

                # Replace backticks (`) with escape characters (\`)
                markdown_chunk = markdown_chunk.replace("$", "\\$")

                # Append the Markdown text to the markdown variable
                markdown_text += markdown_chunk + "\n\n"

            else:
                print(f"{RED}Unable to find the 'text' parameter in the JSON response.")
        else:
            print(f"{RED}Failed to send code review request.")

        # Wait for 10 seconds before the next API call
        time.sleep(10)

    # Generate HTML content
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Pull Panda</title>
  <script src="https://cdn.jsdelivr.net/npm/marked/marked.min.js"></script>
  <style>
    body {{
      font-family: Arial, sans-serif;
      line-height: 1.6;
      margin: 20px;
    }}
    pre {{
      background-color: #f4f4f4;
      padding: 10px;
      border: 1px solid #ddd;
      overflow-x: auto;
    }}
    code {{
      font-family: 'Courier New', Courier, monospace;
      background-color: #f4f4f4;
      padding: 2px 4px;
      border-radius: 4px;
    }}
    #logo {{
      display: block;
      margin: 0 auto;
      width: 200px;
    }}
  </style>
</head>
<body>
  <img id="logo" src="../resources/pullpanda-logo.png" alt="Logo">
  <div id="content">{markdown_text}</div>

  <script>
    document.addEventListener("DOMContentLoaded", function() {{
      const content = document.getElementById('content');
      content.innerHTML = marked.parse(content.innerHTML);
    }});
  </script>
</body>
</html>"""

    # Get the directory where the script is being executed
    script_directory = os.path.dirname(os.path.abspath(__file__))

    # Path to the folder where you want to save the file
    save_directory = os.path.join(script_directory, "reports")

    # Check if the save directory exists, if not, create it
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Name of the file to be saved
    file_name = "pullpanda_report.html"

    # Full path to the file to be saved
    file_path = os.path.join(save_directory, file_name)

    # Save the HTML content to a file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_content)

    # Print the path of the saved file for the user
    print("\n{}The report file has been saved at: file://{}".format(GREEN, file_path))

    webbrowser.open('file://' + os.path.realpath(file_path))


if __name__ == "__main__":

    print(
        """""

                                                                                                                    
                                                                                                    
                                                                                                    
                            ..-****=.                                                               
                          .:##=....-#%-.        .:                                                  
                         .**.        .##- ....#@@%*--===+++==-::-#%%#=.                             
                        .==.          .*#*%@@@@@@@@@@@@@@@@@%#-@*.. ..=-.                           
         :=#%%%%%%%%%%%%=%:            -@@@@@@@@@@@@@@%#***+:.+*.      .=%%%%%%%*-.                 
        +@@%***@=#=@@@@@+#:            -@@@@@@@@@@@@@@#*****=:%*..      .@@@@@@@@@%-                
       -%@@#+*#@+*=@@@@@%-=.       ...=@@@@@@@@@@@@@@@@#*+=:+@@@@+..   ..@@@@@@@@@@+                
       -%@@@@@@@@@@@@@@@@#++.     .*@@@@@@@@@@@%-+%@@@@@@@%%@@@@@@@-.  .#@@@@@@@@@@+                
       =%-:..::::::::.......=:. .=@@@@@@@@@@@@@@@#*%@@@@@@@@@@@@#%@@=. .::::::::::++                
       +%-:%+%@@@@@@@-::::.:@*==%@@@@@@@@@@@%##%%@@@@@@@@@@@@@@@+=@@@=:.##*@%:::::++                
       #@-:#%+:-%%=:%%%+.:.@%**@@@@@@@@@-:...   ..:+@@@@@@@@@@@@@@@@@%.%%:::%%+:::++                
       %@-::++++++++-=++-.=@**%@@@@@@@-.            .#@@@@@@@@*....=@@:=++++++++=:+*                
       %@-:::::::------:..=**#@@@@@@@:.       ...    .@@@@@@#.     .=@*:::::::::::+#                
       %@-::::-::::-::::.*@@@@@@@@@@:.     .=%@@@%:. .%@@@@%.....   :@#:-::---:.::+%                
       %@-::::::==::=-:.=@@@@@@@@@@*.     .#@@@@@@@=  %@@@%.-@@@+.  :@#:-:-----.-:+%                
       %@-:::::::-***+::.%#@@@@@@@@=......-@@@#:::*=.:@@@@=:%@@@*.  :@%-:+*****.=:+%                
       %@-:#-:::=%%%.%%%:.*#%@@@@@@=...:--:@@@=.  ...*@@@@-:.:%@+.. :@@=#%#:-%%-+:+@                
       %@-::::-%@@%:+%::..*%**@@@@@+...::==:#@@*-+.-@@@@@@%::*@%:...:@@+:@@@+*@@*:+@                
       %@-:##########.:#=.:@#*#@@@@@-....:---:...*@@@@@#---#++-=-:..:@@+*##-:::.+:+@                
       %@-::-=++=-:::..:-*#:%#*#@@@@@#:........=@@@@@. :*###=%::...:@@@+-===-::.=:+@                
       %@-:::........:%@%:..-@%**@@@@@@@@@%@@@@@@@@@@%:    .+@=...=@@@@::::::::.=:+@                
       %@-:::......=@@*:.   ..*@#*#@@@@@@@@@@@@@@@@@@@@%:+*@@@@@@@@@@@-+********=:+@                
       %@-::....=@@@%#%#-.    ..%%**#@@@@@@@@@@@@@@@@@@*-@@@@@@@@@@@@=..........-:+@                
       %@-.%=.%@@=:.. ..-#-.    ..%@**#%@@@@@@@@@@@@@@@@@@@@@@@@@%%*:.::::::::::::+@                
       %@-..*@%=..       .:*:.    ..=#%%%%@@@@@@@@@@@@@@@@@@@@%%%*.-=....:*@%+:.-:+@                
       #@-:@@+:.           .=.        ..#@@@@@@@@@@@@@@@%%%#%@+..   .%.#:-*%+%+.=:+@                
       =#:%%-..         .-. .-:.         ...--+#@@@@@@@#=--...       .**.:+@@=:.+:+@                
       ::%#:.            .=- .-.                 .   .          ....  .+@:=%%%%:*:+@                
       .*#:.               :+.-:       ..   .   .. .    .       ..=.   .-%:%@@%.*:+%                
       -#:.                 :#.+.    -@@@@*.#@..@%:@*. =@..    .:+.     .=%:-++.=:+%                
       +=.               :::..*#.    =@*.=@=#@..@%:@#. =@..    .*:.      .=%:.::=:+%                
      :#:.                ..===%.    =@@@@=:%@..@%:@#..=@..    .*.....    .*+.-*#:++                
      =+.                    .*@.    -@*.. .=@@@%::%@%*-###+....-.-....:-=++*.:...--      .         
      #=:..-*#%@@@@@@@%#+:.:...#..  .=##*..:%:..**.*#-@@+:#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*.       
     .#%*+==-:.........::-=+%%*+-.  .%@-%@+@@@-.@@%#@=@=:@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@%-       
      .*.          .:*#####%%%++-.  .%@@@#%@#@#.@%@@@=@-#*@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#        
      .*.          ...      ...-%*...%@..*@+-%@:@#-@%+@+#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@-        
       #.                       .:*#+-...... ..... ....=%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@*.        
       *-                      ....:=*%@@@@%+:..      .#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@=         
       -+.                      ............:-*@+.   .:@@@@@@@@@@@@@@@@@-..:@@@@@@@@@@@@@%+         
       :#-.                                    .-%*. .@%@@@@@@@@@@@@@@@*. .-@@@@@@@@@@@@@#          
       .-%:                                   .. .-%.=%@@@@@@@@@@@@@@@@@%#@@@@@@@@@@@@@@@*          
       :-=#:.                                 .-*:.**+%%%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#           
       -*:+%:.                           ..:..  -#.::%%%%%%%%%%@@@@@@@@@@@@@@@@@@@%%%%%%+           
       -#:.:#+..                           .-#. .=..-%#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#            
       -*:. .:+-.                  .:-+##%#*****###-@#######%%%%%%%%%%%%%%%%%%%%%%%%%##*            
      %++++*##%%%%%%%%%%%%%%%%%%%%%%-*#%%%*+=*%#+-=+##################################%:-           
      %%@@@@@@@@@@@@@@@@@@@@@@@@@@@%#*+=---:-+*=#=*************#######%%###*+++==----..--=          
                                        %*#+--. ::=:-*+===-:.............    ...                    
                                                                                                    
                                                                       ~ by Heroes of Code
    """
    )

    def get_config_value(prompt, key):
      config = {}

      # Check if the config file exists and read it
      if os.path.exists(CONFIG_FILE):
          with open(CONFIG_FILE, "r") as file:
              for line in file:
                  k, v = line.strip().split('=', 1)
                  config[k] = v

      # Get the saved value if it exists
      saved_value = config.get(key, '')

      # Ask the user for the value, using the saved value as default
      if saved_value:
          user_input = input(f"{YELLOW}{prompt} (Press Enter to accept the saved value '{saved_value}' or type a new one): ").strip()
          if user_input:
              config[key] = user_input
          else:
              config[key] = saved_value
      else:
          config[key] = input(f"{YELLOW}{prompt}: ").strip()

      # Save the new value (if it was changed or entered for the first time)
      with open(CONFIG_FILE, "w") as file:
          for k, v in config.items():
              file.write(f"{k}={v}\n")

      return config[key]

    def get_repo_path():
        return get_config_value("\nEnter the path to your local repository", 'repo_path')

    def get_token():
        return get_config_value("\nEnter the Gemini Api Token", 'token')
    
    def get_target_branch_name(): 
        return get_config_value("\nEnter the target branch name", 'target_branch')
    
    try: 
      # Request the repository path from the user
      repo_path = get_repo_path()
      target_branch = get_target_branch_name()
      token = get_token()

      # Calculate and get the diff between the target and current branches
      get_diff(repo_path)
    except KeyboardInterrupt:
      print("\nExiting from script...")
