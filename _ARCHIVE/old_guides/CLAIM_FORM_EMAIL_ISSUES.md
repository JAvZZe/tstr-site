# Claim Form Email Functionality Issues

## Issue Summary
The claim form on https://tstr.directory/claim has two critical email functionality issues:
1. Save Draft button saves data but doesn't send resume link email
2. Verify/Claim button processes claims but doesn't send verification emails

## Detailed Analysis

### Issues Identified:

1. **Save Draft Functionality Issue**:
   - The "Save Draft" button calls the saveDraft function in `web/tstr-frontend/src/pages/claim.astro`
   - The function sends a POST request to `/api/claim` with `mode: 'save_draft'`
   - The backend API processes the draft correctly and saves it to the database
   - **However**, there's a TODO comment in the API that says `// TODO: Send email with resume link` - the email functionality is NOT implemented
   - The function returns a success message but no email is sent

2. **Verify/Claim Functionality Issue**:
   - The "Verify & Claim Profile" button works and shows the loading animation
   - The backend API processes the claim and creates the record in the database
   - **However**, there's another TODO comment in the API that says `// TODO: Send verification email if manual verification required` - the verification email functionality is also NOT implemented
   - The function returns a success message claiming an email was sent, but no email is actually sent

## Root Cause:

The email functionality is completely missing from the system. Looking at the codebase:

1. **No email service provider configured**: The package.json doesn't include Resend, SendGrid, Nodemailer, or any email library
2. **No email configuration**: No API keys or SMTP settings found in environment variables
3. **Incomplete implementation**: Multiple TODO comments in the code explicitly state that email functionality needs to be added
4. **Documentation confirms this**: The system was designed to use Resend as the email provider (mentioned in various documentation files), but it was never implemented

## Current Behavior:

1. **Save Draft**: The functionality works on the backend (saves to database) but doesn't send an email with the resume link
2. **Verification**: The functionality works on the backend (creates claim record) but doesn't send verification emails
3. **User Experience**: Users see the loading animation and success messages, but never receive emails, leading to confusion

## Required Implementation:

To fix the email functionality, the following needs to be implemented:

1. **Add email service dependency** (likely Resend based on documentation)
2. **Configure environment variables** with API keys
3. **Implement email sending functions** in the claim API endpoints:
   - `web/tstr-frontend/src/pages/api/claim.ts` - for draft saving emails
   - `web/tstr-frontend/src/pages/api/claim-listing.ts` - for verification emails
4. **Create email templates** for draft saving and verification
5. **Add error handling** for email delivery failures

## Files to Update:

- `web/tstr-frontend/package.json` - Add email service dependency
- `web/tstr-frontend/src/pages/api/claim.ts` - Implement draft email functionality
- `web/tstr-frontend/src/pages/api/claim-listing.ts` - Implement verification email functionality
- Environment variables in deployment configuration

## Priority: High
This is a critical user-facing issue that affects the core claim functionality of the platform.

## Status: Needs Implementation