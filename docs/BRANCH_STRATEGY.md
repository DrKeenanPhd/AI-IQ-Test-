# AI IQ Test - Branch Strategy & Workflow

**Established:** September 4, 2025  
**Purpose:** Prevent branch drift and establish clear development workflow

## Branch Structure

### 1. Production Branch
- **Purpose:** Live deployment source for Vercel
- **URL:** https://ai-iq-frontend.vercel.app/
- **Protection:** Only accepts PRs from dev branch
- **Versioning:** Tagged releases (v0.1.0, v0.2.0, etc.)
- **Rollback:** Can revert to any tagged version

### 2. Dev Branch  
- **Purpose:** Integration testing and preview deployments
- **Preview URL:** [To be configured with Vercel]
- **Testing:** User acceptance testing before production
- **CI/CD:** Automated builds and lint checks
- **Merge Source:** Accepts changes from local feature branches

### 3. Local Feature Branches
- **Naming:** `devin/{timestamp}-{feature-slug}`
- **Purpose:** Active development and experimentation
- **Lifespan:** Temporary, deleted after merge to dev
- **Testing:** Local development server testing

## Development Workflow

### Phase 1: Local Development
```bash
# Create feature branch from dev
git checkout dev
git pull origin dev
git checkout -b devin/$(date +%s)-feature-name

# Develop and test locally
npm run dev  # Frontend
poetry run fastapi dev app/main.py  # Backend

# Commit changes
git add specific-files
git commit -m "Descriptive commit message"
```

### Phase 2: Dev Branch Integration
```bash
# Push to dev branch for preview
git checkout dev
git merge devin/timestamp-feature-name
git push origin dev

# Verify preview deployment works
# User tests via dev branch preview URL
```

### Phase 3: Production Release
```bash
# Create PR: dev → production
# Wait for CI checks to pass
# User approval required
# Merge to production
# Tag release
git tag v0.1.0
git push origin v0.1.0
```

## Preview & Testing Strategy

### Local Testing (Developer)
- Both frontend and backend running locally
- Manual QA of all features and UI changes
- Lint and build verification before commits

### Dev Branch Testing (User)
- Vercel preview deployment from dev branch
- User acceptance testing via preview URL
- Feedback loop for iterations

### Production Deployment
- Only after dev branch approval
- Automated deployment via Vercel
- Version tagged for rollback capability

## Version Management

### Semantic Versioning
- **v0.1.0** - Initial UI improvements (logo, CTA, widget removal)
- **v0.2.0** - Next major feature set
- **v0.x.y** - Bug fixes and minor improvements

### Rollback Process
```bash
# Emergency rollback
git checkout production
git reset --hard v0.0.9  # Previous stable version
git push origin production --force

# Or revert specific commits
git revert commit-hash
git push origin production
```

## Documentation Requirements

### Each Branch Must Include:
- **Action Plans:** Clear development objectives
- **Change Logs:** What was modified and why
- **Testing Results:** Verification of functionality
- **Known Issues:** Any limitations or bugs

### File Locations:
- `docs/DIFF_REPORT.md` - Branch comparison analysis
- `docs/BRANCH_STRATEGY.md` - This workflow document
- `docs/DEV_BRANCH_LOGS.md` - Development session logs
- `docs/RELEASE_NOTES_vX.Y.Z.md` - Version-specific changes

## Drift Prevention

### Automated Checks:
- Lint and build verification on all branches
- CI/CD pipeline prevents broken deployments
- Required PR reviews for production changes

### Manual Verification:
- Regular branch comparison reports
- User testing at each stage
- Documentation updates with each release

### Communication Protocol:
- Clear commit messages describing changes
- PR descriptions with before/after comparisons
- User approval required for production deployments

## Emergency Procedures

### Broken Production Deployment:
1. Immediate rollback to last known good version
2. Investigate issue on dev branch
3. Fix and test thoroughly before re-deployment
4. Post-mortem documentation

### Dev Branch Issues:
1. Reset dev branch to last stable commit
2. Re-apply changes incrementally
3. Test each change before proceeding
4. Update documentation with lessons learned

## Success Metrics

### Workflow Effectiveness:
- Zero unplanned production issues
- Consistent preview → production experience
- Clear audit trail of all changes
- User confidence in deployment process

### Branch Health:
- Dev branch always deployable
- Production branch always stable
- Clear separation of concerns
- Minimal merge conflicts

## Current Deployment URLs

### Production
- **URL:** https://ai-iq-frontend.vercel.app/
- **Branch:** production
- **Status:** Active deployment
- **Version:** v0.1.0 (tagged)

### Development
- **Target URL:** https://ai-iq-frontend-git-dev-drkeenanphd.vercel.app/
- **Branch:** dev
- **Status:** Needs configuration (currently 404)
- **Version:** Latest dev commits

### Features
- **280px Logo:** ✅ Implemented in both branches
- **VAPI Widget Removal:** ✅ Implemented in both branches  
- **CTA Button Repositioning:** ✅ Implemented in both branches
- **Lint Fixes:** ✅ Zero errors remaining
