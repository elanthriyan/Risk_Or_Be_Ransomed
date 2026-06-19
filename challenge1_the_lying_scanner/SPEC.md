# Risk Scoring Spec (partial — recovered from old wiki export)

Our scoring engine combines CVSS base score with temporal metrics and
asset exposure to produce a final priority score. Some sections of this
doc were lost when we migrated wikis. What survives:

## Temporal multiplier

`temporal_score = cvss_base * E * RL * RC`

Where E, RL, RC are multipliers driven by the CVSS v3.1 temporal metric
group:

- **E (Exploit Code Maturity)** — higher confidence/availability of a
  working exploit should produce a HIGHER multiplier (closer to 1.0).
  Four levels exist in our findings data, ordered from least to most
  mature exploit availability. (Exact numeric table missing from this
  export — check commit history / CHANGELOG, an earlier engineer
  documented it in a commit message before the wiki migration.)

- **RL (Remediation Level)** — a finding with NO fix available should be
  scored as MORE urgent than one with an official patch already
  released. i.e. RL multiplier should be highest when remediation is
  "unavailable" and lowest when an "official fix" exists.

- **RC (Report Confidence)** — confirmed findings should weigh more than
  unconfirmed/unknown ones.

## Exposure weighting

`final_score = temporal_score * exposure_weight`

Exposure weight reflects whether the asset is internet-facing. **This
must come from the asset inventory's ground-truth `internet_facing`
field** — asset *names* in our environment are not a reliable signal
(we have internet-facing assets that were misleadingly named during a
legacy migration, e.g. several "internal-*" named hosts are actually
public-facing edge services).

## Output

Findings are ranked descending by final_score. Ties broken by finding
ID ascending. The top 5 IDs, joined by commas, are the artifact that
matters for risk sign-off.
