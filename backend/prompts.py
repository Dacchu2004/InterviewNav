
def get_interview_questions_prompt(cv_text, job_role, company_name, level_prompt, job_description=None):
    jd_section = ""
    if job_description:
        jd_section = f"JOB DESCRIPTION:\n{job_description}\n\n"

    return (
        f"Based on the following CV/resume text"
        f"{' and Job Description' if job_description else ''}, "
        f"generate a list of 6 to 10 personalized interview questions "
        f"for a {job_role} position at {company_name}. "
        f"The questions should be tailored to the candidate's specific skills, experience, and background mentioned in their CV"
        f"{', while also aligning with the requirements in the Job Description' if job_description else ''}.\n\n"
        f"CV/RESUME TEXT:\n{cv_text}\n\n"
        f"{jd_section}"
        f"Generate interview questions that focus on the candidate's skills, experience, and industry knowledge.\n\n"
        f"{level_prompt}\n\n"
        "Format the questions as a numbered list, one question per line."
    )

def get_feedback_prompt(questions, responses):
    feedback_prompt = (
        "Based on the following interview questions and the candidate's responses, provide a detailed performance analysis in structured JSON format. "
        "Do NOT output any markdown formatting like ```json ... ```. Output raw JSON only.\n"
        "The JSON structure must be:\n"
        "{\n"
        "  \"overall_feedback\": \"A comprehensive, detailed markdown report. It MUST be long and structured. Include these sections with '###' headers: '### Communication Skills', '### Confidence', '### Areas for Improvement', and '### General Advice for Success'. For EACH section, provide at least 2-3 numbered points. Each point must have a bold title (e.g., '**1. Clarity:**') followed by an observation, and then a dedicated Improvement subsection (e.g. '\\n   **Improvement**: ...'). The content must be thorough and educational.\",\n"
        "  \"questions_analysis\": [\n"
        "    {\n"
        "      \"question\": \"Question text\",\n"
        "      \"candidate_answer\": \"Answer text\",\n"
        "      \"status\": \"Correct\" | \"Partial\" | \"Wrong\",\n"
        "      \"score\": 0.0 to 1.0 (float),\n"
        "      \"feedback\": \"Specific advice for this question\"\n"
        "    }\n"
        "  ]\n"
        "}\n\n"
    )
    
    for idx, (question, response) in enumerate(zip(questions, responses), 1):
        feedback_prompt += f"Question {idx}: {question}\nCandidate's Answer: {response}\n\n"
        
    return feedback_prompt
