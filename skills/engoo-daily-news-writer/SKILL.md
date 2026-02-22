---
name: engoo-daily-news-writer
description: Transform web articles into Engoo Daily News format for ESL students at levels 4-9. Helps find articles interactively or converts provided URLs into lesson materials. Use when user wants to create ESL lesson materials from news articles, needs vocabulary extraction with definitions, or wants to generate discussion questions for English learners.
---

# Engoo Daily News Writer

Transform web articles into Engoo Daily News lesson format for ESL students.

## Overview

This skill converts web articles into structured English learning materials following the Engoo Daily News format. Each lesson includes:

1. **Vocabulary** (Exercise 1) - 6-8 key terms with definitions, IPA pronunciation, and example sentences
2. **Article** (Exercise 2) - Adapted article content suitable for ESL learners
3. **Discussion** (Exercise 3) - 5 comprehension and conversation questions
4. **Further Discussion** (Exercise 4) - 5 deeper conversation prompts

## Workflow

### Step 1: Article Sourcing

**If user provides a URL:**
Use the `scripts/fetch_article.py` script to fetch and extract article content:

```bash
python3 scripts/fetch_article.py <url>
```

The script outputs JSON with:
- `title`: Article headline
- `description`: Meta description
- `word_count`: Extracted word count
- `content`: Array of paragraphs with `type` and `text`

**If user asks to help find an article:**
- Ask about topics of interest (technology, health, culture, business, science, sports, etc.)
- Suggest ESL-appropriate sources:
  - BBC Learning English
  - Simple English Wikipedia
  - News in Levels
  - Breaking News English
- Consider article difficulty and relevance for ESL learners

### Step 2: Determine Target Difficulty Level

Ask the user to specify the target difficulty level for the lesson:

**If user specifies a level:** Proceed with that level.

**If user doesn't specify:** Ask:
> "What difficulty level would you like for this lesson?
> - **Level 4 (Intermediate)**: ~210 words, very simple and conversational, short sentences
> - **Level 5-6 (Intermediate)**: 250-300 words, informative but accessible
> - **Level 7-8 (Advanced)**: 310-350 words, journalistic tone, complex sentences
> - **Level 9 (Proficient)**: ~350 words, academic and formal, sophisticated vocabulary"

**Note:** Levels 4-6 include a "Questions" section; Levels 7-9 typically omit it and focus on Discussion.

### Step 3: Content Extraction

The script automatically extracts:
- **Title**: The main headline (cleaned of site suffixes)
- **Content**: Essential paragraphs only (limited to ~600 words)
- **Description**: Meta description if available

Then analyze:
- Main topic and key facts
- Vocabulary candidates suitable for the target difficulty level

### Step 4: Vocabulary Generation

Generate **exactly 6 vocabulary items** appropriate for the **target difficulty level**:

```html
<div class="vocabulary-item">
    <div class="vocabulary-word">word <span class="part-of-speech">(noun)</span></div>
    <div class="vocabulary-pronunciation">/ˌprəˌnʌnsiˈeɪʃən/</div>
    <div class="vocabulary-definition">Simple definition suitable for ESL learners.</div>
    <div class="vocabulary-example">Example sentence using the <b>word</b> in context.</div>
</div>
```

**Each vocabulary item must include:**
1. **The Word** - The vocabulary term
2. **Part of Speech** - Noun, Verb, Adjective, Adverb, Phrase, etc.
3. **IPA Pronunciation** - e.g., /ˌvɛriˈeɪʃən/
4. **Concise Definition** - Clear and appropriate for the level
5. **Example Sentence** - With the target word **bolded** using `<b>` tags

**Selection criteria by level:**
- **Level 4**: High-frequency everyday words, concrete nouns, common verbs
- **Level 5-6**: Academic vocabulary, common idioms, phrasal verbs
- **Level 7-8**: Business/technical terminology, nuanced vocabulary
- **Level 9**: Specialized terminology, abstract nouns, sophisticated vocabulary

**Definition guidelines:**
- Write definitions at or below the target difficulty level
- Avoid circular definitions (defining a word with itself)
- Include context-specific meaning when the word has multiple meanings

**Example sentence guidelines:**
- Write sentences at the target difficulty level
- Context should help clarify meaning
- Use the word naturally in a complete sentence
- **Always bold the target word** in the example sentence

### Step 5: Article Adaptation

Adapt the original article to match the **target difficulty level**:

**Level 4 (Intermediate) - ~210 words:**
- **Tone:** Very simple, conversational, and direct
- **Sentence Style:** Short, single-clause sentences. Use bullet points for readability when appropriate.
- **Grammar:** Simple present and past tense, minimal complex structures
- **Vocabulary:** Everyday words, avoid idioms and phrasal verbs
- **Include:** "Fill in the Blanks" exercise (optional) and "Would You Rather?" (optional)

**Level 5-6 (Intermediate) - 250-300 words:**
- **Tone:** Informative but accessible
- **Sentence Style:** Introduce compound sentences, mix of short and medium length
- **Grammar:** Varied tenses, some passive voice, basic transitions
- **Vocabulary:** Common academic words, simple idioms, everyday phrasal verbs
- **Topics:** Lifestyle, health, general interest, light news

**Level 7-8 (Advanced) - 310-350 words:**
- **Tone:** Journalistic and professional
- **Sentence Style:** Complex sentences with multiple clauses, varied lengths
- **Grammar:** Sophisticated transitions, passive voice, conditional structures
- **Vocabulary:** Business/technical terms, nuanced vocabulary, data-rich (percentages, dates, quotes)
- **Topics:** Finance, technology, international relations, serious news
- **Important:** Omit the "Questions" section - go directly to Discussion

**Level 9 (Proficient) - ~350 words:**
- **Tone:** Academic and formal
- **Sentence Style:** Sophisticated sentence variety, professional flow
- **Grammar:** All complex structures, formal register
- **Vocabulary:** Abstract nouns, specialized terminology, sophisticated vocabulary (e.g., "insurrection," "martial law," "proclamation")
- **Topics:** Politics, economics, academic subjects, complex issues
- **Important:** Omit the "Questions" section - go directly to Discussion

**General principles for all levels:**
- Maintain the core story and key facts from the original article
- Preserve engagement and interest
- Keep paragraphs short (2-4 sentences each)
- Structure: 4-7 paragraphs total
- Create a catchy, news-style headline
- **Preserve the original perspective**: If the source article is written in first-person ("I", "we", "my"), retain the first-person perspective in the adapted article. If it's in third-person, keep it in third-person. Do not convert perspectives.

**Formatting:**
Wrap each paragraph in `<p>` tags:
```html
<p>First paragraph of the adapted article.</p>
<p>Second paragraph of the adapted article.</p>
```

### Step 6: Generate Exercises by Level

The exercise structure differs significantly by level. Follow the exact format for each level:

---

## Level 4 Structure

**Exercise 1: Vocabulary (6 items)**
Standard vocabulary format with word, part of speech, IPA, definition, and bolded example sentence.

**Exercise 2: Fill in the Blanks**
Create 6 sentences with blanks for the vocabulary words:
```html
<section id="fill-in-blanks">
    <h2>Fill in the Blanks</h2>
    <p class="fill-blanks-intro">Fill in the blanks to complete the sentences. Use the words from Exercise 1.</p>
    <ol class="questions-list">
        <li>Next, add the sesame ______ to the pan.</li>
        <li>The fruit has a ______ taste, similar to limes.</li>
        ...
    </ol>
    <p class="word-pool"><strong>Words:</strong> word1, word2, word3, word4, word5, word6</p>
</section>
```

**Exercise 3: Article (~200 words)**
Simple, short paragraphs. Use subheadings to break content into digestible sections.

**Exercise 4: Questions (True/False format)**
Create 3-5 True/False questions:
```html
<section id="questions">
    <h2>Questions</h2>
    <ol class="questions-list">
        <li>Shikuwasa taste like limes. A. True B. False</li>
        <li>The fruit is only grown in summer. A. True B. False</li>
        ...
    </ol>
</section>
```

**Exercise 5: Would You Rather?**
Create 3 questions, each with two options:
```html
<section id="would-you-rather">
    <h2>Would You Rather?</h2>
    <p class="wyr-intro">Tell your tutor which of the two options you prefer, and why.</p>
    <ol class="questions-list">
        <li>Which breakfast would you rather have? <span class="wyr-options">pancakes / eggs Benedict</span></li>
        <li>Which fruit would you rather try? <span class="wyr-options">durian / dragon fruit</span></li>
        <li>Where would you rather travel? <span class="wyr-options">Tokyo / Paris</span></li>
    </ol>
</section>
```

**Exercise 6: Discussion (5 questions)**
Open-ended questions encouraging broader discussion of the article's themes.

**Note:** Level 4 does NOT include a "Further Discussion" section.

---

## Level 5 Structure

**Exercise 1: Vocabulary (6 items)**
Standard vocabulary format.

**Exercise 2: Article (~250 words)**
Informative news articles without subheadings, maintaining coherent narrative flow.

**Exercise 3: Questions (Multiple Choice A/B format)**
Create 3 questions with A/B options:
```html
<section id="questions">
    <h2>Questions</h2>
    <ol>
        <li>How many seats does the cinema have? A. 28 B. 48</li>
        <li>Where is the new cinema located? A. In the city center B. At the airport</li>
        <li>When did it open? A. Last month B. Last week</li>
    </ol>
</section>
```

**Exercise 4: Discussion (5 questions)**
Open-ended questions closely related to the article's content.

**Exercise 5: Further Discussion (5 questions)**
Broader questions that encourage general discussion around the article's topic.

---

## Level 6 Structure

**Exercise 1: Vocabulary (6 items)**
Standard vocabulary format.

**Exercise 2: Article (~300 words)**
More detailed articles including statistics, historical background, or nuanced explanations.

**Exercise 3: Questions (Open-ended, short answer)**
Create 3 questions requiring specific information recall:
```html
<section id="questions">
    <h2>Questions</h2>
    <ol>
        <li>What percentage of kindergarten children in Japan had cavities in the latest government survey?</li>
        <li>How many times per day do Japanese children brush their teeth on average?</li>
        <li>What program has helped improve dental health in schools?</li>
    </ol>
</section>
```

**Exercise 4: Discussion (5 questions)**
Open-ended questions directly related to the article, encouraging deeper analysis.

**Exercise 5: Further Discussion (5 questions)**
Broader questions expanding on the article's general theme.

---

## Levels 7-9 Structure

**Exercise 1: Vocabulary (6 items)**
Standard vocabulary format with more sophisticated terminology.

**Exercise 2: Article (310-350 words)**
Complex, journalistic style with sophisticated transitions.

**Exercise 3: Discussion (5 questions)**
Skip the "Questions" section entirely. Go directly to Discussion.

**Exercise 4: Further Discussion (5 questions)**
Deeper philosophical and analytical questions.

---

**Important Structure Summary:**
- **Level 4:** Vocabulary → Fill in the Blanks → Article → Questions (T/F) → Would You Rather? → Discussion (NO Further Discussion)
- **Level 5:** Vocabulary → Article → Questions (A/B) → Discussion → Further Discussion
- **Level 6:** Vocabulary → Article → Questions (Open) → Discussion → Further Discussion
- **Level 7-9:** Vocabulary → Article → Discussion → Further Discussion (NO Questions section)

### Step 7: Generate HTML Output

1. Read the template file from `assets/template.html`
2. Replace all placeholders with generated content based on level:

**Core Placeholders (all levels):**
| Placeholder | Content |
|-------------|---------|
| `{{TITLE}}` | Article title |
| `{{DATE}}` | Current date in format "Month Day, Year" (e.g., "February 22, 2026") |
| `{{DIFFICULTY}}` | Difficulty level (e.g., "Level 4", "Level 7") |
| `{{SOURCE_URL}}` | Original article URL |
| `{{SOURCE_NAME}}` | Source website name |
| `{{SOURCE_AUTHOR}}` | Author attribution (or source name if no author) |
| `{{VOCABULARY_ITEMS}}` | Formatted vocabulary HTML |
| `{{ARTICLE_CONTENT}}` | Formatted article paragraphs |
| `{{DISCUSSION_QUESTIONS}}` | Formatted discussion questions |
| `{{FURTHER_DISCUSSION_QUESTIONS}}` | Formatted further discussion questions |

**Level-Specific Placeholders:**

| Placeholder | Level 4 | Level 5 | Level 6 | Level 7-9 |
|-------------|---------|---------|---------|-----------|
| `{{FILL_IN_BLANKS_SECTION}}` | Fill in the Blanks HTML | empty string | empty string | empty string |
| `{{QUESTIONS_SECTION}}` | True/False Questions HTML | Multiple Choice (A/B) HTML | Open-ended Questions HTML | empty string |
| `{{WOULD_YOU_RATHER_SECTION}}` | Would You Rather HTML | empty string | empty string | empty string |

**Fill in the Blanks Section (Level 4 only):**
```html
<section id="fill-in-blanks">
    <h2>Fill in the Blanks</h2>
    <p class="fill-blanks-intro">Fill in the blanks to complete the sentences. Use the words from Exercise 1.</p>
    <ol class="questions-list">
        <li>Next, add the sesame ______ to the pan.</li>
        <li>The fruit has a ______ taste, similar to limes.</li>
        ...
    </ol>
    <p class="word-pool"><strong>Words:</strong> word1, word2, word3, word4, word5, word6</p>
</section>
```

**Questions Section Formats:**

*Level 4 (True/False):*
```html
<section id="questions">
    <h2>Questions</h2>
    <ol class="questions-list">
        <li>Shikuwasa taste like limes. A. True B. False</li>
        <li>The fruit is only grown in summer. A. True B. False</li>
        ...
    </ol>
</section>
```

*Level 5 (Multiple Choice A/B):*
```html
<section id="questions">
    <h2>Questions</h2>
    <ol class="questions-list">
        <li>How many seats does the cinema have? A. 28 B. 48</li>
        <li>Where is the new cinema located? A. In the city center B. At the airport</li>
        ...
    </ol>
</section>
```

*Level 6 (Open-ended):*
```html
<section id="questions">
    <h2>Questions</h2>
    <ol class="questions-list">
        <li>What percentage of kindergarten children in Japan had cavities in the latest survey?</li>
        ...
    </ol>
</section>
```

**Would You Rather Section (Level 4 only):**
```html
<section id="would-you-rather">
    <h2>Would You Rather?</h2>
    <p class="wyr-intro">Tell your tutor which of the two options you prefer, and why.</p>
    <ol class="questions-list">
        <li>Which breakfast would you rather have? <span class="wyr-options">pancakes / eggs Benedict</span></li>
        <li>Which fruit would you rather try? <span class="wyr-options">durian / dragon fruit</span></li>
        <li>Where would you rather travel? <span class="wyr-options">Tokyo / Paris</span></li>
    </ol>
</section>
```

3. Write the output HTML file to the user's preferred location

### Step 8: Deliver the Output

- Provide the HTML file to the user
- Summarize what was created:
  - Article title and source
  - Number of vocabulary words
  - Difficulty level
  - Word count of adapted article
- Offer to make adjustments if needed

## Template Variables Reference

The HTML template uses these placeholders:

**Core Placeholders (all levels):**
```
{{TITLE}}                    - Article headline
{{DATE}}                     - Publication/creation date
{{DIFFICULTY}}               - Difficulty level (e.g., "Level 4", "Level 7")
{{SOURCE_URL}}               - Link to original article
{{SOURCE_NAME}}              - Name of source publication
{{SOURCE_AUTHOR}}            - Author attribution
{{VOCABULARY_ITEMS}}         - Vocabulary section HTML
{{ARTICLE_CONTENT}}          - Article paragraphs HTML
{{DISCUSSION_QUESTIONS}}     - Discussion questions HTML (all levels)
```

**Level-Specific Placeholders:**
```
{{FILL_IN_BLANKS_SECTION}}   - Level 4: Fill in the Blanks HTML; Levels 5-9: empty string
{{QUESTIONS_SECTION}}        - Levels 4-6: Questions HTML; Levels 7-9: empty string
{{WOULD_YOU_RATHER_SECTION}} - Level 4: Would You Rather HTML; Levels 5-9: empty string
{{FURTHER_DISCUSSION_SECTION}} - Levels 5-9: Further Discussion HTML; Level 4: empty string
{{FURTHER_DISCUSSION_QUESTIONS}} - Content for Further Discussion (used inside section wrapper)
```

## Example Usage

```
User: Convert this article to Engoo format: https://example.com/news-article
User: Create a Level 5 lesson from this URL: https://example.com/news-article
User: Help me find an article about space exploration and make it into a Level 7 lesson
User: I have an article about climate change. Can you turn it into an Engoo lesson for Level 6?
User: Make an Intermediate lesson (Level 4) from this article: https://example.com/news
```

## Resources

### scripts/fetch_article.py

Fetches and extracts essential article content from a URL. Uses only Python standard library (no dependencies).

**Usage:**
```bash
python3 scripts/fetch_article.py <url> [output.json]
```

**Output:** JSON with structure:
```json
{
  "url": "https://...",
  "title": "Article Title",
  "description": "Meta description",
  "word_count": 450,
  "content": [
    {"type": "p", "text": "Paragraph text..."},
    {"type": "h2", "text": "Section heading"}
  ]
}
```

**Features:**
- Extracts only essential content (limited to ~600 words)
- Filters out navigation, ads, and UI elements
- Works with most news sites and blogs
- No external dependencies (pure Python)

### assets/template.html

Contains the HTML template with styling for the Engoo Daily News format. The template is print-friendly and mobile-responsive.

### references/format-guide.md

Detailed reference for vocabulary formatting, article adaptation principles, and question patterns.
