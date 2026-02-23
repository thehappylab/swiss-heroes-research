---
name: feature_dev_workflow
description: Complete feature development workflow from spec to production deployment. Handles branch creation, local development testing, Playwright e2e tests, Coolify preview deployment, and production merge.
---

# Feature Development Workflow

Standard development workflow for implementing features from specifications through production deployment.

## Prerequisites

- Git repository access (GitHub CLI configured)
- Coolify instance access (coolify CLI configured)
- Local development environment (Node.js, build tools)
- Playwright installed for testing

## Workflow Steps

### Phase 1: Requirements & Planning

1. **Get Task/Specification**
   - Read the spec from Outline/Fizzy/GitHub issue
   - Understand acceptance criteria
   - Note any dependencies or blockers

2. **Ask for Clarification (if needed)**
   - Identify unclear requirements
   - Request specific examples or edge cases
   - Confirm technical approach before starting

### Phase 2: Local Development

3. **Create Feature Branch**
   ```bash
   git checkout main
   git pull origin main
   git checkout -b feature/<descriptive-name>
   ```

4. **Develop Locally**
   - Implement the feature
   - Follow existing code patterns
   - Add appropriate error handling
   - Include loading states and UX feedback

5. **Create Playwright Tests**
   - Write tests that verify the spec is implemented
   - Cover happy path and edge cases
   - Test accessibility requirements
   - Example:
     ```javascript
     test('user can complete workflow', async ({ page }) => {
       await page.goto('/feature');
       await expect(page.getByRole('heading')).toContainText('Expected');
     });
     ```

### Phase 3: Local Verification

6. **Run Production Build Locally**
   ```bash
   npm run build
   npm run preview  # or equivalent
   ```

7. **Run E2E Tests**
   ```bash
   npm run test:e2e
   # or
   npx playwright test
   ```

8. **Manual Click-Through Testing**
   - Test the feature in browser
   - Verify responsive design
   - Check error states
   - Validate with production build (not dev server)

### Phase 4: Deployment

9. **Push to GitHub & Create PR**
   ```bash
   git add .
   git commit -m "feat: descriptive commit message"
   git push origin feature/<name>
   gh pr create --title "Feature: ..." --body "..."
   ```

10. **Monitor Coolify Build**
    - PR triggers automatic Coolify preview deployment
    - Wait for build status
    - Check logs if build fails

11. **Verify Preview App**
    - Coolify provides preview URL
    - Test the deployed preview
    - Run smoke tests
    - Verify migrations ran (if applicable)

### Phase 5: Delivery

12. **Report to User**
    - ✅ "Feature implemented and tested"
    - 🔗 "Preview URL: https://..."
    - 📊 "Build status: Success"
    - 🧪 "Tests: X passed"
    - 📝 "Migration: [Yes/No] - details"

13. **Wait for Approval**
    - User reviews preview
    - User requests changes or approves

14. **Merge or Deploy**
    - If approved: `gh pr merge --squash`
    - Monitor production deployment
    - Verify in production

## Migration Handling

Always specify if a migration is required:

```markdown
**Migration Required:** Yes/No

**Migration Details:**
- Type: Database schema / Config / Asset
- Steps: [specific steps or "automatic via CI/CD"]
- Rollback plan: [if applicable]
```

## Output Format

Give users **relevant updates only** — one line per major step:

```
✅ Phase 1: Got spec "Authentication flow"
✅ Phase 2: Created branch feature/auth-v2, implementing...
✅ Phase 3: Local build passed, 2 Playwright tests written
✅ Phase 4: PR created, Coolify build in progress...
✅ Phase 5: Preview ready at https://preview-xyz.thehappylab.net
   → Build succeeded, 2/2 tests passed
   → Migration: Yes - database schema updated
   ⏳ Waiting for your approval to merge
```

## Error Handling

| Issue | Action |
|-------|--------|
| Build fails | Check Coolify logs, fix, push again |
| Tests fail | Fix locally before pushing |
| Spec unclear | Pause and ask user for clarification |
| Migration error | Document rollback, alert user |
| Preview doesn't work | Check env vars, secrets, dependencies |

## Critical Rule: Never Go Silent

**You MUST report status every 2-3 minutes during active work.**

### Error Recovery (CRITICAL)

If ANY step fails, you MUST:
1. **Report the failure immediately** - Don't wait
2. **Explain what went wrong** - Be specific
3. **Propose next steps** - Offer alternatives
4. **Never stop without reporting** - Silence is unacceptable

**Bad example (DON'T DO THIS):**
```
[Tool call fails]
[No response to user]
[User has to ask "what happened?"]
```

**Good example:**
```
❌ Edit failed: Text didn't match exactly (whitespace issue)
✅ Let me read the file again and retry with correct formatting...
✅ Reading file... [retry with exact match]
✅ Edit successful, continuing...
```

### Progress Checkpoints

During long operations, post updates:

```
⏳ Working on migration fix... [2 min]
   → Tried edit, failed on whitespace
   → Retrying with exact match...

⏳ Still working... [4 min]
   → Edit successful
   → Running build now...

✅ Done! Build passed.
```

### If You Get Stuck

If you can't proceed after 2-3 attempts:
1. Report current status
2. Explain what's blocking
3. Ask user for direction

```
⚠️ Stuck on: File edit keeps failing
   → Tried exact match
   → Tried re-reading file
   → Still failing with: "oldText must match exactly"
❓ Should I: (a) Try write instead of edit, (b) Ask you to check the file?
```

## Tool Requirements

This skill requires:
- `gh` CLI (GitHub)
- `coolify` CLI (deployment)
- `playwright` (testing)
- `git`
- Node.js/npm build tools