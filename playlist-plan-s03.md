# SLCV S3 Playlist Plan — FINAL

**Built:** 2026-05-02 (deep hunt completed; nothing further to find on YouTube)
**Tooling:** [scripts/yt_make_playlist.js](../hub/scripts/yt_make_playlist.js)
**Status:** Ready to ship. The script is pre-patched with Block A (`hub/scripts/yt_make_playlist.js`).

## TL;DR

After exhaustive YouTube search across 8 channels + ID-pattern sweep + episode-keyword search + duration filtering — **only 3 of 6 S3 episodes exist as full uploads on YouTube. The other 3 do not. This is now a verified ceiling.**

## Per-episode status (final)

| Ep | Title | Best YT ID | Length | Source | Status |
|---|---|---|---|---|---|
| **S3E1** | Shilbottle | `7XpvH-j9BHg` | 1:46 | BBC official preview | **No full ep on YT** — exhaustively searched |
| | | `TvHlD7Lg5x0` | 2:18 | Sublimate (routine clip) | |
| **S3E2** | England | `nVk1VGAl7p4` | 12:27 | BBC official | **NOTE: this is S2E2 not S3E2.** Iannucci was S2 interrogator. No good S3E2 surrogate exists. |
| | | `x_TA-X-pMPk` | (full) | unknown | **BBC-blocked outside UK** |
| **S3E3** | Satire | `hLSBxu7njjI` | 28:46 | Ian Kenny | ✅ FULL EPISODE |
| | | `lQAJFVV_h-U` | 2:17 | BBC official preview | |
| | | `id2SNd6HnC8` | 3:05 | Stewart Lee Official | |
| **S3E4** | Context | `6T4P-Fu2Cfo` | 2:02 | BBC official preview | **No full ep on YT** — exhaustively searched |
| | | `2OLXzO1oK2w` | 5:36 | 'consumer' (routine excerpt: Context-free words) | NEW FIND |
| **S3E5** | London | `P0xqBAzVJtc` | 27:46 | Ian Kenny | ✅ FULL EPISODE |
| **S3E6** | Marriage | `uyUskabZ-cY` | 29:10 | Ian Kenny | ✅ FULL EPISODE |

## Correction to earlier plan

The previous version of this file claimed **Iannucci was the S3E2 interrogator**. That was wrong. Per `slcv-transcripts/transcripts/`:
- **Series 2** interrogator: Armando Iannucci (all 6 eps)
- **Series 3** interrogator: Chris Morris (all 6 eps)
- **Series 4** interrogator: Chris Morris (all 6 eps)

The two BBC official "Stewart Lee Talks to Armando Iannucci" clips (`nVk1VGAl7p4` ep 2, 12:27 and `eDRjVwxG9BA` ep 4, 8:34) are **from Series 2, not Series 3**. They're great Comedy Vehicle context but don't belong in an S3-only playlist. Dropped from Block A; available for the Comedy Vehicle Companion (full-show) playlist.

## What was searched (proof of exhaustion)

1. YouTube history DB — every Lee watch since 2016. Verified durations on all 50+ IDs.
2. Ian Kenny full channel scrape (66+ uploads). Comedy Vehicle uploads: Tory Safari Park (S3E3), Boris Johnson (S3E5), Hogwort's Bukkake (S3E6), Dead Mouse (S4E4), Migrant Crisis (S4E5), Jeremy Corbyn (S4E3), Religion, Democracy, Television, Toilet Books, Behind The Wheel, Chris Moyles, The BBC, Franklin Ajaye, Henning Wehn, Financial Crisis, Political Correctness, Muslims & Jews, Girls With Big Breasts. **No S3E1, E2, or E4 full episodes.**
3. L LL channel scrape: only Series 1 episodes 1, 2, 3. **No S3 material.**
4. Comedy Without Errors, The Media Garage, Sublimate, Jimmy Lee, Fucking Duck, KeyboardKramer, Lord Lew — all Lee-related but only routine clips, no full S3 episodes.
5. ID-pattern sweep: William Ham uses `slcv0XYZ` codes but only for Series 4 (slcv0406 = Childhood). No S3 IDs in this naming convention found.
6. Direct YouTube search for episode-content keywords: "imaginary wives" (S3E4), "context free word" (S3E4), "taxi driver England" (S3E2), "internet pornography" (S3E1), "shilbottle full" — surfaced nothing new beyond the clips already cataloged.
7. Web search for Apple TV / streaming alternatives: Apple TV (UK) carries all six. stewartlee.co.uk sells the Series 3 DVD/download.

## Final ready-to-ship playlist (Block A)

The `hub/scripts/yt_make_playlist.js` file has been pre-patched with this. To run: paste into Safari Web Inspector while signed into YouTube on a real video page.

```javascript
const TITLE = "Stewart Lee's Comedy Vehicle — Series 3 (best of YouTube)";
const PRIVACY = "PUBLIC";
const VIDEO_IDS = [
  "7XpvH-j9BHg", // S3E1 BBC preview · "Stewart Lee vs The Internet" · 1:46 (no full ep on YT)
  "TvHlD7Lg5x0", // S3E1 routine clip · Sublimate "Shilbottle" · 2:18
  // S3E2 England — full ep BBC-geo-blocked, no surrogate dropped here
  "lQAJFVV_h-U", // S3E3 BBC preview · "End of Planet of the Apes" · 2:17
  "hLSBxu7njjI", // S3E3 FULL · Ian Kenny "Tory Safari Park" · 28:46
  "id2SNd6HnC8", // S3E3 highlight · Stewart Lee Official "Satire" · 3:05
  "6T4P-Fu2Cfo", // S3E4 BBC preview · "The best local school" · 2:02
  "2OLXzO1oK2w", // S3E4 routine excerpt · "Context-free words" · 5:36 (no full ep on YT)
  "P0xqBAzVJtc", // S3E5 FULL · Ian Kenny "Boris Johnson" · 27:46
  "uyUskabZ-cY", // S3E6 FULL · Ian Kenny "Hogwort's Bukkake" · 29:10
];
```

**To run:**
1. Open Safari, sign into YouTube, navigate to any video page (NOT a "playlist not found" error page).
2. Develop menu → Show JavaScript Console.
3. Paste contents of `hub/scripts/yt_make_playlist.js` into the console → return.
4. Playlist appears in Library → Playlists.

## Bonus material (separate playlist candidates)

For a future "Comedy Vehicle Full Companion" playlist, beyond S3:
- **S1 (full eps from L LL):** `hJ8_mC7Iv5k` (S1E1, 27:43), `5veC7bpVmSA` (S1E2, 28:44), `bwJBfGReuE4` (S1E3, 28:25). No S1E4–E6 found.
- **S2 (Iannucci-as-interrogator):** `nVk1VGAl7p4` (Iannucci ep 2, 12:27 BBC official), `eDRjVwxG9BA` (Iannucci ep 4, 8:34 BBC official). No full S2 eps surfaced from this hunt (Ian Kenny has many S2 routine excerpts but not full episodes).
- **S2 Red Button Extras:** `YAYiVm8sEq8` (1:19:34 by AshCash147).
- **S1 Red Button Extras:** `EvTAHVCRtzM` (1:11:39 by AshCash147), `1nJvUj60XC8` (1:09:44 by GoodWater).
- **S4 (full eps from Ian Kenny):** `2b9eRI-WRgU` (S4E3 Patriotism, 28:18), `QXiiq1EUr7Q` (S4E4 Death, 29:08), `L-tQrcYOpvQ` (S4E5 Migrants, 28:32), `lcDh5p6N4SQ` (S4E6 Childhood, 29:49), `qljGMw9ES2w` (S4E6 alternate by William Ham as "slcv0406", 29:49). **No S4E1 or S4E2 surfaced.**

## Local possession

All 6 S3 episodes are already on disk as 720p HDTV mkv at `slcv-transcripts/media/videos/`. The YouTube playlist is the public-facing artifact.
