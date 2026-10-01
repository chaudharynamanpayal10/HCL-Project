import os
import json
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory
from rag_engine import CampusAIRagEngine

app = Flask(__name__, static_folder="static", template_folder="templates")
rag_engine = CampusAIRagEngine()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat_endpoint():
    data = request.get_json() or {}
    message = data.get("message", "").strip()
    category = data.get("category", "all")

    if not message:
        return jsonify({"error": "Empty message"}), 400

    # Retrieve relevant context from RAG engine
    matches = rag_engine.search(message, top_k=4, category=category)
    result = rag_engine.synthesize_answer(message, matches)

    return jsonify({
        "query": message,
        "category": category,
        "answer": result["answer"],
        "sources": result["sources"],
        "follow_ups": result.get("follow_ups", []),
        "verified_date": result.get("verified_date", "2026-10-01"),
        "confidence": result.get("confidence", 95),
        "timestamp": datetime.now().strftime("%I:%M %p")
    })

@app.route("/api/stats", methods=["GET"])
def stats_endpoint():
    return jsonify({
        "institution": "ABES Engineering College (ABESEC)",
        "status": "Autonomous since 2025",
        "established": 2000,
        "students": "8,090+",
        "alumni": "24,000+",
        "startups": "54 Incubated",
        "highest_package_2025": "60 LPA",
        "highest_package_2026": "45 LPA (Clyromedia)",
        "placement_offers_2025": "1,692",
        "placement_offers_2026": "1,289",
        "campus_size": "15.77 Acres",
        "scopus_publications": "2,690+",
        "patents": "375+ Published, 9 Granted",
        "recruiters": "500+",
        "verified_date": "2026-10-01"
    })

@app.route("/api/programs", methods=["GET"])
def programs_endpoint():
    programs = [
        {"name": "Computer Science & Engineering (CSE)", "degree": "B.Tech", "intake": 900, "duration": "4 Years", "entrance": "JEE Main (85% Counselling / 15% Direct)"},
        {"name": "CSE (Artificial Intelligence & Machine Learning)", "degree": "B.Tech", "intake": 360, "duration": "4 Years", "entrance": "JEE Main (85% Counselling / 15% Direct)"},
        {"name": "CSE (Data Science)", "degree": "B.Tech", "intake": 180, "duration": "4 Years", "entrance": "JEE Main (85% Counselling / 15% Direct)"},
        {"name": "Electronics & Communication Engineering (ECE)", "degree": "B.Tech", "intake": 180, "duration": "4 Years", "entrance": "JEE Main (NBA Accredited)"},
        {"name": "Electrical & Computer Engineering (ELCE/EN)", "degree": "B.Tech", "intake": 120, "duration": "4 Years", "entrance": "JEE Main 2026"},
        {"name": "Mechanical Engineering (ME)", "degree": "B.Tech", "intake": 60, "duration": "4 Years", "entrance": "JEE Main 2026"},
        {"name": "B.Tech CSE (Working Professional)", "degree": "B.Tech", "intake": 30, "duration": "3.5 Years", "entrance": "Diploma / Working Professional"},
        {"name": "B.Tech ECE (Working Professional)", "degree": "B.Tech", "intake": 30, "duration": "3.5 Years", "entrance": "Diploma / Working Professional"},
        {"name": "Bachelor of Computer Applications (BCA)", "degree": "BCA", "intake": 120, "duration": "3 Years", "entrance": "CUET (UG)-2026 / 10+2 Merit"},
        {"name": "Master of Computer Applications (MCA)", "degree": "MCA", "intake": 180, "duration": "2 Years", "entrance": "CUET (PG)-2026"},
        {"name": "M.Tech Computer Science & Engineering", "degree": "M.Tech", "intake": 12, "duration": "2 Years", "entrance": "B.Tech CSE / GATE"},
        {"name": "M.Tech Electronics & Communication", "degree": "M.Tech", "intake": 6, "duration": "2 Years", "entrance": "B.Tech ECE (Up to 100% Scholarship + ₹8k TA)"},
        {"name": "Master of Business Administration (MBA)", "degree": "MBA", "intake": "Inquire via ERP", "duration": "2 Years", "entrance": "CUET (PG) / ERP Online Enquiry"}
    ]
    return jsonify(programs)

@app.route("/api/fees", methods=["GET"])
def fees_endpoint():
    return jsonify({
        "academic_fee_total": 181200,
        "academic_year": "2026-27",
        "breakdown": [
            {"component": "Tuition Fee", "amount": 110000, "type": "Annual"},
            {"component": "Career Planning & Development Fee", "amount": 36000, "type": "Annual"},
            {"component": "Examination Fees", "amount": 9600, "type": "Annual"},
            {"component": "Technology and Digital Learning Support", "amount": 6000, "type": "Annual"},
            {"component": "Industry Engagement & Innovation Support", "amount": 6000, "type": "Annual"},
            {"component": "Student Learning Resource Access & Book Bank", "amount": 5000, "type": "Annual"},
            {"component": "Security Deposit (Refundable - One-Time)", "amount": 5000, "type": "One-Time Refundable"},
            {"component": "Admissions, Registration & Documentation", "amount": 3100, "type": "One-Time"},
            {"component": "Student Welfare & Group Insurance", "amount": 500, "type": "Annual"}
        ],
        "mandatory_uniform": {
            "amount": 9900,
            "items": "Trousers/pants, shirts, ties, scarf (girls), sweater, blazer, T-shirt and sweatshirt."
        },
        "payment_rules": [
            "Academic fees are strictly NOT accepted by cash or cheque.",
            "Authorized modes: Online Payment Gateway, Jodo, Bank Demand Draft, or RTGS/NEFT."
        ],
        "pre_enrollment": [
            {"category": "Gen / OBC (UP & Outside) - Appeared in Entrance", "fee": 1000},
            {"category": "SC / ST (UP) - Appeared in Entrance", "fee": 500},
            {"category": "Gen / OBC (UP & Outside) - Direct Non-Entrance", "fee": 2300},
            {"category": "SC / ST (UP) - Direct Non-Entrance", "fee": 1150}
        ],
        "refund_policy": "Governed by UGC refund guidelines. Hostel withdrawal refunds unutilized mess and laundry on a pro-rata basis along with security deposit."
    })

@app.route("/api/hostel", methods=["GET"])
def hostel_endpoint():
    return jsonify({
        "inventory": "6 Boys Hostels, 2 Girls Hostels",
        "campus_area": "15.77 Acres",
        "boys_hostels": [
            {"type": "4-Seater Non-AC", "total": 136500, "security": 5000},
            {"type": "4-Seater AC", "total": 148000, "security": 5000},
            {"type": "Triple Non-AC", "total": 143000, "security": 5000},
            {"type": "Triple AC", "total": 164000, "security": 5000},
            {"type": "Double Non-AC", "total": 154500, "security": 5000},
            {"type": "Double AC", "total": 177500, "security": 5000}
        ],
        "girls_hostels": [
            {"type": "4-Seater AC", "total": 148000, "security": 5000},
            {"type": "Triple AC", "total": 164000, "security": 5000},
            {"type": "Double AC", "total": 177500, "security": 5000}
        ],
        "rules": [
            "Allotment is strictly first-come, first-served.",
            "AC rooms are allotted only upon full room occupancy.",
            "AC timings: 5:00 PM to 8:00 AM on working days; round-the-clock on holidays (subject to UPPCL commercial power).",
            "Laundry fee: ₹3,500 for up to 500 clothes per year included in charges.",
            "Attached washroom rooms carry ₹10,000 extra charge shared equally among roommates.",
            "Desert coolers prohibited in Girls Hostel; boys cooler subject to permission."
        ]
    })

@app.route("/api/placements", methods=["GET"])
def placements_endpoint():
    return jsonify({
        "year_2025": {
            "highest_package": "60 LPA",
            "total_offers": "1,692",
            "recruiters": "500+"
        },
        "year_2026": {
            "highest_package": "45 LPA",
            "total_offers": "1,289",
            "visiting_companies": "489"
        },
        "highlights_2026": [
            {"name": "Amit Kumar", "branch": "CSE (Data Science)", "company": "Clyromedia", "package": "45 LPA", "role": "SDE-II"},
            {"name": "Supriya Pandey", "branch": "CSE", "company": "Texas Instruments", "package": "39 LPA", "role": "SDE"},
            {"name": "Yashika", "branch": "Computer Science", "company": "Horizon X", "package": "24.48 LPA", "role": "Trainee"}
        ],
        "top_recruiters": [
            "Google", "Microsoft", "Adobe", "Atlassian", "Goldman Sachs",
            "TCS", "Cognizant", "Infosys", "Accenture", "Capgemini", "DXC", "Samsung"
        ]
    })

@app.route("/api/directory", methods=["GET"])
def directory_endpoint():
    return jsonify({
        "deans": [
            {"role": "Dean Academics & Trainings", "name": "Prof. (Dr.) Amit Sinha", "email": "dean.academics@abes.ac.in"},
            {"role": "Dean Student Welfare", "name": "Prof. (Dr.) Amita Tripathy", "email": "dean.sw@abes.ac.in"},
            {"role": "Dean Administration", "name": "Mr. Mohit Misra", "email": "dean.admin@abes.ac.in"}
        ],
        "hods": [
            {"dept": "Computer Science & Engineering", "name": "Prof. (Dr.) Pankaj Sharma", "email": "hodcse@abes.ac.in"},
            {"dept": "CSE (AI & Machine Learning)", "name": "Dr. Deepali Dev", "email": "hodcseaiml@abes.ac.in"},
            {"dept": "CSE (Data Science)", "name": "Dr. Prabhat Singh", "email": "hodcseds@abes.ac.in"},
            {"dept": "Electronics & Communication Eng.", "name": "Prof. (Dr.) Kimmi Verma", "email": "hod.ece@abes.ac.in"},
            {"dept": "Electrical & Computer Eng. (EN)", "name": "Dr. Pragati Shrivastava Deb", "email": "hod.en@abes.ac.in"},
            {"dept": "Mechanical Engineering", "name": "Prof. (Dr.) Ravi Shankar Raman", "email": "hod.me@abes.ac.in"},
            {"dept": "Computer Applications (MCA/BCA)", "name": "Prof. (Dr.) Devendra Kumar", "email": "hodmca@abes.ac.in"},
            {"dept": "Applied Sciences & Humanities", "name": "Dr. Jaya Singh", "email": "hod.ash@abes.ac.in"}
        ],
        "general_contact": {
            "address": "19th KM Stone, NH-09, Ghaziabad, UP 201009",
            "phone": "0120-7135112",
            "email": "info@abes.ac.in",
            "website": "https://www.abes.ac.in"
        }
    })

@app.route("/api/clubs", methods=["GET"])
def clubs_endpoint():
    clubs = [
        {"name": "Software Development Club (SDC)", "category": "Technical", "focus": "Coding, web development, mobile apps, hackathons", "intake": "30 Members", "recruitment": "Domain tasks & evaluation (Graphics, PR, Tech, Events)"},
        {"name": "Dataverse (DS & AI Club)", "category": "Technical / AI", "focus": "Data science, machine learning, Power BI, CodeBids", "intake": "30 Members", "recruitment": "September after Datathon & Hackoverse"},
        {"name": "Minerva Literary Society", "category": "Literary & Debate", "focus": "Debating, anchoring, creative writing, poetry, FORTIFY fest", "intake": "Competitive", "recruitment": "Aptitude writing test + personal interview"},
        {"name": "Kalakrit Cultural Club", "category": "Cultural", "focus": "Dance, music, fashion, vocals, Manthan flagship fest", "intake": "Open", "recruitment": "Auditions in June-July"},
        {"name": "Sports Club", "category": "Athletics", "focus": "Football, cricket, basketball, tennis, swimming, Utsaaha & APL", "intake": "Open", "recruitment": "Fitness trials and sport evaluations"},
        {"name": "Samvaad Theatre Group", "category": "Performing Arts", "focus": "Stage drama, street play, Playhouse (MoU with Treasure Art)", "intake": "Audition-based", "recruitment": "Auditions & interviews in June"},
        {"name": "Creative-U", "category": "Fine Arts", "focus": "Wall painting, sketching, digital art, photography", "intake": "30-40 Members", "recruitment": "Annual drive in June-July"},
        {"name": "Environ Club", "category": "Environmental", "focus": "Green Door, eco-sustainability, Treasure Hunt", "intake": "Volunteer-based", "recruitment": "Annual recruitment drive in August"},
        {"name": "Model United Nations (MUN)", "category": "Diplomacy", "focus": "International debate, global affairs, diplomatic speaking", "intake": "Audition-based", "recruitment": "Annual drive in June"},
        {"name": "Spiritual & Yoga Society (SYC)", "category": "Wellness", "focus": "Yoga camps, meditation, stress relief sessions", "intake": "Open", "recruitment": "Annual drive with continuous enrolment"}
    ]
    return jsonify(clubs)

@app.route("/api/search", methods=["GET"])
def search_endpoint():
    q = request.args.get("q", "").strip()
    cat = request.args.get("category", "all")
    if not q:
        return jsonify([])
    results = rag_engine.search(q, top_k=8, category=cat)
    return jsonify(results)

@app.route("/api/grievance-draft", methods=["POST"])
def grievance_draft_endpoint():
    data = request.get_json() or {}
    name = data.get("name", "Student")
    dept = data.get("department", "CSE")
    year = data.get("year", "1st Year")
    category = data.get("category", "Academic")
    subject = data.get("subject", "General Grievance")
    details = data.get("details", "")

    today_str = datetime.now().strftime("%d %B %Y")
    ticket_id = f"GRC-ABES-{datetime.now().strftime('%Y%m%d%H%M')}"

    draft = f"""================================================================================
OFFICIAL STUDENT GRIEVANCE SUBMISSION DRAFT
ABES Engineering College — Student Grievance Redressal Cell (SGRC)
Reference ID: {ticket_id} | Date: {today_str}
================================================================================

To:
The Head of Department ({dept}) / Convener, Student Grievance Redressal Committee (SGRC)
ABES Engineering College, 19th KM Stone, NH-09, Ghaziabad, UP 201009

Subject: FORMAL GRIEVANCE REGARDING: {subject.upper()}

Respected Sir/Madam,

I, {name}, a student of {dept} ({year}) at ABES Engineering College, hereby formally lodge this grievance for your urgent consideration and resolution under the statutory ABES Grievance Redressal Mechanism.

1. GRIEVANCE CATEGORY:
   {category}

2. DETAILED DESCRIPTION:
   {details}

3. RELIEF REQUESTED:
   I kindly request the concerned department and committee to examine this matter at the earliest and provide an appropriate resolution.

4. STATUTORY TIMELINE ACKNOWLEDGMENT:
   As per official college grievance guidelines (https://www.abes.ac.in/GRC-grievance-redressal-cell.html):
   - Department HOD acknowledgment and decision report is expected within 5 working days.
   - Final SGRC committee approval within 7 days.
   - If not satisfactorily resolved within 4 days of HOD decision, appeal may be submitted to the Central Grievance Committee.
   - External escalation is subject to the University Ombudsperson (AKTU Lucknow).

Yours sincerely,
{name}
Department: {dept} ({year})
ABES Engineering College
[Submitted via Campus-AI Grievance Assistant]
================================================================================
"""
    return jsonify({
        "ticket_id": ticket_id,
        "date": today_str,
        "draft_text": draft
    })

if __name__ == "__main__":
    print("Starting Campus-AI on port 5000...")
    app.run(host="0.0.0.0", port=5000, debug=True)
