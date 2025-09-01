import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { TrendingUp, CheckCircle, AlertTriangle, Clock, Mic, Target } from 'lucide-react'
import './App.css'

interface UserAuth {
  email: string
  name: string
  mobile: string
}

interface TestResult {
  id: string
  user_email: string
  user_name: string
  contact_id?: string
  pain_points: Record<string, any>
  categories: Record<string, any>
  overall_score: number
  recommendations: string[]
  custom_sections?: Record<string, any>
  report_metadata?: Record<string, any>
  created_at: string
  
  session_metadata?: {
    vapi_call_id: string
    call_duration?: number
    agent_confidence_score?: number
    return_user?: boolean
    previous_test_count?: number
    user_website_url?: string
  }
  
  voice_summary?: {
    verbal_summary?: string
    conversation_highlights?: string[]
    call_transcript_summary?: string
    agent_recommendations_spoken?: string[]
    client_concerns_expressed?: string[]
  }
  
  api_data_sources?: {
    tools_used?: string[]
    data_quality_score?: number
    analysis_depth?: string
    missing_data_notes?: string[]
  }
  
  subscription_recommendations?: {
    ai_iq_subscription_recommendation?: string
    vip_support_recommendation?: string
    priority_level?: string
    estimated_roi_timeline?: string
  }
  
  roi_analysis?: {
    estimated_monthly_savings: number
    implementation_cost: number
    roi_percentage: number
    payback_period_months: number
    productivity_gains: string[]
    cost_reduction_areas: string[]
    revenue_opportunities: string[]
    risk_mitigation_value: number
  }
  
  detailed_report?: {
    executive_summary: string
    current_state_analysis: Record<string, any>
    recommended_solutions: Array<{
      title: string
      priority: string
      timeline: string
      investment: string
    }>
    implementation_roadmap: Array<{
      phase: string
      duration: string
      focus: string
    }>
    success_metrics: string[]
    next_steps: string[]
    appendix_data?: Record<string, any>
  }
}

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [, setUserId] = useState<string | null>(null)
  const [testResult, setTestResult] = useState<TestResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [activeTab, setActiveTab] = useState<'test-results' | 'roi-analysis' | 'detailed-report'>('test-results')

  const TabButton: React.FC<{ 
    tabId: 'test-results' | 'roi-analysis' | 'detailed-report', 
    number: string, 
    title: string, 
    color: string 
  }> = ({ tabId, number, title, color }) => (
    <button
      onClick={() => setActiveTab(tabId)}
      className={`flex items-center space-x-3 px-6 py-4 rounded-lg transition-all ${
        activeTab === tabId 
          ? `bg-${color}-500/20 border-${color}-500 text-${color}-400` 
          : 'bg-black/50 border-gray-800 text-gray-400 hover:border-gray-700'
      } border-2`}
    >
      <span className={`text-2xl font-bold ${activeTab === tabId ? `text-${color}-400` : 'text-gray-500'}`}>
        {number}
      </span>
      <span className="font-semibold">{title}</span>
    </button>
  )
  
  const [authForm, setAuthForm] = useState<UserAuth>({
    email: '',
    name: '',
    mobile: ''
  })

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(authForm),
      })

      if (!response.ok) {
        throw new Error('Authentication failed')
      }

      const data = await response.json()
      setUserId(data.user_id)
      setIsAuthenticated(true)
      
      const resultResponse = await fetch(`${API_URL}/test-results`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ user_id: data.user_id }),
      })
      
      if (resultResponse.ok) {
        const resultData = await resultResponse.json()
        setTestResult(resultData)
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }


  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical':
        return <AlertTriangle className="w-5 h-5 text-orange-400" />
      case 'high':
        return <AlertTriangle className="w-5 h-5 text-orange-400" />
      case 'medium':
        return <AlertTriangle className="w-5 h-5 text-yellow-400" />
      case 'low':
        return <CheckCircle className="w-5 h-5 text-blue-400" />
      default:
        return <CheckCircle className="w-5 h-5 text-gray-400" />
    }
  }


  const TestResultsTab: React.FC<{ testResult: TestResult }> = ({ testResult }) => (
    <div className="space-y-8">
      <Card className="bg-black/80 border-gray-800 backdrop-blur-sm">
        <CardHeader>
          <CardTitle className="text-white flex items-center space-x-2">
            <AlertTriangle className="w-6 h-6 text-yellow-400" />
            <span>Critical Pain Points</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {Object.entries(testResult.pain_points).map(([key, point]: [string, any]) => (
            <div key={key} className="flex items-start space-x-3 p-4 bg-black/50 rounded-lg">
              {getSeverityIcon(point.severity)}
              <div className="flex-1">
                <h4 className="font-semibold text-white mb-1">{formatPainPointName(key)}</h4>
                <p className="text-gray-300 text-sm mb-2">{point.description}</p>
                <Badge variant={point.severity === 'high' ? 'destructive' : 'secondary'}>
                  Score: {point.score}/100
                </Badge>
              </div>
            </div>
          ))}
        </CardContent>
      </Card>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {Object.entries(testResult.categories).map(([key, category]: [string, any]) => (
          <Card key={key} className="bg-black/80 border-gray-800 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="text-white text-lg">{formatCategoryName(key)}</CardTitle>
              <CardDescription className="text-gray-300">
                Score: {category.score}/{category.max_score}
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="w-full bg-gray-800 rounded-full h-2">
                  <div 
                    className="bg-teal-500 h-2 rounded-full transition-all duration-300" 
                    style={{ width: `${category.score}%` }}
                  />
                </div>
                <p className="text-gray-300 text-sm">{category.description}</p>
                {category.recommendations && category.recommendations.length > 0 && (
                  <div className="mt-3">
                    <h5 className="text-white font-medium mb-2">Recommendations:</h5>
                    <ul className="text-gray-300 text-sm space-y-1">
                      {category.recommendations.map((rec: string, idx: number) => (
                        <li key={idx} className="flex items-start space-x-2">
                          <span className="text-teal-400 mt-1">•</span>
                          <span>{rec}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  )

  const ROIAnalysisTab: React.FC<{ roiData: any }> = ({ roiData }) => (
    <div className="space-y-8">
      {roiData ? (
        <>
          <Card className="bg-black/80 border-gray-800 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="text-white flex items-center space-x-2">
                <TrendingUp className="w-6 h-6 text-blue-400" />
                <span>ROI Analysis</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div className="bg-blue-500/20 border border-blue-500 rounded-lg p-4">
                    <h4 className="text-blue-400 font-semibold mb-2">Monthly Savings</h4>
                    <p className="text-2xl font-bold text-white">${roiData.estimated_monthly_savings?.toLocaleString()}</p>
                  </div>
                  <div className="bg-blue-500/20 border border-blue-500 rounded-lg p-4">
                    <h4 className="text-blue-400 font-semibold mb-2">ROI Percentage</h4>
                    <p className="text-2xl font-bold text-white">{roiData.roi_percentage?.toFixed(1)}%</p>
                  </div>
                </div>
                <div className="space-y-4">
                  <div className="bg-blue-500/20 border border-blue-500 rounded-lg p-4">
                    <h4 className="text-blue-400 font-semibold mb-2">Implementation Cost</h4>
                    <p className="text-2xl font-bold text-white">${roiData.implementation_cost?.toLocaleString()}</p>
                  </div>
                  <div className="bg-blue-500/20 border border-blue-500 rounded-lg p-4">
                    <h4 className="text-blue-400 font-semibold mb-2">Payback Period</h4>
                    <p className="text-2xl font-bold text-white">{roiData.payback_period_months} months</p>
                  </div>
                </div>
              </div>
              <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4">
                <div>
                  <h4 className="text-blue-400 font-semibold mb-3">Productivity Gains</h4>
                  <ul className="text-gray-300 text-sm space-y-1">
                    {roiData.productivity_gains?.map((gain: string, idx: number) => (
                      <li key={idx} className="flex items-start space-x-2">
                        <span className="text-blue-400 mt-1">•</span>
                        <span>{gain}</span>
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h4 className="text-blue-400 font-semibold mb-3">Cost Reduction Areas</h4>
                  <ul className="text-gray-300 text-sm space-y-1">
                    {roiData.cost_reduction_areas?.map((area: string, idx: number) => (
                      <li key={idx} className="flex items-start space-x-2">
                        <span className="text-blue-400 mt-1">•</span>
                        <span>{area}</span>
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h4 className="text-blue-400 font-semibold mb-3">Revenue Opportunities</h4>
                  <ul className="text-gray-300 text-sm space-y-1">
                    {roiData.revenue_opportunities?.map((opp: string, idx: number) => (
                      <li key={idx} className="flex items-start space-x-2">
                        <span className="text-blue-400 mt-1">•</span>
                        <span>{opp}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>
        </>
      ) : (
        <div className="text-center text-gray-400 py-12">
          <p className="text-lg mb-4">ROI analysis will be available after VAPI integration</p>
          <p className="text-sm">Complete your AI transformation assessment to unlock detailed ROI projections</p>
        </div>
      )}
    </div>
  )

  const DetailedReportTab: React.FC<{ reportData: any }> = ({ reportData }) => (
    <div className="space-y-8">
      {reportData ? (
        <>
          <Card className="bg-black/80 border-gray-800 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="text-white flex items-center space-x-2">
                <Target className="w-6 h-6 text-purple-400" />
                <span>Comprehensive Report</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                <div>
                  <h4 className="text-purple-400 font-semibold mb-3">Executive Summary</h4>
                  <p className="text-gray-300">{reportData.executive_summary}</p>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="text-purple-400 font-semibold mb-3">Recommended Solutions</h4>
                    <div className="space-y-3">
                      {reportData.recommended_solutions?.map((solution: any, idx: number) => (
                        <div key={idx} className="bg-purple-500/20 border border-purple-500 rounded-lg p-3">
                          <h5 className="text-white font-medium">{solution.title}</h5>
                          <p className="text-sm text-gray-300 mt-1">Priority: {solution.priority}</p>
                          <p className="text-sm text-gray-300">Timeline: {solution.timeline}</p>
                          <p className="text-sm text-gray-300">Investment: {solution.investment}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                  <div>
                    <h4 className="text-purple-400 font-semibold mb-3">Success Metrics</h4>
                    <ul className="text-gray-300 text-sm space-y-2">
                      {reportData.success_metrics?.map((metric: string, idx: number) => (
                        <li key={idx} className="flex items-start space-x-2">
                          <span className="text-purple-400 mt-1">•</span>
                          <span>{metric}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>
                <div>
                  <h4 className="text-purple-400 font-semibold mb-3">Next Steps</h4>
                  <ul className="text-gray-300 text-sm space-y-2">
                    {reportData.next_steps?.map((step: string, idx: number) => (
                      <li key={idx} className="flex items-start space-x-2">
                        <span className="text-purple-400 mt-1">{idx + 1}.</span>
                        <span>{step}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>
        </>
      ) : (
        <div className="text-center text-gray-400 py-12">
          <p className="text-lg mb-4">Detailed report will be available after VAPI integration</p>
          <p className="text-sm">Complete your AI transformation assessment to unlock comprehensive analysis</p>
        </div>
      )}
    </div>
  )

  const formatCategoryName = (key: string) => {
    return key.split('_').map(word => 
      word.charAt(0).toUpperCase() + word.slice(1)
    ).join(' ')
  }

  const formatPainPointName = (key: string) => {
    const names: Record<string, string> = {
      'cant_scale_without_burnout': "Can't Scale Without Burning Out",
      'invisible_attention_landscape': 'Invisible in the New Attention Landscape',
      'outgunned_by_competitors': 'Outgunned by AI-Enabled Competitors',
      'tech_gap_ai_advantages': "Tech Gap: Underusing AI's Unfair Advantages"
    }
    return names[key] || formatCategoryName(key)
  }

  const SessionMetadataCard: React.FC<{ sessionData: TestResult['session_metadata'] }> = ({ sessionData }) => {
    if (!sessionData) return null;
    
    return (
      <Card className="bg-black/80 border-gray-800 backdrop-blur-sm">
        <CardHeader>
          <CardTitle className="text-white flex items-center space-x-2">
            <Clock className="w-5 h-5 text-teal-400" />
            <span>Session Details</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {sessionData.call_duration && (
            <div className="flex justify-between items-center">
              <span className="text-gray-300">Call Duration</span>
              <Badge variant="secondary">{Math.round(sessionData.call_duration / 60)} min</Badge>
            </div>
          )}
          {sessionData.agent_confidence_score && (
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-gray-300">Analysis Confidence</span>
                <span className="text-white font-semibold">{sessionData.agent_confidence_score}%</span>
              </div>
              <Progress value={sessionData.agent_confidence_score} className="h-2" />
            </div>
          )}
          {sessionData.return_user && (
            <div className="flex justify-between items-center">
              <span className="text-gray-300">Return User</span>
              <Badge variant="outline" className="text-teal-400 border-teal-400">
                {sessionData.previous_test_count || 0} previous tests
              </Badge>
            </div>
          )}
          {sessionData.user_website_url && (
            <div className="space-y-1">
              <span className="text-gray-300 text-sm">Website Analyzed</span>
              <p className="text-teal-400 text-sm break-all">{sessionData.user_website_url}</p>
            </div>
          )}
        </CardContent>
      </Card>
    );
  };

  const VoiceSummaryCard: React.FC<{ voiceData: TestResult['voice_summary'] }> = ({ voiceData }) => {
    if (!voiceData) return null;
    
    return (
      <Card className="bg-black/80 border-gray-800 backdrop-blur-sm">
        <CardHeader>
          <CardTitle className="text-white flex items-center space-x-2">
            <Mic className="w-5 h-5 text-purple-400" />
            <span>Conversation Summary</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {voiceData.verbal_summary && (
            <div>
              <h5 className="text-sm font-semibold text-purple-400 mb-2">Key Takeaways</h5>
              <p className="text-gray-300 text-sm">{voiceData.verbal_summary}</p>
            </div>
          )}
          
          {voiceData.conversation_highlights && voiceData.conversation_highlights.length > 0 && (
            <div>
              <h5 className="text-sm font-semibold text-purple-400 mb-2">Conversation Highlights</h5>
              <ul className="space-y-1">
                {voiceData.conversation_highlights.map((highlight, idx) => (
                  <li key={idx} className="flex items-start space-x-2">
                    <CheckCircle className="w-3 h-3 text-purple-400 mt-1 flex-shrink-0" />
                    <span className="text-gray-300 text-sm">{highlight}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
          
          {voiceData.client_concerns_expressed && voiceData.client_concerns_expressed.length > 0 && (
            <div>
              <h5 className="text-sm font-semibold text-orange-400 mb-2">Client Concerns</h5>
              <ul className="space-y-1">
                {voiceData.client_concerns_expressed.map((concern, idx) => (
                  <li key={idx} className="flex items-start space-x-2">
                    <AlertTriangle className="w-3 h-3 text-orange-400 mt-1 flex-shrink-0" />
                    <span className="text-gray-300 text-sm">{concern}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </CardContent>
      </Card>
    );
  };

  const DataSourcesCard: React.FC<{ apiData: TestResult['api_data_sources'] }> = ({ apiData }) => {
    if (!apiData) return null;
    
    return (
      <Card className="bg-black/80 border-gray-800 backdrop-blur-sm">
        <CardHeader>
          <CardTitle className="text-white flex items-center space-x-2">
            <img src="/logo.png" alt="AiAlive" className="w-5 h-5" />
            <span>Analysis Sources</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-3">
          {apiData.tools_used && apiData.tools_used.length > 0 && (
            <div>
              <h5 className="text-sm font-semibold text-teal-400 mb-2">Tools Used</h5>
              <div className="flex flex-wrap gap-2">
                {apiData.tools_used.map((tool, idx) => (
                  <Badge key={idx} variant="outline" className="text-teal-400 border-teal-400">
                    {tool}
                  </Badge>
                ))}
              </div>
            </div>
          )}
          
          {apiData.data_quality_score && (
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-gray-300">Data Quality</span>
                <span className="text-white font-semibold">{apiData.data_quality_score}%</span>
              </div>
              <Progress value={apiData.data_quality_score} className="h-2" />
            </div>
          )}
          
          {apiData.analysis_depth && (
            <div className="flex justify-between items-center">
              <span className="text-gray-300">Analysis Depth</span>
              <Badge variant="secondary" className="capitalize">{apiData.analysis_depth}</Badge>
            </div>
          )}
        </CardContent>
      </Card>
    );
  };

  const SubscriptionRecommendationsCard: React.FC<{ subData: TestResult['subscription_recommendations'] }> = ({ subData }) => {
    if (!subData) return null;
    
    const getPriorityColor = (priority: string) => {
      switch (priority) {
        case 'urgent': return 'text-orange-400 border-orange-400';
        case 'high': return 'text-orange-400 border-orange-400';
        case 'medium': return 'text-yellow-400 border-yellow-400';
        case 'low': return 'text-green-400 border-green-400';
        default: return 'text-gray-400 border-gray-400';
      }
    };
    
    return (
      <Card className="bg-black/80 border-gray-800 backdrop-blur-sm">
        <CardHeader>
          <CardTitle className="text-white flex items-center space-x-2">
            <Target className="w-5 h-5 text-purple-400" />
            <span>Recommended Solutions</span>
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {subData.priority_level && (
            <div className="flex justify-between items-center">
              <span className="text-gray-300">Priority Level</span>
              <Badge variant="outline" className={`capitalize ${getPriorityColor(subData.priority_level)}`}>
                {subData.priority_level}
              </Badge>
            </div>
          )}
          
          {subData.ai_iq_subscription_recommendation && (
            <div>
              <h5 className="text-sm font-semibold text-purple-400 mb-2">AI IQ Business Analysis</h5>
              <p className="text-gray-300 text-sm">{subData.ai_iq_subscription_recommendation}</p>
            </div>
          )}
          
          {subData.vip_support_recommendation && (
            <div>
              <h5 className="text-sm font-semibold text-purple-400 mb-2">VIP Support Recommendation</h5>
              <p className="text-gray-300 text-sm">{subData.vip_support_recommendation}</p>
            </div>
          )}
          
          {subData.estimated_roi_timeline && (
            <div>
              <h5 className="text-sm font-semibold text-green-400 mb-2">Expected ROI Timeline</h5>
              <p className="text-gray-300 text-sm">{subData.estimated_roi_timeline}</p>
            </div>
          )}
        </CardContent>
      </Card>
    );
  };

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-black">
        
        <div className="relative z-10 flex items-center justify-center min-h-screen p-4">
          <Card className="w-full max-w-md bg-black/80 border-gray-800 backdrop-blur-sm">
            <CardHeader className="text-center">
              <div className="flex items-center justify-center mb-4">
                <img src="/favicon.png" alt="AiAlive" className="w-10 h-10" />
              </div>
              <CardTitle className="text-2xl font-bold text-white">AI IQ Test Results</CardTitle>
              <CardDescription className="text-gray-300">
                Access your comprehensive AI audit report
              </CardDescription>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleAuth} className="space-y-4">
                <div>
                  <Input
                    type="email"
                    placeholder="Email address"
                    value={authForm.email}
                    onChange={(e) => setAuthForm({...authForm, email: e.target.value})}
                    required
                    className="bg-black/50 border-gray-800 text-white placeholder-gray-400"
                  />
                </div>
                <div>
                  <Input
                    type="text"
                    placeholder="Full name"
                    value={authForm.name}
                    onChange={(e) => setAuthForm({...authForm, name: e.target.value})}
                    required
                    className="bg-black/50 border-gray-800 text-white placeholder-gray-400"
                  />
                </div>
                <div>
                  <Input
                    type="tel"
                    placeholder="Mobile number"
                    value={authForm.mobile}
                    onChange={(e) => setAuthForm({...authForm, mobile: e.target.value})}
                    required
                    className="bg-black/50 border-gray-800 text-white placeholder-gray-400"
                  />
                </div>
                {error && (
                  <Alert className="bg-orange-900/50 border-orange-700">
                    <AlertDescription className="text-orange-200">{error}</AlertDescription>
                  </Alert>
                )}
                <Button 
                  type="submit" 
                  disabled={loading}
                  className="w-full bg-gradient-to-r from-teal-500 to-purple-600 hover:from-teal-600 hover:to-purple-700 text-white font-semibold"
                >
                  {loading ? 'Generating Report...' : 'Access My Report'}
                </Button>
              </form>
            </CardContent>
          </Card>
        </div>
      </div>
    )
  }

  if (!testResult) {
    return (
      <div className="min-h-screen bg-black flex items-center justify-center">
        <div className="text-center text-white">
          <img src="/favicon.png" alt="AiAlive" className="w-16 h-16 mx-auto mb-4 animate-pulse" />
          <h2 className="text-2xl font-bold mb-2">Generating Your AI IQ Report</h2>
          <p className="text-gray-300">Please wait while we analyze your data...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-black">
      <div className="relative z-10">
        <header className="border-b border-gray-800/50 bg-black/30 backdrop-blur-sm">
          <div className="max-w-7xl mx-auto px-4 py-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-6">
                <img src="/logo.png" alt="AiAlive" className="w-12 h-12" />
                <div className="flex flex-col">
                  <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-r from-teal-500 to-purple-600 rounded-full">
                    <span className="text-2xl font-bold text-white">{testResult.overall_score}</span>
                  </div>
                  <span className="text-sm font-semibold text-white mt-1">Your AI IQ Score</span>
                </div>
              </div>
              <div className="text-center flex-1">
                <h1 className="text-2xl font-bold text-white">Test Results</h1>
              </div>
              <div className="text-right">
                <p className="text-white font-semibold">{testResult.user_name}</p>
                <p className="text-gray-400 text-sm">{testResult.user_email}</p>
              </div>
            </div>
          </div>
        </header>

        <main className="max-w-7xl mx-auto px-4 py-8 space-y-8">
          <div className="text-center mb-8">
            <ul className="text-gray-300 space-y-2 max-w-2xl mx-auto">
              <li>• Comprehensive AI readiness assessment completed</li>
              <li>• {Object.keys(testResult.pain_points).length} critical areas identified</li>
              <li>• {Object.keys(testResult.categories).length} business categories analyzed</li>
              <li>• Personalized recommendations generated</li>
            </ul>
          </div>

          <div className="flex flex-col lg:flex-row gap-4 mb-8">
            <TabButton tabId="test-results" number="01" title="AI IQ Test Results" color="teal" />
            <TabButton tabId="roi-analysis" number="02" title="ROI Analysis" color="blue" />
            <TabButton tabId="detailed-report" number="03" title="Comprehensive Report" color="purple" />
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
            <div className="lg:col-span-3">
              {activeTab === 'test-results' && <TestResultsTab testResult={testResult} />}
              {activeTab === 'roi-analysis' && <ROIAnalysisTab roiData={testResult.roi_analysis} />}
              {activeTab === 'detailed-report' && <DetailedReportTab reportData={testResult.detailed_report} />}
            </div>

            <div className="lg:col-span-1">
              <div className="space-y-6">
                <div className="sticky top-4">
                  <Card className="bg-black/80 border-gray-800 backdrop-blur-sm" style={{ width: '24rem', height: '32rem' }}>
                    <CardHeader>
                      <CardTitle className="text-white flex items-center space-x-2">
                        <img src="/favicon.png" alt="AiAlive" className="w-5 h-5" />
                        <span>AI Assistant - Freedom</span>
                      </CardTitle>
                      <CardDescription className="text-gray-300">
                        Chat for follow-up questions and guidance
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="h-full flex flex-col">
                      <div className="flex-1 bg-black/50 border-2 border-dashed border-gray-800 rounded-lg p-4 flex flex-col items-center justify-center">
                        <img src="/favicon.png" alt="AiAlive" className="w-12 h-12 mb-4" />
                        <p className="text-gray-300 text-sm mb-3 text-center">VAPI Widget Integration</p>
                        <p className="text-xs text-gray-400 text-center">
                          30-minute session included with your test results
                        </p>
                        <div className="mt-4 text-center">
                          <p className="text-xs text-teal-400">After 30 minutes:</p>
                          <p className="text-xs text-gray-400">Upgrade for continued access</p>
                        </div>
                        <div className="mt-6 space-y-2 w-full">
                          <button className="w-full bg-teal-600 hover:bg-teal-700 text-white text-xs py-2 px-3 rounded transition-colors">
                            AI Transformation Sessions - $100/mo
                          </button>
                          <button className="w-full bg-purple-600 hover:bg-purple-700 text-white text-xs py-2 px-3 rounded transition-colors">
                            Devin-like Superpowers
                          </button>
                          <button className="w-full bg-blue-600 hover:bg-blue-700 text-white text-xs py-2 px-3 rounded transition-colors">
                            Human Support Option
                          </button>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                </div>
                
                <SessionMetadataCard sessionData={testResult.session_metadata} />
                <VoiceSummaryCard voiceData={testResult.voice_summary} />
                <DataSourcesCard apiData={testResult.api_data_sources} />
                <SubscriptionRecommendationsCard subData={testResult.subscription_recommendations} />
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  )
}

export default App
