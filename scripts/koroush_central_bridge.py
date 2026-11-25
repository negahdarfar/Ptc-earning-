#!/usr/bin/env python3
"""Dependency-free bridge from a repository evidence pack to KOROUSH CENTRAL AI.

Secrets are read only from environment variables. This script never logs the
tenant key, never fetches source URLs, and only submits caller-supplied evidence.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


def request_json(url: str, *, method: str, headers: dict[str, str], body: dict | None = None) -> dict:
    data = json.dumps(body).encode("utf-8") if body is not None else None
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = ""
        try:
            detail = exc.read(1024).decode("utf-8", errors="replace")
        except Exception:
            pass
        raise RuntimeError(f"Central API returned HTTP {exc.code}: {detail[:300]}") from exc
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(f"Central API transport failed: {type(exc).__name__}") from exc
    if not isinstance(payload, dict):
        raise RuntimeError("Central API returned a non-object response")
    return payload


def load_evidence(path: str | None, inline_json: str | None) -> list[dict]:
    if inline_json:
        raw = json.loads(inline_json)
    elif path:
        with open(path, "r", encoding="utf-8") as handle:
            raw = json.load(handle)
    else:
        raise ValueError("Provide evidence JSON or an evidence file")
    evidence = raw.get("evidence") if isinstance(raw, dict) else raw
    if not isinstance(evidence, list) or not 1 <= len(evidence) <= 8:
        raise ValueError("Evidence file must contain 1 to 8 items (array or {evidence: [...]})")
    for index, item in enumerate(evidence):
        if not isinstance(item, dict) or not isinstance(item.get("source_id"), str) or not item["source_id"].strip():
            raise ValueError(f"Evidence item {index + 1} requires source_id")
        if not isinstance(item.get("text"), str) or not item["text"].strip():
            raise ValueError(f"Evidence item {index + 1} requires non-empty text")
    return evidence


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--integration-id", default=os.getenv("KOROUSH_CENTRAL_INTEGRATION_ID"))
    parser.add_argument("--evidence-file", default=os.getenv("KOROUSH_CENTRAL_EVIDENCE_FILE"))
    parser.add_argument("--evidence-json", default=os.getenv("KOROUSH_CENTRAL_EVIDENCE_JSON"))
    parser.add_argument("--idempotency-key", default=os.getenv("KOROUSH_CENTRAL_IDEMPOTENCY_KEY"))
    parser.add_argument("--target-language", default=os.getenv("KOROUSH_CENTRAL_TARGET_LANGUAGE"))
    parser.add_argument("--wait-seconds", type=int, default=480)
    args = parser.parse_args()

    base_url = os.getenv("KOROUSH_CENTRAL_BASE_URL", "").strip().rstrip("/")
    tenant_key = os.getenv("KOROUSH_CENTRAL_TENANT_KEY", "")
    repository = os.getenv("GITHUB_REPOSITORY", "").strip().lower()
    if not base_url.startswith("https://") or not tenant_key.startswith("kor_") or not repository:
        raise ValueError("Set HTTPS KOROUSH_CENTRAL_BASE_URL, KOROUSH_CENTRAL_TENANT_KEY and GITHUB_REPOSITORY")
    if not args.integration_id or not args.idempotency_key or not (args.evidence_file or args.evidence_json):
        raise ValueError("integration-id, evidence and idempotency-key are required")
    if not 1 <= args.wait_seconds <= 1800:
        raise ValueError("wait-seconds must be between 1 and 1800")

    evidence = load_evidence(args.evidence_file, args.evidence_json)
    headers = {"X-Tenant-Key": tenant_key, "Content-Type": "application/json"}
    body = {
        "repository": repository,
        "idempotency_key": args.idempotency_key,
        "evidence": evidence,
        "max_attempts": 3,
    }
    if args.target_language:
        body["target_language"] = args.target_language

    url = base_url + "/api/integrations/" + urllib.parse.quote(args.integration_id, safe=".-") + "/research"
    submitted = request_json(url, method="POST", headers=headers, body=body)
    job_id = submitted.get("job_id")
    status_api = submitted.get("status_api")
    if not isinstance(job_id, str) or not isinstance(status_api, str) or not status_api.startswith("/api/jobs/"):
        raise RuntimeError("Central API response did not contain a valid job status reference")

    print(f"Central job accepted: {job_id} ({submitted.get('status', 'unknown')})")
    deadline = time.monotonic() + args.wait_seconds
    while time.monotonic() < deadline:
        status = request_json(base_url + status_api, method="GET", headers=headers)
        state = status.get("status")
        print(f"Central job state: {state}")
        if state == "succeeded":
            result = status.get("result")
            if isinstance(result, dict):
                print(json.dumps(result, ensure_ascii=False, indent=2)[:12000])
            return 0
        if state in {"failed", "dead_letter", "cancelled"}:
            raise RuntimeError(f"Central job ended with state: {state}")
        time.sleep(5)
    raise TimeoutError(f"Central job {job_id} did not finish within {args.wait_seconds} seconds")


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"Central integration failed: {exc}", file=sys.stderr)
        raise SystemExit(1)
