import git
import requests
import os

GEMINI_AI_TOKEN = ""

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

    # Access the main branch
    main_branch = repo.heads['develop']  # Assuming 'develop' as the main branch, modify as needed

    # Calculate the diff between the two branches
    diff = repo.git.diff(main_branch.commit, current_branch.commit)

    # Send diff for code review to ChatGPT API
    send_diff_for_code_review(diff)

def send_diff_for_code_review(diff):
    """
    Send the diff for code review to ChatGPT API.

    Args:
        diff (str): The diff text to be reviewed.
    """
    # API endpoint for ChatGPT
    api_endpoint = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent?key={}".format(GEMINI_AI_TOKEN)

    # Prepare data for the API request
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": "Me de sugestoes de melhoria pra cada uma das diffs, com exemplo de codigo se for pertinente, como se fosse um code review bem completo: " + diff
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
            markdown_text = response_json['candidates'][0]['content']['parts'][0]['text']

            # Get the directory where the script is being executed
            script_directory = os.path.dirname(os.path.abspath(__file__))

            # Path to the folder where you want to save the file
            save_directory = os.path.join(script_directory, "reports")

            # Check if the save directory exists, if not, create it
            if not os.path.exists(save_directory):
                os.makedirs(save_directory)

            # Name of the file to be saved
            file_name = "code_reviewed.md"

            # Full path to the file to be saved
            file_path = os.path.join(save_directory, file_name)

            # Save the Markdown content to a file
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(markdown_text)

            # Print the path of the saved file for the user
            print("The Markdown file has been saved at:", file_path)
        else:
            print("Unable to find the 'text' parameter in the JSON response.")
    else:
        print("Failed to send code review request. Error:", response.text)

if __name__ == "__main__":

    print(
        """""



                                                           ⣠⣾⣿⣿⣿⣿⣿⣿⣆             ⢠⣾⣿⣿⣿⣿⣿⣷⣦⡀
                                                         ⣰⣿⣿⣿⣿⣿⣿⣿⣿⡿⠟⠛⠉⠉⠉⠉⠉⠉⠉⠉⠉⠈⠙⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⣷
                                                        ⣿⣿⣿⣿⣿⣿⣿⠟⠁                 ⠈⠙⢿⣿⣿⣿⣿⣿⣿⡇
                                                        ⢻⣿⣿⣿⣿⡟⠁                      ⠙⣿⣿⣿⣿⣿⠁
                                                        ⠈⠻⢿⣿⠟     ⣀⣤⣤⣤⡀     ⢀⣤⣤⣤⣄⡀    ⠘⣿⡿⠿⠃
                                                          ⢠⡟    ⣠⣾⣿⣿⣟⣿⡇     ⢸⣿⣿⣻⣿⣿⣦    ⠸⣧
                                                          ⣼⠁    ⣿⣿⣿⣿⣿⡟  ⢀⢀⢀  ⢽⣿⣿⣿⣿⣿⡇  ⣀⣤⣿⣷⣴⣶⣦⣀⡀
                                                        ⢀⣠⣤⣤⣠⣇  ⣿⣿⣿⣿⣿   ⢀⢀⢀  ⢹⣿⣿⣿⣿⡇ ⣿⣿⣿⡏⢹⣿⠉⣿⣿⣿⣷
                                                    ⢠⣾⣿⣿⣿⣿⣿⣿⣿⣶⣄ ⠹⣿⣿⠿⠋         ⠈⠻⣿⣿⠟ ⢸⣿⣇⣽⣿⠿⠿⠿⣿⣅⣽⣿⡇
                                                    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣆                     ⠈⣿⣿⣟⠁   ⠈⣿⣿⣿⡇ 
                                                ⠛⠛⠛⠛⠛⠛⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛⠛
                                                    ⠘⠛⠻⢿⣿⣿⣿⣿⣿⠟⠛⠁                                       


                            :::::::::  :::    ::: :::        :::             :::::::::     :::     ::::    ::: :::::::::      :::     
                            :+:    :+: :+:    :+: :+:        :+:             :+:    :+:  :+: :+:   :+:+:   :+: :+:    :+:   :+: :+:   
                            +:+    +:+ +:+    +:+ +:+        +:+             +:+    +:+ +:+   +:+  :+:+:+  +:+ +:+    +:+  +:+   +:+  
                            +#++:++#+  +#+    +:+ +#+        +#+             +#++:++#+ +#++:++#++: +#+ +:+ +#+ +#+    +:+ +#++:++#++: 
                            +#+        +#+    +#+ +#+        +#+             +#+       +#+     +#+ +#+  +#+#+# +#+    +#+ +#+     +#+ 
                            #+#        #+#    #+# #+#        #+#             #+#       #+#     #+# #+#   #+#+# #+#    #+# #+#     #+# 
                            ###         ########  ########## ##########      ###       ###     ### ###    #### #########  ###     ### 

                                                                                                                  ~ by Heroes of Code



                                                                                                                  
    """
    )

    # Request the repository path from the user
    repo_path = input("Please enter the path to your Git repository: ")

    # Calculate and get the diff between the target and current branches
    get_diff(repo_path)
