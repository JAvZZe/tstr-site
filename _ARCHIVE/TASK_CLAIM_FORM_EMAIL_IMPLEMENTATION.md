# Task: Implement Claim Form Email Functionality

## Description
The claim form on https://tstr.directory/claim has critical email functionality missing:
1. Save Draft button doesn't send resume link email
2. Verify/Claim button doesn't send verification emails

## Priority
High - This is a core user-facing functionality that is currently broken

## Required Implementation

### 1. Add Email Service
- Add Resend (or preferred email service) to package.json
- Configure environment variables with API keys

### 2. Update API Endpoints
- `web/tstr-frontend/src/pages/api/claim.ts` - Implement draft email functionality
- `web/tstr-frontend/src/pages/api/claim-listing.ts` - Implement verification email functionality

### 3. Create Email Templates
- Draft resume email template
- Claim verification email template

### 4. Error Handling
- Add proper error handling for email delivery failures
- Provide appropriate user feedback when emails fail to send

## Reference
See `CLAIM_FORM_EMAIL_ISSUES.md` for complete technical analysis and implementation details.

## Status
Pending Implementation