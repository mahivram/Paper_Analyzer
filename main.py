from TextExtracter import extract_text_from_all_pdfs
from Cleaner import process_all_texts
from Similar import load_all_questions, group_similar_questions, display_top_groups
from Topics import load_important_questions, tag_and_print_topics

def main():
    folder_path = "./papers"  # Folder containing PDF files
    extract_text_from_all_pdfs(folder_path)

    process_all_texts()

    folder = "clean_questions"  # Folder with cleaned questions
    questions = load_all_questions(folder)
    groups = group_similar_questions(questions)
    display_top_groups(groups)

    important_questions = load_important_questions("important_questions.txt")
    if important_questions:
        tag_and_print_topics(important_questions)

if __name__ == "__main__":
    main()
