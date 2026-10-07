-- Generic example schema: store each prediction, then grade it later.
CREATE TABLE IF NOT EXISTS predictions (
    id                INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at        TEXT NOT NULL DEFAULT (datetime('now')),
    sport             TEXT NOT NULL,
    event             TEXT NOT NULL,
    market            TEXT NOT NULL,
    model_probability REAL NOT NULL CHECK (model_probability BETWEEN 0 AND 1),
    result            TEXT CHECK (result IN ('win', 'loss', 'push')),
    graded_at         TEXT
);

CREATE INDEX IF NOT EXISTS idx_predictions_sport_created
    ON predictions (sport, created_at);

-- Calibration check: does a higher predicted probability actually win more often?
SELECT
    ROUND(model_probability, 1) AS probability_bucket,
    COUNT(*)                    AS graded_predictions,
    AVG(result = 'win')         AS actual_hit_rate
FROM predictions
WHERE result IN ('win', 'loss')
GROUP BY probability_bucket
ORDER BY probability_bucket;
