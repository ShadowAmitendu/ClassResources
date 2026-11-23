# Codebase Audit

Audit date: November 23, 2026

## Remediation status

All findings below are resolved or have implementation-level guards. The codebase should be re-audited after future dependency or data-layout changes.

## Findings

### High

1. **Future semesters are hardcoded to placeholder states**
   - Evidence: [index.html](/C:/Users/amite/Development/ClassResources/index.html), `load()`: only 6th and 7th are allowed to load JSON.
   - Impact: Adding content to 1st–5th or 8th under `bca/semesters/` will not display it.
   - Remediation: **Resolved:** load any existing `bca/data/<semester>.json` file dynamically and show a placeholder only when the index is unavailable.

2. **Bulk ZIP paths can be constructed incorrectly**
   - Evidence: [index.html](/C:/Users/amite/Development/ClassResources/index.html), `downloadAll()`: it derives a ZIP path from `parts.indexOf("semesters")`.
   - Impact: A malformed or relocated path can produce `-1 + 2 = 1`, changing or omitting ZIP directory structure.
   - Remediation: **Resolved:** guard `semesterIndex >= 0` and reject empty archive paths.

### Medium

3. **Generated indexes are not removed for deleted semester folders**
   - Evidence: [generate.py](/C:/Users/amite/Development/ClassResources/generate.py), `generate()`: only writes indexes; it does not remove stale JSON files.
   - Impact: A removed semester directory can leave an obsolete JSON index behind.
   - Remediation: **Resolved:** remove JSON files whose semester folder no longer exists.

4. **Theme initialization accepts invalid saved values**
   - Evidence: [index.html](/C:/Users/amite/Development/ClassResources/index.html), theme initialization: `saved` is assigned directly to `data-theme`.
   - Impact: Corrupt or unexpected local storage values can produce an unstyled or inconsistent theme.
   - Remediation: **Resolved:** accept only `light` or `dark`; fall back to system preference otherwise.

5. **Dynamic resource URLs are not HTML-attribute escaped**
   - Evidence: [index.html](/C:/Users/amite/Development/ClassResources/index.html), `renderItems()`: `item.url` and `item.path` are inserted directly into HTML.
   - Impact: A filename containing quotes or special characters could break markup or create unintended attributes.
   - Remediation: **Resolved:** resource URLs are escaped for HTML attribute context.

### Low

6. **External JS dependencies lack Subresource Integrity**
   - Evidence: [index.html](/C:/Users/amite/Development/ClassResources/index.html), JSZip and FileSaver CDN script tags.
   - Impact: CDN compromise or unexpected script replacement could execute third-party code.
   - Remediation: **Resolved:** JSZip and FileSaver are vendored locally in `vendor/`.

7. **Mobile footer hides the author and hosted text**
   - Evidence: [style.css](/C:/Users/amite/Development/ClassResources/style.css), the mobile footer media rule hides `.footer-hosted` and `.footer-author`.
   - Impact: Attribution and the personal website link disappear on small screens.
   - Remediation: **Resolved:** keep hosted, author, and timestamp content in a compact three-column mobile footer.
