# TSTR.site: Analysis & AI-SEO Optimization Strategy

## 1. The Paradigm Shift: From "Search" to "Answer"
Current directories rely on humans typing keywords into Google.
**Future Reality (2025+):** "Agents" (AutoGPT, Gemini, Siri) will act as buyers.
* *User Query:* "Find a lab in Europe that can test hydrogen valves to 700 bar under ISO 19880-3."
* *AI Action:* The AI will not "search"; it will **retrieve** and **synthesize**. It prioritizes structured data over marketing fluff.



## 2. Critique of Current "Generic" Directories
* **Flaw:** They list *who* companies are (e.g., "Acme Labs is a leading provider...").
* **Problem:** LLMs hallucinate when data is vague. If the site doesn't explicitly say "Tested to 700 bar," the AI won't recommend it for safety-critical tasks.
* **Opportunity:** TSTR.site must be a **Deterministic Truth Source**.

## 3. The Strategy: Programmatic "Entity" SEO
We will not build pages for humans to browse casually. We will generate thousands of specific landing pages that act as "API endpoints" for search engines.

### A. The URL Structure (The Hierarchy)
Don't use: `tstr.site/providers/acme-labs`
**Use:** `tstr.site/tests/hydrogen/iso-19880-3/high-pressure`

* **Why?** This creates a semantic "breadcrumb" that teaches the AI the relationship between the *Company* and the *Capability*.
* **Scale:** One template + Database of Standards = 500+ highly specific landing pages.

### B. Schema.org Strategy (The Code)
You must speak the AI's native language (JSON-LD).
**Crucial Markup to Implement:**

```json
{
  "@context": "[https://schema.org](https://schema.org)",
  "@type": "Service",
  "serviceType": "Hydrogen Valve Testing",
  "provider": {
    "@type": "Organization",
    "name": "TÜV SÜD"
  },
  "hasCredential": {
    "@type": "Certification",
    "name": "ISO 19880-3 Accredited"
  },
  "serviceArea": {
    "@type": "Place",
    "name": "European Union"
  },
  "description": "Hydraulic pressure testing up to 1000 bar for hydrogen components."
}
