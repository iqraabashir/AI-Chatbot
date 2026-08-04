def detect_query_type(question):

    question = question.lower()

    programme_keywords = [
        "bca","bba","bsc","ba","bcom",
        "mca","mba","msc","ma","mcom",
        "programme","program","course",
        "eligibility","intake","seat",
        "duration","fee","fees",
        "department","prospectus"
    ]

    pdf_keywords = [
        "policy",
        "ordinance",
        "prospectus",
        "rule",
        "regulation",
        "anti ragging",
        "refund",
        "discipline"
        "admission",
        "admission process",
        "selection process"
    ]

    website_keywords = [
        "latest",
        "notification",
        "notice",
        "result",
        "exam date",
        "date sheet"
    ]

    for word in programme_keywords:
        if word in question:
            return "programme"

    for word in pdf_keywords:
        if word in question:
            return "pdf"

    for word in website_keywords:
        if word in question:
            return "website"

    return "knowledge"