#!/bin/bash

# Script to set PayPal secrets in Supabase
# This should be run with actual PayPal credentials

echo "Setting PayPal secrets in Supabase..."

# Set PayPal configuration secrets
npx supabase secrets set PAYPAL_CLIENT_ID="your_actual_paypal_client_id_here"
npx supabase secrets set PAYPAL_CLIENT_SECRET="your_actual_paypal_client_secret_here" 
npx supabase secrets set PAYPAL_MODE="sandbox"  # or "live" for production
npx supabase secrets set PAYPAL_WEBHOOK_ID="7GL49575E0818380Y"  # From your webhook setup

# Set PayPal Plan IDs (these need to be obtained from PayPal Dashboard after creating plans)
npx supabase secrets set PAYPAL_PLAN_PROFESSIONAL="your_professional_plan_id_here"
npx supabase secrets set PAYPAL_PLAN_PREMIUM="your_premium_plan_id_here"

echo "PayPal secrets have been set in Supabase."
echo "Make sure to replace the placeholder values with actual credentials from your PayPal Dashboard."