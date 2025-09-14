'use client'

import { useEffect, useState } from 'react'
import { useRouter, useSearchParams } from 'next/navigation'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { CheckCircle, XCircle, Loader2 } from 'lucide-react'

export default function AuthCallback() {
  const router = useRouter()
  const searchParams = useSearchParams()
  const [status, setStatus] = useState<'loading' | 'success' | 'error'>('loading')
  const [message, setMessage] = useState('')

  useEffect(() => {
    const handleCallback = async () => {
      const code = searchParams.get('code')
      const error = searchParams.get('error')

      if (error) {
        setStatus('error')
        setMessage('Authentication failed. Please try again.')
        return
      }

      if (!code) {
        setStatus('error')
        setMessage('No authorization code received.')
        return
      }

      try {
        // Exchange code for access token
        const response = await fetch('/api/auth/github', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ code })
        })

        const data = await response.json()

        if (data.success) {
          // Store auth data
          localStorage.setItem('auth_token', data.token)
          localStorage.setItem('user', JSON.stringify(data.user))
          
          setStatus('success')
          setMessage('Successfully authenticated! Redirecting...')
          
          // Redirect to dashboard
          setTimeout(() => {
            router.push('/')
          }, 2000)
        } else {
          setStatus('error')
          setMessage(data.message || 'Authentication failed.')
        }
      } catch (error) {
        setStatus('error')
        setMessage('An error occurred during authentication.')
      }
    }

    handleCallback()
  }, [searchParams, router])

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <Card className="w-full max-w-md">
        <CardHeader className="text-center">
          <CardTitle className="flex items-center justify-center space-x-2">
            {status === 'loading' && <Loader2 className="h-6 w-6 animate-spin" />}
            {status === 'success' && <CheckCircle className="h-6 w-6 text-green-500" />}
            {status === 'error' && <XCircle className="h-6 w-6 text-red-500" />}
            <span>GitHub Authentication</span>
          </CardTitle>
          <CardDescription>
            {status === 'loading' && 'Processing authentication...'}
            {status === 'success' && 'Authentication successful!'}
            {status === 'error' && 'Authentication failed'}
          </CardDescription>
        </CardHeader>
        <CardContent className="text-center">
          <p className="text-sm text-gray-600">{message}</p>
          {status === 'error' && (
            <button
              onClick={() => router.push('/')}
              className="mt-4 text-blue-500 hover:underline"
            >
              Return to Dashboard
            </button>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
