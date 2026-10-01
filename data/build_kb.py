import json
import os

# Create data directory
DATA_DIR = r"C:\Users\naman\.gemini\antigravity\scratch\CampusAI\data"
os.makedirs(DATA_DIR, exist_ok=True)

# Parse and compile base records and chunks provided in prompt
records = [
  {
    "id": "INST-001",
    "category": "institution",
    "title": "Institution identity and address",
    "content": "ABES Engineering College (ABESEC), 19th KM Stone, NH-09, Ghaziabad, Uttar Pradesh 201009. Main phone: 0120-7135112. General email: info@abes.ac.in. Established in 2000. The college states it has been autonomous since 2025.",
    "source": "https://www.abes.ac.in/index.html",
    "source_url": "https://www.abes.ac.in/index.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["ABES", "address", "phone", "email", "autonomous", "established", "location", "Ghaziabad"]
  },
  {
    "id": "INST-002",
    "category": "institution",
    "title": "Current at-a-glance figures",
    "content": "The 2026 website homepage reports: 8,090 students on campus; 24,000+ alumni worldwide; 54 startups incubated; 60 LPA highest placement package in 2025; 1,692 placement offers in 2025; 15.77-acre campus; 500+ recruiters; 2,690+ Scopus publications; 375+ published patents; 9 granted patents; ₹15 lakh consultancy received in 2024-25; ₹107.5 lakh sponsored research in 2024-25.",
    "source": "https://www.abes.ac.in/index.html",
    "source_url": "https://www.abes.ac.in/index.html",
    "source_type": "official_abes",
    "academic_year": "2026",
    "keywords": ["students", "alumni", "startups", "highest package", "campus size", "patents", "research", "consultancy"]
  },
  {
    "id": "ACAD-001",
    "category": "programs",
    "title": "Programs and approved intake shown for 2026",
    "content": "B.Tech: CSE 900; CSE (AI & ML) 360; CSE (Data Science) 180; Electronics & Communication Engineering 180; Electrical & Computer Engineering 120; Mechanical Engineering 60; CSE Working Professional 30; ECE Working Professional 30. BCA 120. MCA 180. M.Tech CSE 12. M.Tech ECE 6.",
    "source": "https://www.abes.ac.in/courses-offered.html",
    "source_url": "https://www.abes.ac.in/courses-offered.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["intake", "seats", "courses", "B.Tech", "CSE", "AIML", "Data Science", "ECE", "ELCE", "Mechanical", "BCA", "MCA", "M.Tech"]
  },
  {
    "id": "ADM-001",
    "category": "admissions",
    "title": "2026-27 B.Tech admission route",
    "content": "For 2026-27, the official admissions page states that 85% of approved seats are filled through counselling based on JEE-2026 and AICTE/AKTU eligibility; 15% are offered through direct admission under AICTE/AKTU and college policy. Direct admission includes online application, shortlisting using qualifying aggregate and JEE score/rank, interview, and selection based on test/interview performance.",
    "source": "https://www.abes.ac.in/courses-offered.html",
    "source_url": "https://www.abes.ac.in/courses-offered.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["counselling", "direct admission", "JEE 2026", "85%", "15%", "shortlisting", "interview", "eligibility"]
  },
  {
    "id": "ADM-002",
    "category": "admissions",
    "title": "2026 entrance examinations referenced",
    "content": "The admissions page references JEE (Main) 2026 for engineering, CUET (UG)-2026 for B.Tech lateral entry/BCA, and CUET (PG)-2026 for MCA.",
    "source": "https://www.abes.ac.in/courses-offered.html",
    "source_url": "https://www.abes.ac.in/courses-offered.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["JEE Main 2026", "CUET UG 2026", "CUET PG 2026", "lateral entry", "entrance exam"]
  },
  {
    "id": "ADM-003",
    "category": "admissions",
    "title": "Admissions document and fee information",
    "content": "The official admissions page contains required-document instructions, academic-fee information, examination-fee notes, pre-enrollment registration charges, hostel fees, payment modes, uniform charges, refund policy, and PM-Vidyalaxmi information. The page should be treated as session-specific and rechecked before answering fee questions.",
    "source": "https://www.abes.ac.in/courses-offered.html",
    "source_url": "https://www.abes.ac.in/courses-offered.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["documents", "fees", "PM-Vidyalaxmi", "refund policy", "registration", "uniform", "verification"]
  },
  {
    "id": "HOST-001",
    "category": "hostel",
    "title": "2026-27 hostel fee structure",
    "content": "For 2026-27, boys' hostel totals including refundable security are listed as ₹136,500 (4-seater non-AC), ₹148,000 (4-seater AC), ₹143,000 (triple non-AC), ₹164,000 (triple AC), ₹154,500 (double non-AC), and ₹177,500 (double AC). Girls' AC hostel totals including refundable security are ₹148,000 (4-seater), ₹164,000 (triple), and ₹177,500 (double).",
    "source": "https://www.abes.ac.in/courses-offered.html",
    "source_url": "https://www.abes.ac.in/courses-offered.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["hostel fee", "boys hostel", "girls hostel", "AC", "non-AC", "double seater", "triple seater", "four seater", "refundable security"]
  },
  {
    "id": "HOST-002",
    "category": "hostel",
    "title": "Hostel conditions & rules",
    "content": "Room allotment is first-come, first-served. AC rooms are allotted only upon full occupancy of the designated room. AC usage is stated as 5 PM–8 AM on working days and round-the-clock on holidays, subject to UPPCL commercial power availability. Limited attached-bathroom rooms have an additional ₹10,000 charge shared equally among roommates. Girls' hostel desert coolers are prohibited; boys' hostel cooler use is subject to college policy.",
    "source": "https://www.abes.ac.in/courses-offered.html",
    "source_url": "https://www.abes.ac.in/courses-offered.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["room allotment", "AC timing", "5 PM to 8 AM", "attached bathroom", "cooler rule", "UPPCL power"]
  },
  {
    "id": "V4-HOST-001",
    "category": "hostel",
    "title": "Hostel inventory and facilities",
    "content": "ABES Life@ABES page states there are 6 boys' hostels and 2 girls' hostels. Accommodation includes AC and non-AC single, double and triple sharing. Facilities mentioned include basketball, badminton, lawn tennis, table tennis, gym, laundry, and mess/canteen facilities in each hostel. Laundry is listed at ₹3,500 for 500 clothes per year and refundable hostel security is ₹5,000.",
    "source": "https://www.abes.ac.in/life-at-abes.html",
    "source_url": "https://www.abes.ac.in/life-at-abes.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["6 boys hostels", "2 girls hostels", "gym", "laundry", "sports", "laundry ₹3500", "500 clothes"]
  },
  {
    "id": "V5-FEE-001",
    "category": "fees",
    "title": "2026-27 academic fee total and itemized breakdown",
    "content": "The current ABES admissions page lists a 2026-27 academic fee total of ₹181,200 for the displayed main fee structure. Detailed breakdown: Tuition Fee ₹110,000; Career Planning & Development Fee ₹36,000; Examination Fees ₹9,600; Technology and Digital Learning Support ₹6,000; Industry Engagement & Innovation Support ₹6,000; Student Learning Resource Access & Book Bank ₹5,000; Security Deposit (Refundable - One-Time) ₹5,000; Admissions, Registration & Documentation ₹3,100; Student Welfare & Group Insurance ₹500.",
    "source": "https://www.abes.ac.in/courses-offered.html",
    "source_url": "https://www.abes.ac.in/courses-offered.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["academic fee", "₹181,200", "tuition fee ₹110,000", "career planning ₹36,000", "examination fee ₹9600", "security deposit ₹5000"]
  },
  {
    "id": "FEE-001",
    "category": "fees",
    "title": "Uniform and payment conditions",
    "content": "For 2026-27, mandatory uniform charges are listed as ₹9,900 (includes specified quantities of trousers/pants, shirts, ties, scarf for girls, sweater, blazer, T-shirt and sweatshirt). Academic fees are strictly not accepted by cheque or cash. Allowed payment routes include payment gateway, Jodo, bank draft, and RTGS/NEFT.",
    "source": "https://www.abes.ac.in/courses-offered.html",
    "source_url": "https://www.abes.ac.in/courses-offered.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["uniform ₹9,900", "blazer", "no cash", "no cheque", "Jodo", "RTGS", "NEFT", "payment gateway"]
  },
  {
    "id": "V5-FEE-012",
    "category": "fees",
    "title": "2026-27 Pre-enrollment registration charges",
    "content": "Pre-enrollment registration charges for direct admission: ₹1,000 for General/OBC of UP and all categories outside UP when candidate appeared for entrance exam/counselling; ₹500 for SC/ST of UP in that case; ₹2,300 for General/OBC of UP and outside UP when candidate did not appear; ₹1,150 for SC/ST of UP when candidate did not appear.",
    "source": "https://www.abes.ac.in/courses-offered.html",
    "source_url": "https://www.abes.ac.in/courses-offered.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["pre-enrollment", "registration charges", "₹1000", "₹500", "₹2300", "₹1150", "direct admission fee"]
  },
  {
    "id": "V5-FEE-015",
    "category": "fees",
    "title": "2026-27 refund policy",
    "content": "For newly admitted students in 2026-27, ABES states that academic fee refund on cancellation follows UGC refund rules. For hostel withdrawal, security plus mess and laundry charges for unutilized months are refundable on a pro-rata basis.",
    "source": "https://www.abes.ac.in/courses-offered.html",
    "source_url": "https://www.abes.ac.in/courses-offered.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["refund policy", "UGC refund rules", "hostel withdrawal", "pro-rata refund", "security refund"]
  },
  {
    "id": "PLACE-001",
    "category": "placements",
    "title": "College-wide placement statistics 2025-26",
    "content": "The placement page currently lists 489 companies for campus placements, 1,289 placement offers, and a highest package of 45 LPA for the 2025-26 statistics block. (The homepage separately reports 60 LPA as the highest package in placements 2025, with 1,692 offers, so chatbot answers must preserve the source year/definition rather than merging the figures).",
    "source": "https://www.abes.ac.in/placement.html",
    "source_url": "https://www.abes.ac.in/placement.html",
    "source_type": "official_abes",
    "academic_year": "2025-26",
    "keywords": ["placements 2025-26", "45 LPA", "489 companies", "1289 offers", "highest package 2026"]
  },
  {
    "id": "V5-INST-002",
    "category": "placements",
    "title": "Homepage placement headline 2025",
    "content": "The homepage reports placements 2025: 60 LPA highest package, 1,692 placement offers in 2025. These figures must remain labelled as 2025 and must not be merged with 2025-26 placement page statistics.",
    "source": "https://www.abes.ac.in/index.html",
    "source_url": "https://www.abes.ac.in/index.html",
    "source_type": "official_abes",
    "academic_year": "2025",
    "keywords": ["60 LPA", "1692 offers", "placements 2025", "highest package"]
  },
  {
    "id": "PLACE-002",
    "category": "placements",
    "title": "Placement recruiters and individual highlights 2026",
    "content": "Prominent campus recruiters include Microsoft, Adobe, Atlassian, Goldman Sachs, Google, TCS, Cognizant, Infosys, Accenture, Capgemini, DXC. 2026 Highlights: Amit Kumar from CSE (Data Science) secured 45 LPA Clyromedia offer (SDE-II); Supriya Pandey from CSE secured 39 LPA Texas Instrument offer (SDE); Yashika from CS secured 24.48 LPA Horizon X offer (Trainee).",
    "source": "https://www.abes.ac.in/placement.html",
    "source_url": "https://www.abes.ac.in/placement.html",
    "source_type": "official_abes",
    "academic_year": "2025-26",
    "keywords": ["Amit Kumar 45 LPA Clyromedia", "Supriya Pandey 39 LPA Texas Instruments", "Yashika 24.48 LPA", "Google", "Microsoft", "Goldman Sachs"]
  },
  {
    "id": "DEPT-001",
    "category": "departments",
    "title": "CSE (AI & ML) Department",
    "content": "CSE-AIML was established in 2020 and offers a four-year B.Tech with approved intake of 360 seats. HOD: Dr. Deepali Dev. Emphasizes machine learning algorithms, computer vision and pattern recognition, ethical/responsible AI, NLP, robotics, intelligent systems, and big data. 2024 average package was ₹6.34 lakh (highest ₹49.12 lakh) and 2025 average package was ₹5.17 lakh (highest ₹12.93 lakh).",
    "source": "https://www.abes.ac.in/cse-aiml.html",
    "source_url": "https://www.abes.ac.in/cse-aiml.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["CSE-AIML", "360 seats", "Dr. Deepali Dev", "computer vision", "NLP", "hackathons"]
  },
  {
    "id": "DEPT-012",
    "category": "departments",
    "title": "Computer Science & Engineering (CSE) Department",
    "content": "B.Tech CSE approved intake is 900 seats; working professional intake 30; M.Tech CSE 12 seats. HOD: Prof. (Dr.) Pankaj Sharma. Facilities include Digital Image Processing Lab, Discrete Mathematics & OS Lab, DBMS Lab, DAA Lab, Networks Lab. Industry training in Cisco network security, AWS/cloud computing, C/C++, Oracle/SQL, Python/ML. MoUs with Cisco, Samsung, CodeChef, EICT, IEEE, ISDC, JNU, Tech Mahindra, UiPath. 2024 placement snapshot: 203 actual placements, 52.00 LPA highest package, 100% placement rate, 423 total offers.",
    "source": "https://www.abes.ac.in/academics/computer-science-engineering.html",
    "source_url": "https://www.abes.ac.in/academics/computer-science-engineering.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["CSE", "900 seats", "Prof. Pankaj Sharma", "52 LPA", "Digital Image Processing Lab", "Cisco", "Samsung"]
  },
  {
    "id": "DEPT-015",
    "category": "departments",
    "title": "CSE (Data Science) Department",
    "content": "B.Tech CSE Data Science approved intake is 180 seats. HOD: Dr. Prabhat Singh. Department page reports 69.35% placement percentage and 137 placement offers. Internships include Coincent, Google Summer of Code, Valenceware, Glorious Insight. Placements include Accenture, Cloud Expert, Centilytics, Gemini Solutions, Hexaware, Versa. 2025-26 industrial visits to IHFC at IIT Delhi campus and AppSquadz Software.",
    "source": "https://www.abes.ac.in/academics/cse-datascience.html",
    "source_url": "https://www.abes.ac.in/academics/cse-datascience.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["CSE Data Science", "180 seats", "Dr. Prabhat Singh", "Google Summer of Code", "IHFC IIT Delhi"]
  },
  {
    "id": "DEPT-003",
    "category": "departments",
    "title": "Electronics & Communication Engineering (ECE) Department",
    "content": "Established in 2000. B.Tech ECE intake is 180 seats (NBA accredited); working professional intake 30; M.Tech ECE intake 6 seats (2-year full-time). HOD: Prof. (Dr.) Kimmi Verma. Research areas: Verilog/Xilinx, VLSI schematic/layout, embedded systems and IoT, RF/microwave, optical communication, wireless sensor networks. Facilities: NI Innovation Centre, Optical/Microwave Lab, VLSI Design Lab, Embedded IoT Lab, CAD Lab across Bhabha and Ramanujan blocks. M.Tech ECE offers 50% or 100% tuition scholarships plus TA ₹7,000/mo (year 1) and ₹8,000/mo (year 2). ECE 2025 placement snapshot: 88 placements, 7.65 LPA highest package, 121 offers, 66.67% rate.",
    "source": "https://www.abes.ac.in/academics/ece-department.html",
    "source_url": "https://www.abes.ac.in/academics/ece-department.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["ECE", "180 seats", "Prof. Kimmi Verma", "VLSI", "NI Innovation Centre", "M.Tech ECE scholarship", "Teaching Assistantship"]
  },
  {
    "id": "DEPT-005",
    "category": "departments",
    "title": "Electrical & Computer Engineering (ELCE / EN) Department",
    "content": "Established in 2022. B.Tech intake listed as 120 seats in current 2026 course table (page profile established at 60). HOD: Dr. Pragati Shrivastava Deb. Research areas: control/instrumentation, AI, renewable energy, power systems, power electronics, EV fundamentals, batteries/BMS, PLC/pneumatics, Cadence microelectronics. 2024 placement snapshot: 64 placements, 7.00 LPA highest package, 95.71% placement percentage, 120 placement offers.",
    "source": "https://www.abes.ac.in/electrical-and-computer-engineering.html",
    "source_url": "https://www.abes.ac.in/electrical-and-computer-engineering.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["ELCE", "EN", "120 seats", "Dr. Pragati Shrivastava Deb", "EV", "PLC", "batteries BMS", "renewable energy"]
  },
  {
    "id": "DEPT-007",
    "category": "departments",
    "title": "Mechanical Engineering Department",
    "content": "B.Tech Mechanical Engineering approved intake is 60 seats. HOD: Prof. (Dr.) Ravi Shankar Raman. Covers design, materials, thermodynamics, fluid mechanics, mechatronics, AutoCAD, SolidWorks, ANSYS, 3D printing/design, sheet-metal design, CNC. Facilities: Central Workshop, Fluid Mechanics Lab, Manufacturing Technology Lab, CAD/CAM Lab. 2024 placement snapshot: 49 placements, 6 LPA highest package, 97.95% placement rate, average package 3.74 LPA. 2024 short-term training on AR/VR in Manufacturing with NITTTR Chandigarh.",
    "source": "https://www.abes.ac.in/academics/mechanical-engineering.html",
    "source_url": "https://www.abes.ac.in/academics/mechanical-engineering.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["Mechanical Engineering", "60 seats", "Prof. Ravi Shankar Raman", "AutoCAD", "SolidWorks", "ANSYS", "3D printing", "AR/VR"]
  },
  {
    "id": "DEPT-010",
    "category": "departments",
    "title": "Computer Applications (BCA & MCA) Department",
    "content": "BCA approved intake is 120 seats (admission referenced with CUET UG-2026). MCA approved intake is 180 seats (admission referenced with CUET PG-2026). HOD: Prof. (Dr.) Devendra Kumar. Infrastructure: 6 classrooms (60 seats each), 2 tutorial rooms (35 seats), departmental library (40 seats), 18 faculty cabins, 120-seat seminar hall. MCA 2025 placement snapshot: 140 placements, 12.93 LPA highest package, 113 companies, 77.78% placement rate, 182 offers.",
    "source": "https://www.abes.ac.in/mca-department.html",
    "source_url": "https://www.abes.ac.in/mca-department.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["BCA", "120 seats", "MCA", "180 seats", "Prof. Devendra Kumar", "CUET UG", "CUET PG", "12.93 LPA"]
  },
  {
    "id": "PROG-004",
    "category": "programs",
    "title": "MBA Program Status and Policy",
    "content": "ABES confirms MBA as an academic offering on its homepage and ERP Online Enquiry portal (https://erp.abes.ac.in/onlineEnquiryMBA/). However, the current public course-seat table does not publish the exact intake and detailed fee breakdown in the same row as BCA/MCA/M.Tech. Under Campus-AI data quality rules, MBA availability is confirmed, but seat count and fee specifics require live verification through the official ERP portal.",
    "source": "https://erp.abes.ac.in/onlineEnquiryMBA/",
    "source_url": "https://erp.abes.ac.in/onlineEnquiryMBA/",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["MBA", "ERP enquiry", "intake policy", "data quality rule", "verification required"]
  },
  {
    "id": "DEPT-009",
    "category": "departments",
    "title": "Information Technology (Historical Context)",
    "content": "Historically established in 2000 with 180 intake and NBA accreditation. In the current 2026-27 approved course intake table, B.Tech IT is not listed as a standalone intake because programs have transitioned to CSE specializations (AI&ML, Data Science, etc.). This information is preserved strictly as historical context.",
    "source": "https://www.abes.ac.in/academics/it-department.html",
    "source_url": "https://www.abes.ac.in/academics/it-department.html",
    "source_type": "official_abes",
    "academic_year": "Historical vs 2026-27",
    "keywords": ["Information Technology", "historical program", "NBA", "transition"]
  },
  {
    "id": "DEPT-011",
    "category": "departments",
    "title": "Applied Sciences & Humanities (ASH)",
    "content": "Provides foundation education for all first-year B.Tech students. Curriculum includes Applied Physics, Electrical/Electronics/Mechanical engineering basics, Linear Algebra & Statistics, C++ Programming, Environment & Sustainability, Soft Skills, Essentials of AI, Design Thinking, Innovation & Entrepreneurship. HOD: Dr. Jaya Singh (Associate Professor & HOD).",
    "source": "https://www.abes.ac.in/applied-science.html",
    "source_url": "https://www.abes.ac.in/applied-science.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["Applied Sciences & Humanities", "ASH", "first year", "Dr. Jaya Singh", "Physics", "C++", "Design Thinking"]
  },
  {
    "id": "LIB-001",
    "category": "library",
    "title": "Central Library resources and automation",
    "content": "The Central Library occupies 1,565 sq.m with a 400 sq.m reading area and 250 seating capacity. Collection: over 115,210 books, 1,224 e-journals, 8,074 e-books, and audio-video materials. Fully automated with KOHA ILMS (previously Libsys). OPAC allows online book search, reservations, and circulation tracking. Remote access available for subscribed e-resources including IEEE, NDLI, DELNET, NPTEL.",
    "source": "https://www.abes.ac.in/library.html",
    "source_url": "https://www.abes.ac.in/library.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["library", "KOHA", "OPAC", "115210 books", "1224 e-journals", "IEEE", "remote access", "DELNET", "NDLI"]
  },
  {
    "id": "GRC-001",
    "category": "grievance",
    "title": "Student Grievance Process (GRC / SGRC)",
    "content": "Official grievance process: 1. Student registers grievance through online grievance portal. 2. Routed to concerned HOD, who must acknowledge and submit solution report within 5 days. 3. Final GRC approval within 7 days. 4. If unsatisfied, student can appeal to Central Grievance Committee within 4 days of HOD reply. 5. GRC report provided to university and student within 15 days. 6. Further escalation is to the Ombudsperson appointed by affiliating university (Dr. A.P.J. Abdul Kalam Technical University, AKTU Lucknow).",
    "source": "https://www.abes.ac.in/GRC-grievance-redressal-cell.html",
    "source_url": "https://www.abes.ac.in/GRC-grievance-redressal-cell.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["grievance", "GRC", "SGRC", "complaint", "5 days HOD", "7 days approval", "4 days appeal", "15 days university", "AKTU Ombudsperson"]
  },
  {
    "id": "WELL-001",
    "category": "student_support",
    "title": "Medical, Wellness & Counselling Support",
    "content": "Campus includes a medical room with an on-duty doctor and 24x7 ambulance service. Professional psychological and emotional counselling is provided through confidential 'Your Dost' sessions for academic, emotional, personal, or career development challenges. Yoga and meditation facilities are also available.",
    "source": "https://www.abes.ac.in/life-at-abes.html",
    "source_url": "https://www.abes.ac.in/life-at-abes.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["medical room", "ambulance", "doctor", "Your Dost", "counselling", "mental health", "wellness", "yoga"]
  },
  {
    "id": "CAMP-001",
    "category": "campus",
    "title": "Campus amenities and dining",
    "content": "15.77-acre green campus featuring swimming pool, floodlit stadium, cricket ground, badminton/tennis/basketball courts, air-conditioned smart classrooms with LCD projectors, auditorium with multimedia sound, open-air theatre (OAT), five seminar halls, seven canteens/messes/kitchens serving 2,000+ students, campus temple, faculty residences and guest house.",
    "source": "https://www.abes.ac.in/life-at-abes.html",
    "source_url": "https://www.abes.ac.in/life-at-abes.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["15.77 acres", "swimming pool", "floodlit stadium", "auditorium", "open air theatre", "7 canteens", "mess"]
  },
  {
    "id": "ADMIN-001",
    "category": "administration",
    "title": "Key functionaries, Deans and HODs",
    "content": "Chairman: Shri Neeraj Goel; General Secretary: Shri Shashwat Goel; Director: Prof. (Dr.) Devendra Kumar Sharma. Dean Academics & Trainings: Prof. (Dr.) Amit Sinha; Dean Student Welfare: Prof. (Dr.) Amita Tripathy; Dean Administration: Mr. Mohit Misra. Department Heads: CSE/CS: Prof. (Dr.) Pankaj Sharma; ECE: Prof. (Dr.) Kimmi Verma; CSE(AIML): Dr. Deepali Dev; CSE(DS): Dr. Prabhat Singh; Mechanical: Prof. (Dr.) Ravi Shankar Raman; EN & ELCE: Dr. Pragati Shrivastava Deb; MCA: Prof. (Dr.) Devendra Kumar; IT/CE: Prof. (Dr.) Amrita Jyoti; ASH: Dr. Jaya Singh.",
    "source": "https://www.abes.ac.in/important-functionaries.html",
    "source_url": "https://www.abes.ac.in/important-functionaries.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["Director", "Dean Academics", "Amit Sinha", "Amita Tripathy", "Pankaj Sharma", "Kimmi Verma", "Deepali Dev", "Prabhat Singh"]
  },
  {
    "id": "CONTACT-001",
    "category": "contacts",
    "title": "Official contacts and email channels",
    "content": "Address: ABES Engineering College, 19th KM Stone, NH-09, Ghaziabad, UP 201009. Phone: 0120-7135112. General Email: info@abes.ac.in. Key role-based emails: dean.academics@abes.ac.in, dean.sw@abes.ac.in, dean.admin@abes.ac.in, hodcse@abes.ac.in, hodcseaiml@abes.ac.in, hodcseds@abes.ac.in, hod.ece@abes.ac.in, hod.me@abes.ac.in, hodmca@abes.ac.in, hod.it@abes.ac.in.",
    "source": "https://www.abes.ac.in/important-functionaries.html",
    "source_url": "https://www.abes.ac.in/important-functionaries.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["contact", "phone 0120-7135112", "info@abes.ac.in", "emails", "address", "NH-09"]
  },
  {
    "id": "CLUBS-001",
    "category": "clubs",
    "title": "Student clubs and technical societies",
    "content": "11+ active student clubs on campus: 1. Software Development Club (SDC): Coding, web/app development, hackathons; domains: Graphics, Social Media, PR, Events, Technical; annual intake ~30 members. 2. Dataverse (DS & AI Club): ML, AI, Hackoverse, PowerDash, CodeBids; intake ~30 members in September. 3. Minerva: Official literary and debating society, organizes FORTIFY. 4. Kalakrit: Cultural club (dance, music, fashion), flagship fest Manthan, Ground Zero. 5. Sports Club: Utsaaha annual sports meet, APL cricket league, football, basketball. 6. Samvaad: Theatre group, Playhouse 26-day workshop, MoU with Treasure Art. 7. Environ Club: Eco-initiatives, Green Door, Scavenger Hunt. 8. Creative-U: Fine arts, painting, photography, sketching. 9. MUN Club: Model United Nations debating. 10. Spiritual & Yoga Society (SYC): Wellness, meditation.",
    "source": "https://www.abes.ac.in/life-at-abes.html",
    "source_url": "https://www.abes.ac.in/life-at-abes.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["clubs", "SDC", "Dataverse", "Minerva", "Kalakrit", "Sports Club", "Utsaaha", "APL", "Samvaad", "Creative-U", "MUN"]
  },
  {
    "id": "RESEARCH-001",
    "category": "research",
    "title": "Research, Innovation and Conferences",
    "content": "Research & Innovation Cell promotes research, patents, and incubation. College metrics: 2,690+ Scopus publications, 375+ published patents, 9 granted patents, 54 incubated startups, ₹107.5 lakh sponsored research in 2024-25. Organized 2nd International Conference on Computing Sciences & Communications (ICCSC-2026) on 12-13 Feb 2026, technically co-sponsored by IEEE UP Section.",
    "source": "https://www.abes.ac.in/innovation.html",
    "source_url": "https://www.abes.ac.in/innovation.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["research", "patents", "Scopus", "startups", "ICCSC-2026", "IEEE UP Section", "innovation"]
  },
  {
    "id": "NOTICE-001",
    "category": "notices",
    "title": "Current 2026 notices and circulars",
    "content": "Key 2026 notifications: 1. Central Government Scholarship renewal/fresh applications for 2026-27 (29-08-2026). 2. B.Tech Branch Change notification for 2026-27 (17-08-2026). 3. Academic Bank of Credits (ABC) ID creation mandate (08-08-2026). 4. AKTU Challenge Evaluation notice (19-06-2026). 5. College topper recognition notification (27-02-2026). Always verify latest circulars on official website for deadlines.",
    "source": "https://www.abes.ac.in/circulars.html",
    "source_url": "https://www.abes.ac.in/circulars.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["circulars", "scholarship", "branch change", "ABC ID", "challenge evaluation", "notices 2026"]
  },
  {
    "id": "PORT-001",
    "category": "student_services",
    "title": "Student portals & forms",
    "content": "Official portals: 1. Online No-Dues Application portal: https://nodues.abes.ac.in/. 2. Online Admission Registration 2026-27: https://erp.abes.ac.in/onlineregistration/Default.aspx. 3. Online MBA Enquiry: https://erp.abes.ac.in/onlineEnquiryMBA/. Downloadable forms include hostel admission for old students, degree/marksheet collection, transfer certificate (TC), character certificate (CC), and fee/hostel security refund.",
    "source": "https://www.abes.ac.in/footer-form.html",
    "source_url": "https://www.abes.ac.in/footer-form.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["no dues portal", "admission portal", "MBA enquiry", "TC", "character certificate", "degree collection"]
  },
  {
    "id": "PRIV-001",
    "category": "privacy",
    "title": "Student Privacy and Data Protection Rules",
    "content": "Campus-AI strictly adheres to student privacy. The chatbot never requests, collects, or exposes student passwords, OTPs, roll numbers, personal phone numbers, or private emails. Portals requiring credentials must be accessed directly by students at official URLs. Official notices are referenced for institutional dates and procedures only.",
    "source": "https://www.abes.ac.in/GRC-grievance-redressal-cell.html",
    "source_url": "https://www.abes.ac.in/GRC-grievance-redressal-cell.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["privacy", "no passwords", "no OTPs", "PII protection", "data security"]
  },
  {
    "id": "ACC-001",
    "category": "accreditation",
    "title": "Accreditation and Autonomy",
    "content": "ABES Engineering College is NAAC accredited since May 2022 and has an active Internal Quality Assurance Cell (IQAC). The college gained autonomous institution status in 2025. Major B.Tech programs (including CSE, ECE) hold NBA accreditation.",
    "source": "https://www.abes.ac.in/naac-accredited-colleges.html",
    "source_url": "https://www.abes.ac.in/naac-accredited-colleges.html",
    "source_type": "official_abes",
    "academic_year": "2026-27",
    "keywords": ["NAAC", "autonomous 2025", "NBA", "IQAC", "accreditation"]
  }
]

out_path = os.path.join(DATA_DIR, "knowledge_base.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(records, f, indent=2, ensure_ascii=False)

print(f"Successfully generated {len(records)} knowledge base records at {out_path}")
