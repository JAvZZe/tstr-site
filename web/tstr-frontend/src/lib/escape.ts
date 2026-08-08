// HTML-escape untrusted strings before interpolating into innerHTML / attributes.
// Security: prevents stored/reflected XSS from user-derived fields (business_name,
// owner_notes, error.message, etc.). Mirrors the tstr-security-hardening skill rule
// "encode output; never innerHTML with untrusted data".
export function escapeHtml(input: unknown): string {
  if (input === null || input === undefined) return '';
  return String(input)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}
