CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(64) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    is_active_account BOOLEAN DEFAULT 1
);

CREATE TABLE IF NOT EXISTS signs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    word VARCHAR(100) NOT NULL,
    language VARCHAR(100) DEFAULT 'ASL (American Sign Language)',
    category VARCHAR(50),
    description TEXT,
    media_url VARCHAR(255),
    landmarks_json TEXT,
    uploaded_by VARCHAR(64) DEFAULT 'Admin'
);

CREATE TABLE IF NOT EXISTS lessons (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(150) NOT NULL,
    language VARCHAR(100) DEFAULT 'ASL (American Sign Language)',
    level VARCHAR(50),
    content TEXT,
    order_index INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS announcements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(150) NOT NULL,
    message TEXT NOT NULL,
    is_active BOOLEAN DEFAULT 1
);

CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    site_name VARCHAR(100) DEFAULT 'SignBridge',
    hero_title VARCHAR(255) DEFAULT 'Bridge the Communication Gap Across All Sign Languages',
    hero_subtitle TEXT DEFAULT 'Real-time sign language translation, multi-language sign library, and interactive learning tools.',
    allow_registration BOOLEAN DEFAULT 1,
    maintenance_mode BOOLEAN DEFAULT 0
);
