# 🛡️ IAF CertSearch API Integration Plan

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
