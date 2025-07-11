def get_user_status(face_detected, speaking):
    if face_detected and speaking:
        return "Kamera va mikrofon ishlamoqda"
    elif face_detected:
        return "Faqat kamera yoniq"
    elif speaking:
        return "Faqat mikrofon ishlamoqda"
    else:
        return "Inaktiv"