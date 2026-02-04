from config import OSNOVA, PLANNERS, BUNDLE


def get_success_message(payload: str) -> str:
    if payload == 'bundle':
        lines = ["🎉 Aksiyani sotib olganingiz uchun rahmat!", "", "Mana uchta planeringiz (2 narxiga):"]
        for key in BUNDLE['planners']:
            p = PLANNERS[key]
            lines.append(f"📊 {p['title']}")
            lines.append(p['link'])
            lines.append("")
        lines.append("Har bir havolaga bosing → yuqori o'ng burchakda «Nusxa yaratish»")
        return "\n".join(lines)

    p = PLANNERS[payload]
    return (
        f"🎉 Sotib olganingiz uchun rahmat!\n\n"
        f"Mana sizning planeringiz:\n\n"
        f"{p['link']}\n\n"
        f"Havolaga bosing → «Nusxa yaratish» tugmasini bosing"
    )


def get_welcome_message() -> str:
    return OSNOVA['description']
