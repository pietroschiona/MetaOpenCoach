import json
import random
import uuid
import os
from datetime import datetime, timedelta

def get_iso_week(date):
    cal_date = date
    week_num_val = cal_date.isocalendar()[1]
    return f"{cal_date.year}-W{str(week_num_val).zfill(2)}"

def generate_mock_data():
    # Sanitized names (Pietro and generic)
    names = ["Pietro"] + [f"Atleta {i}" for i in range(1, 30)]
    
    emojis = ["🤾", "🏃", "💪", "⚡", "🏟️"]
    
    # German Handball Coaching Blocks
    coaching_blocks = [
        "Die Wurfkraft kommt aus der Rumpfstabilität. Achte auf deine Core-Spannung beim Sprungwurf.",
        "Deine Beinarbeit in der 6-0 Abwehr hat sich verbessert, aber die Antizipation muss schneller werden.",
        "Analysen zeigen, dass deine Sprungkraft nach der 40. Minute nachlässt. Intervalltraining ist nötig.",
        "Super Fokus beim Siebenmeter! Die Wurfkontrolle war heute perfekt.",
        "Denk an die Regeneration nach dem Harz-Training. Die Hautpflege der Hände ist wichtig.",
        "Wir arbeiten nächste Woche verstärkt an der Täuschung im Eins-gegen-Eins.",
        "Deine Herzfrequenzvariabilität deutet auf Ermüdung hin. Heute nur leichtes Wurftraining.",
        "Die Videoanalyse deines Stemmwurfs zeigt einen zu niedrigen Ellbogen. Korrigiere das im nächsten Satz."
    ]

    users = []
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    total_adherence = 0
    high_risk_count = 0
    active_count = 0
    
    for i in range(30):
        user_id = str(uuid.uuid4())
        name = names[i]
        user_emoji = random.choice(emojis)
        is_missing_checkin = (i % 5 == 0)
        
        profile = {
            "1_primärziel": str(random.randint(80, 100)),
            "2_aktuelle_leistung": f"Aktuelles technisches Niveau für {name} liegt bei ca. {random.randint(6, 9)}/10.",
            "3_trainingshistorie": f"{random.randint(2, 15)} Jahre Erfahrung im Handball.",
            "4_physischer_zustand": "Gute Ausdauer, starke Wurfarmmuskulatur.",
            "5_verletzungen": random.choices(["Keine.", "Schulterschmerzen.", "Sprunggelenk-Instabilität."], weights=[80, 10, 10])[0],
            "6_verfügbarkeit": "3-4 Einheiten pro Woche.",
            "7_ernährung_regeneration": "Ausgewogen, Fokus auf Proteine.",
            "8_trainingspräferenzen": "Intensive Wurfeinheiten.",
            "9_zusatztext": "Wettbewerbsorientiert.",
            "10_zusatztext": "Stabil."
        }
        
        # Weight/Performance History
        weight_history = []
        base_weight = random.uniform(70, 105)
        trend = random.uniform(-0.1, 0.1)
        days_to_fill = 366 if not is_missing_checkin else 359
        
        for d in range(0, days_to_fill, 7):
            entry_date = start_date + timedelta(days=d)
            current_weight = base_weight + (trend * (d/7)) + random.uniform(-0.5, 0.5)
            weight_history.append({
                "date": entry_date.strftime("%Y-%m-%d"),
                "weight": round(current_weight, 1),
                "bodyFat": round(random.uniform(12, 18), 1)
            })
            
        # Adherence History
        adherence_history = []
        user_sum_adherence = 0
        for d in range(0, days_to_fill, 7):
            entry_date = start_date + timedelta(days=d)
            week_id = get_iso_week(entry_date)
            planned = random.randint(3, 5)
            completed = random.randint(min(planned, 1), planned)
            ratio = completed / planned if planned > 0 else 1
            user_sum_adherence += ratio
            adherence_history.append({
                "week": week_id,
                "workouts_completed": completed,
                "workouts_planned": planned,
                "stressLevel": random.randint(1, 10),
                "sleepHours": round(random.uniform(6, 8.5), 1),
                "rpe": random.randint(5, 9)
            })
        
        avg_user_adherence = user_sum_adherence / len(adherence_history)
        total_adherence += avg_user_adherence
            
        # Chat History - Reduced size (15k tokens)
        chat_history = []
        current_token_estimate = 0
        target_tokens = 15000 
        chat_history.append({"role": "assistant", "content": f"Hallo {name}! Ich bin dein Handball-Coach. Bereit für die Session?", "timestamp": int(start_date.timestamp() * 1000)})
        
        msg_date = start_date + timedelta(hours=1)
        while current_token_estimate < target_tokens:
            role = "user" if len(chat_history) % 2 != 0 else "assistant"
            content = random.choice(coaching_blocks)
            token_count = len(content) // 4
            current_token_estimate += token_count
            chat_history.append({
                "role": role,
                "content": content,
                "timestamp": int(msg_date.timestamp() * 1000)
            })
            msg_date += timedelta(hours=random.randint(1, 48))
            if msg_date > end_date: break
        
        risk_level = "low"
        if i % 8 == 0: 
            risk_level = "high"
            high_risk_count += 1
        elif i % 5 == 0: 
            risk_level = "medium"
        
        if risk_level != "high": active_count += 1
        
        risk_factors = {
            "riskLevel": risk_level,
            "lastUpdate": weight_history[-1]["date"] + "T00:00:00.000Z",
            "trend": random.choice(["stable", "improving", "deteriorating"]),
            "adherenceScore": round(avg_user_adherence, 2),
            "progressScore": round(random.uniform(0.3, 0.9), 2),
            "engagementScore": 0.9,
            "predictedChurnDate": (end_date + timedelta(days=14)).strftime("%Y-%m-%d") if risk_level == "high" else None
        }
        
        users.append({
            "id": user_id,
            "name": name,
            "emoji": user_emoji,
            "createdAt": int((start_date + timedelta(days=random.randint(0, 30))).timestamp() * 1000),
            "profile": profile,
            "progressData": {
                "weightHistory": weight_history,
                "adherenceHistory": adherence_history
            },
            "riskFactors": risk_factors,
            "chatHistory": chat_history,
            "benchmarkProfile": {"initialWeight": weight_history[0]["weight"], "targetWeight": weight_history[0]["weight"] - 5}
        })
        
    db_content = {
        "settings": { "apiKey": "", "aiProvider": "lmstudio", "aiBaseUrl": "http://localhost:1234/v1", "aiModel": "qwen3.5-2b", "configDone": True },
        "users": users,
        "analytics": {
            "lastCalculation": int(datetime.now().timestamp() * 1000),
            "globalMetrics": { "totalClients": 30, "activeClients": active_count, "averageAdherence": round(total_adherence / 30, 2), "averageProgressRate": 0.65, "churnRate": round(high_risk_count / 30, 2) },
            "patterns": {}, "benchmarks": {}
        }
    }
    
    # --- SANITIZED RELATIVE PATH LOGIC ---
    current_dir = os.path.dirname(__file__)
    root_dir = os.path.join(current_dir, "..")
    dist_dir = os.path.join(root_dir, "examples", "software_examples", "Coach_of_Handball_Deutsch", "dist")
    target_path = os.path.join(dist_dir, "database.json")

    if os.path.exists(target_path):
        with open(target_path, "w", encoding="utf-8") as f:
            json.dump(db_content, f, indent=4)
        print(f"MOCK DATA OVERWRITTEN: {target_path}")
    else:
        print(f"SKIPPING: Target database not found at {target_path}")

if __name__ == "__main__":
    generate_mock_data()
