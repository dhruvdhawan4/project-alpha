# modules/sentiment.py
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
import yfinance as yf

class AlternativeSentimentEngine:
    """
    Module 6: Alternative Data & Sentiment Engine
    Extracts market fear metrics and scans public media channels for sentiment spikes.
    """
    def __init__(self):
        pass

    def fetch_market_fear_index(self):
        try:
            vix = yf.Ticker("^VIX")
            vix_hist = vix.history(period="5d")
            if not vix_hist.empty:
                current_vix = vix_hist['Close'].iloc[-1]

                if current_vix > 25:
                    stance = "HIGH_FEAR_PANIC"
                elif current_vix < 13:
                    stance = "COMPLACENCY_EXCESS"
                else:
                    stance = "NORMAL_VOLATILITY"

                return {"Current_VIX": round(current_vix, 2), "VIX_Stance": stance}
        except Exception:
            pass
        
        return {"Current_VIX": 15.0, "VIX_Stance": "NORMAL_VOLATILITY"}

    def analyze_news_buzz(self, company_name):
        try:
            query = urllib.parse.quote(company_name)
            url = f"https://news.google.com/rss/search?q={query}&hl=en-IN&gl=IN&ceid=IN:en"

            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=5) as response:
                xml_data = response.read()

            root = ET.fromstring(xml_data)
            titles = [item.find('title').text for item in root.findall('.//item')[:15]]

            bullish_keywords = ['growth', 'surge', 'profit', 'buy', 'higher', 'earnings', 'deal', 'win', 'expansion', 'up', 'bull']
            bearish_keywords = ['drop', 'fall', 'loss', 'decline', 'risk', 'fraud', 'slump', 'crash', 'investigation', 'down', 'bear']

            bullish_count = 0
            bearish_count = 0

            for title in titles:
                title_lower = title.lower()
                bullish_count += sum(1 for word in bullish_keywords if word in title_lower)
                bearish_count += sum(1 for word in bearish_keywords if word in title_lower)

            total_hits = bullish_count + bearish_count

            if total_hits > 0:
                sentiment_score = (bullish_count - bearish_count) / total_hits
            else:
                sentiment_score = 0.0 

            return {
                "Media_Volume_Hits": len(titles),
                "Sentiment_Score": round(sentiment_score, 2),
                "Buzz_Stance": "Bullish Bias" if sentiment_score > 0.1 else ("Bearish Bias" if sentiment_score < -0.1 else "Neutral")
            }

        except Exception as e:
            return {"Media_Volume_Hits": 0, "Sentiment_Score": 0.0, "Buzz_Stance": "Data Temporarily Offline"}
