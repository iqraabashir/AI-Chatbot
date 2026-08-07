from college_search import search_college, get_last_college

def college_response(question):

    college = search_college(question)

    if college is None:
        college = get_last_college()

    if college is None:
        return None

    q = question.lower()

    answer = [f"🏛 <b>{college['college_name']}</b>\n"]

    if "principal" in q:
        answer.append(f"<b>Principal:</b> {college['principal']}")

    elif "address" in q or "location" in q:
        answer.append(f"<b>Address:</b> {college['address']}")

    elif "hostel" in q:
        answer.append(f"<b>Hostel:</b> {college['hostel']}")

    elif "library" in q:
        answer.append(f"<b>Library:</b> {college['library']}")

    elif "laboratory" in q or "laboratories" in q:
        answer.append(f"<b>Laboratories:</b> {college['laboratories']}")

    elif "sports" in q:
        answer.append(f"<b>Sports:</b> {college['sports']}")

    elif "ncc" in q:
        answer.append(f"<b>NCC:</b> {college['ncc']}")

    elif "nss" in q:
        answer.append(f"<b>NSS:</b> {college['nss']}")

    elif "department" in q or "departments" in q:
        answer.append(f"<b>Departments:</b> {college['departments']}")

    elif "programme" in q or "course" in q:
        answer.append(f"<b>Programmes Offered:</b> {college['programmes_offered']}")

    elif "website" in q:
        answer.append(f"<b>Website:</b> {college['website']}")

    elif "email" in q:
        answer.append(f"<b>Official Email:</b> {college['official_email']}")

    elif "facility" in q or "facilities" in q:
        answer.append(f"<b>Facilities:</b> {college['facilities']}")

    else:
        return f"""
🏛 <b>{college['college_name']}</b>
<b>Overview:</b> {college['overview']}
<b>Principal:</b> {college['principal']}
<b>Address:</b> {college['address']}
<b>Departments:</b> {college['departments']}
<b>Programmes Offered:</b> {college['programmes_offered']}
<b>Facilities:</b> {college['facilities']}
<b>Website:</b> {college['website']}
"""

    return "\n\n".join(answer)