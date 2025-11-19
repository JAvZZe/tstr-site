"""
URL Validation Module for TSTR Scrapers
Validates URLs before adding them to the directory
"""

import requests
import logging
from urllib.parse import urlparse
import time

class URLValidator:
    """
    Validates URLs to ensure they work before adding to directory.
    Implements best practices:
    - HEAD request first (fast, low bandwidth)
    - GET fallback if HEAD fails
    - Handles redirects
    - Configurable timeout
    - Rate limiting
    """
    
    def __init__(self, timeout=5, max_redirects=5):
        self.timeout = timeout
        self.max_redirects = max_redirects
        self.headers = {
            'User-Agent': 'TSTR-Directory-Validator/1.0'
        }
        self.validation_cache = {}  # Cache results to avoid re-validating same URL
        self.stats = {
            'valid': 0,
            'invalid': 0,
            'cached': 0
        }
    
    def validate_url(self, url):
        """
        Validate a single URL.
        
        Returns:
            dict: {
                'valid': bool,
                'status_code': int or None,
                'final_url': str or None,
                'redirected': bool,
                'error': str or None,
                'method': str ('HEAD' or 'GET')
            }
        """
        if not url or not isinstance(url, str):
            return {
                'valid': False,
                'status_code': None,
                'final_url': None,
                'redirected': False,
                'error': 'Invalid URL format',
                'method': None
            }
        
        # Check format
        try:
            parsed = urlparse(url)
            if not all([parsed.scheme, parsed.netloc]):
                return {
                    'valid': False,
                    'status_code': None,
                    'final_url': None,
                    'redirected': False,
                    'error': 'Invalid URL structure',
                    'method': None
                }
        except Exception as e:
            return {
                'valid': False,
                'status_code': None,
                'final_url': None,
                'redirected': False,
                'error': f'URL parsing error: {str(e)}',
                'method': None
            }
        
        # Check cache
        if url in self.validation_cache:
            self.stats['cached'] += 1
            return self.validation_cache[url]
        
        # Try HEAD request first (fast, minimal bandwidth)
        result = self._try_head_request(url)
        
        # If HEAD failed, try GET as fallback
        if not result['valid']:
            result = self._try_get_request(url)
        
        # Cache result
        self.validation_cache[url] = result
        
        # Update stats
        if result['valid']:
            self.stats['valid'] += 1
            logging.info(f"✓ Valid URL ({result['status_code']}): {url}")
        else:
            self.stats['invalid'] += 1
            logging.warning(f"✗ Invalid URL: {url} - {result['error']}")
        
        return result
    
    def _try_head_request(self, url):
        """Try HEAD request for URL validation"""
        try:
            response = requests.head(
                url,
                headers=self.headers,
                timeout=self.timeout,
                allow_redirects=True
            )
            
            # Accept 2xx and 3xx status codes
            if 200 <= response.status_code < 400:
                return {
                    'valid': True,
                    'status_code': response.status_code,
                    'final_url': response.url,
                    'redirected': response.url != url,
                    'error': None,
                    'method': 'HEAD'
                }
            else:
                return {
                    'valid': False,
                    'status_code': response.status_code,
                    'final_url': None,
                    'redirected': False,
                    'error': f'HTTP {response.status_code}',
                    'method': 'HEAD'
                }
        except requests.exceptions.Timeout:
            return {
                'valid': False,
                'status_code': None,
                'final_url': None,
                'redirected': False,
                'error': 'Request timeout',
                'method': 'HEAD'
            }
        except requests.exceptions.ConnectionError:
            return {
                'valid': False,
                'status_code': None,
                'final_url': None,
                'redirected': False,
                'error': 'Connection failed',
                'method': 'HEAD'
            }
        except Exception as e:
            return {
                'valid': False,
                'status_code': None,
                'final_url': None,
                'redirected': False,
                'error': f'HEAD request failed: {str(e)}',
                'method': 'HEAD'
            }
    
    def _try_get_request(self, url):
        """Try GET request as fallback (some servers block HEAD)"""
        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.timeout,
                allow_redirects=True,
                stream=True  # Don't download full content
            )
            
            # Close connection immediately (we only need headers)
            response.close()
            
            # Accept 2xx and 3xx status codes
            if 200 <= response.status_code < 400:
                return {
                    'valid': True,
                    'status_code': response.status_code,
                    'final_url': response.url,
                    'redirected': response.url != url,
                    'error': None,
                    'method': 'GET'
                }
            else:
                return {
                    'valid': False,
                    'status_code': response.status_code,
                    'final_url': None,
                    'redirected': False,
                    'error': f'HTTP {response.status_code}',
                    'method': 'GET'
                }
        except requests.exceptions.Timeout:
            return {
                'valid': False,
                'status_code': None,
                'final_url': None,
                'redirected': False,
                'error': 'Request timeout',
                'method': 'GET'
            }
        except requests.exceptions.ConnectionError:
            return {
                'valid': False,
                'status_code': None,
                'final_url': None,
                'redirected': False,
                'error': 'Connection failed',
                'method': 'GET'
            }
        except Exception as e:
            return {
                'valid': False,
                'status_code': None,
                'final_url': None,
                'redirected': False,
                'error': f'GET request failed: {str(e)}',
                'method': 'GET'
            }
    
    def validate_batch(self, urls, delay=0.5):
        """
        Validate multiple URLs with rate limiting.
        
        Args:
            urls: List of URLs to validate
            delay: Seconds to wait between requests (rate limiting)
        
        Returns:
            dict: {
                'valid_urls': list,
                'invalid_urls': list,
                'results': dict (url -> validation result)
            }
        """
        valid_urls = []
        invalid_urls = []
        results = {}
        
        for idx, url in enumerate(urls, 1):
            if not url:
                continue
            
            logging.info(f"Validating URL {idx}/{len(urls)}: {url}")
            result = self.validate_url(url)
            results[url] = result
            
            if result['valid']:
                valid_urls.append(url)
            else:
                invalid_urls.append(url)
            
            # Rate limiting (except for last URL)
            if idx < len(urls) and delay > 0:
                time.sleep(delay)
        
        return {
            'valid_urls': valid_urls,
            'invalid_urls': invalid_urls,
            'results': results
        }
    
    def get_stats(self):
        """Get validation statistics"""
        return {
            'total_validated': self.stats['valid'] + self.stats['invalid'],
            'valid': self.stats['valid'],
            'invalid': self.stats['invalid'],
            'cached': self.stats['cached'],
            'success_rate': f"{(self.stats['valid'] / max(1, self.stats['valid'] + self.stats['invalid'])) * 100:.1f}%"
        }
    
    def clear_cache(self):
        """Clear validation cache"""
        self.validation_cache.clear()
        logging.info("Validation cache cleared")


# Convenience function for quick validation
def validate_url_simple(url, timeout=5):
    """
    Simple one-off URL validation.
    
    Args:
        url: URL to validate
        timeout: Request timeout in seconds
    
    Returns:
        bool: True if URL is valid and accessible
    """
    validator = URLValidator(timeout=timeout)
    result = validator.validate_url(url)
    return result['valid']
