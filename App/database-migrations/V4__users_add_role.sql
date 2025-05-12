ALTER TABLE users
ADD COLUMN role VARCHAR(10) NOT NULL DEFAULT 'user';

ALTER TABLE users
ADD CONSTRAINT role_check CHECK (role IN ('user', 'admin'));

-- Update existing users to have the default role if not already set
UPDATE users
SET role = 'user'
WHERE role IS NULL;

-- Insert a default admin user if it doesn't already exist
INSERT INTO users (email, password_hash, role)
VALUES ('test@test.com', '$2b$12$eh8m1dy3N2e/P5OvSuzHeeBwoaS9RbZPMThDhGoD0EuHrKbBq9JIW', 'admin')
ON CONFLICT ((lower(email))) DO NOTHING;