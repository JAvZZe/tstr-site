/**
 * URL Validation Script for TSTR Directory
 * 
 * Validates URLs before adding to the directory to ensure they work.
 * Can be run standalone to test batches of URLs.
 */

const axios = require('axios');
/* eslint-disable @typescript-eslint/no-require-imports */
const { URL } = require('url');
const fs = require('fs');

// Validation function (matches backend implementation)
async function validateUrl(url, timeout = 5000) {
  try {
    const response = await axios.head(url, {
      timeout: timeout,
      maxRedirects: 5,
      validateStatus: function (status) {
        return status >= 200 && status < 400;
      },
      headers: {
        'User-Agent': 'TSTR-Directory-Validator/1.0'
      }
    });
    return {
      valid: true,
      statusCode: response.status,
      finalUrl: response.request.res?.responseUrl || url,
      redirected: response.request.res?.responseUrl !== url
    };
  } catch (_error) {
    // Try GET request if HEAD fails (some servers block HEAD requests)
    try {
      const response = await axios.get(url, {
        timeout: timeout,
        maxRedirects: 5,
        maxContentLength: 10240, // Download up to 10KB for validation
        validateStatus: function (status) {
          return status >= 200 && status < 400;
        },
        headers: {
          'User-Agent': 'TSTR-Directory-Validator/1.0'
        }
      });
      return {
        valid: true,
        statusCode: response.status,
        finalUrl: response.request.res?.responseUrl || url,
        redirected: response.request.res?.responseUrl !== url,
        method: 'GET'
      };
    } catch (getError) {
      return {
        valid: false,
        error: getError.message,
        code: getError.code,
        statusCode: getError.response?.status
      };
    }
  }
}

// Batch validation function
async function validateBatch(urls, concurrency = 5) {
  const results = [];

  // Process URLs in batches to avoid overwhelming servers
  for (let i = 0; i < urls.length; i += concurrency) {
    const batch = urls.slice(i, i + concurrency);
    console.log(`\nValidating batch ${Math.floor(i / concurrency) + 1} (${i + 1}-${Math.min(i + concurrency, urls.length)} of ${urls.length})`);

    const batchPromises = batch.map(async (url) => {
      console.log(`  Testing: ${url}`);
      const result = await validateUrl(url);

      if (result.valid) {
        console.log(`  ✓ Valid (${result.statusCode})${result.redirected ? ' - redirected to: ' + result.finalUrl : ''}`);
      } else {
        console.log(`  ✗ Invalid - ${result.error} (${result.code})`);
      }

      return {
        url,
        ...result,
        testedAt: new Date().toISOString()
      };
    });

    const batchResults = await Promise.all(batchPromises);
    results.push(...batchResults);

    // Small delay between batches to be respectful
    if (i + concurrency < urls.length) {
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }

  return results;
}

// Generate validation report
function generateReport(results) {
  const valid = results.filter(r => r.valid);
  const invalid = results.filter(r => !r.valid);
  const redirected = results.filter(r => r.redirected);

  const report = {
    summary: {
      total: results.length,
      valid: valid.length,
      invalid: invalid.length,
      redirected: redirected.length,
      successRate: `${((valid.length / results.length) * 100).toFixed(2)}%`
    },
    validUrls: valid.map(r => ({
      url: r.url,
      statusCode: r.statusCode,
      finalUrl: r.redirected ? r.finalUrl : undefined
    })),
    invalidUrls: invalid.map(r => ({
      url: r.url,
      error: r.error,
      errorCode: r.code,
      statusCode: r.statusCode
    })),
    testedAt: new Date().toISOString()
  };

  return report;
}

// Example usage
async function runValidation() {
  console.log('=== TSTR URL Validator ===\n');

  // Example URLs to test (replace with your actual URLs)
  const testUrls = [
    'https://google.com',           // Valid
    'https://github.com',            // Valid
    'https://thisurldoesnotexist.com/fake', // Invalid
    'https://httpstat.us/404',       // Invalid (404)
    'https://httpstat.us/200',       // Valid
  ];

  console.log(`Testing ${testUrls.length} URLs...\n`);

  const results = await validateBatch(testUrls, 3);
  const report = generateReport(results);

  console.log('\n=== VALIDATION REPORT ===');
  console.log(JSON.stringify(report.summary, null, 2));

  if (report.invalidUrls.length > 0) {
    console.log('\n❌ Invalid URLs:');
    report.invalidUrls.forEach(u => {
      console.log(`  - ${u.url}`);
      console.log(`    Error: ${u.error} (${u.errorCode})`);
    });
  }

  // Save report to file
  const reportFile = `validation-report-${Date.now()}.json`;
  fs.writeFileSync(reportFile, JSON.stringify(report, null, 2));
  console.log(`\n📄 Full report saved to: ${reportFile}`);
}

// Run if called directly
if (require.main === module) {
  runValidation().catch(console.error);
}

// Export for use in other modules
module.exports = {
  validateUrl,
  validateBatch,
  generateReport
};
