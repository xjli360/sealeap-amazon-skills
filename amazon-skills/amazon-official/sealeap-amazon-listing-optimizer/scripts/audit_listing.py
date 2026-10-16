#!/usr/bin/env python3
"""Dependency-free static audit for an evidence-backed Amazon Listing draft.

This catches common, cross-category issues only. The current marketplace
Product Type Definition, Seller Central policy, and human review remain the
authoritative release gates.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


DEFAULT_FORBIDDEN_TITLE_CHARS = "!$?_{}^¬¦"
STOPWORDS = {
    "a", "an", "and", "as", "at", "by", "for", "from", "in", "of",
    "on", "or", "the", "to", "with",
}
RISKY_CLAIM_PATTERNS = {
    "absolute_or_rank_claim": r"(?i)(?:#\s*1|\bno\.\s*1\b|\bbest\b|\bguaranteed\b|\b100%\b|绝对|最佳|第一|保证)",
    "medical_claim": r"(?i)(?:\bcure[sd]?\b|\bmedical(?:ly)?\b|\b(?:treats?|prevents?)\s+(?:disease|infection|pain|illness|condition)s?\b|治疗|治愈|预防疾病)",
    "certification_claim": r"(?i)(?:\bfda\s+approved\b|\bcertified\b|\borganic\b|\bnon[- ]?toxic\b|认证|有机|无毒)",
    "environmental_claim": r"(?i)(?:\beco[- ]?friendly\b|\bbiodegradable\b|\bsustainable\b|环保|可降解|可持续)",
    "promotion_or_shipping": r"(?i)(?:\bfree shipping\b|\blimited time\b|\bsale\b|\bdiscount\b|免邮|限时|折扣|促销)",
}


def _check(severity: str, code: str, message: str, evidence: Any = None) -> dict[str, Any]:
    item: dict[str, Any] = {"severity": severity, "code": code, "message": message}
    if evidence not in (None, "", [], {}):
        item["evidence"] = evidence
    return item


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def _latin_words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?", text.casefold())


def _visible_words(data: dict[str, Any]) -> set[str]:
    fields = [str(data.get("item_name", data.get("title")) or ""),
              str(data.get("title_differentiation", data.get("item_highlights")) or ""),
              str(data.get("description") or "")]
    fields.extend(str(x) for x in _as_list(data.get("bullets")))
    return {word for field in fields for word in _latin_words(field)}


def _rule_int(rules: dict[str, Any], key: str, default: int | None) -> int | None:
    value = rules.get(key, default)
    if value in (None, ""):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _unknown_ids(values: Iterable[Any], known: set[str]) -> list[str]:
    requested = {str(value).strip() for value in values if str(value).strip()}
    return sorted(requested - known)


def audit(data: dict[str, Any]) -> dict[str, Any]:
    checks: list[dict[str, Any]] = []
    rules = data.get("rules") if isinstance(data.get("rules"), dict) else {}
    def text_field(native: str, alias: str) -> str:
        value = data.get(native, data.get(alias, ""))
        if not isinstance(value, str):
            checks.append(_check("ERROR", "TITLE_FIELD_INVALID", f"{native}/{alias} must be a string; extract the correct marketplace/language value from API arrays first."))
            return ""
        return value

    title = text_field("item_name", "title")
    highlights = text_field("title_differentiation", "item_highlights")
    for native, alias in (("item_name", "title"), ("title_differentiation", "item_highlights")):
        if native in data and alias in data and data[native] != data[alias]:
            checks.append(_check("ERROR", "TITLE_ALIAS_CONFLICT", f"Conflicting {native} and {alias}; choose one value."))
    bullets = [str(x).strip() for x in _as_list(data.get("bullets"))]
    search_terms = str(data.get("search_terms") or "").strip()
    description = str(data.get("description") or "").strip()
    claims = _as_list(data.get("claims"))
    evidence = _as_list(data.get("evidence"))
    images = _as_list(data.get("images"))
    questions = _as_list(data.get("purchase_questions"))

    for field in ("marketplace", "sku", "product_type"):
        if not str(data.get(field) or "").strip():
            checks.append(_check("ERROR", f"SCOPE_{field.upper()}_MISSING", f"Required scope field '{field}' is missing."))
    if not str(data.get("seller_id") or "").strip():
        checks.append(_check("WARN", "SCOPE_SELLER_UNVERIFIED", "seller_id is missing; bind any live operation to a verified store identity."))

    live_schema_checked = rules.get("live_schema_checked") is True
    if not live_schema_checked:
        checks.append(_check("WARN", "LIVE_SCHEMA_NOT_CHECKED", "Live Product Type Definition was not confirmed; this draft cannot be released."))
    else:
        if not rules.get("schema_fetched_at"):
            checks.append(_check("WARN", "SCHEMA_FETCH_TIME_MISSING", "Live schema is marked checked but schema_fetched_at is missing."))
        if not rules.get("schema_checksum"):
            checks.append(_check("WARN", "SCHEMA_CHECKSUM_MISSING", "Live schema is marked checked but schema_checksum is missing."))

    title_structure = rules.get("title_structure")
    if title_structure is not None and not isinstance(title_structure, str):
        checks.append(_check("ERROR", "TITLE_STRUCTURE_INVALID", "title_structure must be modular, single, or api_legacy."))
        title_structure = None
    title_policy_known = (
        title_structure in ("modular", "single", "api_legacy")
        and bool(str(rules.get("title_policy_source") or "").strip())
        and bool(str(rules.get("title_policy_checked_at") or "").strip())
    )
    if not title_policy_known:
        checks.append(_check("WARN", "TITLE_POLICY_UNVERIFIED", "Confirm marketplace/product-type title structure, source and check date; no universal 200-character fallback."))

    def title_limit(key: str, default: int | None, cap: int | None = None) -> int | None:
        value = rules.get(key, default)
        if value is None and default is None:
            return None
        if type(value) is not int or value <= 0:
            checks.append(_check("ERROR", "TITLE_LIMIT_INVALID", f"{key} must be a positive integer."))
            return default
        if cap is not None and value > cap:
            checks.append(_check("ERROR", "TITLE_LIMIT_EXCEEDS_STRUCTURE", f"{key} cannot exceed {cap} for the selected title structure."))
            return cap
        return value

    title_default = {"modular": 75, "api_legacy": 200}.get(title_structure)
    title_cap = {"modular": 75, "api_legacy": 200}.get(title_structure)
    title_max = title_limit("title_max_chars", title_default, title_cap)
    highlights_max = title_limit("item_highlights_max_chars", 125, 125) if title_structure == "modular" else None
    combined_max = title_limit("combined_title_max_chars", 200, 200) if title_structure == "modular" else None
    if title_structure == "single" and title_max is None:
        checks.append(_check("ERROR", "TITLE_LIMIT_MISSING", "Single-field exceptions require an explicit current title limit."))
    if highlights and title_structure != "modular":
        checks.append(_check("ERROR", "HIGHLIGHTS_NOT_CONFIRMED", "Item Highlights requires verified modular title support."))
    if title_structure == "api_legacy":
        checks.append(_check("WARN", "LEGACY_API_RECONCILIATION", "Documented API compatibility can accept a title up to 200 without Item Highlights; Amazon may split catalog content. Readback of submitted values does not verify final catalog display."))
    if title_structure == "modular":
        if len(highlights) > highlights_max:
            checks.append(_check("ERROR", "ITEM_HIGHLIGHTS_TOO_LONG", f"Item Highlights has {len(highlights)} characters; limit is {highlights_max}."))
        if len(title) + len(highlights) > combined_max:
            checks.append(_check("ERROR", "COMBINED_TITLE_TOO_LONG", f"Combined title fields exceed {combined_max} characters."))
        if any(char in highlights for char in "\r\n"):
            checks.append(_check("WARN", "ITEM_HIGHLIGHTS_FORMAT", "Use comma-separated comparison phrases, not multiline copy."))
    if highlights.strip():
        if highlights.strip().casefold() == title.strip().casefold():
            checks.append(_check("WARN", "ITEM_HIGHLIGHTS_REDUNDANT", "Item Highlights repeats the title; supply documented differentiating details."))
        if not any(isinstance(claim, dict) and set(map(str, _as_list(claim.get("fields")))) & {"item_highlights", "title_differentiation"} for claim in claims):
            checks.append(_check("WARN", "ITEM_HIGHLIGHTS_EVIDENCE_UNMAPPED", "Map Item Highlights claims to verified evidence before release."))
    search_max = _rule_int(rules, "search_terms_max_bytes", 250) or 250
    bullet_min = _rule_int(rules, "bullet_min_count", 3) or 0
    bullet_max = _rule_int(rules, "bullet_max_count", 5)
    bullet_chars_max = _rule_int(rules, "bullet_max_chars", None)
    main_min_side = _rule_int(rules, "main_image_min_longest_side", 1000) or 1000
    main_min_fill = _rule_int(rules, "main_image_min_fill_percent", 85) or 85
    forbidden = str(rules.get("title_forbidden_chars", DEFAULT_FORBIDDEN_TITLE_CHARS))

    if not title.strip():
        checks.append(_check("ERROR", "TITLE_MISSING", "Title is empty."))
    else:
        if title_max is not None and len(title) > title_max:
            checks.append(_check("ERROR", "TITLE_TOO_LONG", f"Title has {len(title)} characters; configured limit is {title_max}."))
        found = sorted({char for char in title if char in forbidden})
        if found:
            checks.append(_check("ERROR", "TITLE_FORBIDDEN_CHARS", "Title contains generally forbidden characters.", found))
        words = [word for word in _latin_words(title) if word not in STOPWORDS]
        repeats = {word: count for word, count in Counter(words).items() if count > 2}
        if repeats:
            checks.append(_check("ERROR", "TITLE_WORD_REPEATED", "A non-stopword appears more than twice in the title.", repeats))
        if "  " in title:
            checks.append(_check("WARN", "TITLE_DOUBLE_SPACE", "Title contains repeated spaces."))

    non_empty_bullets = [item for item in bullets if item]
    if len(non_empty_bullets) < bullet_min:
        checks.append(_check("WARN", "BULLETS_BELOW_CONFIGURED_MIN", f"Only {len(non_empty_bullets)} non-empty bullets were provided; configured minimum is {bullet_min}."))
    if bullet_max is not None and len(bullets) > bullet_max:
        checks.append(_check("WARN", "BULLETS_OVER_CONFIGURED_MAX", f"{len(bullets)} bullets were provided; configured maximum is {bullet_max}."))
    if any(not item for item in bullets):
        checks.append(_check("WARN", "BULLET_EMPTY", "One or more bullet slots are empty."))
    if bullet_chars_max is not None:
        for index, bullet in enumerate(bullets, start=1):
            if len(bullet) > bullet_chars_max:
                checks.append(_check("ERROR", "BULLET_TOO_LONG", f"Bullet {index} has {len(bullet)} characters; configured limit is {bullet_chars_max}."))

    search_bytes = len(search_terms.encode("utf-8"))
    if search_bytes > search_max:
        checks.append(_check("ERROR", "SEARCH_TERMS_TOO_LARGE", f"Backend search terms use {search_bytes} UTF-8 bytes; configured limit is {search_max}."))
    if re.search(r"[,;:|]", search_terms):
        checks.append(_check("WARN", "SEARCH_TERMS_PUNCTUATION", "Backend search terms contain punctuation; space separation is normally sufficient."))
    search_words = _latin_words(search_terms)
    duplicate_backend = sorted(word for word, count in Counter(search_words).items() if count > 1)
    if duplicate_backend:
        checks.append(_check("WARN", "SEARCH_TERMS_DUPLICATE", "Backend search terms repeat tokens.", duplicate_backend))
    visible_overlap = sorted(set(search_words) & _visible_words(data))
    if visible_overlap:
        checks.append(_check("INFO", "SEARCH_TERMS_VISIBLE_OVERLAP", "Some backend tokens already appear in visible copy; review whether the bytes add value.", visible_overlap))

    combined_copy = " ".join([title, highlights, *bullets, description, search_terms])
    for code, pattern in RISKY_CLAIM_PATTERNS.items():
        matches = sorted({match.group(0) for match in re.finditer(pattern, combined_copy)})
        if matches:
            checks.append(_check("WARN", code.upper(), "Potentially high-risk wording requires marketplace-specific evidence and review.", matches))

    competitor_terms = [str(item).strip() for item in _as_list(rules.get("competitor_terms")) if str(item).strip()]
    competitor_hits = sorted(term for term in competitor_terms if term.casefold() in combined_copy.casefold())
    if competitor_hits:
        checks.append(_check("WARN", "COMPETITOR_OR_TRADEMARK_TERM", "Configured competitor/trademark terms appear in the draft; perform an IP and compatibility-use review.", competitor_hits))

    evidence_by_id: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(evidence, start=1):
        if not isinstance(item, dict):
            checks.append(_check("ERROR", "EVIDENCE_INVALID", f"Evidence item {index} must be an object."))
            continue
        evidence_id = str(item.get("id") or "").strip()
        if not evidence_id:
            checks.append(_check("ERROR", "EVIDENCE_ID_MISSING", f"Evidence item {index} has no id."))
            continue
        if evidence_id in evidence_by_id:
            checks.append(_check("ERROR", "EVIDENCE_ID_DUPLICATE", f"Evidence id '{evidence_id}' is duplicated."))
        evidence_by_id[evidence_id] = item
        if not str(item.get("source") or "").strip():
            checks.append(_check("ERROR", "EVIDENCE_SOURCE_MISSING", f"Evidence '{evidence_id}' has no source."))
        elif re.search(r"(?i)\b(?:todo|tbd|placeholder|required)\b|待补|占位", str(item.get("source"))):
            checks.append(_check("WARN", "EVIDENCE_SOURCE_PLACEHOLDER", f"Evidence '{evidence_id}' source still looks like a placeholder.", item.get("source")))
        if item.get("verified") is not True:
            checks.append(_check("WARN", "EVIDENCE_NOT_VERIFIED", f"Evidence '{evidence_id}' is not marked verified."))

    known_evidence = set(evidence_by_id)
    for index, claim in enumerate(claims, start=1):
        if not isinstance(claim, dict):
            checks.append(_check("ERROR", "CLAIM_WITHOUT_EVIDENCE", f"Claim {index} is not an evidence-mapped object.", claim))
            continue
        claim_id = str(claim.get("id") or f"claim-{index}").strip()
        text = str(claim.get("text") or "").strip()
        ids = _as_list(claim.get("evidence_ids"))
        if not text:
            checks.append(_check("WARN", "CLAIM_TEXT_MISSING", f"Claim '{claim_id}' has no text."))
        if not ids:
            checks.append(_check("ERROR", "CLAIM_WITHOUT_EVIDENCE", f"Claim '{claim_id}' has no evidence_ids.", text))
        unknown = _unknown_ids(ids, known_evidence)
        if unknown:
            checks.append(_check("ERROR", "CLAIM_UNKNOWN_EVIDENCE", f"Claim '{claim_id}' references unknown evidence ids.", unknown))
        unverified = sorted(
            evidence_id for evidence_id in {str(value) for value in ids}
            if evidence_id in evidence_by_id and evidence_by_id[evidence_id].get("verified") is not True
        )
        if unverified:
            checks.append(_check("ERROR", "CLAIM_UNVERIFIED_EVIDENCE", f"Claim '{claim_id}' relies on unverified evidence.", unverified))
        if not _as_list(claim.get("fields")):
            checks.append(_check("WARN", "CLAIM_FIELDS_MISSING", f"Claim '{claim_id}' does not identify its destination fields."))

    valid_images = [item for item in images if isinstance(item, dict)]
    if len(valid_images) != len(images):
        checks.append(_check("ERROR", "IMAGE_METADATA_INVALID", "Every image entry must be an object."))
    if not valid_images:
        checks.append(_check("WARN", "IMAGES_NOT_AUDITED", "No image metadata was supplied; visual compliance was not checked."))
    else:
        if len(valid_images) < 4:
            checks.append(_check("WARN", "IMAGE_SET_THIN", "Fewer than four images were supplied; this is below Amazon Ads' common optimization recommendation."))
        main = next((item for item in valid_images if str(item.get("role", "")).upper() in {"MAIN", "MAIN_IMAGE"}), None)
        if not main:
            checks.append(_check("ERROR", "MAIN_IMAGE_MISSING", "No MAIN image metadata was supplied."))
        else:
            try:
                width = int(main.get("width") or 0)
                height = int(main.get("height") or 0)
            except (TypeError, ValueError):
                width = height = 0
                checks.append(_check("ERROR", "MAIN_IMAGE_DIMENSIONS_INVALID", "MAIN image width/height must be integers."))
            if max(width, height) and max(width, height) < main_min_side:
                checks.append(_check("WARN", "MAIN_IMAGE_SMALL", f"MAIN image longest side is below configured {main_min_side}px baseline.", {"width": width, "height": height}))
            fill = main.get("product_fill_percent")
            try:
                if fill is not None and float(fill) < main_min_fill:
                    checks.append(_check("WARN", "MAIN_IMAGE_LOW_FILL", f"Product occupies less than configured {main_min_fill}% main-image baseline.", fill))
            except (TypeError, ValueError):
                checks.append(_check("ERROR", "MAIN_IMAGE_FILL_INVALID", "product_fill_percent must be numeric."))
            background = main.get("background_rgb")
            if background is not None:
                if not isinstance(background, (list, tuple)) or list(background) != [255, 255, 255]:
                    checks.append(_check("ERROR", "MAIN_IMAGE_BACKGROUND", "MAIN image background metadata is not pure white RGB 255/255/255.", background))
            for flag in ("contains_text", "contains_watermark", "contains_unincluded_props"):
                if main.get(flag) is True:
                    checks.append(_check("ERROR", f"MAIN_IMAGE_{flag.upper()}", f"MAIN image metadata reports {flag.replace('_', ' ')}."))

        for index, item in enumerate(valid_images, start=1):
            role = str(item.get("role") or f"image-{index}")
            if role.upper() in {"MAIN", "MAIN_IMAGE"}:
                continue
            if not str(item.get("message") or "").strip():
                checks.append(_check("WARN", "IMAGE_MESSAGE_MISSING", f"Secondary image '{role}' has no single-message brief."))
            ids = _as_list(item.get("evidence_ids"))
            unknown = _unknown_ids(ids, known_evidence)
            if unknown:
                checks.append(_check("ERROR", "IMAGE_UNKNOWN_EVIDENCE", f"Secondary image '{role}' references unknown evidence ids.", unknown))
            if item.get("mobile_checked") is not True:
                checks.append(_check("WARN", "IMAGE_MOBILE_NOT_CHECKED", f"Secondary image '{role}' is not marked as checked on mobile."))
            if item.get("is_a_plus") is True and not str(item.get("alt_text") or "").strip():
                checks.append(_check("WARN", "A_PLUS_ALT_TEXT_MISSING", f"A+ image '{role}' has no alt text."))

    if not questions:
        checks.append(_check("WARN", "PURCHASE_QUESTIONS_MISSING", "No purchase-question matrix was supplied."))
    for index, item in enumerate(questions, start=1):
        if not isinstance(item, dict) or not str(item.get("question") or "").strip():
            checks.append(_check("WARN", "PURCHASE_QUESTION_INVALID", f"Purchase question {index} is missing or invalid."))
            continue
        if not _as_list(item.get("answered_in")):
            checks.append(_check("WARN", "PURCHASE_QUESTION_UNANSWERED", f"Purchase question {index} has no answered_in fields.", item.get("question")))

    severity_counts = Counter(item["severity"] for item in checks)
    if severity_counts["ERROR"]:
        status = "FAIL"
    elif severity_counts["WARN"]:
        status = "WARN"
    else:
        status = "PASS"
    schema_recorded = live_schema_checked and bool(rules.get("schema_fetched_at")) and bool(rules.get("schema_checksum"))
    release_gate = "HOLD" if severity_counts["ERROR"] or not schema_recorded or not title_policy_known else "READY_FOR_REVIEW"

    return {
        "status": status,
        "release_gate": release_gate,
        "scope": {
            "marketplace": data.get("marketplace"),
            "marketplace_id": data.get("marketplace_id"),
            "seller_id": data.get("seller_id"),
            "asin": data.get("asin"),
            "sku": data.get("sku"),
            "product_type": data.get("product_type"),
            "parentage_level": data.get("parentage_level"),
        },
        "metrics": {
            "title_chars": len(title),
            "title_limit": title_max,
            "title_structure": title_structure,
            "item_highlights_chars": len(highlights),
            "item_highlights_limit": highlights_max,
            "combined_title_chars": len(title) + len(highlights),
            "bullet_count": len(bullets),
            "search_terms_bytes": search_bytes,
            "search_terms_limit": search_max,
            "evidence_count": len(evidence_by_id),
            "claim_count": len(claims),
            "image_count": len(valid_images),
        },
        "counts": {key.lower(): severity_counts[key] for key in ("ERROR", "WARN", "INFO")},
        "checks": checks,
        "disclaimer": "Static common-rule audit only; live Product Type Definition, marketplace policy, visual review, and explicit human approval remain authoritative.",
    }


def render_markdown(result: dict[str, Any]) -> str:
    lines = [
        f"# Listing audit: {result['status']}",
        "",
        f"- Release gate: `{result['release_gate']}`",
        f"- Scope: `{json.dumps(result['scope'], ensure_ascii=False)}`",
        f"- Metrics: `{json.dumps(result['metrics'], ensure_ascii=False)}`",
        f"- Counts: `{json.dumps(result['counts'], ensure_ascii=False)}`",
        "",
        "## Checks",
        "",
    ]
    if not result["checks"]:
        lines.append("- No common static issues found.")
    for item in result["checks"]:
        evidence = f" Evidence: `{json.dumps(item['evidence'], ensure_ascii=False)}`" if "evidence" in item else ""
        lines.append(f"- **{item['severity']} · {item['code']}** — {item['message']}{evidence}")
    lines.extend(["", f"> {result['disclaimer']}"])
    return "\n".join(lines)


def demo_payload() -> dict[str, Any]:
    return {
        "marketplace": "US",
        "marketplace_id": "ATVPDKIKX0DER",
        "seller_id": "DEMO-VERIFIED",
        "asin": "B0DEMO0001",
        "sku": "DEMO-SKU",
        "product_type": "PET_SUPPLIES",
        "parentage_level": "NONE",
        "title": "Demo Brand Ceramic Hamster Hideout, Blue, 5 Inch",
        "item_highlights": "Ceramic, check entrance dimensions before purchase",
        "bullets": [
            "Measured 5-inch ceramic hideout for the documented use case",
            "Glazed surface wipes clean with a damp cloth",
            "Check the entrance dimensions before purchase",
        ],
        "description": "A ceramic shelter with documented size and care guidance.",
        "search_terms": "dwarf hamster house ceramic shelter",
        "evidence": [
            {"id": "F1", "source": "demo packaging specification", "verified": True},
        ],
        "claims": [
            {"id": "C1", "text": "5-inch ceramic hideout", "evidence_ids": ["F1"], "fields": ["title", "bullet_1"]},
        ],
        "purchase_questions": [
            {"question": "Will it fit?", "answered_in": ["bullet_3", "PT01"]},
        ],
        "images": [
            {"role": "MAIN", "width": 1600, "height": 1600, "background_rgb": [255, 255, 255], "product_fill_percent": 88, "contains_text": False},
            {"role": "PT01", "width": 1600, "height": 1600, "message": "Verified dimensions", "evidence_ids": ["F1"], "mobile_checked": True},
            {"role": "PT02", "width": 1600, "height": 1600, "message": "Surface detail", "mobile_checked": True},
            {"role": "PT03", "width": 1600, "height": 1600, "message": "Package contents", "mobile_checked": True},
        ],
        "rules": {
            "live_schema_checked": True,
            "schema_fetched_at": "DEMO-ONLY",
            "schema_checksum": "DEMO-ONLY",
            "title_structure": "modular",
            "title_policy_source": "SYNTHETIC demo policy; not live validation",
            "title_policy_checked_at": "2026-10-16",
            "title_max_chars": 75,
            "item_highlights_max_chars": 125,
            "search_terms_max_bytes": 250,
        },
    }


def should_fail(result: dict[str, Any], threshold: str) -> bool:
    if threshold == "never":
        return False
    if threshold == "error":
        return result["counts"]["error"] > 0
    if threshold == "warn":
        return result["counts"]["error"] > 0 or result["counts"]["warn"] > 0
    return result["release_gate"] == "HOLD"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", nargs="?", type=Path, help="Listing draft JSON file")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    parser.add_argument("--demo", action="store_true", help="Audit an embedded safe demo payload")
    parser.add_argument("--fail-on", choices=("never", "error", "warn", "hold"), default="never", help="Return exit code 2 when the selected threshold is met")
    args = parser.parse_args()
    if not args.demo and args.input is None:
        parser.error("provide an input JSON file or use --demo")
    try:
        data = demo_payload() if args.demo else json.loads(args.input.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"input error: {exc}", file=sys.stderr)
        return 2
    if not isinstance(data, dict):
        print("input error: top-level JSON value must be an object", file=sys.stderr)
        return 2
    result = audit(data)
    print(render_markdown(result) if args.format == "markdown" else json.dumps(result, ensure_ascii=False, indent=2))
    return 2 if should_fail(result, args.fail_on) else 0


if __name__ == "__main__":
    sys.exit(main())
