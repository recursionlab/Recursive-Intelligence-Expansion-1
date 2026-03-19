#!/usr/bin/env python3
\"\"\"Document search/filter for RIEM{} codebase.
Search by title/date/status across .md files. Recursive from current dir.\"\"\"

import os
import argparse
import re
from datetime import datetime
from pathlib import Path

def find_docs(path='.', recursive=True):
    \"\"\"Find all .md files.\"\"\"
    pattern = '**/*.md' if recursive else '*.md'
    return list(Path(path).rglob(pattern) if recursive else Path(path).glob(pattern))

def parse_metadata(file_path):
    \"\"\"Extract title/date/status from frontmatter or content.\"\"\"
    content = Path(file_path).read_text()
    
    # Frontmatter title/date
    fm_match = re.search(r'---\\ntitle: (.*?)\\ndate: (\\d{4}-\\d{2}-\\d{2})', content, re.DOTALL)
    if fm_match:
        title, date_str = fm_match.groups()
        status = 'analyzed' if 'status: analyzed' in content else 'pending'
        return title.strip(), date_str, status
    
    # Fallback: first H1, last mod date
    h1_match = re.search(r'^# (.*)$', content, re.MULTILINE)
    title = h1_match.group(1).strip() if h1_match else file_path.name
    date = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d')
    status = 'pending'  # Default
    
    return title, date, status

def search_docs(query, docs):
    \"\"\"Simple text search + filter.\"\"\"
    results = []
    for doc in docs:
        title, date, status = parse_metadata(doc)
        content = Path(doc).read_text()
        if (query.lower() in title.lower() or 
            query.lower() in content.lower() or
            query in date):
            results.append({
                'path': str(doc.relative_to(Path.cwd())),
                'title': title,
                'date': date,
                'status': status
            })
    return results

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='RIEM{} Doc Search')
    parser.add_argument('query', help='Search term')
    parser.add_argument('--path', default='.', help='Search path')
    parser.add_argument('--title-only', action='store_true')
    parser.add_argument('--status', help='Filter status')
    args = parser.parse_args()
    
    docs = find_docs(args.path)
    results = search_docs(args.query, docs)
    
    print(f'Found {len(results)} docs:')
    for r in results:
        print(f"- {r['path']} ({r['title']}, {r['date']}, {r['status']})")

