"""
TradingView cookies for API requests.
Uses browser cookie extraction to bypass TradingView's bot detection.
"""
import rookiepy
from tradingview_screener import Query

def test_cookies():
    domains = ['.tradingview.com']

    # 1. Chromium Dene
    try:
        cookies = rookiepy.chromium(domains)
        if cookies:
            print("✅ TradingView cookie'leri Chromium tarayıcısından başarıyla okundu.")
            return rookiepy.to_cookiejar(cookies)
    except Exception:
        pass

    # 2. Chrome Dene
    try:
        cookies = rookiepy.chrome(domains)
        if cookies:
            print("✅ TradingView cookie'leri Chrome tarayıcısından başarıyla okundu.")
            return rookiepy.to_cookiejar(cookies)
    except Exception:
        pass

    # 3. Firefox Dene
    try:
        cookies = rookiepy.firefox(domains)
        if cookies:
            print("✅ TradingView cookie'leri Firefox tarayıcısından başarıyla okundu.")
            return rookiepy.to_cookiejar(cookies)
    except Exception:
        pass

    # 4. Hiçbir tarayıcıda aktif oturum bulunamazsa (Graceful Info Fallback)
    print("ℹ️ Tarayıcılarda aktif TradingView oturumu bulunamadı. Manuel sessionid yedeği devrede.")
    return {'sessionid': '<tarayici_sessionid_yedeği>'}

if __name__ == "__main__":
    test_cookies()
