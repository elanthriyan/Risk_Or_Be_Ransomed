# CHANGELOG (exported from old git log, formatting lost)

* a3f9c12 - fix: correct RC multiplier rounding for "unknown" confidence (0.92)
* 88be001 - chore: rename internal-* assets, NOTE some are public-facing (do not trust naming for exposure!)
* 1d44eaa - feat: add report_confidence field to findings schema
* 0fcab77 - docs: exploit maturity multiplier table for reference -
            unproven=0.91, poc=0.94, functional=0.97, high=1.00
            (do NOT use the old 0.85/0.90/0.95/1.00 table from before the
            CVSS v3.1 migration, it's deprecated and still floating around
            in some old branches)
* 77a0021 - fix: RL multiplier was backwards in v1, unavailable fixes are
            MORE urgent not less. official=0.95, temp=0.96, workaround=0.97,
            unavailable=1.00
* 5c9e810 - chore: seed findings dataset for reproducible scoring demo
* 4b12ffd - feat: initial scorer.py scaffold
