from extractData.callAI import askAI
import json
from extractData.llm import hardSkillsModel
from pydantic import BaseModel

class Response(BaseModel):
    skills: list[str]

def getMatchedSkillsFromList(jobSkills: list[str], userSkills: list[str]) -> list[str]:
    # """Examples:
    #         - React → Frontend Development
    #         - HTML/CSS → Web Development
    #         - FastAPI → API Development
    #         - PostgreSQL → SQL Databases"""
    prompt = f"""You are a skill-matching system.
    Your task is to identify which skills from userSkills directly or indirectly satisfy the requirements in jobSkills.
    Rules:
    - The "skills" array must contain ONLY skills that appear in userSkills.
    - A direct match occurs when a user skill represents the same technology, tool, programming language, or concept as a job skill.
    - A related match is allowed when a specific user skill reasonably implies or covers a more general job skill.
    - Do NOT infer a specific technology from a general skill.
    - Do NOT add skills that are not present in userSkills.
    jobSkills:
    {jobSkills}
    userSkills:
    {userSkills}"""
    # prompt = promptTemplate.format(jobSkills=jobSkills, userSkills=userSkills)
    # result = json.loads(askAI("fast", prompt))["skills"]
    structuredModel = hardSkillsModel.with_structured_output(Response)
    result = structuredModel.invoke(prompt)
    # print("Skills: ", result.skills)
    return result.skills

def getMatchedSkills(jobDescription: str, userSkills: list[str]) -> list[str]:
    # """Examples:
    #         - React → Frontend Development
    #         - HTML/CSS → Web Development
    #         - FastAPI → API Development
    #         - PostgreSQL → SQL Databases"""
    prompt = f"""You are a skill-matching system.
    Your task is to identify which skills from userSkills directly or indirectly satisfy the requirements in the jobDescription.
    Rules:
    - The "skills" array must contain ONLY skills that appear in userSkills.
    - A match occurs when a user skill represents the same technology, tool, programming language, or concept mentioned in jobDescription.
    - Do NOT add skills that are not present in userSkills.
    jobDescription:
    {jobDescription}
    userSkills:
    {userSkills}"""
    # prompt = promptTemplate.format(jobSkills=jobSkills, userSkills=userSkills)
    # result = json.loads(askAI("fast", prompt))["skills"]
    structuredModel = hardSkillsModel.with_structured_output(Response)
    result = structuredModel.invoke(prompt)
    # print("Skills: ", result.skills)
    return result.skills

if __name__ == "__main__":
    import time
    start = time.perf_counter()
    jobSkills = [
        "Web Development",
        "API Integration",
        "SQL Databases",
        "Git",
        "AWS"
    ]
    userSkills = [
        "Python",
        "React",
        "FastAPI",
        "PostgreSQL",
        "GitHub",
        "Docker",
        "OpenCV"
    ]
    # print(getMatchedSkills(jobSkills, userSkills))
    print(getMatchedSkills("""AI-Native Software Engineer - Early Career
Location: Remote — global applications welcome; please apply via the region closest to you
Company: ChainGPT
Type: Full-Time

About ChainGPT
ChainGPT is a fast-moving Web3 and AI company building products at the intersection of blockchain infrastructure, token ecosystems, and intelligent automation. We value speed, ownership, clarity, and high standards. Our team is made up of self-driven operators who move fast, think independently, and use cutting-edge tools to create real commercial impact.

We foster a transparent, collaborative, and high-performance culture where strong ideas win, autonomy is expected, and execution matters.

We’re building Brain by AIVM, a platform that makes enterprise AI verifiable, governed, and genuinely trustworthy.

We’re a small, fast-moving team working at the frontier of AI, governance, and enterprise trust. At this stage, a sharp AI-native marketer can have an outsized impact on how the world sees us.

About the Role
We’re looking for an exceptional early-career engineer who has grown up building with AI.

You may be fresh out of university, still studying, or entirely self-taught. What matters most is raw ability, curiosity, strong technical instincts, and a genuine obsession with modern AI tooling.

This is a high-growth role for someone who wants to learn how a company is built from the inside while contributing to real product work from day one. You’ll work closely with the founders and senior engineers, build real features and prototypes, and learn how to use AI agents to move faster than traditional teams.

What You’ll Do
Build real features, prototypes, and demos using tools like Codex, Claude Code, and modern AI coding agents.
Turn ideas into working demos quickly, then help make them more reliable, scalable, and production-ready.
Learn how to direct, evaluate, and control AI coding agents to multiply engineering output.
Work closely with founders and senior engineers across product, engineering, and strategy.
Explore new AI development workflows and help the team move faster.
Contribute to a fast-moving product where experimentation, speed, and quality all matter.

Requirements

What We’re Looking For
You build with AI tools regularly and can show us what you’ve made.
You have examples of projects, repos, demos, prototypes, or technical experiments.
You’re excited about tools like Codex, Claude Code, Cursor, AI agents, and agentic development workflows.
You learn by building and ship constantly.
You have strong technical curiosity and are willing to figure things out independently.
You care more about output and learning speed than titles or credentials.
You’re comfortable working in a fast-moving environment with real responsibility.
Bonus Points
You’ve created content, demos, or tutorials around AI or software development.
You’ve tried to start something of your own.
You have a side project you’re deeply interested in.
You’ve experimented with AI agents, coding workflows, automations, or developer tools.
You’re interested in AI infrastructure, enterprise AI, governance, or agentic systems.
Why Join Us
Front-row seat: Learn how a company is built directly from founders and senior engineers.
Real responsibility: You’ll work on meaningful projects, not just small tasks.
Strong mentorship: You’ll be supported while being pushed to grow quickly.
Frontier work: Build in one of the most exciting categories in tech right now.
Output-first culture: We care about what you can build, learn, and ship.

Benefits

What We Offer

Work alongside the ChainGPT core team on high-impact AI and Web3 products across our ecosystem.
Remote-first setup with flexible hours, focused on outcomes, trust, and ownership.
Competitive compensation, with performance-based upside where applicable to the role.
Fast-moving environment with direct collaboration across all team members, including senior management, and clear accountability with no micromanagement.
The support to do your best work, including the tools you need, structured onboarding, and clear room to grow.
Company Culture and Values

At ChainGPT, we value Trust, Effective Speed, Innovation, and Growth. As our AI-Native Software Engineer - Early Career, you will embody these core values and have the opportunity to contribute to our culture and help drive our success. Join us on this exciting journey as we shape the future of blockchain and crypto technology.

Additional Information:

Employment Compliance and Confidentiality:
All employees will be onboarded through our official payroll and HR provider, which manages employment documentation, tax withholdings, and compliance with legal requirements based on the employee’s country of residence. As part of the onboarding process, each new hire is required to complete a Know Your Customer (KYC) verification, sign a Non-Disclosure Agreement (NDA), execute an employment contract, and fulfill any additional legal requirements specific to your jurisdiction. This process ensures compliance, protects company information, and establishes a secure and professional employment relationship.
Employment Structure:
The position is offered on either an employee or contractor basis, depending on the location and role. Individuals will receive payment via direct deposit on a monthly basis. Additional details regarding compensation, benefits, and company policies will be provided during onboarding and outlined in the official employment agreement.
Compensation:
Salaries are paid in fiat currency via direct deposit on a monthly schedule, with payments issued on the first business day of each month. This structure ensures timely and transparent compensation aligned with local financial systems.
Probationary Period:
All new employees will undergo a 90-day probationary period, which serves as a mutual evaluation phase. During this time, both the employee and ChainGPT can assess fit, performance, and long-term alignment with the role and company.""", userSkills))
    end = time.perf_counter()
    print(f"La tarea tomó {end-start:.2f}s")
    