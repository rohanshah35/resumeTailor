import os
import openai
import argparse
from dotenv import load_dotenv

def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def ensure_generated_folder():
    generated_dir = "generated"
    os.makedirs(generated_dir, exist_ok=True)
    return generated_dir

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Customize your LaTeX resume using GPT-4o/4.1 and a job posting.")
    parser.add_argument("--job", required=True, help="Path to job posting file (txt or pdf)")
    parser.add_argument("--resume", required=True, help="Path to your base LaTeX resume (.tex)")
    parser.add_argument("--achievements", required=False, help="Path to your achievement bank file (txt, optional)")
    parser.add_argument("--output", required=False, default="tailored_resume.tex", help="Filename for output tailored LaTeX resume")
    parser.add_argument("--changes_output", required=False, default="changes_and_reasoning.md", help="Filename for output changes/reasoning markdown")
    args = parser.parse_args()

    generated_dir = ensure_generated_folder()
    output_path = os.path.join(generated_dir, os.path.basename(args.output))
    changes_output_path = os.path.join(generated_dir, os.path.basename(args.changes_output))

    openai.api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL")

    job_posting = read_file(args.job)
    resume_template = read_file(args.resume)
    achievements = read_file(args.achievements) if args.achievements else None

    system_prompt = (
        "You are a meticulous and ethical resume editor with expert LaTeX skills. "
        "You are provided with: (1) a job posting, (2) a base LaTeX resume (which serves as a template), "
        "and (optionally) (3) an 'achievement bank'—a collection of additional, real, user-verified experiences or accolades. "
        "Your task is to create a tailored resume for this specific job. "
        "\n\n"
        "Strictly follow these instructions:\n"
        "1. Never invent or fabricate skills or achievements. Use content found in the base resume or the achievement bank. "
        "2. If the achievement bank is provided, you may add, reword, or substitute items from it to better match the job description, but you must not change their meaning. "
        "3. If the achievement bank is not provided, do NOT invent new accomplishments. "
        "4. Use emphasis to your advantage, scan the resume and the bank to emphasize certain technologies and/or points based on what the job posting values. This does NOT mean bolding random key words."
        "5. If information in the base resume does NOT match or pertain to the job posting, consider de-emphasizing or removing it, unless it is necessary for resume completeness or context. "
        "6. Do NOT drastically change the structure, section order, or formatting of the resume. Make only minimal, targeted edits where needed to highlight relevance to the job posting. Preserve the original look, flow, and personal details of the base resume unless the job posting explicitly requests changes. "
        "7. Maintain a professional, clean LaTeX format. Do NOT include any explanation, markdown, or chatty language—ONLY the LaTeX code for the tailored resume. "
        "8. Make the edits as succinct and targeted as possible, focusing only on what is genuinely relevant to the job. Aim to replace the data first, rather than rewording or rephrasing existing entries. Although you are encouraged the wording if greater emphasis, clarity, or grammatical correction is needed in reflection of the job posting. "
        "9. Never change formatting, contact info, or personal details. "
        "10. IMPORTANT: The resume must stay one page long or under. Keep resume output to under 4000 characters (NOT INCLUDING LATEX CODE ONLY OUTPUT TEXT)"
        "\n\n"
        "AFTER making the edits, output a section describing what you changed and why, referencing specific resume sections where useful. This section must be formatted in valid, clear Markdown. "
        "For each section you changed (such as Experience, Skills, Education, etc.), use a second-level heading: '## Section Name'. "
        "For each subsection (such as a particular job or degree), use a third-level heading with two spaces indentation: '  ### Subsection Name'. "
        "Under each subsection heading, use a bulleted list with four spaces indentation for each bullet. Each bullet must be: '- [what changed] (Reason: [why])'. "
        "If a section does not have subsections, place the bulleted list directly under the section heading. "
        "New lines should be between every second-level heading. "
        "Do not include any extra section titles or commentary—output ONLY the Markdown list described above. "
        "Be very specific in what you changed. If you didn't change anything in a section, detail that and why you thought it was sufficient. "
        "After the last bullet, output a line containing only three hyphens ('---'). "
        "After the '---', output ONLY the final tailored LaTeX resume code, with no other text or explanation."
    )

    user_prompt = (
        f"JOB POSTING:\n{job_posting}\n\n"
        f"BASE RESUME (LaTeX):\n{resume_template}\n\n"
    )
    if achievements:
        user_prompt += f"ACHIEVEMENT BANK:\n{achievements}\n\n"

    print("Processing... This may take a moment.")
    response = openai.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.3
    )

    output = response.choices[0].message.content
    if "---" in output:
        changes, latex_resume = output.split("---", 1)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(latex_resume.strip())
        with open(changes_output_path, "w", encoding="utf-8") as f:
            f.write(changes.strip())
        print(f"Tailored resume saved to {output_path}")
        print(f"Changes and reasoning saved to {changes_output_path}")
    else:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(output)
        with open(changes_output_path, "w", encoding="utf-8") as f:
            f.write("Could not extract changes and reasoning section.\n\n" + output)
        print(f"Output saved to {output_path}")
        print(f"Changes and reasoning saved to {changes_output_path}")

    print("Done.")

if __name__ == "__main__":
    main()
