# IAF CertSearch API Setup Guide for TSTR.directory

## 🚨 Important: Free Tier Limitations

The IAF CertSearch API **Free tier ($0/month, 3 credits/month)** is **insufficient for production use** with TSTR.directory's ~700+ listings.

### Why Free Tier Won't Work:
- **3 credits/month** = Only 3 company verifications per month
- TSTR.directory has **700+ active listings** requiring verification
- At free tier rate, it would take **~19+ years** to verify all listings once
- No practical way to keep verifications current with new/expiring certifications

## 📊 Recommended Plan: Basic 499 (~$499/year)

| Tier | Annual Cost | Monthly Cost | Company Credits/year | Credits/month | Best For |
|------|-------------|--------------|----------------------|---------------|----------|
| **Free** | $0 | $0 | 36 | 3 | Proof of Concept only |
| **Basic 499** | ~$499 | ~$42/month | 150 | ~12/month | **Production seeding & maintenance** |
| Standard | ~$999 | ~$83/month | 400 | ~33/month | Mid-scale growth |
| Enterprise | Custom | Custom | High Volume | High Volume | Full automation |

### Why Basic 499 is Recommended:
1. **Cost-effective**: ~$42/month for 150 verifications
2. **Smart usage**: With our search-first approach, we can verify ~100-150 high-confidence matches/month
3. **Sustainable**: Allows for regular updates and new listing verification
4. **ROI**: Enables trusted badge display, improving user confidence and conversion

## 🔑 Step-by-Step Setup Instructions

### 1. Register for IAF Account
- Go to: [https://www.iafcertsearch.org](https://www.iafcertsearch.org)
- Click "Register" or "Sign Up"
- Complete registration with your organization details
- Verify your email address

### 2. Select & Purchase a Plan
- Log in to your IAF CertSearch dashboard
- Navigate to **"Membership and Billing"** or **"Plans & Pricing"**
- Select **"Basic 499"** plan (or higher if anticipating rapid growth)
- Complete payment process (credit card or invoice)
- **Note**: Activation may take up to 24 hours

### 3. Generate Your API Key
- After plan activation, go to **"API Settings"** in dashboard
- Click **"Generate API Key"**
- **Copy the key immediately** (you won't see it again!)
- Store it securely - treat it like a password

### 4. Configure TSTR.directory
#### Option A: Environment Variable (Recommended)
```bash
# In your shell or deployment configuration:
export IAF_API_KEY="your-actual-api-key-here"
```

#### Option B: .env File
1. Copy the example file:
   ```bash
   cd web/tstr-automation
   cp .env.example .env
   ```
2. Edit `.env` and replace:
   ```
   IAF_API_KEY=your-actual-api-key-here
   ```
3. **Important**: Add `.env` to `.gitignore` to prevent committing secrets
   ```bash
   echo ".env" >> .gitignore
   ```

### 5. Test Your Configuration
Run the IAF client to verify it works:
```bash
cd web/tstr-automation
python3 iaf_api_client.py
```
You should see placeholder output indicating the client initialized correctly.

## 💡 Cost Optimization Strategies

Our implementation includes several techniques to maximize your API credits:

### 1. Search-First Approach
- Use free/low-cost search endpoints to find potential matches
- Only consume verification credits for high-confidence matches (>80%)
- Reduces unnecessary verification calls

### 2. Intelligent Matching
- Combines business name, location, website, and other factors
- Calculates confidence scores to avoid low-probability verifications
- Prevents wasting credits on clearly wrong matches

### 3. Result Caching
- Search results cached for 24 hours
- Verification results cached for 30 days
- Prevents redundant API calls for same companies

### 4. Monthly Credit Tracking
- Tracks usage against your plan limits
- Prevents unexpected overages
- Resets automatically each month

### 5. Selective Verification
- Focus on listings most likely to have IAF certifications
- Priority: Laboratories, testing facilities, certification bodies
- Lower priority: Consultants, training providers, etc.

## 📈 Expected Usage & Planning

With Basic 499 plan (150 credits/year):

### Initial Seeding (Month 1-3):
- Verify high-priority listings: ~50-75 credits
- Focus on: ISO 17025 labs, specialty testing facilities
- Leave buffer for new discoveries

### Ongoing Maintenance (Month 4+):
- New listings: ~5-10 credits/month
- Renewal checks: ~10-15 credits/month (expiring certs)
- Random audits: ~5-10 credits/month
- Total: ~20-35 credits/month (well within 150/year)

### Growth Scenario:
If adding 50 new listings/month:
- New listings: ~25 credits/month (50% verification rate)
- Maintenance: ~15 credits/month
- Total: ~40 credits/month = ~480/year
- Would require upgrading to Standard plan (~$999/year)

## 🔒 Security Best Practices

1. **Never commit API keys**: `.env` files should be in `.gitignore`
2. **Use environment variables**: Preferred method for deployments
3. **Rotate keys periodically**: Generate new key if compromised
4. **Limit permissions**: IAF API keys should only have necessary permissions
5. **Monitor usage**: Check dashboard monthly for unexpected consumption

## 🛠️ Troubleshooting

### "Invalid API Key" Errors:
- Double-check key was copied correctly (no extra spaces)
- Verify plan is active (may take 24h after payment)
- Ensure you're using the correct API endpoint

### "Insufficient Credits" Errors:
- Check current usage in IAF dashboard
- Verify monthly reset occurred
- Consider upgrading plan if consistently exceeding limits

### Connection/Timeout Errors:
- Check internet connectivity
- Verify API endpoint is correct
- Try again later (may be temporary server issue)

### No Matches Found:
- Try variations of business name (remove "Ltd", "Inc", etc.)
- Search by location alone to see what's in database
- Consider that some companies may not be in IAF database yet

## 📞 Support & Resources

- **IAF CertSearch Support**: Contact via website dashboard
- **API Documentation**: Available in IAF developer portal (when available)
- **TSTR.directory**: Monitor enrichment_cron.log for verification activity
- **Community**: Check IAF forums for best practices

## 💰 Cost Justification

### Investment: ~$499/year (~$42/month)
### Returns:
1. **Increased Trust**: Verified badges increase user confidence
2. **Higher Conversion**: Trusted laboratories get more inquiries
3. **Premium Opportunities**: Potential for verified listing upgrades
4. **Competitive Advantage**: Differentiates from unverified directories
5. **Data Quality**: Improves overall dataset reliability

### Break-even Analysis:
- If verification leads to just **1 additional premium listing/month** at $50/listing
- Monthly revenue: $50
- Monthly cost: $42
- **Net profit: $8/month** (after just 1 conversion)
- Realistic expectation: Much higher conversion rates

---
*Guide Updated: 2026-05-25*
*Based on: IAF API Integration Plan and production requirements*