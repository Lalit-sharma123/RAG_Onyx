from ingestion.loader import load_documents


def load_all_sources():
    docs = []

    docs.extend(load_documents())  # includes PDFs now

    # mock connectors
    docs.extend(["Slack message example"])
    docs.extend(["Google Drive doc example"])

    return docs