# Supabase MCP Authentication URL

Visit this URL in your browser to authenticate the Supabase MCP server:

https://api.supabase.com/v1/oauth/authorize?response_type=code&client_id=3e0274c2-e6e4-4f58-ba4f-4d7c7ff5f87b&code_challenge=EFBzI9KF4Bbz4zl0v3bNuz_QBewJ1GrY4VRrBGuWQB4&code_challenge_method=S256&redirect_uri=http%3A%2F%2Flocalhost%3A57363%2Fcallback&state=RWPZ4_qHMf_DwCpF8JoRPZseFxLKJA67yrY6tJIwJdY&scope=organizations%3Aread+projects%3Aread+projects%3Awrite+database%3Awrite+database%3Aread+analytics%3Aread+secrets%3Aread+edge_functions%3Aread+edge_functions%3Awrite+environment%3Aread+environment%3Awrite+storage%3Aread&resource=https%3A%2F%2Fmcp.supabase.com%2Fmcp%3Fproject_ref%3Dhaimjeaetrsaauitrhfy

## Instructions:

1. **Click the link above** or copy and paste it into your browser
2. **Log in to your Supabase account** if prompted
3. **Grant the requested permissions** to allow MCP server access
4. **After authorization**, you will be redirected to a localhost URL (which may show an error page - this is expected)
5. **Copy the FULL URL** from your browser's address bar
6. **Provide that callback URL** to me using:
   ```
   mcp__supabase__complete_authentication callback_url="[PASTE_FULL_CALLBACK_URL_HERE]"
   ```

Once authenticated, I will be able to access Supabase MCP tools to:
- List database tables
- Execute SQL queries (e.g., check listing counts)
- Run security and performance advisors
- And other database operations

## Troubleshooting:
- If you encounter issues, ensure you are logged into the correct Supabase account associated with project `haimjeaetrsaauitrhfy`
- The redirect URI `http://localhost:57363/callback` is expected to fail to load - this is normal
- The important part is capturing the full redirect URL from the address bar