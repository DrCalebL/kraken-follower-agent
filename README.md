# 🚀 Nike Rocket - Kraken Futures Follower Agent

Automated trading agent that follows professional Kraken Futures signals with one-click deployment.

## ⚡ One-Click Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/DrCalebL/kraken-follower-agent)

---

## 📋 What This Does

This agent automatically:
- ✅ Receives trading signals from Nike Rocket API
- ✅ Executes trades on YOUR Kraken Futures account
- ✅ Uses bracket orders (automatic TP/SL)
- ✅ Manages positions safely (skips if already in trade)
- ✅ Tracks your P&L automatically
- ✅ Reports profits for monthly billing (10% profit sharing)

**Your funds stay in YOUR Kraken account!** This is non-custodial.

---

## 🔧 Setup (5 Minutes)

### Prerequisites

1. **Nike Rocket API Key** - Get this after signing up
2. **Kraken Futures Account** - [Sign up here](https://futures.kraken.com)
3. **Kraken API Credentials** - Create at Kraken Settings → API

---

### Deployment Steps

**1. Click "Deploy to Render" button above**

**2. Sign into Render** (free account, no credit card needed)

**3. Enter your credentials:**

```
FOLLOWER_API_URL: https://nike-rocket-api-production.up.railway.app
USER_API_KEY: Your Nike Rocket API key (from signup)
KRAKEN_API_KEY: Your Kraken API key
KRAKEN_API_SECRET: Your Kraken API secret
USE_TESTNET: true (for testing) or false (for live trading)
```

**4. Click "Create Web Service"**

**5. Wait 2-3 minutes for deployment**

**✅ Done!** Your agent is now running 24/7!

---

## 🔒 Security

**Your API keys are safe:**
- ✅ Stored encrypted on Render
- ✅ Only you can see them
- ✅ Agent can ONLY trade (cannot withdraw)
- ✅ You can revoke access anytime

**Kraken API permissions needed:**
- ✅ General API: **Full access**
- ❌ Withdrawal API: **No access** (CRITICAL - never enable this!)

---

## 💰 Pricing

**No subscription fees!**

- Pay only **10% of monthly profits**
- No fees on losing months
- 7-day grace period for payment

**Example:**
- Month 1: +$500 profit → Pay $50
- Month 2: -$200 loss → Pay $0
- Month 3: +$1000 profit → Pay $100

---

## 📊 How It Works

```
1. Nike Rocket algorithm analyzes market
2. Generates BUY/SELL signal
3. Broadcasts to Nike Rocket API
4. Your agent receives signal (within 10 seconds)
5. Agent fetches your REAL Kraken account balance
6. Calculates position size (2% risk)
7. Executes on YOUR Kraken account
8. Position managed with automatic TP/SL
9. Position closes when TP or SL hit
10. Agent reports P&L for billing
```

---

## ⚙️ Settings

### Account Balance
**Automatically fetched from Kraken!** The agent queries your real account balance before each trade, so position sizing is always 100% accurate.

**Multi-currency support:**
- USD
- USDT  
- USDC

Your positions scale automatically as your account grows!

### Testnet vs Live
- **Testnet (true):** Practice with fake money on Kraken demo
- **Live (false):** Real trading with real money

**Always test on testnet first!**

---

## 🆘 Support

**Issues?**
- Check Render logs for errors
- Verify Kraken API keys are correct
- Ensure API has trading permissions
- Make sure Kraken account has sufficient margin

**Need help?**
- Email: support@nikerocket.io
- Discord: [Join our community]

---

## 📈 Performance

Agent performance matches the master algorithm:
- Typical win rate: ~45-50%
- Average trade: 2-4% gain
- Risk management: 2% per trade
- Uses leverage: 1-5x

**Past performance does not guarantee future results.**

---

## ⚠️ Risk Warning

**Cryptocurrency trading involves substantial risk:**
- You can lose your entire investment
- Leverage amplifies both gains and losses
- Only trade with money you can afford to lose
- This is not financial advice

**You are responsible for:**
- Your trading decisions
- Your Kraken account
- Your risk management
- Understanding the risks

---

## 📜 Terms

By deploying this agent:
- ✅ You agree to 10% profit sharing on winning months
- ✅ You understand trading risks
- ✅ You control your funds (non-custodial)
- ✅ You can stop anytime

---

## 🎉 Ready to Start?

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/DrCalebL/kraken-follower-agent)

**Questions before deploying?** Contact support!

---

**Happy Trading! 🚀💰**
