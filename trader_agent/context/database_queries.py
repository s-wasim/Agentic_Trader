from enum import Enum

class ContextQueries(Enum):
    __BASE_TICKER_QUERY = """
SELECT T.TickerName, TBL.{} FROM AGENTIC_TRADER.{} AS TBL
    INNER JOIN AGENTIC_TRADER.Ticker T USING(TickerName)
WHERE T.TickerName IN ('{}')
"""
    __EXTENDED_TICKER_QUERY = """
SELECT T.TickerName, TBL_1.{}, TBL_2.{} FROM AGENTIC_TRADER.{} AS TBL_1
    INNER JOIN AGENTIC_TRADER.{} TBL_2 USING(TickerFinancesID)
    INNER JOIN AGENTIC_TRADER.Ticker USING(TickerName)
WHERE T.TickerName IN ('{}')
"""

    @staticmethod
    def get_all_tickers(sector, shariah=True):
        return f"""
SELECT TickerName, CompanyName, Sector 
FROM AGENTIC_TRADER.Ticker {"" if not shariah else "INNER JOIN AGENTIC_TRADER.PriceHistory USING(TickerName)"}
WHERE IsActive=1 AND Sector={sector};
"""

    @staticmethod
    def get_price_history(**kwargs):
        ContextQueries.__BASE_TICKER_QUERY.format(
            ", TBL.".join(["PriceDate", "Price"]),
            "PriceHistory",
            "', '".join(kwargs["tickers"])
        )

    @staticmethod
    def get_payouts(**kwargs):
        ContextQueries.__BASE_TICKER_QUERY.format(
            ", TBL.".join(["PayoutDate", "PayoutType", "FaceValue", "PayoutPercent"]),
            "Payouts",
            "', '".join(kwargs["tickers"])
        )

    @staticmethod
    def get_technical_indicators(**kwargs):
        ContextQueries.__BASE_TICKER_QUERY.format(
            ", TBL.".join(["IndicatorName", "IndicatorValue"]),
            "PriceHistory",
            "', '".join(kwargs["tickers"])
        )

    @staticmethod
    def get_company_finances(**kwargs):
        ContextQueries.__EXTENDED_TICKER_QUERY.format(
            ", TBL_1.".join(["FinancialsType"]),
            ", TBL_2.".join(["Year", "MetricName", "MetricValue"]),
            "Ticker_Financials", "Financial_Details",
            "', '".join(kwargs["tickers"])
        )