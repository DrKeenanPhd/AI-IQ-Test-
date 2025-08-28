# AI IQ Test Results Platform

A dynamic web report page that displays comprehensive AI audit results for businesses, featuring beautiful data visualization and AI widget integration.

## Features

- **Authentication**: Simple login with email, name, and mobile (ready for GHL integration)
- **Beautiful Design**: Dark theme with teal/purple gradients matching modern aesthetics
- **Comprehensive Reports**: Structured around 4 critical pain points and 5 business categories
- **AI Widget Integration**: Placeholder for VAPI HTML code insertion
- **Data Visualization**: Progress bars, scores, recommendations, and priority actions
- **Responsive Design**: Works perfectly on all device sizes

## Architecture

### Backend (FastAPI)
- **Location**: `ai-iq-backend/`
- **Framework**: FastAPI with Pydantic models
- **Database**: Currently in-memory (ready for Supabase integration)
- **API Endpoints**:
  - `POST /auth/login` - User authentication
  - `POST /test-results` - Create test results
  - `GET /test-results/{result_id}` - Get specific test result
  - `GET /users/{user_id}/test-results` - Get user's test results

### Frontend (React + TypeScript)
- **Location**: `ai-iq-frontend/`
- **Framework**: React with TypeScript, Vite, Tailwind CSS
- **UI Components**: shadcn/ui components with Lucide icons
- **Features**: Form validation, loading states, error handling

## Pain Points Analyzed

1. **Can't Scale Without Burning Out**
2. **Invisible in the New Attention Landscape**
3. **Outgunned by AI-Enabled Competitors**
4. **Tech Gap: Underusing AI's Unfair Advantages**

## Business Categories

1. **Website Form and Function**
2. **Social Media Effectiveness**
3. **Digital Presence**
4. **Communication**
5. **Marketing**

## Setup Instructions

### Prerequisites
- Node.js 18+ and npm/pnpm
- Python 3.12+ and Poetry
- Supabase account (for production)

### Backend Setup
```bash
cd ai-iq-backend
poetry install
poetry run fastapi dev app/main.py
```

### Frontend Setup
```bash
cd ai-iq-frontend
npm install
npm run dev
```

### Environment Variables

#### Backend (.env)
```
# Add when integrating with Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key

# Add when integrating with GHL
GHL_API_KEY=your_ghl_api_key
GHL_LOCATION_ID=your_ghl_location_id
```

#### Frontend (.env)
```
VITE_API_URL=http://localhost:8000
```

## Supabase Integration

1. Create a new Supabase project
2. Run the SQL schema from `supabase-schema.sql`
3. Update backend environment variables
4. Replace in-memory database with Supabase client

## GHL Integration

The authentication system is designed to integrate with GoHighLevel:
- User signup creates/updates GHL contacts
- Mobile number and email sync with GHL
- Ready for monthly subscription billing

## AI Widget Integration

The report includes a placeholder section where users can insert their VAPI HTML code:
- Dashed border container for easy identification
- Instructions for code insertion
- Responsive design maintains layout integrity

## Deployment

### Backend Deployment
```bash
# Deploy to Fly.io (FastAPI projects)
cd ai-iq-backend
# Ensure all dependencies are in pyproject.toml
# Deploy using built-in deployment tools
```

### Frontend Deployment
```bash
cd ai-iq-frontend
npm run build
# Deploy dist/ folder to hosting platform
```

## Sample Data Structure

The application generates comprehensive test results including:
- Pain point scores and severity levels
- Category breakdowns with strengths/weaknesses
- Strategic recommendations
- Priority action items
- Overall AI IQ score

## Development Notes

- Backend uses in-memory storage for proof of concept
- Frontend matches reference design aesthetic perfectly
- All components are responsive and accessible
- Error handling and loading states implemented
- Ready for production deployment with minimal changes

## Recent Updates

### ✅ GHL Integration Complete
- **Authentication Sync**: User signup/login automatically creates/updates GHL contacts
- **Dynamic Test Parameters**: Extract test parameters from GHL contact custom fields
- **Results Storage**: Test results automatically saved to GHL custom fields
- **Webhook Support**: Handle form submissions from GHL with automatic test generation

### ✅ Dynamic Report Structure
- **Adaptive Layouts**: Grid automatically adjusts based on number of categories (3, 5, or more)
- **Custom Sections**: Industry-specific and company-size-specific insights
- **Expandable Content**: Sections grow/shrink based on content amount
- **Configurable Parameters**: JSON-based configuration for test weights and thresholds

### ✅ Enhanced Backend Architecture
- **Modular Design**: Separate files for models, GHL client, and test engine
- **Type Safety**: Full Pydantic model validation with enums and structured data
- **Flexible Scoring**: Parameter-based scoring with configurable weights
- **Error Handling**: Graceful degradation when GHL credentials unavailable

## Next Steps

1. **Supabase Integration**: Replace in-memory database for production persistence
2. **VAPI Integration**: Enable AI widget functionality
3. **Advanced Analytics**: Add reporting dashboard for test results trends
4. **A/B Testing**: Implement test variations for optimization
