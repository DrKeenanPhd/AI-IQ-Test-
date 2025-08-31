import { useState } from 'react'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Progress } from '@/components/ui/progress'
import { Badge } from '@/components/ui/badge'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Brain, TrendingUp, Users, Globe, MessageSquare, Target, CheckCircle, AlertTriangle, XCircle, Clock, Mic } from 'lucide-react'
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
}

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [, setUserId] = useState<string | null>(null)
  const [testResult, setTestResult] = useState<TestResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  
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

  const getCategoryIcon = (category: string) => {
    switch (category) {
      case 'website_form_function': return <Globe className="w-6 h-6" />
      case 'social_media_effectiveness': return <Users className="w-6 h-6" />
      case 'digital_presence': return <TrendingUp className="w-6 h-6" />
      case 'communication': return <MessageSquare className="w-6 h-6" />
      case 'marketing': return <Target className="w-6 h-6" />
      default: return <Brain className="w-6 h-6" />
    }
  }

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'high': return <XCircle className="w-5 h-5 text-red-400" />
      case 'medium': return <AlertTriangle className="w-5 h-5 text-yellow-400" />
      case 'low': return <CheckCircle className="w-5 h-5 text-green-400" />
      default: return <AlertTriangle className="w-5 h-5 text-yellow-400" />
    }
  }

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
              <h5 className="text-sm font-semibold text-red-400 mb-2">Client Concerns</h5>
              <ul className="space-y-1">
                {voiceData.client_concerns_expressed.map((concern, idx) => (
                  <li key={idx} className="flex items-start space-x-2">
                    <AlertTriangle className="w-3 h-3 text-red-400 mt-1 flex-shrink-0" />
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
        case 'urgent': return 'text-red-400 border-red-400';
        case 'high': return 'text-orange-400 border-orange-400';
        case 'medium': return 'text-yellow-400 border-yellow-400';
        case 'low': return 'text-green-400 border-green-400';
        default: return 'text-gray-400 border-gray-400';
      }
    };
    
    return (
      <Card className="bg-gray-800/50 border-gray-700 backdrop-blur-sm">
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
        <div className="absolute inset-0 bg-gradient-to-r from-teal-500/10 via-purple-500/10 to-teal-500/10"></div>
        
        <div className="relative z-10 flex items-center justify-center min-h-screen p-4">
          <Card className="w-full max-w-md bg-black/80 border-gray-800 backdrop-blur-sm">
            <CardHeader className="text-center">
              <div className="flex items-center justify-center mb-4">
                <img src="/logo.png" alt="AiAlive" className="w-10 h-10" />
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
                  <Alert className="bg-red-900/50 border-red-700">
                    <AlertDescription className="text-red-200">{error}</AlertDescription>
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
          <img src="/logo.png" alt="AiAlive" className="w-16 h-16 mx-auto mb-4 animate-pulse" />
          <h2 className="text-2xl font-bold mb-2">Generating Your AI IQ Report</h2>
          <p className="text-gray-300">Please wait while we analyze your data...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-black">
      <div className="absolute inset-0 bg-gradient-to-r from-teal-500/5 via-purple-500/5 to-teal-500/5"></div>
      
      <div className="relative z-10">
        <header className="border-b border-gray-800/50 bg-black/30 backdrop-blur-sm">
          <div className="max-w-7xl mx-auto px-4 py-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <img src="/logo.png" alt="AiAlive" className="w-8 h-8" />
                <h1 className="text-2xl font-bold text-white">AI IQ Test Results</h1>
              </div>
              <div className="text-right">
                <p className="text-white font-semibold">{testResult.user_name}</p>
                <p className="text-gray-400 text-sm">{testResult.user_email}</p>
              </div>
            </div>
          </div>
        </header>

        <main className="max-w-7xl mx-auto px-4 py-8 space-y-8">
          <div className="text-center mb-12">
            <div className="inline-flex items-center justify-center w-24 h-24 bg-gradient-to-r from-teal-500 to-purple-600 rounded-full mb-6">
              <span className="text-3xl font-bold text-white">{testResult.overall_score}</span>
            </div>
            <h2 className="text-4xl font-bold text-white mb-4">Your AI IQ Score</h2>
            <p className="text-xl text-gray-300 max-w-2xl mx-auto">
              Based on our comprehensive analysis of your business across 5 key categories
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
            <div className="lg:col-span-2 space-y-8">
              <Card className="bg-black/80 border-gray-800 backdrop-blur-sm">
                <CardHeader>
                  <CardTitle className="text-white flex items-center space-x-2">
                    <AlertTriangle className="w-6 h-6 text-yellow-400" />
                    <span>Critical Pain Points</span>
                  </CardTitle>
                </CardHeader>
                <CardContent className="space-y-4">
                  {Object.entries(testResult.pain_points).map(([key, point]: [string, any]) => (
                    <div key={key} className="flex items-start space-x-3 p-4 bg-gray-700/30 rounded-lg">
                      {getSeverityIcon(point.severity)}
                      <div className="flex-1">
                        <h4 className="font-semibold text-white mb-1">{formatPainPointName(key)}</h4>
                        <p className="text-gray-300 text-sm mb-2">{point.description}</p>
                        <Badge variant={point.severity === 'high' ? 'destructive' : 'secondary'}>
                          Score: {point.score}/10
                        </Badge>
                      </div>
                    </div>
                  ))}
                </CardContent>
              </Card>

              <div className={`grid gap-6 ${
                Object.keys(testResult.categories).length <= 3 
                  ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3' 
                  : Object.keys(testResult.categories).length <= 5
                  ? 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3'
                  : 'grid-cols-1 md:grid-cols-2 lg:grid-cols-3'
              }`}>
                {Object.entries(testResult.categories).map(([key, category]: [string, any]) => (
                  <Card key={key} className="bg-black/80 border-gray-800 backdrop-blur-sm">
                    <CardHeader className="pb-3">
                      <div className="flex items-center space-x-2 mb-2">
                        {getCategoryIcon(key)}
                        <CardTitle className="text-lg text-white">{formatCategoryName(key)}</CardTitle>
                      </div>
                      <div className="space-y-2">
                        <div className="flex justify-between items-center">
                          <span className="text-2xl font-bold text-white">{category.score}</span>
                          <span className="text-sm text-gray-400">/ {category.max_score}</span>
                        </div>
                        <Progress value={category.percentage} className="h-2" />
                        <p className="text-sm text-gray-300">{category.percentage}% Complete</p>
                      </div>
                    </CardHeader>
                    <CardContent className="pt-0">
                      <div className="space-y-3">
                        <div>
                          <h5 className="text-sm font-semibold text-green-400 mb-1">Strengths</h5>
                          <ul className="text-xs text-gray-300 space-y-1">
                            {category.strengths?.map((strength: string, idx: number) => (
                              <li key={idx} className="flex items-start space-x-1">
                                <CheckCircle className="w-3 h-3 text-green-400 mt-0.5 flex-shrink-0" />
                                <span>{strength}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                        <div>
                          <h5 className="text-sm font-semibold text-red-400 mb-1">Areas for Improvement</h5>
                          <ul className="text-xs text-gray-300 space-y-1">
                            {category.weaknesses?.map((weakness: string, idx: number) => (
                              <li key={idx} className="flex items-start space-x-1">
                                <XCircle className="w-3 h-3 text-red-400 mt-0.5 flex-shrink-0" />
                                <span>{weakness}</span>
                              </li>
                            ))}
                          </ul>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                ))}
              </div>
            </div>

            <div className="space-y-6">
              <Card className="bg-black/80 border-gray-800 backdrop-blur-sm">
                <CardHeader>
                  <CardTitle className="text-white">AI Assistant</CardTitle>
                  <CardDescription className="text-gray-300">
                    Chat with Freedom for follow-up questions
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="bg-gray-700/30 border-2 border-dashed border-gray-600 rounded-lg p-6 text-center">
                    <img src="/logo.png" alt="AiAlive" className="w-10 h-10 mx-auto mb-3" />
                    <p className="text-gray-300 text-sm mb-3">VAPI Widget Here</p>
                    <p className="text-xs text-gray-400">
                      Insert your VAPI HTML code here to activate your AI assistant
                    </p>
                  </div>
                </CardContent>
              </Card>

              <SessionMetadataCard sessionData={testResult.session_metadata} />
              <VoiceSummaryCard voiceData={testResult.voice_summary} />
              <DataSourcesCard apiData={testResult.api_data_sources} />
              <SubscriptionRecommendationsCard subData={testResult.subscription_recommendations} />
            </div>
          </div>


          <Card className="bg-black/80 border-gray-800 backdrop-blur-sm">
            <CardHeader>
              <CardTitle className="text-white flex items-center space-x-2">
                <Target className="w-6 h-6 text-teal-400" />
                <span>Recommended Action Plan</span>
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="text-lg font-semibold text-white mb-4">Strategic Recommendations</h4>
                  <ul className="space-y-3">
                    {testResult.recommendations.map((rec, idx) => (
                      <li key={idx} className="flex items-start space-x-3">
                        <div className="flex-shrink-0 w-6 h-6 bg-gradient-to-r from-teal-500 to-purple-600 rounded-full flex items-center justify-center">
                          <span className="text-xs font-bold text-white">{idx + 1}</span>
                        </div>
                        <p className="text-gray-300">{rec}</p>
                      </li>
                    ))}
                  </ul>
                </div>
                <div>
                  <h4 className="text-lg font-semibold text-white mb-4">Priority Actions</h4>
                  <div className="space-y-4">
                    {Object.entries(testResult.categories).map(([key, category]: [string, any]) => (
                      <div key={key} className="bg-gray-700/30 rounded-lg p-4">
                        <h5 className="font-semibold text-white mb-2">{formatCategoryName(key)}</h5>
                        <ul className="text-sm text-gray-300 space-y-1">
                          {category.priority_actions?.map((action: string, idx: number) => (
                            <li key={idx} className="flex items-start space-x-2">
                              <TrendingUp className="w-3 h-3 text-teal-400 mt-1 flex-shrink-0" />
                              <span>{action}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {testResult.custom_sections && Object.entries(testResult.custom_sections).map(([key, section]: [string, any]) => (
            <Card key={key} className="bg-black/80 border-gray-800 backdrop-blur-sm">
              <CardHeader>
                <CardTitle className="text-white flex items-center space-x-2">
                  <img src="/logo.png" alt="AiAlive" className="w-6 h-6" />
                  <span>{section.title}</span>
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {Object.entries(section.content).map(([contentKey, contentValue]: [string, any]) => (
                    <div key={contentKey}>
                      <h4 className="text-lg font-semibold text-white mb-2 capitalize">
                        {contentKey.replace(/_/g, ' ')}
                      </h4>
                      {Array.isArray(contentValue) ? (
                        <ul className="space-y-2">
                          {contentValue.map((item: string, idx: number) => (
                            <li key={idx} className="flex items-start space-x-2">
                              <CheckCircle className="w-4 h-4 text-teal-400 mt-1 flex-shrink-0" />
                              <span className="text-gray-300">{item}</span>
                            </li>
                          ))}
                        </ul>
                      ) : (
                        <p className="text-gray-300">{contentValue}</p>
                      )}
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          ))}
        </main>
      </div>
    </div>
  )
}

export default App
