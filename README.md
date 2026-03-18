# Netherworld Navigator - Cloud Deployment

## Vercel Deployment

This is the cloud-ready version of Netherworld Navigator, configured for Vercel deployment.

### Features
- ✅ Serverless Python API
- ✅ Static frontend hosting
- ✅ CORS configured
- ✅ Multi-state legal queries
- ✅ State law link integration

### Deploy to Vercel

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Deploy:
   ```bash
   cd netherworld-navigator-cloud
   vercel --prod
   ```

3. Follow the prompts to connect your GitHub account and deploy.

### API Endpoints
- `/api/health` - Health check
- `/api/search?q=query` - Search with state law links
- `/api/initialize` - System initialization

### Local Development
```bash
vercel dev
```

Then visit http://localhost:3000

