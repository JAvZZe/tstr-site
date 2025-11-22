# Contributing Guidelines

Thank you for contributing to **Awesome Niche Testing**! This list serves thousands of engineers, procurement professionals, and R&D teams searching for certified testing laboratories. To maintain the highest quality standards, please follow these guidelines carefully.

---

## Submission Review Timeline

Due to the high volume of community submissions and our rigorous verification process, **free community submissions are reviewed on a monthly basis** (typically the first week of each month). Pull requests may take **3-4 weeks** to be reviewed and merged.

**Need your listing live urgently?**  
→ Use the [**Fast Track**](SPONSORSHIP.md#-fast-track-50-one-time) option for 48-hour review and verification ($50 one-time fee).

---

## Eligibility Requirements

### ✅ Eligible Providers

Your laboratory or testing service **must meet ALL** of these criteria:

1. **Physical Laboratory:** Must operate at least one physical testing facility with lab equipment and trained personnel
2. **Active Operations:** Must be currently accepting projects (we verify by calling/emailing)
3. **Verifiable Credentials:** Must hold at least one recognized accreditation:
   - ISO/IEC 17025 (Testing & Calibration)
   - ISO/IEC 17020 (Inspection Bodies)
   - A2LA, UKAS, NATA, NVLAP, or equivalent national accreditation
   - Industry-specific: NADCAP (aerospace), GMP (pharmaceutical), CLIA (clinical)
4. **Public Website:** Must have an active website with contact information
5. **Niche Specialization:** Must offer specialized testing beyond commodity services

### ❌ Not Eligible

- **Software Testing:** QA automation, unit testing frameworks, code coverage tools
- **Pure Consulting Firms:** Companies that outsource all lab work to third parties
- **Defunct Labs:** Closed facilities or labs that have ceased operations
- **Marketing Aggregators:** Directories or brokers that don't operate labs
- **Unaccredited Labs:** Facilities without any recognized third-party accreditation

---

## Submission Process

### Step 1: Search for Duplicates

Before submitting, search the repository to ensure your lab isn't already listed:

```bash
# Search for lab name
Ctrl+F (or Cmd+F) in the README.md file

# Check category sections thoroughly
```

**Duplicate submissions will be closed immediately without review.**

---

### Step 2: Choose Your Category

Select **ONE** primary category for your lab:

- **Biotech & Pharma** — GMP, sterility testing, biocompatibility, pharmaceutical analysis
- **EMC & Electronics** — EMI/EMC, FCC, CE, environmental simulation, DO-160
- **Environmental & Stress** — HALT/HASS, thermal cycling, salt spray, IP ingress, altitude
- **Materials Analysis** — Metallurgy, failure analysis, tensile testing, XRF, ICP-MS
- **Certification Bodies** — Accreditation organizations, notified bodies, standards authorities

**Don't see your category?** [Open an issue](../../issues/new) to request a new category (requires 5+ labs to justify creation).

---

### Step 3: Format Your Submission

Use this **exact template** — submissions that don't follow this format will be rejected:

```markdown
- [**Lab Name**](https://lab-website.com/) - Brief description including key capabilities, certifications, and specializations (max 150 words). Location: City, State/Province, Country.
```

#### ✅ Good Example:

```markdown
- [**Element Materials Technology**](https://www.element.com/) - Global network of EMC, environmental, and dynamics testing labs. Capabilities include FCC/CE certification, MIL-STD-810 testing, DO-160 avionics qualification, and RTCA DO-160G environmental simulation. ISO/IEC 17025 accredited with A2LA and UKAS recognition. Location: Multiple locations (USA, UK, Germany, Singapore).
```

#### ❌ Bad Examples:

```markdown
# Too vague
- [Lab XYZ](https://example.com/) - We do testing.

# Marketing fluff (will be edited or rejected)
- [Lab XYZ](https://example.com/) - The world's leading, best-in-class, award-winning testing laboratory...

# Missing location
- [Lab XYZ](https://example.com/) - ISO 17025 accredited materials testing.

# Dead link
- [Lab XYZ](https://broken-link.com/) - Environmental testing services.
```

---

### Step 4: Provide Verification Data

To expedite review, include this information in your Pull Request description:

```markdown
## Verification Details

**Lab Name:** [Full legal name]  
**Website:** [URL]  
**Primary Location:** [City, State/Province, Country]  
**Phone Number:** [For verification purposes]  

**Accreditations (provide links to certificates or registry entries):**
- [ ] ISO/IEC 17025: [Certificate URL or A2LA/UKAS scope link]
- [ ] ISO/IEC 17020: [Certificate URL]
- [ ] Other: [Specify: NADCAP, GMP, CLIA, etc.]

**Key Capabilities (select all that apply):**
- [ ] EMC/EMI Testing
- [ ] Environmental Simulation (HALT/HASS)
- [ ] Materials Testing (tensile, hardness, metallography)
- [ ] Chemical Analysis (ICP-MS, XRF, GC-MS)
- [ ] Pharmaceutical Testing (HPLC, GMP, sterility)
- [ ] Other: [Specify]

**Target Industries:**
- [ ] Aerospace
- [ ] Automotive
- [ ] Medical Devices
- [ ] Consumer Electronics
- [ ] Industrial Equipment
- [ ] Energy (Oil & Gas, Hydrogen, Renewables)
- [ ] Pharmaceutical/Biotech
- [ ] Other: [Specify]

**Additional Context:**
[Any relevant details: recent expansions, new certifications, specialized equipment]
```

---

### Step 5: Submit Your Pull Request

1. **Fork this repository**
2. **Create a new branch:** `git checkout -b add-[lab-name]`
3. **Add your entry** to the appropriate category section in `README.md` (alphabetical order)
4. **Commit your changes:** `git commit -m "Add [Lab Name] to [Category]"`
5. **Push to your fork:** `git push origin add-[lab-name]`
6. **Open a Pull Request** against the `main` branch
7. **Fill out the verification template** (Step 4) in the PR description

---

## Review Process

### What We Check:

1. **Accreditation Validity:** We verify certificates via A2LA, UKAS, NATA, or equivalent public registries
2. **Website Activity:** Must be live and updated within the last 12 months
3. **Contact Info:** We call/email to confirm the lab is accepting projects
4. **Duplicate Check:** Ensure lab isn't already listed under a different name
5. **Formatting:** Entry follows the template and markdown guidelines

### Possible Outcomes:

- ✅ **Approved & Merged:** Congratulations! Your lab is now listed.
- 🔄 **Changes Requested:** We'll comment on your PR with required fixes.
- ❌ **Rejected:** Lab doesn't meet eligibility criteria (reason provided).
- ⏸️ **Queued:** Submission is valid but in the monthly review backlog.

**Average Review Time (Free Submissions):** 3-4 weeks  
**Fast Track Review Time:** 48 hours ([Learn more](SPONSORSHIP.md))

---

## The Monthly Review Queue

To maintain data quality and prevent spam, free community submissions undergo a thorough verification process:

- **Week 1 of each month:** New submissions reviewed
- **Week 2:** Verification calls/emails sent to labs
- **Week 3:** Accreditation certificates cross-checked
- **Week 4:** Approved PRs merged in batch

**Current Queue Status:** [Check the Projects board](../../projects/1)

**Why the wait?** Each submission requires:
- 15-20 minutes of manual verification
- Phone/email confirmation (labs may take days to respond)
- Certificate validation via third-party registries
- Cross-checking against existing entries

**Can't wait 3-4 weeks?**  
The [Fast Track option](SPONSORSHIP.md#-fast-track-50-one-time) includes:
- Priority review queue (48-hour turnaround)
- Dedicated verification team
- **"✓ Verified"** badge on your listing
- Premium placement within your category

---

## Quality Standards

### Writing Style

- **Factual, not promotional:** Avoid superlatives like "best," "leading," "world-class"
- **Specific capabilities:** List exact standards (ISO 19880-3, SAE J2601) not "hydrogen testing"
- **Concise:** 100-150 words maximum
- **Grammar:** Proper capitalization, punctuation, and spelling

### Examples of High-Quality Entries:

✅ **Excellent:**
```markdown
- [**TÜV SÜD**](https://www.tuvsud.com/) - European notified body for CE marking and global product certification. Capabilities include ISO 19880-3 hydrogen valve testing (700 bar), UN ECE R134 fuel cell vehicle certification, and ISO 11114-4 embrittlement testing. ISO/IEC 17025 accredited with German DAkkS recognition. Operates 20+ testing facilities across Europe and Asia. Location: Munich, Germany (headquarters).
```

✅ **Good:**
```markdown
- [**Intertek**](https://www.intertek.com/) - HALT/HASS, thermal shock, vibration, and combined environmental testing. MIL-STD-810, IEC 60068 compliance. ISO/IEC 17025 accredited. Location: Multiple locations (USA, UK, China).
```

❌ **Poor (will be rejected/edited):**
```markdown
- [Lab Name](https://example.com/) - We're the best testing lab with award-winning services and world-class quality.
```

---

## After Your Submission

### If Approved:

1. **Celebrate!** Your lab is now discoverable by thousands of engineers monthly.
2. **Monitor Traffic:** Use UTM parameters in your URL to track referrals from this list.
3. **Keep Info Current:** Submit a PR if your accreditations or capabilities change.
4. **Consider Upgrading:** [Lab Partner sponsorship](SPONSORSHIP.md#-lab-partner-250month) includes analytics and enhanced visibility.

### If Changes Requested:

1. **Read the feedback carefully** in the PR comments.
2. **Make the requested edits** in your branch.
3. **Push the updates:** `git push origin add-[lab-name]`
4. **Reply to the review comment** to notify maintainers.

### If Rejected:

1. **Don't resubmit immediately** — read the rejection reason.
2. **Address the core issue:** Obtain accreditation, update website, etc.
3. **Reapply after 90 days** once eligibility criteria are met.

---

## Community Guidelines

### Be Professional

- This is a professional directory for B2B services
- No personal attacks or negative comments about competitors
- Disputes about placement or descriptions should be raised via issues, not PR comments

### No Gaming the System

- Do not create fake reviews or testimonials
- Do not submit competitors with inaccurate information
- Do not use multiple accounts to submit the same lab

**Violations result in permanent ban and removal of all associated entries.**

### Respect Maintainer Decisions

- Maintainers have final say on inclusion/exclusion
- Decisions are based on publicly verifiable data, not opinions
- Appeals can be submitted via email (see SPONSORSHIP.md for contact info)

---

## Beyond Pull Requests

### Report Issues

Found a dead link, outdated accreditation, or incorrect information?

1. **Open an issue:** [Report a problem](../../issues/new?template=report-issue.md)
2. **Provide evidence:** Link to expired certificate, screenshot of broken website, etc.
3. **We'll investigate** and update/remove the entry within 7 days

### Suggest Improvements

Have ideas for new categories, better organization, or additional features?

1. **Open a discussion:** [Start a conversation](../../discussions)
2. **Community input welcome** — we prioritize high-value suggestions
3. **Major changes require 10+ upvotes** before implementation

### Newsletter & Updates

Want to know when your submission is merged or when new categories launch?

- **Watch this repo** (click "Watch" button at top)
- **Subscribe to the newsletter:** [Join the mailing list](https://tstr.site/newsletter)
- **Follow on Twitter/LinkedIn:** [@TSTRsite](https://twitter.com/tstrsite)

---

## Legal & Ethics

### Conflicts of Interest

- Maintainers will not review submissions for labs they own or are employed by
- Third-party reviewers validate sponsored entries to prevent bias

### Data Privacy

- Phone numbers provided for verification are **never** published
- Email addresses are only used for submission confirmation
- We comply with GDPR and CCPA data protection regulations

### Intellectual Property

- By submitting, you confirm you have the right to represent the lab
- Lab logos and trademarks remain property of their respective owners
- This list is licensed under [CC0 1.0 Universal](../LICENSE)

---

## Questions?

**Before asking, check:**
1. [Frequently Asked Questions](SPONSORSHIP.md#frequently-asked-questions) in SPONSORSHIP.md
2. [Existing issues](../../issues) — your question may already be answered
3. [Discussions board](../../discussions) — community-answered questions

**Still need help?**
- **General questions:** [Open a discussion](../../discussions/new)
- **Submission problems:** Comment on your PR
- **Sponsorship inquiries:** sponsors@[your-domain].com
- **Urgent issues:** Email maintainers@[your-domain].com

---

## Thank You!

Your contribution helps engineers worldwide find the right testing services faster. Every verified lab listing saves hours of research time and connects manufacturers with quality testing providers.

**Want to make an even bigger impact?**  
[Become a verified partner](SPONSORSHIP.md) and help us maintain this resource long-term.

---

**Maintained by [TSTR.site](https://tstr.site)** — Advanced search engine for standards-based testing services.
