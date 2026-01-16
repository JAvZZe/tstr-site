/**
 * SEO Helper for TSTR.directory
 * Centralizes title and meta description logic to ensure length compliance.
 */

const BRAND_NAME = 'TSTR.directory';
const SHORT_BRAND = 'TSTR';

/**
 * Formats a page title to stay within SEO limits (ideal under 60-70 chars).
 * @param parts Array of strings to join (e.g. [Listing Name, Region])
 * @param includeBrand Whether to append the brand name
 */
export function formatTitle(parts: string[], includeBrand: boolean = true): string {
    // Filter out empty parts and remove redundancies
    let uniqueParts = parts
        .filter(Boolean)
        .map(p => p.trim());

    // Deduplicate: if part A contains part B, or vice versa, keep only the more descriptive one
    uniqueParts = uniqueRegionsAndCategories(uniqueParts);

    let title = uniqueParts.join(' in ');

    const brandSuffix = ` | ${SHORT_BRAND}`;

    // If title is already long, maybe skip the brand or use the short version
    if (title.length + brandSuffix.length > 65) {
        if (title.length > 65) {
            return truncate(title, 65);
        }
        return title + brandSuffix;
    }

    return title + ` | ${BRAND_NAME}`;
}

/**
 * Truncates a description to stay within 160 characters (ideal for meta tags).
 */
export function formatDescription(text: string, limit: number = 155): string {
    if (!text) return '';
    if (text.length <= limit) return text;

    // Try to cut at the last space before the limit
    const truncated = text.substring(0, limit);
    const lastSpace = truncated.lastIndexOf(' ');

    if (lastSpace > limit * 0.8) {
        return truncated.substring(0, lastSpace) + '...';
    }

    return truncated + '...';
}

/**
 * Internal helper to remove redundant parts in parts array
 */
function uniqueRegionsAndCategories(parts: string[]): string[] {
    const result: string[] = [];
    for (let i = 0; i < parts.length; i++) {
        let isDuplicate = false;
        for (let j = 0; j < parts.length; j++) {
            if (i === j) continue;
            // If parts[i] is a substring of parts[j], parts[i] is redundant
            if (parts[j].toLowerCase().includes(parts[i].toLowerCase()) && parts[j].length > parts[i].length) {
                isDuplicate = true;
                break;
            }
        }
        if (!isDuplicate) {
            result.push(parts[i]);
        }
    }
    // If we have just one part, return it. If we have multiple, ensure they are unique.
    return [...new Set(result)];
}

function truncate(str: string, max: number): string {
    return str.length > max ? str.substring(0, max - 3) + '...' : str;
}
