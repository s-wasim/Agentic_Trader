-- Partitioned base table for all tickers (not usually needed, but possible)
CREATE TABLE IF NOT EXISTS AGENTIC_TRADER.Ticker (
    TickerName VARCHAR(16) PRIMARY KEY,
    CompanyName VARCHAR(128) NOT NULL,
    Sector VARCHAR(64),
    IsActive BOOLEAN DEFAULT TRUE
);

-- Financials tables (NO partitioning)

CREATE TABLE IF NOT EXISTS AGENTIC_TRADER.Financials_IncomeStatement (
    Finances_Ticker_ID INT AUTO_INCREMENT PRIMARY KEY,
    TickerName VARCHAR(16) NOT NULL,
    Year INT CHECK (Year > 1900),
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
    EPS DECIMAL(10, 2),
    FOREIGN KEY (TickerName) REFERENCES AGENTIC_TRADER.Ticker (TickerName) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS AGENTIC_TRADER.Financials_BalanceSheet (
    Finances_Ticker_ID INT AUTO_INCREMENT PRIMARY KEY,
    TickerName VARCHAR(16) NOT NULL,
    Year INT CHECK (Year > 1900),
    FixedAssets DECIMAL(20, 2),
    Investments DECIMAL(20, 2),
    CashInHandAndBank DECIMAL(20, 2),
    StoresAndSpares DECIMAL(20, 2),
    StockInTrade DECIMAL(20, 2),
    TradeDebts DECIMAL(20, 2),
    CurrentAssets DECIMAL(20, 2),
    QuickAssets DECIMAL(20, 2),
    TotalAssets DECIMAL(20, 2),
    InterestBearingLongTermLiability DECIMAL(20, 2),
    NonInterestBearingLongTermLiability DECIMAL(20, 2),
    InterestBearingShortTermLiability DECIMAL(20, 2),
    NonInterestBearingShortTermLiability DECIMAL(20, 2),
    TradesPayables DECIMAL(20, 2),
    TotalCurrentLiabilities DECIMAL(20, 2),
    TotalLiabilities DECIMAL(20, 2),
    PaidUpCapital DECIMAL(20, 2),
    Reserves DECIMAL(20, 2),
    PreferredEquity DECIMAL(20, 2),
    SurplusOnRevaluationOfAssets DECIMAL(20, 2),
    ShareholderEquity DECIMAL(20, 2),
    PaidUpValue DECIMAL(10, 2),
    NumberOfShares DECIMAL(20, 2),
    FOREIGN KEY (TickerName) REFERENCES AGENTIC_TRADER.Ticker (TickerName) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS AGENTIC_TRADER.Financials_CashFlow (
    Finances_Ticker_ID INT AUTO_INCREMENT PRIMARY KEY,
    TickerName VARCHAR(16) NOT NULL,
    Year INT CHECK (Year > 1900),
    OperatingCashFlow DECIMAL(20, 2),
    CapitalExpenditure DECIMAL(20, 2),
    CashflowFromInvesting DECIMAL(20, 2),
    CashFlowFromFinancing DECIMAL(20, 2),
    NetChange DECIMAL(20, 2),
    OpeningCash DECIMAL(20, 2),
    ClosingCash DECIMAL(20, 2),
    FCFF DECIMAL(20, 2),
    FCFE DECIMAL(20, 2),
    FOREIGN KEY (TickerName) REFERENCES AGENTIC_TRADER.Ticker (TickerName) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS AGENTIC_TRADER.Financials_Ratios (
    Finances_Ticker_ID INT AUTO_INCREMENT PRIMARY KEY,
    TickerName VARCHAR(16) NOT NULL,
    Year INT CHECK (Year > 1900),
    Payout DECIMAL(10, 2),
    PlowBack DECIMAL(10, 2),
    ReturnOnEquity DECIMAL(10, 2),
    ReturnOnAssets DECIMAL(10, 2),
    BookValuePerShare DECIMAL(20, 2),
    EarningPerShare DECIMAL(20, 2),
    NetWorkingCapitalToTotalAssets DECIMAL(10, 2),
    CurrentRatio DECIMAL(10, 2),
    AcidTest DECIMAL(10, 2),
    TimesInterestEarned DECIMAL(10, 2),
    TotalDebtRatio DECIMAL(10, 2),
    DebtToEquity DECIMAL(10, 2),
    ReturnOnCapitalEmployed DECIMAL(10, 2),
    AverageCollectionPeriod DECIMAL(10, 2),
    DaysSalesInventory DECIMAL(10, 2),
    TotalAssetsTurnover DECIMAL(10, 2),
    GrossProfitMargin DECIMAL(10, 2),
    NetProfitMargin DECIMAL(10, 2),
    FOREIGN KEY (TickerName) REFERENCES AGENTIC_TRADER.Ticker (TickerName) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS AGENTIC_TRADER.Financials_Dividends (
    Finances_Ticker_ID INT AUTO_INCREMENT PRIMARY KEY,
    TickerName VARCHAR(16) NOT NULL,
    Year INT CHECK (Year > 1900),
    CashDividend DECIMAL(20, 2),
    AnnualDividendPerShare DECIMAL(20, 2),
    PreferredDividend DECIMAL(20, 2),
    FOREIGN KEY (TickerName) REFERENCES AGENTIC_TRADER.Ticker (TickerName) ON DELETE CASCADE
);

-- Bridge table for finances
CREATE TABLE IF NOT EXISTS AGENTIC_TRADER.Ticker_Financials (
    TickerFinancesID SERIAL PRIMARY KEY,
    TickerName VARCHAR(16) NOT NULL,
    Finances_Ticker_ID INT NOT NULL,
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
        Finances_Ticker_ID,
        FinancialsType
    ),
    FOREIGN KEY (TickerName) REFERENCES AGENTIC_TRADER.Ticker (TickerName) ON DELETE CASCADE
);

-- Payouts table
CREATE TABLE IF NOT EXISTS AGENTIC_TRADER.Payouts (
    PayoutID BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    TickerName VARCHAR(16) NOT NULL,
    PayoutDate DATE NOT NULL,
    PayoutType VARCHAR(16) NOT NULL CHECK (
        PayoutType IN ('Dividend', 'Bonus')
    ),
    FaceValue NUMERIC(10, 2) CHECK (FaceValue >= 0),
    PayoutPercent NUMERIC(10, 2) CHECK (PayoutPercent >= 0),
    FOREIGN KEY (TickerName) REFERENCES AGENTIC_TRADER.Ticker (TickerName) ON DELETE CASCADE
);

-- Bridge table for payouts
CREATE TABLE IF NOT EXISTS AGENTIC_TRADER.Ticker_Payouts (
    TickerPayoutID BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    TickerName VARCHAR(16) NOT NULL,
    PayoutID BIGINT UNSIGNED NOT NULL,
    UNIQUE (TickerName, PayoutID),
    FOREIGN KEY (TickerName) REFERENCES AGENTIC_TRADER.Ticker (TickerName) ON DELETE CASCADE,
    FOREIGN KEY (PayoutID) REFERENCES AGENTIC_TRADER.Payouts (PayoutID) ON DELETE CASCADE
);

-- Price table
CREATE TABLE IF NOT EXISTS AGENTIC_TRADER.PriceHistory (
    PriceID BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    TickerName VARCHAR(16) NOT NULL,
    PriceDate DATE NOT NULL,
    Price NUMERIC(20, 2) CHECK (Price >= 0),
    FOREIGN KEY (TickerName) REFERENCES AGENTIC_TRADER.Ticker (TickerName) ON DELETE CASCADE
);

-- Bridge table for price
CREATE TABLE IF NOT EXISTS AGENTIC_TRADER.Ticker_PriceHistory (
    TickerPriceID SERIAL PRIMARY KEY,
    TickerName VARCHAR(16) NOT NULL,
    PriceID BIGINT UNSIGNED,
    UNIQUE (TickerName, PriceID),
    FOREIGN KEY (TickerName) REFERENCES AGENTIC_TRADER.Ticker (TickerName) ON DELETE CASCADE,
    FOREIGN KEY (PriceID) REFERENCES AGENTIC_TRADER.PriceHistory (PriceID) ON DELETE CASCADE
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

-- Bridge table for technicals
CREATE TABLE IF NOT EXISTS AGENTIC_TRADER.Ticker_Technicals (
    TickerTechnicalID BIGINT UNSIGNED PRIMARY KEY,
    TickerName VARCHAR(16) NOT NULL,
    TechnicalID  BIGINT UNSIGNED,
    UNIQUE (TickerName, TechnicalID),
    FOREIGN KEY (TickerName) REFERENCES AGENTIC_TRADER.Ticker (TickerName) ON DELETE CASCADE,
    FOREIGN KEY (TechnicalID) REFERENCES AGENTIC_TRADER.TechnicalIndicators (TechnicalID) ON DELETE CASCADE
);