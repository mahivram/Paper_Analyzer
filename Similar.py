import os
from rapidfuzz import fuzz
from collections import defaultdict

no_que = 25  # Top N most repeated questions

def load_all_questions(folder):
    all_questions = []
    for filename in os.listdir(folder):
        if filename.endswith("_cleaned.txt"):
            path = os.path.join(folder, filename)
            with open(path, "r", encoding="utf-8") as f:
                questions = [q.strip() for q in f.read().split("\n") if q.strip()]
                for q in questions:
                    all_questions.append((q, filename))
    return all_questions

def group_similar_questions(questions, threshold=85):
    groups = []
    used = set()

    for i, (q1, file1) in enumerate(questions):
        if i in used:
            continue
        group = [(q1, file1)]
        used.add(i)
        for j in range(i + 1, len(questions)):
            q2, file2 = questions[j]
            if j in used:
                continue
            score = fuzz.ratio(q1.lower(), q2.lower())
            if score >= threshold:
                group.append((q2, file2))
                used.add(j)
        groups.append(group)
    return groups

def display_top_groups(groups, top_n=no_que):
    print("\n📊 Top Repeated Questions:")
    sorted_groups = sorted(groups, key=len, reverse=True)

    top_questions = []

    for i, group in enumerate(sorted_groups[:top_n]):
        print(f"\n🔁 Q{i+1} (Appears {len(group)} times):\n{group[0][0]}")
        files = [f for _, f in group]
        print(f"   ↳ Found in: {', '.join(sorted(set(files)))}")
        top_questions.append(group[0][0])  # Take representative question

    # Save top questions to file
    with open("important_questions.txt", "w", encoding="utf-8") as out:
        for q in top_questions:
            out.write(q + "\n")

    print(f"\n✅ Saved {len(top_questions)} important questions to important_questions.txt")

