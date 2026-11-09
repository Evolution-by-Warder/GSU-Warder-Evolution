# GitHub Releases – retention and safe cleanup

Status as of 2026-11-09. This policy is part of the cross-project Warder release hygiene programme. **It does not authorize blind automatic deletions.**

## Inventory
- Repository: `Evolution-by-Warder/GSU-Warder-Evolution`
- Observed GitHub Releases: **10**
- Latest observed tag: `v13.41-r4`

## Policy
1. Keep at least the **five most recent stable production releases** in each actively distributed project, plus specifically identified historical milestones and any supported rollback version.
2. Keep **every release currently referenced** by an updater, feed, installer, plugin catalog, README, documentation, published package manifest or an active user-facing URL, regardless of age.
3. Identify stale TEST/RC builds separately; never count them as production rollback releases. A candidate can be removed only after its source and test evidence are retained and all relevant refs have been checked.
4. Before removing a Release or its asset, inventory versions/tags/URLs and run repository-wide searches for references, validate that a currently supported installed version can still update or reinstall, and preserve a verified recovery copy.
5. Deletion of a GitHub Release, deletion of an asset and deletion of a Git tag are **separate operations**. Never rewrite release artifacts or silently remove tags. Record actions and exact identifiers in the project progress register.
6. Apply the policy after each new stable publication and periodically review accumulated TEST assets. Publishing automation must not delete previous versions as a side effect.

## Pending cleanup

The existing 10 Releases are **inventory only**, not a reviewed deletion list. First check all live updater URLs and installation dependencies, then produce an explicit keep/remove manifest. Do not delete any Release until that manifest has been validated.


## Cross-project scope
Apply the same release hygiene process in FullHDGlass, PiconHub, GSU and Warder Radio. Exempt backup/archival snapshots from generic pruning. The aim is to keep release history readable without breaking installations or update feeds.
