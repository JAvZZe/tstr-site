# Google Cloud Credential Exposure Incident Response

## Purpose

Coordinate immediate containment and appeal work for the confirmed Google Cloud credential exposure affecting project `gen-lang-client-0780104741`.

This runbook intentionally does not include credential values. Do not paste keys, tokens, service account JSON, screenshots containing secrets, or raw scanner output into this file, chat, commits, tickets, or logs.

## Incident Classification

- Severity: Critical
- Status: Confirmed public credential exposure
- Primary risk: Unauthorized Google Cloud API usage and resource creation
- Related systems: GitHub, Supabase, Cloudflare, OCI, local `.env`, GitHub Actions

## Immediate Containment

1. Open Google Cloud Console for `gen-lang-client-0780104741`.
2. Review billing, IAM, API keys, service accounts, Compute Engine, Cloud Run, Cloud Functions, App Engine, Vertex AI, Maps Platform, and enabled APIs.
3. Delete any unauthorized VMs, disks, snapshots, service accounts, service account keys, workloads, functions, buckets, or API credentials.
4. Disable or delete every exposed API key and service account key. Treat every key referenced by GitHub secret scanning as compromised.
5. Confirm billing export, budget alerts, and usage dashboards show no continuing unauthorized activity.

## Credential Rebuild Rules

Create only replacement credentials that are needed for production.

- Browser Maps key: restrict by HTTP referrer to `https://tstr.directory/*` and required Cloudflare preview domains only.
- Backend Maps or geocoding key: restrict by OCI egress IP only and restrict to the exact required APIs.
- Gemini key: create separately from Maps keys and restrict to required Generative Language APIs.
- Service accounts: prefer workload identity or console-managed credentials. Do not create downloadable JSON keys unless there is no viable alternative.
- API restrictions: every key must have explicit API restrictions.
- Owner labels: document purpose, owner, deployment surface, and rotation date in the credential description.

## Evidence To Collect

Do not collect secret values. Capture only metadata and timestamps.

- Secret scanning alert numbers and provider types.
- Google Cloud audit log timestamps for unauthorized access or resource creation.
- List of deleted unauthorized resource names or IDs, excluding secrets.
- Timestamps when old credentials were revoked.
- Timestamps when new restricted credentials were created.
- Verification that new keys have application and API restrictions.
- Billing and quota screenshots with secret-bearing fields hidden.

## Google Appeal Package

Submit the appeal only after containment is complete.

Include:

- Project ID: `gen-lang-client-0780104741`
- Incident summary: public GitHub credential exposure discovered through GitHub secret scanning.
- Remediation summary: all exposed keys revoked, unauthorized resources removed, replacement keys restricted by API and origin/IP, non-Git secret stores audited.
- Evidence: alert numbers, revocation timestamps, cleanup timestamps, and screenshots with secret values redacted.
- Prevention controls: GitHub push protection, secret scanning, restricted keys, least-privilege service accounts, recurring secret inventory.

Do not claim remediation is complete until old keys fail, new keys work only from intended surfaces, and GitHub secret alerts are resolved or marked revoked.

## Verification Checklist

- [ ] No unauthorized Google Cloud resources remain.
- [ ] No active exposed Google API keys remain.
- [ ] No downloadable service account keys remain unless explicitly justified.
- [ ] Replacement keys are API restricted.
- [ ] Browser keys are referrer restricted.
- [ ] Backend keys are IP restricted.
- [ ] Old exposed keys fail.
- [ ] New keys work from intended production and preview surfaces only.
- [ ] Billing and quota dashboards show no unexplained ongoing usage.
- [ ] Appeal package submitted with redacted evidence.
