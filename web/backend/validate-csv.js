/**
 * CSV URL Validator
 * 
 * Reads a CSV file with listing data and validates all URLs.
 * Generates a report showing which URLs are valid/invalid.
 */

const fs = require('fs');
const { validateUrl, validateBatch, generateReport } = require('./url-validator');

// Simple CSV parser
function parseCSV(filePath) {
  const content = fs.readFileSync(filePath, 'utf-8');
  const lines = content.trim().split('\n');
  const headers = lines[0].split(',').map(h => h.trim());
  
  const data = [];
  for (let i = 1; i < lines.length; i++) {
    const values = lines[i].split(',').map(v => v.trim());
    const row = {};
    headers.forEach((header, index) => {
      row[header] = values[index];
    });
    data.push(row);
  }
  
  return data;
}

// Validate all URLs in CSV
async function validateCSV(csvFile) {
  console.log(`\n=== Validating URLs from ${csvFile} ===\n`);
  
  // Parse CSV
  const listings = parseCSV(csvFile);
  console.log(`Found ${listings.length} listings to validate\n`);
  
  // Extract URLs
  const urls = listings.map(l => l.website).filter(url => url);
  
  if (urls.length === 0) {
    console.log('❌ No URLs found in CSV file!');
    return;
  }
  
  console.log(`Validating ${urls.length} URLs...\n`);
  
  // Validate URLs in batches
  const results = await validateBatch(urls, 3); // 3 concurrent requests
  
  // Generate report
  const report = generateReport(results);
  
  // Create enriched listings with validation status
  const validatedListings = listings.map(listing => {
    const validation = results.find(r => r.url === listing.website);
    return {
      ...listing,
      urlValid: validation ? validation.valid : false,
      urlStatus: validation ? validation.statusCode : null,
      urlError: validation ? validation.error : null,
      urlFinalUrl: validation ? validation.finalUrl : null
    };
  });
  
  // Display summary
  console.log('\n=== VALIDATION SUMMARY ===');
  console.log(`Total Listings: ${listings.length}`);
  console.log(`Total URLs: ${urls.length}`);
  console.log(`✓ Valid: ${report.summary.valid}`);
  console.log(`✗ Invalid: ${report.summary.invalid}`);
  console.log(`Success Rate: ${report.summary.successRate}`);
  
  // Show invalid URLs
  if (report.invalidUrls.length > 0) {
    console.log('\n❌ INVALID URLs:');
    report.invalidUrls.forEach((u, i) => {
      console.log(`\n${i + 1}. ${u.url}`);
      console.log(`   Error: ${u.error}`);
      console.log(`   Code: ${u.errorCode}`);
      
      // Find the listing info
      const listing = listings.find(l => l.website === u.url);
      if (listing) {
        console.log(`   Listing: ${listing.name}`);
      }
    });
  }
  
  // Show valid URLs with redirects
  const redirected = results.filter(r => r.valid && r.redirected);
  if (redirected.length > 0) {
    console.log('\n⚠️  URLs WITH REDIRECTS:');
    redirected.forEach((r, i) => {
      console.log(`\n${i + 1}. ${r.url}`);
      console.log(`   → ${r.finalUrl}`);
      
      const listing = listings.find(l => l.website === r.url);
      if (listing) {
        console.log(`   Listing: ${listing.name}`);
      }
    });
  }
  
  // Save reports
  const timestamp = Date.now();
  
  // Full JSON report
  const reportFile = `validation-report-${timestamp}.json`;
  fs.writeFileSync(reportFile, JSON.stringify(report, null, 2));
  console.log(`\n📄 Full report saved to: ${reportFile}`);
  
  // Validated listings CSV
  const validListings = validatedListings.filter(l => l.urlValid);
  const invalidListings = validatedListings.filter(l => !l.urlValid);
  
  if (validListings.length > 0) {
    const validCSV = `valid-listings-${timestamp}.csv`;
    const validContent = [
      'name,category,website,location,statusCode,finalUrl',
      ...validListings.map(l => 
        `"${l.name}",${l.category},${l.website},"${l.location}",${l.urlStatus},${l.urlFinalUrl || l.website}`
      )
    ].join('\n');
    fs.writeFileSync(validCSV, validContent);
    console.log(`✅ Valid listings saved to: ${validCSV}`);
  }
  
  if (invalidListings.length > 0) {
    const invalidCSV = `invalid-listings-${timestamp}.csv`;
    const invalidContent = [
      'name,category,website,location,error,errorCode',
      ...invalidListings.map(l => 
        `"${l.name}",${l.category},${l.website},"${l.location}","${l.urlError}",${l.urlError ? 'ERROR' : 'N/A'}`
      )
    ].join('\n');
    fs.writeFileSync(invalidCSV, invalidContent);
    console.log(`❌ Invalid listings saved to: ${invalidCSV}`);
  }
  
  console.log('\n=== VALIDATION COMPLETE ===\n');
  
  return {
    total: listings.length,
    valid: validListings.length,
    invalid: invalidListings.length,
    report
  };
}

// Run if called directly
if (require.main === module) {
  const csvFile = process.argv[2] || 'sample-urls-to-validate.csv';
  
  if (!fs.existsSync(csvFile)) {
    console.error(`❌ Error: CSV file '${csvFile}' not found`);
    console.log('\nUsage: node validate-csv.js <csv-file>');
    console.log('Example: node validate-csv.js sample-urls-to-validate.csv');
    process.exit(1);
  }
  
  validateCSV(csvFile)
    .then(result => {
      if (result.invalid > 0) {
        console.log('⚠️  Some URLs failed validation. Review the invalid-listings CSV file.');
      } else {
        console.log('✅ All URLs validated successfully!');
      }
    })
    .catch(error => {
      console.error('Error:', error);
      process.exit(1);
    });
}

module.exports = { validateCSV };
