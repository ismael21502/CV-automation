import json 
from callAI import callAI

def selectSoftSkills(jobSoftSkills, softSkills):
    prompt = f"""
        You are an HR and recruiting expert.

        Given a list of job soft skills and a list of candidate soft skills, select the candidate soft skills that best match the job requirements.

        Consider semantic similarity, not only exact matches.
        For example:
        - Initiative is similar to Proactivity.
        - Analytical Thinking is similar to Problem Solving.
        - Self-directed Work is similar to Autonomy.

        Rules:
        - Select at most 3-4 candidate soft skills.
        - Prefer the strongest matches.
        - Do not invent new skills.
        - Return ONLY a JSON array of strings.

        Job soft skills:
        {jobSoftSkills}

        Candidate soft skills:
        {softSkills}
        """
    return callAI(prompt)

