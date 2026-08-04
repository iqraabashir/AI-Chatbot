def contains_any(question, words):
    question = question.lower()
    return any(word in question for word in words)
INTAKE = [
    "seat",
    "seats",
    "intake",
    "capacity",
    "available seats",
    "total seats",
    "strength"
]
FEE = [
    "fee",
    "fees",
    "cost",
    "charges",
    "tuition",
    "payment",
    "price"
]
ELIGIBILITY = [
    "eligibility",
    "eligible",
    "qualification",
    "criteria",
    "requirements",
    "required"
]

DURATION = [
    "duration",
    "year",
    "years",
    "semester",
    "semesters",
    "time",
    "period"
]

COLLEGE = [
    "college",
    "offered",
    "offers",
    "where",
    "campus"
]

DEPARTMENT = [
    "department",
    "dept",
    "school",
    "faculty"
]
ADMISSION = [
    "admission",
    "apply",
    "application",
    "admission process"
]

SELECTION = [
    "selection",
    "selection process",
    "selection criteria"
]

OVERVIEW = [
    "about",
    "overview",
    "details",
    "information",
    "tell me",
    "explain"
]