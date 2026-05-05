## 🛡️ IAF CertSearch API Integration Plan (API-FIRST PIVOT)

### 🚨 Strategy Update
Manual bulk upload attempts (XLSX) encountered UI mapping blockers. The project is now pivoting to an **API-First Verification** strategy using the IAF CertSearch REST API. This will allow for programmatic matching and automated data enrichment without manual UI intervention.

## Executive Cost Summary
The IAF CertSearch API has moved to a **Company-Based Usage** model (as of July 2025). Credits are consumed per company verified, with unlimited access to all their certificates (ISO 9001, 17025, etc.) once "claimed."

| Tier | Annual Cost (Est.) | Company Credits | Best For |
| :--- | :--- | :--- | :--- |
| **Free** | $0 | 3 / month | Proof of Concept tests. |
| **Basic 499** | ~$499 / year | 150 / year | Small scale niche verification. |
| **Standard** | ~$999 / year | 400 / year | Mid-scale directory growth. |
| **Enterprise** | **Custom Quote** | **High Volume** | **Full directory automation.** |

---

## 🛠️ User Registration Checklist
To enable this integration, the following manual steps are required:

1.  **Register Account**: Create an account at [iafcertsearch.org](https://www.iafcertsearch.org).
2.  **Select Plan**: Choose a plan under "Membership and Billing" (Start with **Basic 499** for production seeding).
3.  **Generate API Key**:
    *   Navigate to **API Settings** in the dashboard.
    *   Click **Generate API Key**.
    *   Copy the key and add it to your `.env` file as `IAF_API_KEY`.
4.  **Confirm Activation**: API keys typically require 24 hours for full activation.

---

## 📐 Technical Implementation (TSTR.site)
We will implement a specialized **`IAFVerifyClient`** to handle the matching and credit consumption logic.

---

## 🔍 IAF Data Ecosystem Analysis (Strategic)
As per the steering update, we will analyze the IAF's data pipeline to inform TSTR's own negotiation strategy with standards bodies.

### 1. Data Sourcing Analysis
*   **Source**: IAF aggregates from national ABs (UKAS, A2LA, etc.) and global CBs.
*   **Mechanism**: Data is pushed via XML/XLSX or pulled via API from the member bodies.
*   **Negotiation Goal**: Understand the multilateral recognition arrangements (MLA/MRA) that underpin this data sharing to position TSTR as a value-add discovery partner.

### 2. Partnership Positioning
*   Analyze the 'Quality Trade' management of the IAF CertSearch platform.
*   Evaluate how TSTR can negotiate similar direct data feeds from niche-specific ABs by demonstrating high-intent lead generation for their accredited members.

### 1. The "Matching" Problem
TSTR has 700+ listings. We cannot afford to "blindly" verify all of them via API.
*   **Strategy**: Use the **Search API** (low cost/free) to find potential matches first.
*   **Action**: Only consume a "Verify" credit if the search returns a high-confidence match for an existing TSTR laboratory.

### 2. Global Bypassing
This API will be the primary tool to bypass anti-bot protections in:
*   **Australia (NATA)**: Indexed in IAF.
*   **China (CNAS)**: Indexed in IAF.
*   **Germany (DAkkS)**: Indexed in IAF.

---

## 🚀 Next Technical Step
I am creating a **`web/tstr-automation/iaf_api_client.py`** skeleton. Once you provide the `IAF_API_KEY`, I can run the first verification for the blocked Australian labs.
