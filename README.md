# Epistemic Type System for Agents

Runtime layer that tracks **how** each piece of information is known and enforces rules so uncertain or inferred content is not presented as fact.

This repository is built incrementally. **Phase 1** introduces the core data model (`Claim`, epistemic types, sources). Later phases add classification, rules, memory, formatting, and the full pipeline.

## Install (development)

```bash
pip install -e ".[dev]"
```

Python 3.10+.
