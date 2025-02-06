# Best practice of Writing Git Commit

---

## **1. Separate Subject Line and Body**

- Use the first line as a concise summary (subject line).
- Follow it with a blank line, then the body if needed.

---

## **2. Keep the Subject Line Short and Informative**

- Limit it to **50 characters or less**.
- Use the **imperative mood** (e.g., "Add feature," not "Added feature").

---

## **3. Explain the "What," "Why," and "How" in the Body**

- The **"what"** is usually in the subject line.
- Use the body to explain the **"why"** (the problem solved) and optionally the **"how"** (important technical notes).
- Keep lines in the body under **72 characters**.

---

## **4. Be Specific**

- Focus on what the commit accomplishes.
- Avoid vague phrases like "Fix stuff" or "Update code."

---

## **5. Use a Consistent Format**

Example:

```plaintext
Short, descriptive subject line

Optional body that explains why the change was made.
Use bullet points if you made multiple related changes:
- Fixed a bug where X
- Improved performance of Y by doing Z
```

---

## **6. Commit Small and Logical Units**

- Commit only one logical change at a time.
- Avoid bundling unrelated changes in a single commit.

---

## **7. Reference Issues or Tickets**

- Include references to issue trackers or tickets if applicable (e.g., `Fixes #123`).

---

## **8. Proofread Your Message**

- Review your message before committing for typos and clarity.

---

### Example Commit Messages

**Good:**

```plaintext
Add user authentication API

- Implement OAuth2 for secure logins
- Add endpoint for user login and logout
- Include tests for edge cases
```

**Bad:**

```plaintext
fix stuff
```

# Detailed and Structured Guide With Examples, Explanations, and Scenarios

---

## **1. Commit Message Structure**

A good commit message has **three parts**:

### **a. Subject Line (Header)**

- **Purpose:** Summarizes the change.
- **Rules:**
  - Keep it under **50 characters**.
  - Write in the **imperative mood** (e.g., "Fix bug," "Add feature," not "Fixed bug" or "Added feature").
  - Avoid punctuation (no period at the end).
- **Examples:**
  - ✅ `Fix login button alignment on mobile`
  - ✅ `Add caching layer for database queries`

---

### **b. Blank Line**

- Separate the subject from the body with **one blank line** to ensure proper rendering in tools like GitHub.

---

### **c. Commit Body (Optional)**

- **Purpose:** Provides more context about the change.
- **Rules:**
  - Keep each line **72 characters or fewer** for readability.
  - Focus on the **why** (reason for the change) and **how** (important implementation details).
  - Use bullet points or paragraphs for clarity if you have multiple points.
- **Examples:**

  ```plaintext
  Refactor user session handling

  - Extract session management logic into a helper module
  - Improve session expiration checks for better security
  - Add unit tests to validate session behavior
  ```

---

### **d. Footer (Optional)**

- **Purpose:** References metadata like issue numbers or breaking changes.
- **Format:**
  - Use keywords like `Fixes`, `Resolves`, or `Closes` to auto-link issues in version control systems (e.g., GitHub).
  - For breaking changes, include a `BREAKING CHANGE:` tag.
- **Examples:**

  ```plaintext
  Fix API pagination bug

  Ensure that page offsets return correct results for edge cases.

  Fixes #1234
  ```

  ```plaintext
  Refactor order processing system

  This commit introduces significant changes to the order pipeline.
  Old APIs for order placement will no longer be supported.

  BREAKING CHANGE: Deprecate legacy order APIs
  ```

---

## **2. Imperative Mood Explained**

Writing in the imperative mood means using commands, as if you're giving an instruction to apply the commit.

- ✅ `Add search feature` (imperative, concise)
- ❌ `Added search feature` (past tense)
- ❌ `Adding search feature` (progressive tense)

Why? The commit describes what the change **does when applied**, not what you did.

---

## **3. When to Use the Commit Body**

Use the body for:

- Explaining **why** a change was made if it's not immediately obvious.
- Summarizing **complex changes**.
- Highlighting **potential side effects** or breaking changes.
- Documenting **edge cases** or assumptions.

**Example for Complex Changes:**

```plaintext
Implement file upload validation

Validate uploaded files for:
- Supported file types (PNG, JPEG, PDF)
- Size limit of 5MB
- Malicious content using an antivirus scanner

This ensures better security and prevents storage bloat.
```

---

## **4. Splitting Commits by Logical Changes**

Each commit should represent one **logical unit** of work. Avoid grouping unrelated changes.

### **Example:**

Suppose you:

- Fix a typo in the README.
- Add a new feature.
- Refactor code.

You should create **three separate commits**:

1. `Fix typo in README`
2. `Add user authentication API`
3. `Refactor session handling logic`

Why? It makes reviewing and reverting changes easier.

---

## **5. Avoid Vague Commit Messages**

Be specific about what the commit does. Avoid generic messages.

- ❌ `Update code`
- ❌ `Fix stuff`
- ✅ `Improve API response time by optimizing SQL queries`
- ✅ `Fix null pointer exception in user profile handler`

---

## **6. Handling Bug Fixes**

When fixing bugs, include the **problem, root cause, and solution** in the body.

**Example:**

```plaintext
Fix crash on app startup

The app crashed when loading the user profile due to a null pointer
exception caused by missing configuration values. Added a default
configuration to handle this edge case.
```

---

## **7. Referencing Issues or Tasks**

Reference tickets, issues, or pull requests to provide traceability.

- Format:
  - `Fixes #1234`
  - `Closes #5678`

**Example:**

```plaintext
Add email notifications for new users

Send welcome emails when a user successfully registers.

Fixes #101
```

---

## **8. Best Practices for Teams**

- **Use a style guide:** Agree on a standard like [Conventional Commits](https://www.conventionalcommits.org/).
- **Review commits:** Enforce quality through code reviews.
- **Avoid WIP commits:** Keep incomplete work in local branches or use `git stash`.
- **Rebase before merging:** Squash related commits into a single logical unit.

---

## **9. Real-Life Commit Examples**

### **Bug Fix**

```plaintext
Fix incorrect total in shopping cart

Corrected the calculation logic for subtotal and tax. Previously,
the total displayed was off by a rounding error in edge cases.

Fixes #321
```

### **Feature Addition**

```plaintext
Add feature to export reports as CSV

- Implemented export functionality for report views
- Added unit tests for file formatting and download functionality
- Updated documentation with usage examples
```

### **Refactor**

```plaintext
Refactor payment processing logic

- Moved payment gateway integration into a dedicated service
- Simplified error handling with custom exceptions
- Improved test coverage for edge cases
```

---
