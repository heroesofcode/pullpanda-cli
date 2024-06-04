![image (1)-Photoroom](https://github.com/heroesofcode/pullpanda/assets/13969802/bc5b59e7-8345-4ab4-b40e-3f35a8d09721)

# Pull Panda

This tool automates the process of sending code diffs for review using the Gemini API. It helps developers streamline their code review process by generating detailed feedback and suggestions for improvement.

## Features

* **Calculate Git Diffs:** Automatically calculates the differences between the current branch and the main branch of a Git repository.

* **Send Diffs for Review:** Sends the calculated diffs to the Gemini API for a detailed code review.
  
* **Save Review Reports:** Saves the review feedback in a HTML file for easy reference and sharing.

## Prerequisites

* Python 3.x
* **gitpython** library
* **request** library
* Gemini API token

## Installation

1. Clone this repository to your local machine:

   ```bash
   https://github.com/heroesofcode/pullpanda-cli.git
   cd pullpanda-cli
   ```
   
2. Install the required Python packages: 

```bash
pip install gitpython requests
```

3. Set up your Gemini API token: 

* Open the script file in a text editor.

* Replace the GEMINI_AI_TOKEN variable with your actual Gemini API token:

```python
GEMINI_AI_TOKEN = "your_api_token_here"
```

## Usage

1. Run the script: 

```bash
python pullpanda.py
```

2. Enter the path to your local project repository when prompted.

3. The script will calculate the diff between the current branch and the main branch (assumed to be **develop** in this example). Modify the script if your main branch has a different name.

4. The diff will be sent to the Gemini API for review.

5. The review feedback will be saved as a HTML file in the **reports** directory within the script's directory.

## Example Output

Upon successful execution, you will see a message indicating where the review report has been saved:

```bash
The Markdown file has been saved at: /path/to/reports/pullpanda_report.html
```

## Customization

* **Main Branch:** If your main branch is not named develop, change the line in the get_diff function:

```python
main_branch = repo.heads['your_main_branch']
```

* **Review Prompt:** Customize the review prompt in the **send_diff_for_code_review** function if needed:

```python
"text": "Your custom prompt here: " + diff
```

## License

This project is licensed under the MIT License.
