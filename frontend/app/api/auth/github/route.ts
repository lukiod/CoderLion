import { NextRequest, NextResponse } from 'next/server'

export async function POST(request: NextRequest) {
  try {
    const { code } = await request.json()
    
    if (!code) {
      return NextResponse.json({ success: false, message: 'Authorization code is required' })
    }

    // Exchange code for access token
    const tokenResponse = await fetch('https://github.com/login/oauth/access_token', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        client_id: process.env.GITHUB_CLIENT_ID,
        client_secret: process.env.GITHUB_CLIENT_SECRET,
        code,
      }),
    })

    const tokenData = await tokenResponse.json()

    if (tokenData.error) {
      return NextResponse.json({ success: false, message: tokenData.error_description })
    }

    // Get user info from GitHub
    const userResponse = await fetch('https://api.github.com/user', {
      headers: {
        'Authorization': `Bearer ${tokenData.access_token}`,
        'Accept': 'application/vnd.github.v3+json',
      },
    })

    const userData = await userResponse.json()

    if (!userResponse.ok) {
      return NextResponse.json({ success: false, message: 'Failed to fetch user data' })
    }

    // Create JWT token (simplified - in production, use proper JWT library)
    const jwtToken = `jwt_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`

    return NextResponse.json({
      success: true,
      token: jwtToken,
      user: {
        id: userData.id,
        username: userData.login,
        email: userData.email,
        avatar_url: userData.avatar_url,
        name: userData.name,
      }
    })
  } catch (error) {
    return NextResponse.json({ 
      success: false, 
      message: 'An error occurred during authentication' 
    })
  }
}
