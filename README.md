# CodeLion 🦁

AI code review for people who actually read their pull requests.

CodeLion connects to your GitHub repos, looks at your pull requests, and gives real feedback on things that matter — security issues, performance problems, and messy code.

No server-side AI processing.
No weird permissions.
No black box magic.

Your Gemini API key stays in your browser. Your code stays yours.

---

## Why I built this

Most AI code review tools feel… off.

Some need full access to your repositories.
Some send your code to their servers.
Some give feedback so generic it’s basically useless.

I wanted something different:

* secure by design
* actually helpful
* simple to connect
* fast enough to use on every PR

So CodeLion runs AI from the client, uses focused review agents, and plugs straight into GitHub.

That’s it.

---

## What it does

When a pull request is opened or updated, CodeLion:

* checks for security risks
* looks for performance problems
* points out questionable patterns
* suggests cleaner implementations
* keeps a history of reviews

Think of it like having a small review team that never gets tired.

---

## How it works

1. Sign in with GitHub
2. Connect a repo
3. Open a PR
4. CodeLion reviews it automatically
5. You get structured feedback

Each AI agent focuses on one concern (security, performance, style, etc.).

No giant monolithic prompt. Just focused reviewers.

---

## Architecture (simple version)

Frontend → Next.js app running on Vercel
Backend → FastAPI service
Database → Supabase PostgreSQL
Auth → GitHub OAuth
AI → Google Gemini (called from the browser)

The important part:

**AI runs client-side.**
Your API key never touches our backend.

---

## Stack

Frontend

* Next.js 14
* TypeScript
* Tailwind
* Sup
