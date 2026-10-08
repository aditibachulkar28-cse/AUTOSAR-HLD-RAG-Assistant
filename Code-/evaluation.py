import csv
from pathlib import Path
import pandas as pd
from .config import EVALUATION_DIR
from .rag_pipeline import answer_question

def run_evaluation(embedder, store):
    questions = pd.read_csv(EVALUATION_DIR / "evaluation_questions.csv")
    rows = []
    for _, item in questions.iterrows():
        result = answer_question(item.question, embedder, store)
        pages = {str(e["page"]) for e in result["evidence"]}
        expected = {p.strip() for p in str(item.expected_pages).split(",")}
        retrieval = bool(pages & expected)
        citation = "[Source:" in result["answer"]
        keywords = [w.lower() for w in str(item.expected_answer).split() if len(w) > 4]
        coverage = sum(w.strip(".,").lower() in result["answer"].lower() for w in keywords) / max(1, len(keywords))
        rows.append({"id":item.id,"question":item.question,"retrieval_success":retrieval,"citation_present":citation,"answer_keyword_coverage":round(coverage,2),"retrieved_pages":", ".join(sorted(pages)),"mode":result["mode"]})
    results = pd.DataFrame(rows)
    results.to_csv(EVALUATION_DIR / "evaluation_results.csv", index=False)
    metrics = {"questions":len(results), "retrieval_success_rate":results.retrieval_success.mean()*100, "citation_coverage":results.citation_present.mean()*100, "answer_coverage":results.answer_keyword_coverage.mean()*100}
    metrics["overall_score"] = (metrics["retrieval_success_rate"] + metrics["citation_coverage"] + metrics["answer_coverage"]) / 3
    (EVALUATION_DIR / "evaluation_summary.md").write_text("# Evaluation Summary\n\nGenerated after running the evaluation. These are prototype retrieval and keyword metrics, not human-quality measurements.\n\n" + "\n".join(f"- **{k.replace('_',' ').title()}**: {v:.1f}" if isinstance(v,float) else f"- **{k.title()}**: {v}" for k,v in metrics.items()), encoding="utf-8")
    return metrics
