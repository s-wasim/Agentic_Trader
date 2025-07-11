CREATE DATABASE IF NOT EXISTS AGENTIC_TRADER;
-- DROP DATABASE AGENTIC_TRADER;
-- Partitioned base table for all tickers (not usually needed, but possible)
CREATE TABLE IF NOT EXISTS AGENTIC_TRADER.Ticker (
    TickerName VARCHAR(16) PRIMARY KEY,
    CompanyName VARCHAR(128) NULL,
    Sector VARCHAR(64),
    IsActive BOOLEAN DEFAULT TRUE
);

-- Financials tables
-- Bridge table for finances
CREATE TABLE IF NOT EXISTS AGENTIC_TRADER.Ticker_Financials (
    TickerFinancesID SERIAL PRIMARY KEY,
    TickerName VARCHAR(16) NOT NULL,
    FinancialsType VARCHAR(32) NOT NULL CHECK (
        FinancialsType IN (
            'IncomeStatement',
            'BalanceSheet',
            'CashFlow',
            'Ratios',
            'Dividends'
        )
    ),
    UNIQUE (
        TickerName,
        FinancialsType
    ),
    FOREIGN KEY (TickerName) REFERENCES AGENTIC_TRADER.Ticker (TickerName) ON DELETE CASCADE
);

/* PIVOT FINANCIALS TABLE AS:
    Sales DECIMAL(20, 2) CHECK (Sales >= 0),
    COGS DECIMAL(20, 2) CHECK (COGS >= 0),
    GrossProfit DECIMAL(20, 2),
    AdministrativeExpenses DECIMAL(20, 2),
    SellingDistributiveExpenses DECIMAL(20, 2),
    FinancialCharges DECIMAL(20, 2),
    ChangeInValueOfInvestment DECIMAL(20, 2),
    OtherExpenses DECIMAL(20, 2),
    EBITDA DECIMAL(20, 2),
    EBIT DECIMAL(20, 2),
    EBT DECIMAL(20, 2),
    Tax DECIMAL(20, 2),
    PAT DECIMAL(20, 2),
    EPS DECIMAL(10, 2)
*/

CREATE TABLE IF NOT EXISTS AGENTIC_TRADER.Financial_Details (
    ID SERIAL PRIMARY KEY,
    TickerFinancesID BIGINT UNSIGNED,
    Year INT CHECK (Year > 1900),
    MetricName VARCHAR(250),
    MetricValue DECIMAL(20, 2),
    FOREIGN KEY (TickerFinancesID) REFERENCES AGENTIC_TRADER.Ticker_Financials (TickerFinancesID) ON DELETE CASCADE
);

-- Payouts table
CREATE TABLE IF NOT EXISTS AGENTIC_TRADER.Payouts (
    ID SERIAL PRIMARY KEY,
    TickerName VARCHAR(16) NOT NULL,
    PayoutDate DATE NOT NULL,
    PayoutType VARCHAR(16) NOT NULL CHECK (
        PayoutType IN ('Dividend', 'Bonus', 'Split')
    ),
    FaceValue NUMERIC(10, 2) CHECK (FaceValue >= 0),
    PayoutPercent NUMERIC(10, 2) CHECK (PayoutPercent >= 0),
    FOREIGN KEY (TickerName) REFERENCES AGENTIC_TRADER.Ticker (TickerName) ON DELETE CASCADE
);

-- Price table
CREATE TABLE IF NOT EXISTS AGENTIC_TRADER.PriceHistory (
    PriceID SERIAL PRIMARY KEY,
    TickerName VARCHAR(16) NOT NULL,
    PriceDate DATE NOT NULL,
    Price NUMERIC(20, 2) CHECK (Price >= 0),
    FOREIGN KEY (TickerName) REFERENCES AGENTIC_TRADER.Ticker (TickerName) ON DELETE CASCADE
);

-- Technicals table
CREATE TABLE IF NOT EXISTS AGENTIC_TRADER.TechnicalIndicators (
    TechnicalID BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    TickerName VARCHAR(16) NOT NULL,
    IndicatorName VARCHAR(32) NOT NULL,
    IndicatorValue TEXT NOT NULL,
    IndicatorAction VARCHAR(16),
    FOREIGN KEY (TickerName) REFERENCES AGENTIC_TRADER.Ticker (TickerName) ON DELETE CASCADE
);