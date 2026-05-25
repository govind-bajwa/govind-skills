# Crystallize — Framework Engine Reference

This file is the backend of the Crystallize skill. It contains the thinking frameworks the skill auto-selects from. These frameworks are NEVER exposed to the user by name unless naming them adds value. They generate the questions you ask and the analysis you perform.

---

## Stage 1 Frameworks

### SCQA (Situation-Complication-Question-Answer)
**Purpose:** Force-fit narrative structure onto raw, unstructured input.

From the user's brain dump, extract:
- **Situation:** What is the current state of things? What context exists?
- **Complication:** What's the tension, gap, or problem? What changed or is missing?
- **Question:** What needs to be resolved? What decision or action is implied?
- **Answer:** What direction is the user already leaning toward (even if vague)?

If SCQA slots are empty after the user's initial dump, your follow-up questions should target the empty slots.

### Cynefin Complexity Assessment
**Purpose:** Determine how deep the session needs to go.

Assess the idea against four domains:

| Domain | Signal | Session Depth |
|--------|--------|---------------|
| **Simple** | Clear cause-effect. User knows what they want, just needs structure. Few moving parts. | Light: Stages 1-2-3-5 |
| **Complicated** | Knowable but needs analysis. Multiple components with non-obvious interactions. Expert knowledge helps. | Standard: All stages |
| **Complex** | Emergent. The user doesn't fully know what they want yet. Many interdependencies. The act of exploring changes the idea. | Deep: All stages, extended Stage 4 |
| **Chaotic** | Urgent, no clear patterns. User needs to act NOW and make sense later. | Action-first: Stages 1-5, components retrofitted |

**How to read the signals:**
- User says "I know exactly what I want, I just need to organize it" → probably Simple
- User describes multiple pieces that need to fit together → probably Complicated
- User says "I have this jumbled thing and I don't even know what it is yet" → probably Complex
- User says "everything is on fire and I need to move NOW" → probably Chaotic

---

## Stage 2 Frameworks

### DSRP (Distinctions, Systems, Relationships, Perspectives)
**Purpose:** The core analysis engine. Generates the questions that uncover structure.

Apply to the idea as information comes in:

**Distinctions — What is / what isn't:**
- What is included in this idea? What is explicitly NOT included?
- Where are the boundaries? What's in scope vs. out of scope?
- What is this similar to but different from? (Analogies that almost work but don't)
- Questions to ask: "What is this NOT?" / "Where does this end and something else begin?"

**Systems — Parts and wholes:**
- What are the component parts of this idea?
- What larger system does this idea fit into?
- Are there subsystems within components?
- Questions to ask: "What are the pieces of this?" / "What does this fit inside of?"

**Relationships — Connections and causality:**
- What causes what? (A enables B, A blocks C)
- What depends on what? (B can't start until A is done)
- What amplifies or dampens what? (Success in A makes B easier)
- What's the sequence? (A before B before C, or can they run in parallel?)
- Questions to ask: "If this changes, what else is affected?" / "What has to exist before this can work?"

**Perspectives — Different viewpoints:**
- Who are the different stakeholders? How does each see this?
- How does this look from the user's perspective vs. the builder's perspective?
- What would a critic say? What would an enthusiast say?
- What changes if you zoom out? Zoom in?
- Questions to ask: "Who else is affected by this?" / "How would [different person] see this?"

### Gap Analysis Pattern
As DSRP generates insights, track what's defined vs. undefined:

```
[Component] → Defined: what it does, who it's for
             → Undefined: how it connects to [other], technical constraints
```

Your Stage 2 questions should target the undefined gaps, not re-ask about what's already clear.

---

## Stage 3 Frameworks

### MECE Decomposition (Mutually Exclusive, Collectively Exhaustive)
**Purpose:** Ensure the component structure has no overlaps and no gaps.

After identifying components, check:

**Mutually Exclusive test:**
- Does any component overlap with another? (If Component A and Component B both cover "user onboarding," they're not ME)
- Could any two components be merged without losing meaning?
- Fix: Split overlapping functions into distinct responsibilities, or merge redundant components

**Collectively Exhaustive test:**
- Is there anything the idea needs to do that no component covers?
- If you removed all components, would anything be left unaccounted for?
- Walk through the user's original brain dump — is every element captured somewhere?
- Fix: Add missing components, or expand existing ones

**MECE restructuring process:**
1. List all components
2. For each pair, ask: do these overlap? If yes, split or merge.
3. For the whole set, ask: is anything missing? If yes, add.
4. Repeat until clean.

### Pyramid Principle (for Structure Reveal presentation)
**Purpose:** Present the mid-process synthesis answer-first.

When showing the user what you've found:
1. Lead with the core idea (the answer / thesis)
2. Support with the 3-5 major components (the supporting arguments)
3. Under each component, show the evidence/detail

Never build up to a conclusion. State the conclusion, then support it. This is how consultants present — it respects the user's time and tests your synthesis immediately.

---

## Stage 4 Frameworks

### Causal Loop Diagramming
**Purpose:** Map the dynamic relationships between components to find feedback loops, bottlenecks, and leverage points.

**Reinforcing loops (R):** Growth begets growth. Decline begets decline.
- Pattern: A↑ → B↑ → A↑ (or A↓ → B↓ → A↓)
- Example: "More content → more audience → more motivation → more content"
- Significance: These accelerate. They're the engine of growth OR the spiral of decline.

**Balancing loops (B):** Self-correcting. Growth triggers a constraint.
- Pattern: A↑ → B↑ → A↓
- Example: "More features → more complexity → slower development → fewer features"
- Significance: These stabilize. They prevent runaway growth but also cap potential.

**Bottleneck identification:**
- Where does a single component constrain everything downstream?
- What happens if that component fails or is delayed?
- Is there a single point of failure?

**Leverage points:**
- Where would a small change produce a large effect?
- Which component, if improved 2x, would improve the whole system most?

Present loops as: "[Component A] drives [Component B] which reinforces/constrains [Component C]"

### Second-Order Effects Analysis
**Purpose:** Surface what's NOT obvious — the ripple effects.

For each major component or decision:
1. **First-order:** What directly happens? (obvious)
2. **Second-order:** What does THAT cause? (less obvious)
3. **Third-order:** And then what? (often where the real insight is)

Example:
- Decision: Add AI-generated content to the system
- First-order: Content volume increases
- Second-order: Quality variance increases, curation becomes necessary
- Third-order: You now need a quality framework, which changes the entire workflow

Ask: "If this works, what problem does success create?"

### Opportunity Mapping
**Purpose:** Show what each component unlocks.

For each component, map:
- **Immediate value:** What does this enable right away?
- **Adjacent opportunities:** What becomes possible once this exists?
- **Platform potential:** What could others build on top of this?

This reframes components from "things to build" into "capabilities that unlock possibilities."

---

## Stage 5 Frameworks

### Impact Mapping (for Next Actions)
**Purpose:** Connect actions to outcomes so nothing is arbitrary.

Structure next actions as:
- **WHY** → the goal/outcome this serves
- **WHO** → who does this action
- **HOW** → what behavioral change or capability is needed
- **WHAT** → the specific deliverable or action

Every next action should trace back to a component, which traces back to the core idea. If an action doesn't connect, cut it.

### Core-Adjacent-Aspirational Prioritization
**Purpose:** Prevent scope creep by naming what's essential vs. what's optional.

- **Core:** Must exist for the idea to work at all. The minimum viable version.
- **Adjacent:** Makes it significantly better. High value, moderate effort. Should exist in v2.
- **Aspirational:** The dream state. Only after core and adjacent are solid. Often where the most exciting ideas live — but they're traps if pursued too early.

Rule: If someone can't tell the difference between their core and their aspirational, the idea isn't crystallized yet. Push harder on prioritization.

---

## Framework Selection Quick Reference

| What's unclear | Primary framework | What it generates |
|---|---|---|
| The narrative / what the idea even IS | SCQA | Situation, Complication, Question, Answer |
| Complexity / how deep to go | Cynefin | Session routing (light/standard/deep/action-first) |
| Parts and connections | DSRP | Components, boundaries, relationships, perspectives |
| Overlap or gaps in structure | MECE | Clean, complete component decomposition |
| Dynamic interactions | Causal Loops | Feedback loops, bottlenecks, leverage points |
| Ripple effects | Second-Order Effects | Hidden consequences and created problems |
| What each piece enables | Opportunity Mapping | Immediate/adjacent/platform value per component |
| Presentation order | Pyramid Principle | Answer-first structure for the reveal |
| Action prioritization | Impact Mapping | Goal-traced, specific next actions |
| Scope control | Core/Adjacent/Aspirational | What's essential vs. optional vs. dream-state |
