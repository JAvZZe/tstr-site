// Zero-dependency input validation at API boundaries.
// Security: enforces the tstr-security-hardening rule "validate ALL external
// input at the system boundary". Rejects malformed/oversized/unsafe input
// before it reaches DB or email paths. No external deps (avoids lockfile/supply-chain churn).

export type ValidationResult<T> = { ok: true; data: T } | { ok: false; error: string };

export function requiredString(
  value: unknown,
  field: string,
  opts: { max?: number; email?: boolean } = {}
): ValidationResult<string> {
  if (typeof value !== 'string') return { ok: false, error: `${field} is required` };
  const trimmed = value.trim();
  if (trimmed.length === 0) return { ok: false, error: `${field} is required` };
  if (opts.max && trimmed.length > opts.max)
    return { ok: false, error: `${field} exceeds ${opts.max} chars` };
  if (opts.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(trimmed))
    return { ok: false, error: `${field} is not a valid email` };
  return { ok: true, data: trimmed };
}

export function optionalString(value: unknown, opts: { max?: number } = {}): string {
  if (typeof value !== 'string') return '';
  const t = value.trim();
  return opts.max && t.length > opts.max ? t.slice(0, opts.max) : t;
}

// Validate a JSON request body against a set of field rules.
export function validateJson<T extends Record<string, unknown>>(
  raw: string,
  rules: (body: any) => ValidationResult<T>
): ValidationResult<T> {
  let parsed: unknown;
  try {
    parsed = JSON.parse(raw);
  } catch {
    return { ok: false, error: 'Invalid JSON body' };
  }
  if (typeof parsed !== 'object' || parsed === null || Array.isArray(parsed))
    return { ok: false, error: 'Body must be a JSON object' };
  return rules(parsed);
}
