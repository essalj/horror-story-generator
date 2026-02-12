# Horror Story Generator - Cleanup Plan

## Store filer der kan fjernes (1.4GB+)
- [ ] generated_stories/ (969MB) - behold kun eksempler
- [ ] effects/ (423MB) - beholde eller flytte til assets repo
- [ ] temp_concatenated_music.mp3 (34MB) - temp fil
- [ ] __pycache__/ (292K) - kan regenereres

## Gamle/backup filer med _ prefix
- [ ] __old__flow_01_openrouter.py
- [ ] _1_create_compilation_from_files.py
- [ ] _adhoc_splittging mp4 and adding music.py
- [ ] _test_run_story.py
- [ ] _x_core_mp4_creation.py
- [ ] _x_mp4_creation_script.py
- [ ] _xgpt5_upload_to_yt.py

## Organisering
```
horror-story-generator/
├── README.md
├── requirements.txt
├── .env.example
├── src/
│   ├── flows/           # Hoved flows
│   ├── tools/           # Utility tools
│   ├── services/        # Services
│   └── core/            # Core funktionalitet
├── prompts/             # Prompt bibliotek
├── assets/              # Billeder, lyd, etc.
└── examples/            # Eksempel outputs
```

## Aktive Python filer (beholdes)
- flow_0b_short_story_gen_assistants.py (90KB - hovedfil)
- flow_1_orchestrator.py
- flow_1_get_story_from_open_router.py
- tools_*.py (alle tools)
