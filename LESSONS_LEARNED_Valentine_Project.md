# Project Retrospective: Valentine Horror Compilation
**Date:** 2026-02-14  
**Status:** Completed (with issues)  
**Duration:** ~6 hours (estimated 2 hours)

---

## 🎯 What We Built
- 10 Valentine horror stories compiled into one video
- Epic intro with DALL-E 3 generated image
- Final video: 97 MB, 22 minutes, with audio

---

## ✅ What Worked

1. **Dashboard created** - Cost tracking system operational
2. **10 stories collected** - 7 original + 3 extra
3. **Intro with narration** - Using OpenAI TTS (onyx voice)
4. **Final video exported** - Successfully concatenated

---

## ❌ What Didn't Work

### 1. Missing Elements in Final Video
| Element | Status | Why | Fix for Next Time |
|---------|--------|-----|-------------------|
| Heartbeat between stories | ❌ Missing | Not included in concat list | Add explicit step: "Insert heartbeat_X.mp4 between each story" |
| 60 min rain ending | ❌ Missing (only ~4 min) | Wrong file used (test file) | Use `ls -lh` to verify file size before concat |
| Story 6 | ❌ Missing | Corrupted/missing file | Validate all story files exist with `test -f` before concat |

### 2. Audio Issues
| Issue | Root Cause | Prevention |
|-------|-----------|------------|
| Intro initially silent (-91 dB) | Used `anullsrc` instead of actual TTS | Always use OpenAI TTS or Edge TTS, never synthetic silence |
| Rain volume too low | Wrong audio generation method | Test with `ffmpeg -af volumedetect` before adding to concat |

### 3. Process Problems
| Problem | Impact | Solution |
|---------|--------|----------|
| Time estimate off by 3x | Frustration, rushed ending | Always multiply estimate by 3x for safety |
| Process killed 4+ times | Lost progress, had to restart | Use smaller batch operations, checkpoint frequently |
| Side distractions (MiniMax, AR glasses) | Lost 2+ hours | Say NO to new tasks mid-project |
| Didn't push to Git | No backup, no version history | Push after EACH major milestone |
| Didn't verify final output | Missing elements discovered late | Create validation checklist |

---

## 📋 Validation Checklist (for future projects)

### Before Concat:
- [ ] All story files exist (`ls story_*.mp4 | wc -l`)
- [ ] All files have audio (test with `volumedetect`)
- [ ] All files same format (1920x1080, 30fps, AAC 48000Hz stereo)
- [ ] Intro has audible narration (> -40 dB)
- [ ] Rain file is actually 60 minutes (check file size)
- [ ] Heartbeat files exist and have audio

### After Concat:
- [ ] Final video plays without errors
- [ ] Audio present throughout (`ffprobe` check)
- [ ] Duration matches expected (10 stories × ~3 min = ~30 min + 60 min rain = ~90 min)
- [ ] All segments visible in timeline
- [ ] No silent sections except intentional

---

## 🎯 Key Lessons

1. **Test audio levels ALWAYS** - Don't assume, verify with `volumedetect`
2. **Check file sizes** - 4MB ≠ 60 minutes of video
3. **One task at a time** - No side quests (MiniMax, AR glasses, etc.)
4. **Push to Git frequently** - After each working component
5. **Overestimate time** - Always 3x initial estimate
6. **Follow the flow** - Don't skip steps or improvise
7. **Validate outputs** - Checklist before saying "done"

---

## 🔧 Optimized Flow for Next Time

```
Step 1: Generate 8 stories
   ↓ Validate: Each story 900-1400 words
   
Step 2: Generate narration for all 8
   ↓ Validate: Audio files > 100KB, test playback
   
Step 3: Generate DALL-E images (5 per story)
   ↓ Validate: 40 images total, check quality
   
Step 4: Create individual videos
   ↓ Validate: 8 MP4s, each with audio
   
Step 5: Create intro + outro
   ↓ Validate: Intro has audible narration
   
Step 6: Standardize all to same format
   ↓ Validate: All 1920x1080, 30fps, AAC 48000Hz
   
Step 7: Create heartbeat transitions
   ↓ Validate: 7 heartbeat files with audible sound
   
Step 8: Create 60 min rain
   ↓ Validate: File size > 50MB, duration 3600s
   
Step 9: Concatenate in order
   Order: Intro → Story 0 → Heartbeat → Story 1 → Heartbeat → ... → Rain
   ↓ Validate: Final duration ~90 min
   
Step 10: Final validation
   - Play first 30 seconds
   - Check middle section
   - Check rain section exists
   - Push to Git
```

---

## 📝 Action Items

- [ ] Write validation functions in Python
- [ ] Create `validate_video.py` script
- [ ] Push current code to GitHub
- [ ] Document flow in README
- [ ] Test optimized flow on 1 story before 8-story batch

---

## 💭 Personal Reflection

I need to:
1. Be more honest about time estimates
2. Say no to distractions
3. Test outputs rigorously
4. Push to Git after each milestone
5. Follow checklists, don't wing it

**Next project:** Appalachian Trail stories  
**Must do:** Use this checklist, no exceptions.
