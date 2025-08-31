# AI IQ Frontend Deployment Guide

## Vercel Deployment Configuration

### Prerequisites
- Vercel account configured
- Domain `aiiq.aiaugmented.net` configured in Cloudflare
- Backend API running at `https://app-oxlftweu.fly.dev`

### Environment Variables
Set these in Vercel Dashboard → Project Settings → Environment Variables:

```
VITE_API_URL=https://app-oxlftweu.fly.dev
```

### Domain Configuration
1. **Vercel Dashboard**: Add custom domain `aiiq.aiaugmented.net`
2. **Cloudflare DNS**: Add CNAME record pointing to Vercel
3. **SSL**: Automatic via Vercel

### Deployment Commands
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy to production
vercel --prod

# Or deploy via Git integration (recommended)
# Push to main branch triggers automatic deployment
```

### Build Configuration
- **Framework**: Vite
- **Build Command**: `npm run build`
- **Output Directory**: `dist`
- **Install Command**: `npm install`

### Post-Deployment Verification
1. Test authentication with GHL contacts
2. Verify API connectivity to backend
3. Test responsive design on mobile/tablet/desktop
4. Confirm voice integration components render when data is available

### Troubleshooting
- **Build Errors**: Check TypeScript compilation with `npm run build`
- **API Issues**: Verify CORS settings in backend
- **Domain Issues**: Check Cloudflare DNS propagation
- **Authentication**: Verify GHL webhook endpoints are accessible

### Production URLs
- **Frontend**: `https://aiiq.aiaugmented.net`
- **Report Pages**: `https://aiiq.aiaugmented.net/report/{contact_id}`
- **Backend API**: `https://app-oxlftweu.fly.dev`
