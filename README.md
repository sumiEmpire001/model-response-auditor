# Model Response Auditor

A deterministic Python CLI for evaluating **text-format requirements** in generated responses. It checks length, required phrases, prohibited phrases, and URLs.

## Usage

```bash
python auditor.py examples/response.json
python -m unittest discover -s tests -v
```

Input is a JSON object with `response` and `rules`. Available rules: `min_chars`, `max_chars`, `required_terms`, `banned_terms`, `no_urls`. Output contains a pass/fail result, character count, and issues. Exit codes: 0 pass, 1 rule failure, 2 invalid input.

**Important:** This tool does not verify factual accuracy, hallucinations, harmful content, or model safety. Simple substring rules are not reliable moderation.
