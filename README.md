# CodeLion 🦁

An open-source AI-powered code review tool with multi-agent architecture, powered by Google Gemini.

## ✨ Features

- **🔐 Client-Side Security**: Your API keys stay in your browser, never on our servers
- **🔑 GitHub OAuth**: Secure one-click sign-in with GitHub
- **🤖 Multi-Agent Architecture**: Specialized agents for security, performance, and style
- **⚡ Real-time Reviews**: Instant code reviews on pull requests
- **🎯 Production Ready**: Built for scale with Supabase and Vercel
- **💎 Modern UI**: Beautiful, responsive dashboard with real-time updates

## 🏗️ Architecture

### **Why This Design?**
- **Client-Side API Keys**: Your Gemini API key never touches our servers - better security and privacy
- **GitHub OAuth**: Industry-standard authentication, not API keys
- **Supabase Database**: Stores user sessions, repository connections, and review history
- **Multi-Agent System**: Each agent specializes in different aspects of code review

## 🚀 Tech Stack

- **Frontend**: Next.js 14 + TypeScript + Tailwind CSS + Supabase
- **Backend**: FastAPI + Supabase PostgreSQL
- **AI**: Google Gemini API (client-side)
- **Auth**: GitHub OAuth
- **Deployment**: Vercel + Supabase

## 🎯 Quick Start

### **1. Deploy to Vercel (Recommended)**

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/yourusername/coderlion)

### **2. Set up Supabase**

1. Create a [Supabase project](https://supabase.com)
2. Copy your database URL and keys
3. Add them to your Vercel environment variables

### **3. Configure GitHub OAuth**

1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Create a new OAuth App
3. Set callback URL to: `https://your-domain.vercel.app/auth/callback`
4. Add `GITHUB_CLIENT_ID` and `GITHUB_CLIENT_SECRET` to Vercel

### **4. Get Gemini API Key**

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Users will enter this in the app (stored locally)

## 🔧 Local Development

```bash
# Clone the repository
git clone https://github.com/yourusername/coderlion.git
cd coderlion

# Install dependencies
cd frontend && npm install
cd ../backend && pip install -r requirements.txt

# Set up environment
cp env.example .env
# Update .env with your Supabase and GitHub credentials

# Start development servers
cd frontend && npm run dev
cd backend && uvicorn app.main:app --reload
```

## 🏗️ Production Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   User Browser  │    │   Vercel Edge   │    │  Supabase DB    │
│                 │    │                 │    │                 │
│ • API Key (LS)  │◄──►│ • Next.js App   │◄──►│ • User Sessions │
│ • GitHub OAuth  │    │ • API Routes    │    │ • Repositories  │
│ • Review UI     │    │ • Webhooks      │    │ • Review History│
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  GitHub API     │
                       │ • OAuth Flow    │
                       │ • Webhook Events│
                       │ • PR Data       │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │  Gemini API     │
                       │ • Code Analysis │
                       │ • Multi-Agents  │
                       │ • Review Gen    │
                       └─────────────────┘
```

## 🔐 Security Features

- **Client-Side API Keys**: Your Gemini API key never leaves your browser
- **GitHub OAuth**: Industry-standard authentication
- **Supabase RLS**: Row-level security for data isolation
- **JWT Tokens**: Secure session management
- **HTTPS Only**: All communication encrypted

## 🚀 Deployment

### **Vercel (Recommended)**

1. **Fork this repository**
2. **Connect to Vercel**
3. **Add environment variables**:
   ```
   NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
   GITHUB_CLIENT_ID=your_github_client_id
   GITHUB_CLIENT_SECRET=your_github_client_secret
   ```
4. **Deploy!**

### **Other Platforms**

- **Railway**: Use the `railway.json` config
- **Render**: Use the `render.yaml` config
- **Docker**: Use the provided `Dockerfile`

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

## 🆘 Support

- **Discord**: Join our community
- **GitHub Issues**: Report bugs and request features
- **Documentation**: Check our [docs](https://coderlion.dev)

---

**Built with ❤️ by the CodeLion team**
