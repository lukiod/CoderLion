'use client'

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import { Input } from '@/components/ui/input'
import { 
  Github, 
  Shield, 
  Zap, 
  Code, 
  BarChart3, 
  Clock,
  CheckCircle,
  AlertCircle,
  XCircle,
  Eye,
  EyeOff,
  Key,
  Settings
} from 'lucide-react'

interface Review {
  id: number
  github_pr_id: number
  repository_name: string
  status: string
  summary: string
  confidence_score: number
  created_at: string
}

interface Stats {
  total_reviews: number
  status_counts: Record<string, number>
  average_confidence_score: number
  total_comments: number
}

export default function Dashboard() {
  const [reviews, setReviews] = useState<Review[]>([])
  const [stats, setStats] = useState<Stats | null>(null)
  const [loading, setLoading] = useState(true)
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [geminiApiKey, setGeminiApiKey] = useState('')
  const [showApiKey, setShowApiKey] = useState(false)
  const [isValidatingKey, setIsValidatingKey] = useState(false)
  const [keyValid, setKeyValid] = useState<boolean | null>(null)

  useEffect(() => {
    // Check authentication status
    const checkAuth = () => {
      const token = localStorage.getItem('auth_token')
      const user = localStorage.getItem('user')
      if (token && user) {
        setIsAuthenticated(true)
      }
    }

    // Load Gemini API key from localStorage
    const loadApiKey = () => {
      const savedKey = localStorage.getItem('gemini_api_key')
      if (savedKey) {
        setGeminiApiKey(savedKey)
        setKeyValid(true)
      }
    }

    checkAuth()
    loadApiKey()

    // Mock data for demo
    setReviews([
      {
        id: 1,
        github_pr_id: 123,
        repository_name: 'myorg/myapp',
        status: 'completed',
        summary: 'Found 3 security issues and 2 performance improvements',
        confidence_score: 85,
        created_at: '2024-01-15T10:30:00Z'
      },
      {
        id: 2,
        github_pr_id: 124,
        repository_name: 'myorg/myapp',
        status: 'in_progress',
        summary: 'Analyzing code changes...',
        confidence_score: 0,
        created_at: '2024-01-15T11:00:00Z'
      }
    ])

    setStats({
      total_reviews: 15,
      status_counts: {
        completed: 12,
        in_progress: 2,
        pending: 1,
        failed: 0
      },
      average_confidence_score: 78.5,
      total_comments: 45
    })

    setLoading(false)
  }, [])

  const handleGitHubSignIn = () => {
    // Redirect to GitHub OAuth
    const githubAuthUrl = `https://github.com/login/oauth/authorize?client_id=${process.env.NEXT_PUBLIC_GITHUB_CLIENT_ID}&redirect_uri=${window.location.origin}/auth/callback&scope=repo,user`
    window.location.href = githubAuthUrl
  }

  const handleApiKeyChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setGeminiApiKey(e.target.value)
    setKeyValid(null)
  }

  const validateApiKey = async () => {
    if (!geminiApiKey.trim()) return

    setIsValidatingKey(true)
    try {
      // Test the API key with a simple request
      const response = await fetch('/api/validate-gemini-key', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ apiKey: geminiApiKey })
      })
      
      const result = await response.json()
      setKeyValid(result.valid)
      
      if (result.valid) {
        localStorage.setItem('gemini_api_key', geminiApiKey)
      }
    } catch (error) {
      setKeyValid(false)
    } finally {
      setIsValidatingKey(false)
    }
  }

  const clearApiKey = () => {
    setGeminiApiKey('')
    setKeyValid(null)
    localStorage.removeItem('gemini_api_key')
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-4 w-4 text-green-500" />
      case 'in_progress':
        return <Clock className="h-4 w-4 text-blue-500" />
      case 'pending':
        return <AlertCircle className="h-4 w-4 text-yellow-500" />
      case 'failed':
        return <XCircle className="h-4 w-4 text-red-500" />
      default:
        return <AlertCircle className="h-4 w-4 text-gray-500" />
    }
  }

  const getStatusBadge = (status: string) => {
    const variants = {
      completed: 'default',
      in_progress: 'secondary',
      pending: 'outline',
      failed: 'destructive'
    } as const

    return (
      <Badge variant={variants[status as keyof typeof variants] || 'outline'}>
        {status.replace('_', ' ')}
      </Badge>
    )
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading CodeLion...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg flex items-center justify-center">
                <span className="text-white font-bold text-lg">🦁</span>
              </div>
              <h1 className="text-2xl font-bold text-gray-900">CodeLion</h1>
            </div>
            
            <div className="flex items-center space-x-4">
              {/* API Key Status */}
              {keyValid === true && (
                <div className="flex items-center space-x-2 text-green-600">
                  <Key className="h-4 w-4" />
                  <span className="text-sm font-medium">API Key Connected</span>
                </div>
              )}
              
              {/* GitHub Sign In */}
              {!isAuthenticated ? (
                <Button onClick={handleGitHubSignIn} className="flex items-center space-x-2">
                  <Github className="h-4 w-4" />
                  <span>Sign in with GitHub</span>
                </Button>
              ) : (
                <div className="flex items-center space-x-2">
                  <Button variant="outline" className="flex items-center space-x-2">
                    <Settings className="h-4 w-4" />
                    <span>Settings</span>
                  </Button>
                  <Button className="flex items-center space-x-2">
                    <Github className="h-4 w-4" />
                    <span>Connect Repository</span>
                  </Button>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <Tabs defaultValue="overview" className="space-y-6">
          <TabsList>
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="reviews">Reviews</TabsTrigger>
            <TabsTrigger value="repositories">Repositories</TabsTrigger>
            <TabsTrigger value="agents">Agents</TabsTrigger>
          </TabsList>

          <TabsContent value="overview" className="space-y-6">
            {/* Setup Section */}
            {(!isAuthenticated || !keyValid) && (
              <Card className="border-blue-200 bg-blue-50">
                <CardHeader>
                  <CardTitle className="text-blue-900">🚀 Get Started with CodeLion</CardTitle>
                  <CardDescription className="text-blue-700">
                    Complete the setup to start using AI-powered code reviews
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-6">
                  {/* GitHub Authentication */}
                  {!isAuthenticated && (
                    <div className="flex items-center justify-between p-4 border border-blue-200 rounded-lg bg-white">
                      <div className="flex items-center space-x-3">
                        <Github className="h-6 w-6 text-gray-600" />
                        <div>
                          <h3 className="font-medium text-gray-900">Connect GitHub</h3>
                          <p className="text-sm text-gray-500">Sign in to connect your repositories</p>
                        </div>
                      </div>
                      <Button onClick={handleGitHubSignIn} className="flex items-center space-x-2">
                        <Github className="h-4 w-4" />
                        <span>Sign in with GitHub</span>
                      </Button>
                    </div>
                  )}

                  {/* API Key Setup */}
                  {isAuthenticated && !keyValid && (
                    <div className="space-y-4">
                      <div className="flex items-center space-x-3">
                        <Key className="h-6 w-6 text-gray-600" />
                        <div>
                          <h3 className="font-medium text-gray-900">Add Gemini API Key</h3>
                          <p className="text-sm text-gray-500">Your API key is stored locally and never shared</p>
                        </div>
                      </div>
                      
                      <div className="flex space-x-2">
                        <div className="relative flex-1">
                          <Input
                            type={showApiKey ? 'text' : 'password'}
                            value={geminiApiKey}
                            onChange={handleApiKeyChange}
                            placeholder="Enter your Gemini API key"
                            className="pr-10"
                          />
                          <Button
                            type="button"
                            variant="ghost"
                            size="icon"
                            className="absolute right-0 top-0 h-full px-3"
                            onClick={() => setShowApiKey(!showApiKey)}
                          >
                            {showApiKey ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                          </Button>
                        </div>
                        <Button 
                          onClick={validateApiKey} 
                          disabled={!geminiApiKey.trim() || isValidatingKey}
                        >
                          {isValidatingKey ? 'Validating...' : 'Validate'}
                        </Button>
                      </div>

                      {keyValid === false && (
                        <div className="flex items-center space-x-2 text-red-600">
                          <XCircle className="h-4 w-4" />
                          <span className="text-sm">Invalid API key. Please check and try again.</span>
                        </div>
                      )}

                      <div className="text-xs text-gray-500 space-y-1">
                        <p>• Get your API key from <a href="https://makersuite.google.com/app/apikey" target="_blank" className="text-blue-500 hover:underline">Google AI Studio</a></p>
                        <p>• Your key is stored locally in your browser</p>
                        <p>• It's only used for processing your code reviews</p>
                      </div>
                    </div>
                  )}
                </CardContent>
              </Card>
            )}

            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Reviews</CardTitle>
                  <BarChart3 className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{stats?.total_reviews || 0}</div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Avg Confidence</CardTitle>
                  <CheckCircle className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{stats?.average_confidence_score || 0}%</div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Total Comments</CardTitle>
                  <Code className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">{stats?.total_comments || 0}</div>
                </CardContent>
              </Card>

              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">Active Agents</CardTitle>
                  <Shield className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">3</div>
                </CardContent>
              </Card>
            </div>

            {/* Recent Reviews */}
            <Card>
              <CardHeader>
                <CardTitle>Recent Reviews</CardTitle>
                <CardDescription>Latest code reviews from your repositories</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {reviews.map((review) => (
                    <div key={review.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center space-x-4">
                        {getStatusIcon(review.status)}
                        <div>
                          <p className="font-medium">PR #{review.github_pr_id}</p>
                          <p className="text-sm text-gray-500">{review.repository_name}</p>
                          <p className="text-sm text-gray-600">{review.summary}</p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        {getStatusBadge(review.status)}
                        {review.confidence_score > 0 && (
                          <Badge variant="outline">
                            {review.confidence_score}% confidence
                          </Badge>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="reviews">
            <Card>
              <CardHeader>
                <CardTitle>All Reviews</CardTitle>
                <CardDescription>Complete history of code reviews</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {reviews.map((review) => (
                    <div key={review.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex items-center space-x-4">
                        {getStatusIcon(review.status)}
                        <div>
                          <p className="font-medium">PR #{review.github_pr_id}</p>
                          <p className="text-sm text-gray-500">{review.repository_name}</p>
                          <p className="text-sm text-gray-600">{review.summary}</p>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        {getStatusBadge(review.status)}
                        {review.confidence_score > 0 && (
                          <Badge variant="outline">
                            {review.confidence_score}% confidence
                          </Badge>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="repositories">
            <Card>
              <CardHeader>
                <CardTitle>Connected Repositories</CardTitle>
                <CardDescription>Repositories connected to CodeLion</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-center py-8">
                  <Github className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <p className="text-gray-500">No repositories connected yet</p>
                  <Button className="mt-4">Connect Your First Repository</Button>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="agents">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Shield className="h-5 w-5 text-red-500" />
                    <span>Security Agent</span>
                  </CardTitle>
                  <CardDescription>Detects security vulnerabilities and best practices</CardDescription>
                </CardHeader>
                <CardContent>
                  <Badge variant="default">Active</Badge>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Zap className="h-5 w-5 text-yellow-500" />
                    <span>Performance Agent</span>
                  </CardTitle>
                  <CardDescription>Identifies performance bottlenecks and optimizations</CardDescription>
                </CardHeader>
                <CardContent>
                  <Badge variant="default">Active</Badge>
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center space-x-2">
                    <Code className="h-5 w-5 text-blue-500" />
                    <span>Style Agent</span>
                  </CardTitle>
                  <CardDescription>Enforces code style and formatting standards</CardDescription>
                </CardHeader>
                <CardContent>
                  <Badge variant="default">Active</Badge>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  )
}
