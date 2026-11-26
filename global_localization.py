import os
from sentinel import smart_generate, PRIMARY_MODEL

CURRENCY_MAP = {
    "IN": {"code": "INR", "symbol": "₹", "multiplier": 1.0},
    "US": {"code": "USD", "symbol": "$", "multiplier": 0.012},
    "GB": {"code": "GBP", "symbol": "£", "multiplier": 0.0095},
    "EU": {"code": "EUR", "symbol": "€", "multiplier": 0.011},
    "AE": {"code": "AED", "symbol": "AED ", "multiplier": 0.044},
}

LANGUAGE_MAP = {
    "IN": {"lang": "Professional English Only", "welcome": "Build, Automate & Scale Your Business with AI"},
    "AE": {"lang": "Arabic", "welcome": "قم بناء وت स्वتمة وتوسيع نطاق عملك باستخدام الذكاء الاصطناعي"},
    "EU": {"lang": "French", "welcome": "Construisez, automatisez et développez votre entreprise avec l'IA"},
    "US": {"lang": "English", "welcome": "Build, Automate & Scale Your Business with AI"}
}

def get_localized_pricing(base_inr_amount: float, country_code: str = "IN") -> dict:
    """Converts base INR pricing to visitor's local country currency dynamically."""
    cc = country_code.upper()
    cfg = CURRENCY_MAP.get(cc, CURRENCY_MAP["IN"])
    converted = round(base_inr_amount * cfg["multiplier"], 2)
    return {
        "currency_code": cfg["code"],
        "symbol": cfg["symbol"],
        "amount": converted,
        "formatted": f"{cfg['symbol']}{converted:,.2f}"
    }

def generate_tailored_client_solution(client_name: str, country: str, raw_requirement: str) -> dict:
    """Rule 3: Zero Copy-Paste. Generates a 100% custom tailored product architecture based on exact client need."""
    prompt = f"""
    Client: {client_name} | Country: {country}
    Raw Need: "{raw_requirement}"
    
    Tum aIValue8 ke Master Solutions Architect ho. Rule: Koi copy-paste solution nahi dena hai. Is specific client ki exact requirement ke hisaab se ek custom tailormade product/architecture design karo.
    Reply ONLY valid JSON:
    {{
      "tailored_product_name": "Customized solution title",
      "custom_architecture": "3-line exact technical workflow designed specifically for this client",
      "value_justification": "Why this custom build solves their unique bottleneck",
      "suggested_tier": "Enterprise / Custom Build"
    }}
    """
    raw = smart_generate(prompt, system_prompt="Tum Custom Solutions Architect ho.", model=PRIMARY_MODEL, json_mode=True)
    return json.loads(raw)
