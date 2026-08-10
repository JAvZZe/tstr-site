"""
IAF CertSearch API Client for TSTR.directory
Handles certification verification with credit-conscious approach
"""

import logging
import os
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any

logger = logging.getLogger(__name__)

@dataclass
class IAFCertification:
    """Represents a certification from IAF CertSearch"""
    certificate_id: str
    standard: str  # e.g., "ISO 9001", "ISO 17025"
    scope: str
    issue_date: str
    expiry_date: str
    status: str
    issuing_body: str
    certificate_number: str | None = None

@dataclass
class IAFCompanyMatch:
    """Represents a potential company match from IAF search"""
    company_name: str
    country: str
    city: str | None = None
    website: str | None = None
    email: str | None = None
    phone: str | None = None
    certifications: list[IAFCertification] = None
    confidence_score: float = 0.0  # 0.0 to 1.0

class IAFVerifyClient:
    """
    Client for IAF CertSearch API with smart credit usage

    Strategy:
    1. Use free/search endpoints first to find potential matches
    2. Only consume verification credits for high-confidence matches
    3. Cache results to avoid redundant API calls
    4. Track credit usage to stay within plan limits
    """

    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('IAF_API_KEY')
        if not self.api_key:
            # Sell-now / activate-later model: the IAF verification plan is sold
            # on the site (pricing.astro) but the backend activates only once a
            # paid IAF CertSearch API key is set. Degrade gracefully instead of
            # crashing so a live call never 500s before activation.
            self.active = False
            logger.warning("IAFVerifyClient initialised WITHOUT IAF_API_KEY — "
                           "verification is INACTIVE (sell-now / activate-on-key). "
                           "Set IAF_API_KEY to enable.")
            return

        self.active = True
        self.base_url = "https://api.iafcertsearch.org"  # To be confirmed
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

        # Credit tracking (would be persisted in practice)
        self.monthly_credits_used = 0
        self.monthly_credit_limit = 150  # Basic 499 plan
        self.last_reset = datetime.now().replace(day=1)

        # Simple in-memory cache (would use Redis/DiskCache in production)
        self._search_cache = {}
        self._verify_cache = {}

    def _check_credit_availability(self, credits_needed: int = 1) -> bool:
        """Check if we have enough credits remaining"""
        # Reset monthly counter if needed
        now = datetime.now()
        if now.month != self.last_reset.month or now.year != self.last_reset.year:
            self.monthly_credits_used = 0
            self.last_reset = now.replace(day=1)

        return (self.monthly_credits_used + credits_needed) <= self.monthly_credit_limit

    def _track_credit_usage(self, credits_used: int):
        """Track credit consumption"""
        self.monthly_credits_used += credits_used
        logger.info(f"IAF API credits used: {credits_used}. Monthly total: {self.monthly_credits_used}/{self.monthly_credit_limit}")

    def search_companies(self, query: str, country: str = None, limit: int = 10) -> list[IAFCompanyMatch]:
        """
        Search for companies using the search endpoint (typically free/low cost)
        Returns potential matches for manual review or automated matching
        """
        # Check cache first
        cache_key = f"search:{query}:{country}:{limit}"
        if cache_key in self._search_cache:
            cached_result, timestamp = self._search_cache[cache_key]
            if datetime.now() - timestamp < timedelta(hours=24):  # Cache for 24h
                return cached_result

        # TODO: Implement actual API call
        # endpoint = f"{self.base_url}/v1/companies/search"
        # params = {"q": query, "limit": limit}
        # if country:
        #     params["country"] = country
        #
        # response = requests.get(endpoint, headers=self.headers, params=params)
        # response.raise_for_status()
        # data = response.json()
        #
        # # Process results into IAFCompanyMatch objects
        # matches = []
        # for item in data.get('results', []):
        #     match = IAFCompanyMatch(
        #         company_name=item.get('name', ''),
        #         country=item.get('country', ''),
        #         city=item.get('city'),
        #         website=item.get('website'),
        #         email=item.get('email'),
        #         phone=item.get('phone'),
        #         confidence_score=self._calculate_confidence(query, item)
        #     )
        #     matches.append(match)
        #
        # # Cache results
        # self._search_cache[cache_key] = (matches, datetime.now())
        # return matches

        logger.info(f"IAF search for: '{query}' (country: {country}) - [PLACEHOLDER]")
        return []  # Placeholder

    def verify_company(self, company_name: str, country: str = None) -> list[IAFCertification] | None:
        """
        Verify a specific company and retrieve its certifications
        Consumes verification credits - use judiciously
        """
        # Check cache first
        cache_key = f"verify:{company_name}:{country}"
        if cache_key in self._verify_cache:
            cached_result, timestamp = self._verify_cache[cache_key]
            if datetime.now() - timestamp < timedelta(days=30):  # Cache verifications longer
                return cached_result

        # Check credit availability
        if not self._check_credit_availability(1):
            logger.warning("Insufficient IAF credits for verification")
            return None

        # TODO: Implement actual API call
        # endpoint = f"{self.base_url}/v1/companies/verify"
        # data = {"name": company_name}
        # if country:
        #     data["country"] = country
        #
        # response = requests.post(endpoint, headers=self.headers, json=data)
        # response.raise_for_status()
        # result = response.json()
        #
        # # Track credit usage
        # self._track_credit_usage(1)
        #
        # # Process certifications
        # certifications = []
        # for cert_data in result.get('certifications', []):
        #     cert = IAFCertification(
        #         certificate_id=cert_data.get('id', ''),
        #         standard=cert_data.get('standard', ''),
        #         scope=cert_data.get('scope', ''),
        #         issue_date=cert_data.get('issue_date', ''),
        #         expiry_date=cert_data.get('expiry_date', ''),
        #         status=cert_data.get('status', ''),
        #         issuing_body=cert_data.get('issuing_body', ''),
        #         certificate_number=cert_data.get('certificate_number')
        #     )
        #     certifications.append(cert)
        #
        # # Cache results
        # self._verify_cache[cache_key] = (certifications, datetime.now())
        # return certifications

        logger.info(f"IAF verification for: '{company_name}' (country: {country}) - [PLACEHOLDER] - Would consume 1 credit")
        return []  # Placeholder

    def smart_verify_tstr_listing(self, tstr_listing: dict[str, Any]) -> dict[str, Any]:
        """
        Smart verification approach for TSTR listings:
        1. Search for potential matches using business name/location
        2. Calculate confidence score based on name, location, website matching
        3. Only verify if confidence > threshold (e.g., 0.8)
        4. Return enriched listing with certification data
        """
        business_name = tstr_listing.get('business_name', '')
        country = tstr_listing.get('country', '')
        city = tstr_listing.get('city', '')
        website = tstr_listing.get('website', '')

        if not business_name:
            logger.warning("Cannot verify listing without business name")
            return tstr_listing

        # Sell-now / activate-later: if no IAF_API_KEY is set, the backend is
        # inactive. Return the listing unchanged (no crash, no false claim).
        if not getattr(self, 'active', False):
            logger.info(f"IAF inactive (no key) — skipping verification for {business_name}")
            return {**tstr_listing, 'iaf_verified': False, 'iaf_match_confidence': 0.0,
                    'iaf_status': 'inactive'}

        # Search for potential matches
        search_query = f"{business_name} {city} {country} {website}".strip()
        matches = self.search_companies(search_query, country=country, limit=5)

        if not matches:
            logger.info(f"No IAF matches found for: {business_name}")
            return {**tstr_listing, 'iaf_verified': False, 'iaf_match_confidence': 0.0}

        # Find best match
        best_match = max(matches, key=lambda m: m.confidence_score)

        # Only verify if high confidence match
        if best_match.confidence_score >= 0.8:
            logger.info(f"High confidence match ({best_match.confidence_score:.2f}) for {business_name}. Verifying...")
            certifications = self.verify_company(best_match.company_name, country=best_match.country)

            enriched_listing = {
                **tstr_listing,
                'iaf_verified': bool(certifications),
                'iaf_match_confidence': best_match.confidence_score,
                'iaf_matched_name': best_match.company_name,
                'iaf_matched_country': best_match.country,
                'iaf_certifications': [
                    {
                        'standard': cert.standard,
                        'scope': cert.scope,
                        'issue_date': cert.issue_date,
                        'expiry_date': cert.expiry_date,
                        'status': cert.status,
                        'issuing_body': cert.issuing_body,
                        'certificate_number': cert.certificate_number
                    } for cert in certifications
                ] if certifications else [],
                'iaf_verification_date': datetime.now().isoformat()
            }

            return enriched_listing
        else:
            logger.info(f"Low confidence match ({best_match.confidence_score:.2f}) for {business_name}. Skipping verification.")
            return {
                **tstr_listing,
                'iaf_verified': False,
                'iaf_match_confidence': best_match.confidence_score,
                'iaf_matched_name': best_match.company_name,
                'iaf_matched_country': best_match.country
            }

    def _calculate_confidence(self, query: str, search_result: dict) -> float:
        """
        Calculate confidence score between search query and IAF result
        Based on name similarity, location matching, etc.
        """
        # This would be implemented with fuzzy string matching
        # For now, return a placeholder
        return 0.75  # Placeholder

# Example usage
if __name__ == "__main__":
    # Example of how to use the client
    import os

    from dotenv import load_dotenv

    load_dotenv()  # Load environment variables from .env

    try:
        client = IAFVerifyClient()

        # Example TSTR listing
        tstr_listing = {
            'business_name': 'Example Testing Labs Ltd',
            'country': 'Australia',
            'city': 'Sydney',
            'website': 'https://examplelabs.com.au',
            'listing_id': 'TSTR-00123'
        }

        # Smart verification
        enriched = client.smart_verify_tstr_listing(tstr_listing)
        print(f"Enriched listing: {enriched}")

    except Exception as e:
        logger.error(f"Error initializing IAF client: {e}")