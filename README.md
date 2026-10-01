# 🎓 Campus-AI: Intelligent Student Support System
### Official AI Assistant & Portal for ABES Engineering College (ABESEC)
*Autonomous Institution Since 2025 | NAAC Accredited | Affiliated with AKTU Lucknow*

---

## 🌟 Executive Overview
**Campus-AI** is a production-grade, full-stack AI-powered student support platform and conversational intelligence system designed for **ABES Engineering College**. Grounded in the **ABES Complete Knowledge Corpus (v5.0)**, Campus-AI delivers zero-hallucination, citation-backed answers regarding admissions, academic fee structures, hostel allotments, placement records, department leadership, student grievance redressal (GRC), campus clubs, and institutional policies.

Campus-AI is designed with **Python (Flask, scikit-learn, TF-IDF, NumPy)** powering a custom, ultra-fast Neural Retrieval-Augmented Generation (RAG) engine, coupled with a frontend Single Page Application featuring glassmorphism aesthetics, responsive sidebars, interactive simulators, text-to-speech audio narration, and live citation inspection.

---

## 🛡️ Critical Data Quality & Integrity Guardrails
Campus-AI strictly enforces official ABES data policies:
1. **Strict Placement Year Separation:**
   - **Placements 2025 (Official Headline Benchmark):** **60 LPA** Highest Package, **1,692** Placement Offers.
   - **Placements 2025-26 (Placement Analytics Block):** **45 LPA** Highest Package (Amit Kumar, Clyromedia SDE-II), **1,289** Placement Offers, **489** Visiting Companies.
   - *Guardrail:* The engine **never merges** or conflates figures from different sessions.
2. **MBA Availability & Verification Protocol:**
   - Confirms MBA as an active academic program with an active ERP workflow (`https://erp.abes.ac.in/onlineEnquiryMBA/`), while responsibly withholding unverified public seat figures.
3. **Student Privacy Shield (Zero-PII):**
   - Automatically detects and rejects passwords, OTPs, student roll numbers, or personal phone numbers. Directs students to authentic college portals (`erp.abes.ac.in`, `nodues.abes.ac.in`).
4. **Historical vs Current Program Fidelity:**
   - Differentiates active 2026-27 programs (CSE 900, CSE-AIML 360, CSE-DS 180, ECE 180, ELCE 120, ME 60, BCA 120, MCA 180, M.Tech CSE 12, M.Tech ECE 6) from historical programs like standalone B.Tech IT.

---

## 🚀 Key Features

### 1. 💬 Flagship AI Chat Assistant
- **Verified Markdown Answers:** Formatted tables, bullet points, callouts, and key highlight metrics.
- **Collapsible Source Verification Cards:** Every answer links to exact chunk IDs (`[V5-FEE-001-C01]`, `[DEPT-001-C01]`), official verified URLs (`https://www.abes.ac.in/...`), and verified dates (`2026-10-01`).
- **Interactive Action Toolbar:** One-click copy, Text-to-Speech audio reader using browser Web Speech Synthesis, and user feedback thumbs-up.
- **Dynamic Follow-Up Chips:** Generates context-aware clickable prompts for effortless exploratory dialogue.
- **Voice Dictation:** Hands-free speech recognition input using the Web Speech API.

### 2. 🧮 2026-27 Interactive Fee Calculator & Receipt Simulator
- Itemized breakdown of the **₹181,200 base academic fee** (Tuition ₹110k, Career Planning ₹36k, Exam ₹9.6k, Tech Support ₹6k, Industry ₹6k, Book Bank ₹5k, Security ₹5k refundable, Reg ₹3.1k, Insurance ₹500).
- Real-time toggles for:
  - Official mandatory uniform set (**₹9,900**).
  - Hostel accommodation options (4-seater, triple, double; AC and non-AC).
  - Direct admission pre-enrollment slabs (₹500 / ₹1,000 / ₹1,150 / ₹2,300).
- Live printable invoice draft with payment method warnings (*No cash or cheque*).

### 3. 🏡 Hostel Room Allocator Matrix
- Full side-by-side pricing for **6 Boys' Hostels** and **2 Girls' Hostels** (₹136.5k to ₹177.5k).
- Policy cards detailing:
  - **AC operational timings:** 5:00 PM to 8:00 AM on working days; 24-hours on holidays.
  - **Laundry policy:** ₹3,500/year for up to 500 garments.
  - **Desert cooler rules:** Prohibited in girls' hostel; regulated in boys' hostel.
  - **Attached bathroom surcharge:** ₹10,000 shared among roommates.

### 4. 📊 Placement Analytics Dashboard
- Separate visual cards for **Placements 2025** vs **Placements 2025-26**.
- Star 2026 alumni spotlight:
  - **Amit Kumar** (CSE Data Science) → Clyromedia, 45 LPA (SDE-II).
  - **Supriya Pandey** (CSE) → Texas Instruments, 39 LPA (SDE).
  - **Yashika** (Computer Science) → Horizon X, 24.48 LPA (Trainee).
- Marquee recruiters badges: Google, Microsoft, Adobe, Atlassian, Goldman Sachs, TCS, Infosys, Accenture, Samsung.

### 5. 📚 Approved Programs & Intake Directory
- Searchable directory of all AICTE-approved undergraduate and postgraduate courses.
- Filter by degree (B.Tech, BCA, MCA, M.Tech) with approved seat intakes and entrance eligibility criteria.

### 6. ⚖️ Statutory Grievance Redressal Assistant (GRC / SGRC)
- Visual statutory workflow tracker:
  - **Stage 1:** Online filing routed to HOD.
  - **Stage 2:** HOD acknowledgment & solution report within **5 working days**.
  - **Stage 3:** Final GRC committee approval within **7 days**.
  - **Stage 4:** Appeal to Central Grievance Committee within **4 days** of HOD reply.
  - **Stage 5:** University case dispatch within **15 days**; external escalation to the **AKTU Ombudsperson**.
- **Instant Grievance Draft Generator:** Generates an official, reference-coded grievance letter ready for submission or printing.

### 7. 🏛️ Leadership & Department Directory
- Direct contact emails and roles for Chairman, Director, Deans (Dean Academics, Dean SW, Dean Admin), and Heads of Department across all engineering disciplines.

### 8. 🎭 Clubs & Student Life
- Detailed portfolios for 10+ student clubs: SDC (coding, 30 intake), Dataverse (AI/DS, 30 intake), Minerva (literary), Kalakrit (culture), Sports Club (Utsaaha & APL), Samvaad (theatre/Playhouse), Creative-U, Environ, MUN, and Spiritual & Yoga Society.

### 9. 🔍 Neural RAG Inspector
- Interactive drawer allowing students, evaluators, and faculty to inspect live chunk embeddings, cosine relevance percentages, category filters, and raw JSON metadata.

---

## 🛠️ Project Architecture

```
CampusAI/
├── app.py                      # Flask REST API server and template router
├── rag_engine.py               # Hybrid TF-IDF + Keyword neural retrieval & synthesis engine
├── run.py                      # Python launcher with automatic browser opening
├── run.bat                     # Windows single-click launcher
├── test_app.py                 # Comprehensive automated test suite
├── requirements.txt            # Python dependencies (Flask, scikit-learn, numpy, scipy)
├── data/
│   ├── knowledge_base.json     # Consolidated ABES topic records
│   ├── rag_chunks.json         # 54+ fine-grained cited chunks with source URLs
│   ├── build_kb.py             # Knowledge base generator script
│   └── build_rag_chunks.py     # RAG chunk compiler script
├── static/
│   ├── css/
│   │   └── styles.css          # Glassmorphism styling, responsive layout, animations
│   └── js/
│       └── app.js              # Reactive frontend controller, audio synthesizer, simulators
└── templates/
    └── index.html              # Modern, accessible Single Page Application
```

---

## ⚡ Quick Start & Execution

### Prerequisites
- Python 3.10+ (Standard Python runtime).
- Dependencies: `pip install -r requirements.txt` (Already installed in local environment: `flask`, `numpy`, `scikit-learn`, `scipy`).

### Running the Application

Option 1: Using Python Launcher (Automatically opens browser):
```bash
python run.py
```

Option 2: Using Windows Batch Script:
```cmd
run.bat
```

Option 3: Direct Flask Execution:
```bash
python app.py
```

Access the interface in your browser at:
👉 **`http://localhost:5000`**

### Running the Test Suite
To verify all 8 integration tests:
```bash
python test_app.py
```

Output:
```
[PASS] GET /: 200 OK (HTML loaded successfully)
[PASS] POST /api/chat (Fees): Verified answer with ₹181,200 and source citations
[PASS] POST /api/chat (Placements): Verified strict year separation (2025 60 LPA vs 2026 45 LPA)
[PASS] POST /api/chat (Privacy Guardrail): Credentials rejected, privacy warning delivered
[PASS] GET /api/fees: Verified 2026-27 total = ₹181,200
[PASS] GET /api/hostel: Verified boys and girls options
[PASS] POST /api/grievance-draft: Generated statutory draft with Reference ID & 5-day HOD clause
[PASS] GET /api/search?q=koha: Returned 8 matching chunks
[SUCCESS] ALL 8 INTEGRATION TESTS PASSED! Campus-AI is fully verified.
```

---

## 🌐 REST API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Serves the main Single Page Application |
| `POST` | `/api/chat` | RAG query processing with answer synthesis, sources, and follow-ups |
| `GET` | `/api/stats` | At-a-glance institutional metrics and verified date |
| `GET` | `/api/programs` | Approved academic courses, intake counts, and entrance exams |
| `GET` | `/api/fees` | Itemized academic fee breakdown and payment rules |
| `GET` | `/api/hostel` | Boys & girls hostel rooms, pricing, and operational rules |
| `GET` | `/api/placements` | 2025 vs 2025-26 statistics, star highlights, and recruiters |
| `GET` | `/api/directory` | Official contact directory for Deans and HODs |
| `GET` | `/api/clubs` | Campus societies, intake capacities, and recruitment cycles |
| `POST` | `/api/grievance-draft` | Generates official reference-coded grievance letter draft |
| `GET` | `/api/search?q=...` | Direct search into neural RAG chunk database |

---

## 🔒 Privacy & Compliance
Campus-AI complies with the **ABES Student Privacy Protocol v5.0**. It operates strictly with public institutional knowledge. Private authentication credentials (ERP passwords, SMS OTPs, University roll numbers) are guarded by client- and server-side interceptors that redirect users to authenticated HTTPS portal endpoints.
## Project Screenshot
<img width="1912" height="1031" alt="image" src="https://github.com/user-attachments/assets/b28f2056-757a-4e96-8a95-0389a4b6e990" />

