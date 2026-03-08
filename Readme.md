   Noctra🌙

Your vibe, reflected in sound.
Noctra is a minimalist AI discovery tool that translates fleeting thoughts and complex moods into curated musical atmospheres. It’s designed for the "nocturnal creator"—those who find inspiration in underrated books, dark roast coffee, and the silence of white tulips.

🎨Design Philosophy
The "Plum Noir" Aesthetic: A custom radial gradient (HEX-2D033B \rightarrow HEX-050812) that provides a deep, velvety backdrop for late-night sessions.
Breathing Typography: A rhythmic CSS pulse on the "Noctra" serif title that mimics a steady heartbeat or an echo.
The Tulip Glow: A high-contrast interaction where the input area glows "Soft White" upon focus, inspired by the elegance of white tulips.

🛠️ Technical Implementation
Intelligence: Powered by gemini-3.1-flash-lite-preview for high-speed, emotive prompt processing.

Smart Playback:

 		1. Native Integration: Uses the spotify:search URI protocol to launch the desktop/mobile app directly.
 
 		2. Logic Fallback: A custom JavaScript "Focus-Check" that redirects to a web search if the native app isn't detected within 2 seconds.

Architecture: Built with Python (Flask) and optimized for Vercel Serverless Functions to ensure 100% uptime with zero cost.

🚀 Deployment
Clone: git clone https://github.com/your-username/noctra-mood.git

Environment: Add your GEMINI_API_KEY to Vercel.

Live: Visit- noctra-mood.vercel.app
