# 🤖 AGENT REFERENCE: OPENCODE

> **NOTE**: This is a reference document for the OpenCode agent.
> **Context**: `AI_PROJECTS_SPACE` System

---

## 🧠 OPENCODE MODEL CAPABILITIES

### **GPT 5.1 Codex** (`opencode/gpt-5.1-codex`) - **PRIMARY**
- **Strengths**: Modern web frameworks (React, Astro), Tailwind CSS, UI patterns.
- **Cost**: $1.07/1M input, $8.50/1M output.
- **Use for**: UI components, styling, landing pages.

### **Qwen3 Coder** (`opencode/qwen3-coder`) - **BUDGET**
- **Strengths**: Bulk code generation, repetitive tasks.
- **Cost**: $0.45/1M input, $1.50/1M output.
- **Use for**: Scaffolding, bulk files.

### **Claude Sonnet 4.5** (`opencode/claude-sonnet-4-5`) - **COMPLEX**
- **Strengths**: Reasoning, system design, API integration.
- **Cost**: $3.00/1M input, $15.00/1M output.
- **Use for**: DB schema, Analytics, Architecture.

---

## 🔄 WORKFLOW PATTERNS

### **Vibe Coding Pattern**
```
Create a modern directory website with:
- Hero section with gradient background
- Category cards with hover effects
- Search functionality with autocomplete
- Responsive design using Tailwind CSS
```

### **Plan Mode**
Use `<TAB>` to switch to Plan mode for complex features.

### **Continuity Workflow**
1. **Start**: `./resume.sh` (or `./bootstrap.sh TSTR.site`)
2. **Work**: `./checkpoint.sh "label"`
3. **Handoff**: `./handoff.sh <agent> <reason>`

### **Database Operations**
```bash
cd SYSTEM/state
python3 db_utils.py task-add <project> <description>
python3 db_utils.py learning-add "Learning" "tag" 5 "tags"
```

---

## 🛠️ CONFIGURATION

### **Recommended Config**
```json
{
  "model": "opencode/gpt-5.1-codex",
  "provider": {
    "opencode": {
      "models": {
        "gpt-5.1-codex": {
          "options": { "temperature": 0.7, "maxTokens": 8192 }
        }
      }
    }
  }
}
```
