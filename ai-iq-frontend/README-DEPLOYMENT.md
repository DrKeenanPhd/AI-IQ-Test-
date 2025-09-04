# AI IQ Test Frontend - Deployment Guide

## Vercel Deployment Configuration

### Production Deployment
- **URL:** https://ai-iq-frontend.vercel.app/
- **Branch:** production
- **Root Directory:** ai-iq-frontend
- **Framework:** Vite
- **Build Command:** npm run build
- **Install Command:** npm ci
- **Output Directory:** dist

### Environment Variables
```
VITE_API_URL=https://app-oxl-ftweu.fly.dev
```

### Dev Branch Deployment (Option B - Separate Project)
- **Target URL:** https://ai-iq-frontend-dev.vercel.app/
- **Branch:** dev (as production branch of separate project)
- **Configuration:** Identical to production but deploys from dev branch
- **Project Name:** ai-iq-frontend-dev

## Vercel Configuration Files

### vercel.json
Located at `ai-iq-frontend/vercel.json` - handles SPA routing:
- Rewrites all routes to index.html
- Security headers configured

### vite.config.ts
Located at `ai-iq-frontend/vite.config.ts` - Vite build configuration:
- Path aliases configured
- Server settings for development

## Build Process
1. Install dependencies: `npm ci`
2. Run linting: `npm run lint`
3. Build application: `npm run build`
4. Output generated in `dist/` directory

## Deployment Triggers
- Push to production branch triggers production deployment
- Push to dev branch triggers dev project deployment
- Pull requests create preview deployments

## Version Management
- Production releases tagged with semantic versioning (v0.1.0, v0.2.0, etc.)
- Tags created after successful production deployments
- Rollback capability via git tags

## Troubleshooting Production Deployment
If production deployment shows old UI despite having commits:
1. Check Vercel project settings:
   - Production Branch should be "production"
   - Root Directory should be "ai-iq-frontend"
   - Framework Preset should be "Vite"
2. Verify build settings:
   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm ci`
3. Check environment variables are set
4. Manually redeploy latest commit in Vercel dashboard
5. Clear Vercel build cache if needed

## Dev Branch Deployment Setup
To create separate dev project:
1. Create new Vercel project: ai-iq-frontend-dev
2. Connect same GitHub repo
3. Set Production Branch to "dev"
4. Configure same build settings as production
5. Set same environment variables
6. Deploy and verify functionality

## Current Status
- Production: v0.1.0 tagged, needs redeploy to show UI improvements
- Dev: Needs separate Vercel project configuration
- Both branches have UI improvements: 280px logo, removed widget, repositioned CTA
