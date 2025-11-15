# 🚀 Nike Rocket - Kraken Futures Follower Agent

**Automated trading agent that executes professional Kraken Futures signals with one-click deployment.**

⚠️ **LIVE TRADING ONLY** - This system trades real money from day one. Start small!

---

## 🚨 CRITICAL: Kraken Futures Must Be Activated

**Before deploying, you MUST unlock Kraken Futures:**

1. Have "Intermediate" or "Pro" Kraken verification (not "Starter")
2. Click "Unlock Futures" in Kraken Pro (one-time setup)
3. Create Futures API keys (different from regular API keys!)

**Without activating Futures, your API keys won't work!**

[See detailed instructions below](#what-you-need-first)

---

## ⚡ One-Click Deploy

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/DrCalebL/kraken-follower-agent)

**Click the button above to deploy in 5 minutes!**

---

## 📋 What This Agent Does

Your personal trading bot that runs 24/7:

- ✅ Receives trading signals from Nike Rocket master algorithm
- ✅ Automatically fetches YOUR real Kraken account balance
- ✅ Calculates position size (2% risk per trade)
- ✅ Executes trades on YOUR Kraken Futures account
- ✅ Places 3-order brackets (Entry + Take-Profit + Stop-Loss)
- ✅ Manages positions safely (skips duplicate trades)
- ✅ Reports P&L for monthly billing (10% profit sharing)

**Your funds stay in YOUR Kraken account!** This is non-custodial - you maintain full control.

---

## 🎯 How It Works

```
1. Nike Rocket algorithm analyzes Kraken Futures markets
2. Master algo identifies high-probability trade setup  
3. Signal broadcast to Nike Rocket API (Railway)
4. Your follower agent detects signal (within 10 seconds)
5. Agent fetches your REAL Kraken balance automatically
6. Agent calculates position size (2% risk, auto-leveraged)
7. Agent checks for existing positions (safety!)
8. If clear, executes 3 orders on YOUR Kraken account:
   → Market entry order (instant execution)
   → Limit take-profit order (auto-exit at target)
   → Stop-loss order (protects against big losses)
9. Position managed automatically until TP or SL hit
10. Agent reports trade result for billing
```

**Zero manual intervention required!**

---

## 💰 Pricing - Simple Profit Sharing

**No subscription. No monthly fees.**

You only pay **10% of monthly profits:**

| Your Monthly P&L | What You Pay |
|------------------|--------------|
| +$1,000 profit | $100 (10%) |
| +$500 profit | $50 (10%) |
| $0 (break even) | $0 |
| -$200 (loss) | $0 |

**Payment process:**
- Monthly statement email (3rd of each month)
- 7-day grace period to pay
- Pay via crypto (USDT/USDC)
- Trading continues during grace period
- After 7 days: new signals pause until paid

---

## 🔧 Setup (5 Minutes)

### What You Need First

1. **Nike Rocket API Key**
   - Sign up at: https://nike-rocket-api-production.up.railway.app/signup
   - Verify your email
   - Copy your API key (starts with `nk_`)

2. **Kraken Futures Account with "Intermediate" Verification**
   - Create account at: https://pro.kraken.com
   - **Complete "Intermediate" verification** (required for Futures!)
     - Provide: Full name, DOB, phone, address
     - Upload: Photo ID, proof of address, selfie
     - Wait 10 min to 24 hours for approval
   - **Unlock Futures trading:**
     1. Go to Kraken Pro → Trade tab
     2. Select any Futures market
     3. Click "Unlock Futures" button
     4. Accept Terms of Service
     5. Accept Risk Disclosure
   - Fund your Futures wallet ($500+ recommended)

3. **Kraken Futures API Credentials**
   - **AFTER unlocking Futures above:**
   - In Kraken: Settings → API → Futures section
   - Click "Generate Key"
   - Set permissions:
     - ✅ General: **Full access**
     - ❌ Transfers: **No access** (CRITICAL!)
   - Copy both Public and Private keys

---

### Deployment Steps

**1. Click the "Deploy to Render" button above**

**2. Sign into Render**
- Free account, no credit card required
- Sign up with GitHub/Google/GitLab

**3. Fill in the form:**

```
Blueprint Name: nike-rocket-follower
Branch: main
```

**4. Environment Variables:**

```
FOLLOWER_API_URL: https://nike-rocket-api-production.up.railway.app
USER_API_KEY: nk_your_api_key_here
KRAKEN_API_KEY: your_kraken_public_key
KRAKEN_API_SECRET: your_kraken_private_key
```

**5. Click "Deploy"**

**6. Wait 2-3 minutes**

**7. Check logs** - You should see:
```
🚀 NIKE ROCKET FOLLOWER AGENT
Mode: 🔴 LIVE (REAL MONEY) 🔴
✅ Connected to Kraken Futures (LIVE)
✅ Access verified
📡 Polling for signals every 10 seconds...
```

**✅ You're live!**

---

## 🔒 Security & Safety

### Your Funds Are Protected

**What Nike Rocket CAN do:**
- ✅ Place market/limit/stop orders
- ✅ View your balance
- ✅ View your positions
- ✅ Cancel orders

**What Nike Rocket CANNOT do:**
- ❌ Withdraw your funds
- ❌ Transfer to other accounts
- ❌ Change your password
- ❌ Access your email
- ❌ Anything except trading

**Why?** You disabled "Transfers" permission when creating API keys!

### Risk Management Built-In

Every trade includes:
- ✅ **Stop-loss order** - Max 2% loss per trade
- ✅ **Take-profit order** - Automatic profit-taking
- ✅ **Position sizing** - Scales with your balance
- ✅ **Duplicate check** - Won't double up on same symbol

### How to Stop Trading

**Option 1: Pause (Temporary)**
- Render dashboard → Your service → Manual Deploy → Suspend

**Option 2: Revoke API Access (Permanent)**
- Kraken → Settings → API → Delete key

**Option 3: Delete Service**
- Render dashboard → Your service → Settings → Delete Service

---

## 📊 Expected Performance

### Realistic Expectations

**Win rate:** ~45-50% of trades are winners

**Average returns:**
- Good months: +10% to +20%
- Average months: +5% to +8%
- Bad months: -3% to +2%
- **Long-term target: +5% to +10% per month**

**Risk per trade:** Maximum 2% with stop-loss protection

**Leverage used:** 2-5x (automatically calculated)

### Example Results

**Starting with $2,000:**

| Month | Return | Balance | Fee |
|-------|--------|---------|-----|
| 1 | +$240 (12%) | $2,240 | $24 |
| 2 | -$45 (-2%) | $2,195 | $0 |
| 3 | +$175 (8%) | $2,370 | $17.50 |
| 4 | +$95 (4%) | $2,465 | $9.50 |
| 5 | -$75 (-3%) | $2,390 | $0 |
| 6 | +$335 (14%) | $2,725 | $33.50 |

**6-Month result:** +$725 (+36%), Net: +$640 after fees

⚠️ **Past performance does not guarantee future results!**

---

## 🎓 Key Features

### 1. Automatic Balance Fetching

**No manual updates needed!**

- Agent queries YOUR real Kraken balance before every trade
- Supports USD, USDT, USDC
- Position sizes scale automatically as your account grows
- If balance drops, position sizes shrink automatically
- Always maintains 2% risk regardless of account size

**Example:**
```
Account $1,000 → Risk $20/trade → Size: 10 contracts
Account $5,000 → Risk $100/trade → Size: 50 contracts
Account $10,000 → Risk $200/trade → Size: 100 contracts
```

**Set it and forget it!**

### 2. Smart Position Management

**Safety first:**
- Checks for existing positions before trading
- Skips signals if already in same market
- Prevents overexposure
- Protects your capital

**Example from logs:**
```
🔍 Checking for existing positions...
⚠️ Existing position found: 737 contracts
⚠️ Already have a position, skipping signal
```

### 3. Professional Order Execution

**3-order bracket system:**

1. **Entry:** Market order (instant execution)
2. **Take-Profit:** Limit order at target price
3. **Stop-Loss:** Stop order to limit losses

**All placed in 2 seconds:**
```
📝 Placing entry order...
✅ Entry order placed: a05d5325-...
📝 Placing take-profit order...
✅ Take-profit order placed: a05d5328-...
📝 Placing stop-loss order...
✅ Stop-loss order placed: a05d5329-...
```

### 4. Real-Time Logging

**Complete transparency:**
- See every signal received
- See every order placed
- See every balance check
- See every P&L result

**Monitor anytime in Render dashboard!**

---

## 🆘 Troubleshooting

### "Access denied" error

**Problem:** Agent can't authenticate with Nike Rocket API

**Fix:**
1. Verify USER_API_KEY is correct (starts with `nk_`)
2. Check for spaces before/after key
3. Confirm email is verified
4. Try creating new API key

### "Kraken authentication failed"

**Problem:** Can't connect to Kraken account

**Fix:**
1. **Verify Futures is unlocked** (Kraken Pro → Trade → Any Futures market → "Unlock Futures")
2. Verify KRAKEN_API_KEY and KRAKEN_API_SECRET are correct
3. Check you set "General" to "Full access"
4. Confirm "Transfers" is "No access"
5. Verify you're at "Intermediate" verification level (not "Starter")
6. Try creating new Kraken API keys after unlocking Futures

### "No funds detected"

**Problem:** Kraken Futures wallet is empty

**Fix:**
1. Log into Kraken → Futures section
2. Check balance (need $100+ minimum)
3. Transfer from Spot to Futures if needed
4. Wait 1 minute and check logs again

### "No signals for days"

**Problem:** Not seeing any trades

**Fix:**
- **This is normal!** Algorithm is selective
- Could be days between signals
- Check logs verify agent is still polling
- If polling every 10 seconds → It's working!
- Quality over quantity

### Agent crashed

**Problem:** Service shows offline/crashed

**Fix:**
1. Check Render logs for specific errors
2. Click "Manual Deploy" → "Deploy latest commit"
3. Verify API keys haven't expired
4. Contact support if persistent

---

## 📞 Support

### Need Help?

**Email:** support@nikerocket.io

**Include:**
- Your USER_API_KEY (starts with `nk_`)
- Screenshot of error in Render logs
- What you've already tried
- When the issue started

**Response time:** Within 24 hours

### Resources

- **Quick Start Guide:** Full step-by-step setup guide
- **API Status:** https://nike-rocket-api-production.up.railway.app/
- **Discord:** Join our trading community
- **Documentation:** https://docs.nikerocket.io

---

## ⚠️ Risk Warning

### IMPORTANT - READ CAREFULLY

**Cryptocurrency futures trading involves substantial risk:**

- ✅ You can lose your entire investment
- ✅ Leverage amplifies both gains AND losses
- ✅ Past performance does not guarantee future results
- ✅ This is not financial advice
- ✅ We are not financial advisors
- ✅ Only trade with money you can afford to lose completely

**You are responsible for:**
- Your trading decisions
- Your account management  
- Understanding the risks
- Any losses incurred

**By deploying this agent, you agree to:**
- 10% profit sharing on winning months
- No refunds on losing trades
- All terms and conditions
- Risk disclosure above

---

## 🎉 Ready to Start?

### Deploy Now

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/DrCalebL/kraken-follower-agent)

**Setup takes 5 minutes. Trading runs 24/7.**

### Questions Before Deploying?

**Email:** support@nikerocket.io

We're here to help!

---

## 📈 Why Nike Rocket?

### Proven Track Record
- Years of development
- Tested on historical data
- Live trading since 2024
- Consistent methodology

### Professional Risk Management
- 2% max risk per trade
- Stop-loss on every position
- Position sizing scales automatically
- Never over-leveraged

### Fully Automated
- No manual trading
- No chart watching
- No emotional decisions
- Set it and forget it

### Transparent Billing
- Only pay on profits
- Detailed monthly reports
- No hidden fees
- Fair profit-sharing

---

**Happy Trading! 🚀💰**

---

*Repository: https://github.com/DrCalebL/kraken-follower-agent*  
*Last updated: November 15, 2025*  
*Version: 2.0 (Live Trading)*
