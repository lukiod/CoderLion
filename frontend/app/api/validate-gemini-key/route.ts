import { NextRequest, NextResponse } from 'next/server'
import { GoogleGenerativeAI } from '@google/generative-ai'

export async function POST(request: NextRequest) {
  try {
    const { apiKey } = await request.json()
    
    if (!apiKey) {
      return NextResponse.json({ valid: false, error: 'API key is required' })
    }

    // Test the API key with a simple request
    const genAI = new GoogleGenerativeAI(apiKey)
    const model = genAI.getGenerativeModel({ model: 'gemini-pro' })
    
    try {
      // Make a simple test request
      const result = await model.generateContent('Hello')
      await result.response
      
      return NextResponse.json({ valid: true })
    } catch (error) {
      return NextResponse.json({ valid: false, error: 'Invalid API key' })
    }
  } catch (error) {
    return NextResponse.json({ valid: false, error: 'Invalid request' })
  }
}
