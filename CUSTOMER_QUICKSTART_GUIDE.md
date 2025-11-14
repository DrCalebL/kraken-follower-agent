# 🚀 Nike Rocket - Customer Quick Start Guide

**Welcome to Nike Rocket automated trading!**

This guide will help you get started in **under 10 minutes**.

---

## 📋 What You Need

Before starting, make sure you have:

- ✅ Valid email address
- ✅ Kraken Futures account (or create one)
- ✅ Computer or phone with internet
- ✅ 10 minutes of time

**That's it!** No coding skills needed.

---

## 🎯 STEP 1: Sign Up for Nike Rocket

### 1.1 Visit the Signup Page

Go to: **https://nike-rocket-api-production.up.railway.app/signup**

### 1.2 Enter Your Email

- Type your email address
- Click **"Create Account"**
- Wait 2 seconds...

### 1.3 Save Your API Key

You'll see something like: `nk_abc123def456xyz`

**IMPORTANT:** 
- ✅ Copy this key immediately
- ✅ Save it in a password manager or secure note
- ✅ You'll need it in Step 3!

---

## 🔑 STEP 2: Create Kraken API Keys

### 2.1 Option A: Practice with Testnet (Recommended!)

**Best for beginners - Use fake money first!**

1. Go to: **https://demo-futures.kraken.com**
2. Click **"Sign Up"** (top right)
3. Create free demo account
4. You'll get $100,000 fake USD to practice!
5. Follow Step 2.3 below to create API keys

### 2.2 Option B: Use Real Kraken Account

**For live trading with real money**

1. Go to: **https://pro.kraken.com**
2. Log into your account
3. Follow Step 2.3 below to create API keys

### 2.3 Creating Your API Keys

**Follow these steps exactly:**

1. Click your **name** (top right corner)
2. Click **"Settings"**
3. Click **"Connections & API"** tab
4. Scroll down to **"Futures trading API"** section
5. Click **"Create API key"** button (purple button on the right)

6. A modal will appear: **"Add Futures API key"**

7. **Set Permissions** (CRITICAL - READ CAREFULLY):
   
   **General API:**
   - Select: **"Full access"** (click the circle - it turns purple)
   
   **Withdrawal API:**
   - Select: **"No access"** (click the circle - it turns purple)
   - ⚠️ **NEVER select "Full access" for Withdrawal API!**
   
   **IP address restriction:**
   - Leave toggle **"Off"**

8. Click **"Generate key"** button (purple button at bottom)

9. **Copy BOTH values immediately:**
   - **API Key:** Starts with letters/numbers
   - **API Secret:** Long string of random characters

**⚠️ CRITICAL:** Your API Secret is shown **ONLY ONCE**! If you close the window without copying it, you'll need to create a new API key.

**Save both securely:**
- Password manager (recommended: 1Password, LastPass, Bitwarden)
- Secure notes app
- Write them down and keep in a safe place

---

## 🚀 STEP 3: Deploy Your Follower Agent

### 3.1 Click Deploy Button

From the Nike Rocket signup page, click the green button: **"Deploy to Render →"**

Or go directly to: https://render.com/deploy?repo=https://github.com/DrCalebL/kraken-follower-agent

### 3.2 Sign Into Render

If you don't have a Render account:
- Click **"Get Started for Free"**
- Sign up with GitHub, GitLab, or Google
- **No credit card required!**

If you already have an account:
- Just sign in

### 3.3 Fill In Your Credentials

You'll see a form with these fields:

**Blueprint Name:**
- Leave as: `Nike Kraken Signals` (or name it whatever you want)

**Branch:**
- Leave as: `main`

**USER_API_KEY:**
- Paste the API key from Step 1.3
- Example: `nk_abc123def456xyz`

**KRAKEN_API_KEY:**
- Paste your Kraken API Key from Step 2.3
- Example: `abcd1234efgh5678`

**KRAKEN_API_SECRET:**
- Paste your Kraken API Secret from Step 2.3
- Example: `xyz789abc123def456ghi789`

### 3.4 Leave Other Settings As-Is

**FOLLOWER_API_URL:**
- Already set to: `https://nike-rocket-api-production.up.railway.app`
- Don't change this!

**USE_TESTNET:**
- `true` = Practice with demo account (fake money)
- `false` = Live trading (real money)
- Start with `true` if using Kraken Demo!

**Note:** The agent automatically fetches your real account balance from Kraken, so you don't need to enter it manually!

### 3.5 Deploy!

1. Click **"Apply"** or **"Create Web Service"** button
2. Wait 2-3 minutes while Render deploys
3. You'll see a progress bar...
4. When done, you'll see: **"Live"** with a green dot! ✅

---

## 🎉 STEP 4: Verify It's Working

### 4.1 Check Render Logs

In your Render dashboard:
1. Click on your deployed service
2. Click **"Logs"** tab
3. You should see:
   ```
   🚀 NIKE ROCKET FOLLOWER AGENT
   API URL: https://nike-rocket-api-production.up.railway.app
   Mode: TESTNET (Demo)
   💰 Account balance will be fetched when signal arrives
   ✅ Access verified
   📡 Polling for signals every 10 seconds...
   ⏳ No new signals (polling...)
   ```

**If you see this, you're all set!** ✅

### 4.2 What Happens Next

Your agent is now running 24/7! It will:

1. **Poll for signals** every 10 seconds
2. **Receive trade signals** from Nike Rocket master algorithm
3. **Fetch your real account balance** from Kraken
4. **Calculate position size** (2% risk based on actual balance)
5. **Execute trades** automatically on your Kraken account
6. **Manage positions** with automatic TP/SL orders
7. **Report P&L** back to Nike Rocket for billing

**You don't need to do anything else!**

**When a signal arrives, you'll see:**
```
📡 NEW SIGNAL RECEIVED
💰 Fetching account balance...
💰 Current equity: $10,523.45 USD
✅ No existing position found
🎯 POSITION SIZING:
Account Equity: $10,523.45
Risk Amount (2%): $210.47
🚀 EXECUTING KRAKEN BRACKET ORDER...
✅ Order executed successfully!
```

---

## 💰 STEP 5: Understanding Billing

### 5.1 How It Works

- **No monthly subscription!**
- You only pay **10% of monthly profits**
- If you lose money or break even → You pay **$0**

### 5.2 Examples

**Month 1:**
- Profit: +$1,000
- You pay: $100 (10%)

**Month 2:**
- Profit: -$200 (loss)
- You pay: $0

**Month 3:**
- Profit: +$500
- You pay: $50 (10%)

### 5.3 Payment Process

At the end of each month:
1. You'll receive an email with your P&L summary
2. If you made a profit, you'll get a payment link
3. Pay via crypto (USDT/USDC accepted)
4. You have 7 days to pay
5. After payment, trading continues normally!

**If you don't pay within 7 days:**
- Your agent will stop receiving new signals
- Your existing positions stay open (with TP/SL protection)
- Once you pay, signals resume immediately

---

## 🛡️ STEP 6: Safety & Security

### 6.1 Your Funds Are Safe

- ✅ Your money **NEVER leaves Kraken**
- ✅ We **cannot withdraw** your funds (you disabled that permission!)
- ✅ You maintain **full control** of your account
- ✅ You can **revoke API access** anytime

### 6.2 Risk Management

Every trade has:
- ✅ Automatic **stop-loss** protection
- ✅ Automatic **take-profit** targets
- ✅ **2% max risk** per trade
- ✅ Professional **risk management**

### 6.3 How to Stop Trading

**To pause trading:**
1. Go to your Render dashboard
2. Click your service
3. Click **"Manual Deploy"** → **"Suspend"**

**To completely stop:**
1. Go to Kraken Settings → API
2. Delete the API key
3. Agent will stop immediately

---

## ❓ Troubleshooting

### "Access denied" error

**Problem:** Agent can't connect to Nike Rocket API

**Solution:**
1. Check your USER_API_KEY is correct
2. Make sure you copied it exactly (no spaces!)
3. Try creating a new API key on signup page

### "Kraken authentication failed" error

**Problem:** Agent can't connect to Kraken

**Solution:**
1. Check KRAKEN_API_KEY and KRAKEN_API_SECRET are correct
2. Make sure you set "General API" to "Full access"
3. Make sure you set "Withdrawal API" to "No access"
4. Try creating a new Kraken API key

### "No signals received" message

**Problem:** Agent is running but no trades happening

**Solution:**
- This is normal! The master algorithm only trades when conditions are right
- Could be hours or days between signals
- Agent is working - just waiting for good opportunities
- Check back later or view logs to confirm it's still polling

### Agent stopped working

**Problem:** Agent shows "Crashed" or "Offline"

**Solution:**
1. Check Render logs for error messages
2. Try clicking "Manual Deploy" → "Deploy latest commit"
3. Verify your Kraken API keys haven't expired
4. Contact support if issue persists

---

## 📞 Getting Help

### Support Channels

**Email:** support@nikerocket.io
**Discord:** [Join our community]
**Documentation:** https://nike-rocket-api-production.up.railway.app/

### Before Contacting Support

Please have ready:
1. Your USER_API_KEY
2. Screenshot of Render logs
3. Description of the problem
4. When the problem started

**We typically respond within 24 hours!**

---

## 🎓 Tips for Success

### 1. Start with Testnet!

- Practice with fake money first
- Get comfortable with the system
- Once confident, switch to live trading

### 2. Don't Overtrade

- The algorithm is selective
- Quality > Quantity
- Trust the process

### 3. Your Position Sizes Scale Automatically

- Agent fetches your REAL account balance before each trade
- Position sizes grow as your account grows
- Position sizes shrink if you have losses
- Always maintains 2% risk - no manual updates needed!

### 4. Monitor Performance

- Check your Render logs weekly
- Review your Kraken account regularly
- Track monthly P&L
- Watch how your positions scale with balance

### 5. Be Patient

- This is not "get rich quick"
- Consistent profits take time
- Some months will be down, some up
- Long-term average is what matters

---

## 📊 Expected Performance

### Realistic Expectations

**Win Rate:** ~45-50% of trades are winners
**Average Win:** 2-4% per trade
**Average Loss:** 1-2% per trade (stop-loss protection)
**Monthly Target:** 5-15% return on capital

### Example Results

**$10,000 Starting Capital:**
- Month 1: +$800 (8%)
- Month 2: -$200 (-2%)
- Month 3: +$1,200 (12%)
- Month 4: +$400 (4%)

**6-Month Average:** ~7% per month

**⚠️ Past performance does not guarantee future results!**

---

## 🎉 You're All Set!

**Congratulations!** Your automated trading agent is now live!

### What Happens Now?

1. ✅ Agent runs 24/7 on Render (you can close your computer!)
2. ✅ Receives signals from Nike Rocket master algorithm
3. ✅ Executes trades automatically on your Kraken account
4. ✅ Manages risk with stop-loss and take-profit orders
5. ✅ Reports P&L for monthly billing

### Sit Back and Let It Work!

You don't need to:
- ❌ Watch charts
- ❌ Make trading decisions
- ❌ Set manual orders
- ❌ Stay up late

The algorithm does it all for you!

---

## 📱 Stay Updated

**Join our community:**
- Discord: Real-time trade alerts
- Email: Monthly performance reports
- Twitter: Market updates

---

**Happy Trading!** 🚀💰

*Questions? Email: support@nikerocket.io*

---

*This guide was last updated: November 14, 2025*
*Version: 1.0*
