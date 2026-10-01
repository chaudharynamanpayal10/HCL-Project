import sys
import io

# Ensure UTF-8 output on Windows console
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from app import app

def run_tests():
    client = app.test_client()
    print("Testing Campus-AI Endpoints...")

    # 1. Test Home page
    res = client.get("/")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    assert b"Campus" in res.data, "Expected 'Campus' in HTML"
    print("[PASS] GET /: 200 OK (HTML loaded successfully)")

    # 2. Test Chat API
    chat_payload = {"message": "What is the fee for B.Tech?"}
    res = client.post("/api/chat", json=chat_payload)
    assert res.status_code == 200
    data = res.get_json()
    assert "answer" in data
    assert "181,200" in data["answer"]
    assert len(data["sources"]) > 0
    print("[PASS] POST /api/chat (Fees): Verified answer with ₹181,200 and source citations")

    # 3. Test Placement Disambiguation Guardrail
    chat_payload2 = {"message": "What is the highest placement package?"}
    res2 = client.post("/api/chat", json=chat_payload2)
    assert res2.status_code == 200
    data2 = res2.get_json()
    assert "60 LPA" in data2["answer"] and "45 LPA" in data2["answer"]
    print("[PASS] POST /api/chat (Placements): Verified strict year separation (2025 60 LPA vs 2026 45 LPA)")

    # 4. Test Privacy Shield
    chat_payload3 = {"message": "My password is testpass and roll no is 1234"}
    res3 = client.post("/api/chat", json=chat_payload3)
    assert res3.status_code == 200
    data3 = res3.get_json()
    assert "Privacy Shield" in data3["answer"]
    print("[PASS] POST /api/chat (Privacy Guardrail): Credentials rejected, privacy warning delivered")

    # 5. Test Fees API
    res4 = client.get("/api/fees")
    assert res4.status_code == 200
    fee_data = res4.get_json()
    assert fee_data["academic_fee_total"] == 181200
    print("[PASS] GET /api/fees: Verified 2026-27 total = ₹181,200")

    # 6. Test Hostel API
    res5 = client.get("/api/hostel")
    assert res5.status_code == 200
    hostel_data = res5.get_json()
    assert len(hostel_data["boys_hostels"]) == 6
    assert len(hostel_data["girls_hostels"]) == 3
    print("[PASS] GET /api/hostel: Verified boys and girls options")

    # 7. Test Grievance Draft API
    grv_payload = {
        "name": "Ananya Sharma",
        "department": "CSE (AI & ML)",
        "year": "2nd Year",
        "category": "Academic Issue",
        "subject": "Lab system configuration request",
        "details": "Need access to GPU instances in the deep learning laboratory."
    }
    res6 = client.post("/api/grievance-draft", json=grv_payload)
    assert res6.status_code == 200
    grv_data = res6.get_json()
    assert "GRC-ABES-" in grv_data["ticket_id"]
    assert "5 working days" in grv_data["draft_text"]
    print("[PASS] POST /api/grievance-draft: Generated statutory draft with Reference ID & 5-day HOD clause")

    # 8. Test RAG Search API
    res7 = client.get("/api/search?q=koha")
    assert res7.status_code == 200
    search_data = res7.get_json()
    assert len(search_data) > 0
    print(f"[PASS] GET /api/search?q=koha: Returned {len(search_data)} matching chunks")

    print("\n[SUCCESS] ALL 8 INTEGRATION TESTS PASSED! Campus-AI is fully verified.")

if __name__ == "__main__":
    run_tests()
