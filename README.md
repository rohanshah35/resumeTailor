# Resume Tailor

This tool automatically tailors your LaTeX resume to a specific job posting, using your provided resume as a template and optionally incorporating achievements from your own “achievement bank.”

---

## Setup

1. **Clone this repository or download the files.**

2. **Create a `.env` file** with your OpenAI API key and model name:

    ```
    OPENAI_API_KEY=your_openai_api_key_here
    OPENAI_MODEL=recommended to use gpt-4.1
    ```

3. **Prepare your input files:**

    - `job.txt` – The job posting (plain text)
    - `resume.tex` – Your base LaTeX resume
    - `achievements.txt` – (Optional) Your structured achievement bank

---

## How to Structure `achievements.txt`

The achievements file is **plain text**, divided into clear sections. Recommended sections:

- **Experience Bank**
- **Project Bank**
- **Technical Skills Bank**
- **Coursework Bank**
- **Add whatever extra you want**

## Usage

Run the script with:
python tailor.py --job job.txt --resume resume.tex --achievements achievements.txt --output tailored_resume.tex

## Output

You will recieve a .tex file with your new resume as well as a file describing the changes made in detail. Both can be found in the "generated" folder.