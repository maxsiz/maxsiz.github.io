#!/usr/bin/env python3
"""Pull a traffic report for iber.dev from GA4 and Search Console.

Writes markdown to stdout, or to codex/reports/ with --write.

Credentials
-----------
A service account with Viewer on the GA4 property and on the Search Console
property. Point GOOGLE_APPLICATION_CREDENTIALS at its JSON key -- never commit
the key. The GA4 numeric property id goes in GA4_PROPERTY_ID.

    export GOOGLE_APPLICATION_CREDENTIALS=/path/to/key.json
    export GA4_PROPERTY_ID=123456789
    python3 codex/scripts/ga4_report.py --days 7

Standard GA4 reports lag 24-48h, so a run is only meaningful for periods that
ended at least a day ago. That is why the default window ends yesterday.
"""

import argparse
import datetime as dt
import os
import sys
from pathlib import Path

SITE_URL = os.environ.get("GSC_SITE_URL", "sc-domain:iber.dev")
PROPERTY_ID = os.environ.get("GA4_PROPERTY_ID", "")
TARGET_QUERIES = [
    "ethereum smart contract development",
    "smart contract audit",
    "blockchain r&d team",
    "web3 development company",
]


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def date_range(days):
    end = dt.date.today() - dt.timedelta(days=1)
    return end - dt.timedelta(days=days - 1), end


def table(headers, rows):
    if not rows:
        return "_no data_\n"
    out = ["| " + " | ".join(headers) + " |",
           "|" + "|".join(["---"] * len(headers)) + "|"]
    for row in rows:
        out.append("| " + " | ".join(str(c) for c in row) + " |")
    return "\n".join(out) + "\n"


def ga4_section(start, end):
    try:
        from google.analytics.data_v1beta import BetaAnalyticsDataClient
        from google.analytics.data_v1beta.types import (
            DateRange, Dimension, Metric, RunReportRequest,
        )
    except ImportError:
        fail("google-analytics-data not installed, see codex/scripts/requirements.txt")

    if not PROPERTY_ID:
        fail("GA4_PROPERTY_ID is not set")

    client = BetaAnalyticsDataClient()
    window = [DateRange(start_date=str(start), end_date=str(end))]

    def run(dimensions, metrics, limit=10):
        request = RunReportRequest(
            property=f"properties/{PROPERTY_ID}",
            date_ranges=window,
            dimensions=[Dimension(name=d) for d in dimensions],
            metrics=[Metric(name=m) for m in metrics],
            limit=limit,
        )
        response = client.run_report(request)
        return [[v.value for v in row.dimension_values] + [v.value for v in row.metric_values]
                for row in response.rows]

    parts = ["## Google Analytics 4\n"]

    totals = run([], ["sessions", "totalUsers", "screenPageViews"])
    parts.append("### Totals\n")
    parts.append(table(["sessions", "users", "pageviews"], totals))

    parts.append("\n### Channels\n")
    parts.append(table(["channel", "sessions", "users"],
                       run(["sessionDefaultChannelGroup"], ["sessions", "totalUsers"])))

    parts.append("\n### Landing pages\n")
    parts.append(table(["landing page", "sessions"],
                       run(["landingPage"], ["sessions"])))

    parts.append("\n### Key events\n")
    parts.append(table(["event", "count"],
                       run(["eventName"], ["eventCount"], limit=25)))

    return "\n".join(parts)


def gsc_section(start, end):
    """Search Console figures, or a note explaining why they are missing.

    Access is a separate grant from GA4 and arrives later -- the property has
    to be verified first. A missing grant is a known state, not a crash: the
    GA4 half of the report is still worth having, and a scheduled run that
    goes red every week for a reason nobody can fix from here is noise.
    """
    try:
        from googleapiclient.discovery import build
        from googleapiclient.errors import HttpError
        from google.auth import default as google_auth_default
    except ImportError:
        fail("google-api-python-client not installed, see codex/scripts/requirements.txt")

    scopes = ["https://www.googleapis.com/auth/webmasters.readonly"]
    credentials, _ = google_auth_default(scopes=scopes)
    service = build("searchconsole", "v1", credentials=credentials, cache_discovery=False)

    def query(dimensions, limit=10):
        body = {
            "startDate": str(start),
            "endDate": str(end),
            "dimensions": dimensions,
            "rowLimit": limit,
        }
        response = service.searchanalytics().query(siteUrl=SITE_URL, body=body).execute()
        return response.get("rows", [])

    try:
        query([])
    except HttpError as error:
        if error.resp.status in (403, 404):
            return (f"\n## Search Console\n\n_Not available: no access to `{SITE_URL}`._\n"
                    "Verify the property and grant the service account access, "
                    "then this section fills in on the next run. "
                    "Figures start accumulating from the verification date -- "
                    "Search Console does not backfill.\n")
        raise

    def fmt(rows, label):
        return [[
            " / ".join(r.get("keys", [])) or label,
            r.get("clicks", 0),
            r.get("impressions", 0),
            f"{r.get('ctr', 0) * 100:.1f}%",
            f"{r.get('position', 0):.1f}",
        ] for r in rows]

    headers = [" ", "clicks", "impressions", "ctr", "position"]
    parts = ["\n## Search Console\n", "### Totals\n"]
    parts.append(table(headers, fmt(query([]), "total")))

    parts.append("\n### Top queries\n")
    parts.append(table(headers, fmt(query(["query"], limit=15))))

    parts.append("\n### Top pages\n")
    parts.append(table(headers, fmt(query(["page"], limit=15))))

    tracked = [r for r in query(["query"], limit=1000)
               if r.get("keys", [""])[0].lower() in TARGET_QUERIES]
    parts.append("\n### Target queries\n")
    parts.append(table(headers, fmt(tracked, "-")))

    return "\n".join(parts)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--days", type=int, default=7, help="window length, default 7")
    parser.add_argument("--write", action="store_true",
                        help="write to codex/reports/ instead of stdout")
    parser.add_argument("--skip-gsc", action="store_true", help="GA4 only")
    args = parser.parse_args()

    if not os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        fail("GOOGLE_APPLICATION_CREDENTIALS is not set")

    start, end = date_range(args.days)
    report = [f"# iber.dev traffic report\n", f"_{start} to {end}_\n\n",
              ga4_section(start, end)]
    if not args.skip_gsc:
        report.append(gsc_section(start, end))

    text = "".join(report)

    if args.write:
        target = Path("codex/reports") / f"{end:%Y-%m}.md"
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("a", encoding="utf-8") as handle:
            handle.write(text + "\n\n---\n\n")
        print(f"appended to {target}", file=sys.stderr)
    else:
        print(text)


if __name__ == "__main__":
    main()
