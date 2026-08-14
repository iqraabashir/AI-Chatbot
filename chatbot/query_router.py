
def detect_query_type(question):
    question = question.lower()
    print(question)
    if "integrated" in question:    
        return "programme"

    programme_keywords = [
    # UG
      "ba","bsc","bcom","bca","bba",

    # Integrated
      "integrated","integrated msc","integrated ma",
      "integrated mba","integrated mca","msc","chemistry",
      "bed","b.ed","med","m.ed",

    # PG
      "ma","msc","mcom","mba","mca",

    # General
      "programme","program","course","courses",
      "specialization","school",

    # Programme information
      "eligibility","fee","fees","intake","seat","seats",
      "duration","selection","admission",
      "admission process","selection process",
      "cuet",
      "study",
      "studied",
      "where can i study",
      "where to study",
      "information technology",
      "it",
      "computer applications",
      "computer science",
      "data science",
      "physics",
      "chemistry",
      "geography",
      "mathematics",
      "botany",
      "zoology",
      "economics",
      "english",
      "history",
      "psychology",
      "statistics",
      "biotechnology",
      "biochemistry",
      "environmental science",
      "urdu",
      "education"
    ]

    pdf_keywords = [
        "policy",
        "ordinance",
        "prospectus",
        "rule",
        "regulation",
        "anti ragging",
        "refund",
        "discipline",
        "admission",
        "admission process",
        "selection process"
    ]

    website_keywords = [
        "latest",
        "latest notification",
        "notification",
        "notifications",
        "notice",
        "result",
        "results",
        "exam",
        "exam date",
        "datesheet",
        "date sheet",
        "circular",
        "circulars",
        "tender",
        "news"
    ]
    # universityinfo
    university_keywords = [
        "university",
        "cluster university",
        "university mission",
        "university vision",
        "university name",
        "university established",
        "university type",
        "university headquarters",
        "university purpose",
        "university funding",

        "constituent colleges",
        "constituent college",

        "chancellor",
        "vice chancellor",
        "pro chancellor",
        "vc",
        "pro-chancellor",
        "registrar",

        "controller of examinations",
        "controller of examination",
        "controller of exams",
        "controller exams",
        "exam controller",
        "examination controller",
        "exam controller of university",
        "university exam controller",
        "university examination controller",
        "controller of university exams",
        "controller of university examinations"

]
    college_keywords = [
       "principal",
       "campus",
       "address",
       "location",
       "district",
       "state",

       "hostel",
       "library",
       "laboratory",
       "laboratories",
       "sports",
       "ncc",
       "nss",
       "facilities",
       "website",
       "google map",
       "email",
       
       "sri pratap college",
       "sp college",
       "spc",
       "amar singh college",
       "government college for women",
       "abdul ahad azad",
       "institute of advanced studies",
       "gcw",
       "asc",
       "aaamc",
       "aaamdc",
       "gdc bemina",
       "iase"   
    ]
    programme_fields = [
      "fee",
      "fees",
      "eligibility",
      "duration",
      "intake",
      "admission",
      "selection",
      "overview"
    ]
    if any(x in question for x in programme_fields):
        return "programme"
    # uniinfo
    for word in university_keywords:
            if word in question:
                return "university"

    
    for word in college_keywords:
        if word in question:
            return "college"
    
    if "integrated" in question:
        return "programme"
    print("programme_keywords", programme_keywords)
  
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