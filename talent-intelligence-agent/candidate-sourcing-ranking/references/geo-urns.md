# LinkedIn location codes (geoUrn)

A wrong geoUrn silently returns zero results, so only codes verified in a live search are listed. When a run resolves a new one, add it here with the date.

| Location (as LinkedIn names it) | geoUrn | Verified |
|---|---|---|
| San Francisco Bay Area | 90000084 | 2026-09-29 |
| Greater Boston | 90000007 | 2026-06-10 |

## Resolving a new location

1. Open a people search with one plain keyword, for example `https://www.linkedin.com/search/results/people/?keywords=recruiter`.
2. Open the **Locations** filter, type the metro, select it, and click Show results.
3. Read the `geoUrn` value out of the resulting URL.
4. Confirm the first page of results shows people in that location.
5. Add the row above.

URL pattern for searches:
`https://www.linkedin.com/search/results/people/?keywords=<URL-encoded phrase>&geoUrn=%5B%22<geoUrn>%22%5D&origin=FACETED_SEARCH&page=<n>`

Remote or national searches: leave `geoUrn` out, or use the country code once it is verified.
