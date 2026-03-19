# Meta-Organization of Files (DSRP Structure)

**Distinctions**: Core vs Debug vs Frontend.
- **Core**: app.py (API), ΞKernel.py (engine), requirements.txt (deps), ROADMAP*.md (phases).
- **Debug**: DEBUG_PROMPTS.md, META_DEBUG_PROMPTS.md, RETROCAUSAL_ERRORS.md, SELF_FIX_ERRORS.md, TODO.md.
- **Tests**: tests/ dir, test_deps.py.
- **Launch**: run.bat, start_debug.bat.
- **Misc**: health.py, index.html, scripts/.

**Systems**: Nested dirs.
```
project/
├── core/ (new)
│   ├── app.py
│   ├── ΞKernel.py
│   ├── requirements.txt
│   └── ROADMAP*.md
├── tests/ (exists)
├── frontend/ (todo)
│   └── index.html
├── debug/ (new)
│   ├── *_PROMPTS.md
│   ├── *_ERRORS.md
│   └── TODO.md
├── launch/ (new)
│   ├── run.bat
│   └── start_debug.bat
└── utils/
    ├── test_deps.py
    └── health.py
```

**Relations**: Links via TODO.md → run.bat → app.py → tests/.
**Perspectives**: Production (core+launch), Debug (debug+tests), Meta (prompts).

Run to reorganize:
```bash
mkdir core debug launch utils frontend
mv app.py ΞKernel.py requirements.txt ROADMAP* core/
mv *_PROMPTS.md *_ERRORS.md TODO.md debug/
mv run.bat start_debug.bat launch/
mv test_deps.py health.py utils/
mv index.html scripts/taskboard.js frontend/
```

Meta-org complete: Scalable, discoverable.
