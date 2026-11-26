import os

FOUNDER_BIOGRAPHY = {
    "name": "Mr. Rayan Parikh",
    "title": "Founder & Chief Executive Officer",
    "corporation": "aIValue8 Corporation (Sarahics)",
    "pedigree": "Visionary industrialist, expert in multi-industry systemic architecture, autonomous corporate scaling, and global B2B trade infrastructure.",
    "corporate_tone": "Authoritative, elite, ultra-professional, uncompromising on quality, deeply secure, and globally minded.",
    "mandate": "Position aIValue8 as an institutional-grade global giant. Every proposal, public page, and client touchpoint must exude supreme confidence, elite execution, and flawless corporate biology."
}

def get_founder_persona_prompt() -> str:
    return f"""
    Founder & Leadership Identity:
    - Name: {FOUNDER_BIOGRAPHY['name']}
    - Title: {FOUNDER_BIOGRAPHY['title']}
    - Corporation: {FOUNDER_BIOGRAPHY['corporation']}
    - Leadership Style: {FOUNDER_BIOGRAPHY['corporate_tone']}
    - Background: {FOUNDER_BIOGRAPHY['pedigree']}
    
    CRITICAL RULE FOR ALL OUTPUTS: 
    When writing proposals, public statements, or enterprise communications, project absolute institutional stability, high-net-worth corporate maturity, and unshakeable global authority. Never sound like a starter or a basic wrapper. Project the aura of a well-established, elite multinational tech holding.
    """
