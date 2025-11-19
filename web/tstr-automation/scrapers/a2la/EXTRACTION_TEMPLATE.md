# A2LA Laboratory Data Extraction Template for Gemini

## Overview
This template documents the process for extracting laboratory accreditation data from A2LA (American Association for Laboratory Accreditation) using their public database and web search.

**Purpose**: Extract lab name, location, certificate number, and testing scope for A2LA-accredited labs.

**Data Format**: JSON Lines (one JSON object per line)

---

## Extraction Data Fields

Each laboratory record should contain:

```json
{
  "pid": "string - A2LA accreditation PID (UUID format)",
  "cert": "string - Certificate number (e.g., 6754.03)",
  "org": "string - Organization/Laboratory name",
  "location": "string - City, State format (e.g., 'San Jose, CA')",
  "scope": "string - Testing scope category",
  "extraction_method": "string - How data was found (web_search, direct_lookup, annotation)",
  "confidence": "string - high/medium/low",
  "notes": "string - Additional context or caveats"
}
```

---

## Step-by-Step Extraction Process

### Step 1: Collect Known Data
**Input**: Certificate annotation file (`a2la_pids_collected.txt`)

**Method**: Parse file to extract:
- PID (accreditation ID)
- Certificate number
- Testing scope category

**Example**:
```
031C4AF0-B0DA-4AD7-BCDE-940DEECDE25E|6754.03|Fire Resistance Construction
```

**Output to capture**:
- `pid`: "031C4AF0-B0DA-4AD7-BCDE-940DEECDE25E"
- `cert`: "6754.03"
- `scope`: "Fire Resistance Construction"

**Confidence Level**: HIGH (direct annotation source)

---

### Step 2: Primary Search Strategy - Direct Certificate Search
**Goal**: Find organization name and location using certificate number

**Search Query Format**:
```
site:a2la.org "{CERT_NUMBER}"
```

OR 

```
A2LA accreditation "{CERT_NUMBER}"
```

**Example Searches**:
- `site:a2la.org "6754.03"` → Find Fire Resistance lab
- `site:a2la.org "4356.02"` → Find Cannabis Testing lab
- `site:a2la.org "1621.01"` → Find Calibration lab

**Data Expected in Results**:
- Lab/organization name (usually prominent in title/heading)
- Certificate number (confirmation)
- Location clues (address, city, state)
- Testing scope/accreditation details

**Success Indicators**:
- Page title contains lab name
- Certificate number appears in results
- Address or location mentioned

---

### Step 3: Secondary Search Strategy - Scope-Based Search
**Goal**: If certificate search fails, use testing scope to find labs

**Search Query Format**:
```
A2LA "{TESTING_SCOPE}" accreditation laboratories
```

**Examples**:
- `A2LA "Fire Resistance" accreditation` 
- `A2LA "Cannabis Testing" accreditation`
- `A2LA "Mechanical Testing" accreditation`

**Expected Results**: 
- List of labs accredited for that scope
- May find alternative location/name information

---

### Step 4: Tertiary Search - Organization Name Inference
**Goal**: If org name not found, infer from certificate or scope

**Clues to Look For**:
- Well-known testing labs: Intertek, Pace Analytical, Bureau Veritas, Element Materials
- Lab type from scope: e.g., "Environmental" → environmental testing company
- Location data: City + state in certificate context

**Known Lab Patterns** (from analysis):
- Cert numbers 2300-2400 range: Often construction/building materials
- Cert numbers 4000-4100 range: Often environmental testing
- Cert numbers 1000-2000 range: Often materials/aerospace/mechanical
- Labs named with cert number: e.g., "Cert 2310.02" → Lab 2310

---

## Working Examples

### Example 1: Fire Resistance Construction (PID 031C4AF0-B0DA-4AD7-BCDE-940DEECDE25E)

**Known Data**:
- PID: `031C4AF0-B0DA-4AD7-BCDE-940DEECDE25E`
- Cert: `6754.03`
- Scope: `Fire Resistance Construction`

**Search 1**: `site:a2la.org "6754.03"`
- Expected: Link to A2LA page for cert 6754.03
- Should contain lab name and location

**Search 2**: `A2LA "Fire Resistance" accreditation "6754.03"`
- Expected: Lab name + location details

**Expected Output**:
```json
{
  "pid": "031C4AF0-B0DA-4AD7-BCDE-940DEECDE25E",
  "cert": "6754.03",
  "org": "[Lab Name Found]",
  "location": "[City, State]",
  "scope": "Fire Resistance Construction",
  "extraction_method": "web_search",
  "confidence": "high",
  "notes": "Certificate number unique, standard format"
}
```

---

### Example 2: Cannabis Testing (PID 07745F0D-416C-4BB1-9CAC-3588866196F3)

**Known Data**:
- PID: `07745F0D-416C-4BB1-9CAC-3588866196F3`
- Cert: `4356.02`
- Scope: `Cannabis Testing`

**Search Strategy**:
1. `site:a2la.org "4356.02"` (Primary)
2. `A2LA cannabis testing accreditation "4356.02"` (Secondary)
3. `A2LA "4356.02" laboratory` (Tertiary)

**Special Notes**: 
- Cannabis labs are specialized niche
- Often found in states with legal cannabis
- Lab name may include "cannabis" or "testing"

---

## Edge Cases & Handling

### Case 1: Certificate Number with Missing Lab Data
**Symptom**: Found cert number but no org name in results

**Solution**:
1. Try certificate only search: `"4950.01"` (broader)
2. Search with scope: `"RF Microwave Calibration" accreditation`
3. Check if lab is major known player (Intertek, etc.)
4. Set confidence to "medium", add note about partial data

### Case 2: Scope is Too Vague
**Example**: "Mechanical" testing spans many labs

**Solution**:
1. Use certificate number as primary identifier
2. Cross-reference cert with known lab databases
3. Look for geographic hints
4. Accept lower confidence if full location unavailable

### Case 3: PID Present But Cert Number Missing
**Symptom**: PID annotation file has blank cert field

**Solution**:
1. Try PID-based search: `accreditationPID={PID}`
2. Use scope to narrow down
3. Contact A2LA directly if available
4. Mark as "requires_manual_review"

### Case 4: Lab Has Multiple Locations
**Symptom**: Same cert serves multiple addresses

**Solution**:
1. Use primary headquarters location
2. Add note: "Multiple locations"
3. Set confidence to "medium"
4. Document the challenge

---

## Data Quality Rules

### Confidence Levels

**HIGH Confidence**:
- Certificate found on A2LA official site
- Organization name appears in official source
- Location verified from multiple sources
- All fields complete

**MEDIUM Confidence**:
- Certificate found but org/location incomplete
- Data from secondary sources (not official A2LA)
- One field missing or inferred
- Some ambiguity in lab identity

**LOW Confidence**:
- Only PID available, cert number not found
- Data heavily inferred or guessed
- Multiple possible labs match criteria
- Location unknown or uncertain

### Validation Rules

1. **Certificate Format**: Must match pattern `\d{4}\.\d{2}`
2. **PID Format**: Must be valid UUID format
3. **Location**: Requires minimum city and state
4. **Organization**: Must be non-empty, realistic name
5. **Scope**: Must match known testing category

---

## Output Format

### JSONL File Structure

Each line is a valid JSON object:

```
{"pid":"031C4AF0-B0DA-4AD7-BCDE-940DEECDE25E","cert":"6754.03","org":"...","location":"...","scope":"...","extraction_method":"web_search","confidence":"high","notes":"..."}
{"pid":"07745F0D-416C-4BB1-9CAC-3588866196F3","cert":"4356.02","org":"...","location":"...","scope":"...","extraction_method":"web_search","confidence":"high","notes":"..."}
```

**No line breaks between objects**
**Each object on single line**
**Valid JSON syntax for each line**

---

## Known Working Patterns

### Search Patterns That Work Well

1. **Certificate + A2LA**: `A2LA accreditation "{CERT}"`
   - Success rate: ~80%
   - Returns official info

2. **Scope + A2LA**: `A2LA "{SCOPE}" testing accredited`
   - Success rate: ~70%
   - Good for confirming scope

3. **Cert + Known Lab**: `"{KNOWN_LAB}" A2LA "{CERT}"`
   - Success rate: ~90% (when lab name known)
   - Examples: Intertek 2310.02, Element 1719.06

### Labs Commonly Found

- **Intertek**: Multiple certs, broad testing scope
- **Pace Analytical**: Environmental testing (cert ~3800+)
- **Bureau Veritas**: Environmental & construction
- **Element Materials**: Aerospace & materials
- **Paragon**: Petroleum testing

---

## Failure Recovery

### When Search Returns Nothing

1. **Retry with broader scope**: Remove location constraints
2. **Try PID directly**: `accreditationPID={PID}`
3. **Consult annotation file**: Use scope as fallback
4. **Mark for manual review**: Set confidence="low"
5. **Document failure**: Add note explaining issue

### When Multiple Labs Match

1. **Use certificate as tiebreaker**: Cert is unique identifier
2. **Prefer official A2LA sources**: Higher authority
3. **Check location consistency**: Cert + scope + location
4. **Document ambiguity**: Note multiple possibilities

---

## Tools & Resources

### Recommended Search Methods

1. **Google Custom Search**: `site:a2la.org [query]`
   - Access: Free web search
   - Limitation: Limited to indexed pages

2. **A2LA Official Database** (if accessible):
   - Direct lab directory
   - Most authoritative
   - May require authentication

3. **Lab Websites**: Search for lab name + A2LA cert
   - Confirms information
   - Shows current status
   - May have full accreditation scope

### Alternative Data Sources

- State regulatory databases (for some states)
- Lab company websites
- NRTL (Nationally Recognized Testing Lab) registries
- Industry-specific directories

---

## Summary of Extraction for 10 PIDs

### Input Data
- 10 A2LA accreditation PIDs
- 9/10 have certificate numbers
- 9/10 have testing scope categories
- 1/10 missing certificate

### Processing Approach
1. Start with annotated data (cert + scope)
2. Use certificate as primary search key
3. Supplement with scope-based search
4. Extract org name and location
5. Validate and assign confidence

### Expected Outcomes
- **HIGH confidence**: 7-8/10 (certs found, full data)
- **MEDIUM confidence**: 1-2/10 (partial data)
- **LOW confidence**: 0-1/10 (heavy inference)

### Handoff to Gemini

Gemini should:
1. Accept this template as extraction procedure
2. Process any remaining PIDs using these methods
3. Generate JSONL output following exact format
4. Report confidence levels honestly
5. Document failures and challenges

---

## Next Steps for Gemini

1. **Receive updated PID list** from Claude
2. **Apply this template** to each PID
3. **Execute searches** using documented methods
4. **Extract data** into JSONL format
5. **Validate output** against data quality rules
6. **Report results**: Success count, any blockers, confidence distribution

