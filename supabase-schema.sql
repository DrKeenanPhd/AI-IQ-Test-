
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    mobile VARCHAR(50) NOT NULL,
    ghl_contact_id VARCHAR(255), -- For GHL integration
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS test_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    pain_points JSONB NOT NULL,
    categories JSONB NOT NULL,
    overall_score INTEGER NOT NULL,
    recommendations TEXT[] NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_ghl_contact_id ON users(ghl_contact_id);
CREATE INDEX IF NOT EXISTS idx_test_results_user_id ON test_results(user_id);
CREATE INDEX IF NOT EXISTS idx_test_results_created_at ON test_results(created_at);

ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE test_results ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own data" ON users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own data" ON users
    FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can view own test results" ON test_results
    FOR SELECT USING (user_id = auth.uid());

CREATE POLICY "Users can insert own test results" ON test_results
    FOR INSERT WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update own test results" ON test_results
    FOR UPDATE USING (user_id = auth.uid());


-- Tokens for smart-link access
CREATE TABLE IF NOT EXISTS tokens (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    token TEXT UNIQUE NOT NULL,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    purpose TEXT DEFAULT 'dashboard_access',
    used BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    expires_at TIMESTAMP WITH TIME ZONE NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_tokens_user_id ON tokens(user_id);
CREATE INDEX IF NOT EXISTS idx_tokens_expires_at ON tokens(expires_at);

-- Sessions for sidebar history (normalized high-level record)
CREATE TABLE IF NOT EXISTS sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    title TEXT,
    summary TEXT,
    score INTEGER,
    score_max INTEGER DEFAULT 200,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    data JSONB
);
CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_sessions_created_at ON sessions(created_at);

-- Test runs for cadence enforcement and async jobs
CREATE TABLE IF NOT EXISTS test_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    type TEXT CHECK (type IN ('full','mini')) NOT NULL,
    topic TEXT,
    status TEXT CHECK (status IN ('queued','running','complete','failed')) DEFAULT 'queued',
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    score NUMERIC,
    payload JSONB,
    source TEXT,
    created_by TEXT
);
CREATE INDEX IF NOT EXISTS idx_test_runs_user_id ON test_runs(user_id);
CREATE INDEX IF NOT EXISTS idx_test_runs_started_at ON test_runs(started_at);

-- Monthly IQ scores for badge/deltas
CREATE TABLE IF NOT EXISTS iq_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    score NUMERIC NOT NULL,
    period_month TEXT NOT NULL,
    computed_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    delta_vs_prev NUMERIC
);
CREATE UNIQUE INDEX IF NOT EXISTS uq_iq_scores_user_month ON iq_scores(user_id, period_month);

-- Enable RLS and basic policies
ALTER TABLE tokens ENABLE ROW LEVEL SECURITY;
ALTER TABLE sessions ENABLE ROW LEVEL SECURITY;
ALTER TABLE test_runs ENABLE ROW LEVEL SECURITY;
ALTER TABLE iq_scores ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users view own tokens" ON tokens
    FOR SELECT USING (user_id = auth.uid());
CREATE POLICY "Users insert own tokens" ON tokens
    FOR INSERT WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users view own sessions" ON sessions
    FOR SELECT USING (user_id = auth.uid());
CREATE POLICY "Users insert own sessions" ON sessions
    FOR INSERT WITH CHECK (user_id = auth.uid());
CREATE POLICY "Users update own sessions" ON sessions
    FOR UPDATE USING (user_id = auth.uid());

CREATE POLICY "Users view own test runs" ON test_runs
    FOR SELECT USING (user_id = auth.uid());
CREATE POLICY "Users insert own test runs" ON test_runs
    FOR INSERT WITH CHECK (user_id = auth.uid());
CREATE POLICY "Users update own test runs" ON test_runs
    FOR UPDATE USING (user_id = auth.uid());

CREATE POLICY "Users view own iq scores" ON iq_scores
    FOR SELECT USING (user_id = auth.uid());
CREATE POLICY "Users insert own iq scores" ON iq_scores
    FOR INSERT WITH CHECK (user_id = auth.uid());
