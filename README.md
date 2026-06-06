# Bazov

> **Bazov** - Relationship Intelligence Platform
> 
> Crawl, analyze, and map professional relationships with AI-powered insights.

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for local frontend dev)
- Python 3.11+ (for local backend dev)
- Git

### 1. Clone & Setup
```bash
git clone https://github.com/yojedesign/Bazov.git
cd Bazov
```

### 2. Configure Environment
Copy and update environment files:
```bash
# Frontend
cp frontend/.env.example frontend/.env.local

# Backend
cp backend/.env.example backend/.env

# Crawlers
cp crawlers/.env.example crawlers/.env
```

### 3. Start with Docker (Recommended)
```bash
# Build and start all services
docker-compose -f docker/docker-compose.yml up -d --build

# View logs
docker-compose -f docker/docker-compose.yml logs -f

# Stop services
docker-compose -f docker/docker-compose.yml down
```

### 4. Local Development (Optional)

#### Frontend
```bash
cd frontend
npm install
npm run dev
# Open http://localhost:3000
```

#### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
# Open http://localhost:8000/docs
```

#### Crawlers
```bash
cd crawlers
pip install -r requirements.txt
# Run LinkedIn scraper
cd linkedin
scrapy crawl linkedin_profiles
```

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        Bazov Platform                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────┐  │
│  │  Frontend   │───▶│   Backend   │───▶│     Supabase        │  │
│  │  (Next.js)  │    │  (FastAPI)  │    │   (PostgreSQL)      │  │
│  └─────────────┘    └─────────────┘    └─────────────────────┘  │
│           ▲                  ▲  ▲  ▲                              │
│           │                  │  │  └──────────────────────────────┘
│           │                  │  │
│  ┌─────────────┐            │  └─────────────┐                    │
│  │   Clerk     │            │   ┌─────────────┐                    │
│  │  (Auth)     │            │   │  Crawlers   │                    │
│  └─────────────┘            │   │ (Scrapy)    │                    │
│                          │   └─────────────┘                    │
│                          │         ▲                              │
│                          │         │                              │
│                          │   ┌─────────────┐                    │
│                          │   │    MCPs     │                    │
│                          │   │ (Microsvc)  │                    │
│                          │   └─────────────┘                    │
│                          └──────────────────────────────────────┘
│
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
Bazov/
├── frontend/               # Next.js (TypeScript, TailwindCSS, Clerk)
│   ├── app/
│   │   ├── (auth)/         # Auth pages (sign-in, sign-up, callback)
│   │   ├── dashboard/      # Main dashboard
│   │   ├── layout.tsx      # Root layout
│   │   └── page.tsx        # Landing page
│   ├── components/
│   │   ├── ui/             # ShadCN components
│   │   ├── auth/           # Auth components
│   │   └── dashboard/      # Dashboard components
│   ├── lib/
│   │   ├── api/            # API clients
│   │   ├── hooks/          # React hooks
│   │   └── utils/          # Utilities
│   ├── public/             # Static assets
│   ├── .env.example
│   ├── next.config.js
│   ├── package.json
│   └── tsconfig.json
│
├── backend/                # FastAPI (Python, SQLAlchemy, Supabase)
│   ├── app/
│   │   ├── api/
│   │   │   ├── v1/         # API versioning
│   │   │   │   ├── auth.py # Auth endpoints
│   │   │   │   ├── users.py
│   │   │   │   ├── signals.py
│   │   │   │   └── relationships.py
│   │   │   └── __init__.py
│   │   ├── core/
│   │   │   ├── config.py   # Settings
│   │   │   ├── dependencies.py
│   │   │   └── security.py
│   │   ├── db/
│   │   │   ├── base.py      # Base models
│   │   │   ├── session.py   # DB session
│   │   │   └── models/      # SQLAlchemy models
│   │   ├── models/         # Pydantic schemas
│   │   ├── services/       # Business logic
│   │   │   ├── signal_service.py
│   │   │   └── relationship_service.py
│   │   └── main.py
│   ├── tests/
│   │   ├── conftest.py
│   │   └── test_*.py
│   ├── requirements.txt
│   └── .env.example
│
├── crawlers/               # Scrapy + Playwright
│   ├── linkedin/
│   │   ├── spiders/
│   │   │   ├── profiles.py
│   │   │   └── connections.py
│   │   ├── items.py
│   │   ├── middlewares.py
│   │   └── settings.py
│   ├── news/
│   │   ├── spiders/
│   │   │   └── tech_news.py
│   │   └── items.py
│   └── requirements.txt
│
├── mcps/                   # Microservices (Python)
│   ├── signal_processor/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── models.py
│   │   │   └── nlp/
│   │   │       ├── extractor.py
│   │   │       └── classifiers.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── relationship_mapper/
│       ├── app/
│       │   ├── main.py
│       │   └── graph/
│       │       ├── algorithms.py
│       │       └── models.py
│       ├── Dockerfile
│       └── requirements.txt
│
├── docker/
│   ├── Dockerfile.frontend
│   ├── Dockerfile.backend
│   ├── Dockerfile.crawlers
│   ├── docker-compose.yml
│   └── docker-compose.override.yml
│
├── docs/
│   ├── architecture.md
│   ├── api/
│   │   └── v1/
│   │       ├── auth.md
│   │       ├── signals.md
│   │       └── relationships.md
│   └── deployment.md
│
├── .github/
│   └── workflows/
│       ├── ci.yml
│       ├── cd.yml
│       └── test.yml
│
├── .gitignore
├── .env.example
└── README.md
```

---

## 🔧 Configuration

### Environment Variables

#### Frontend (`frontend/.env.local`)
```bash
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=your_clerk_publishable_key
CLERK_SECRET_KEY=your_clerk_secret_key
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### Backend (`backend/.env`)
```bash
# Database
DATABASE_URL=postgresql://postgres:postgres@db:5432/bazov
SUPABASE_URL=https://your-project-ref.supabase.co
SUPABASE_KEY=your-supabase-anon-key

# Auth
CLERK_SECRET_KEY=your_clerk_secret_key
CLERK_WEBHOOK_SECRET=your_clerk_webhook_secret

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# Settings
DEBUG=true
SECRET_KEY=your-secret-key
```

#### Crawlers (`crawlers/.env`)
```bash
# LinkedIn
LINKEDIN_USERNAME=your_linkedin_email
LINKEDIN_PASSWORD=your_linkedin_password

# Proxy (optional)
PROXY_URL=http://your-proxy:port
```

---

## 🔌 API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/v1/auth/webhook` | Clerk webhook handler |
| GET | `/api/v1/auth/me` | Get current user |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/users` | List users |
| GET | `/api/v1/users/{id}` | Get user by ID |
| POST | `/api/v1/users` | Create user |
| PUT | `/api/v1/users/{id}` | Update user |
| DELETE | `/api/v1/users/{id}` | Delete user |

### Signals
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/signals` | List signals |
| POST | `/api/v1/signals` | Create signal |
| GET | `/api/v1/signals/types` | Get signal types |

### Relationships
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/relationships` | List relationships |
| POST | `/api/v1/relationships` | Create relationship |
| GET | `/api/v1/relationships/graph` | Get relationship graph |
| POST | `/api/v1/relationships/path` | Find shortest path |

---

## 🤖 Crawlers

### LinkedIn Scraper
- **Purpose**: Extract profile data, connections, and work history
- **Tech**: Playwright (for dynamic content) + Scrapy
- **Output**: Structured JSON to backend API

### News Scraper
- **Purpose**: Extract hiring, funding, and partnership signals
- **Sources**: TechCrunch, Hacker News, company blogs
- **Tech**: Scrapy + BeautifulSoup
- **Output**: Signals to backend API

---

## 🧠 MCPs (Microservices)

### Signal Processor
- **Purpose**: NLP-based extraction of business signals
- **Features**:
  - Entity recognition (companies, people)
  - Signal classification (hiring, funding, partnership)
  - Sentiment analysis
- **Tech**: spaCy, Transformers

### Relationship Mapper
- **Purpose**: Graph-based relationship analysis
- **Features**:
  - Shortest path between entities
  - Community detection
  - Centrality metrics
- **Tech**: NetworkX, igraph

---

## 🐳 Docker

### Build & Run
```bash
# Build all images
docker-compose -f docker/docker-compose.yml build

# Start services
docker-compose -f docker/docker-compose.yml up -d

# Stop services
docker-compose -f docker/docker-compose.yml down

# View logs
docker-compose -f docker/docker-compose.yml logs -f
```

### Individual Services
```bash
# Frontend only
docker-compose -f docker/docker-compose.yml up frontend

# Backend only
docker-compose -f docker/docker-compose.yml up backend

# Database only
docker-compose -f docker/docker-compose.yml up db
```

---

## 🚀 Deployment

### Local Development
1. Start Docker services
2. Frontend: http://localhost:3000
3. Backend API: http://localhost:8000/docs
4. Supabase Studio: http://localhost:3001

### Production (Future)
- **Frontend**: Vercel / Netlify
- **Backend**: Fly.io / Railway
- **Database**: Supabase Cloud
- **Crawlers**: AWS Lambda / Google Cloud Functions
- **MCPs**: Kubernetes / Docker Swarm

---

## 📊 Database Schema

### Core Tables

#### Users
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    clerk_id VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Companies
```sql
CREATE TABLE companies (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255),
    industry VARCHAR(255),
    size VARCHAR(50),
    founded_year INTEGER,
    description TEXT,
    logo_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### People
```sql
CREATE TABLE people (
    id UUID PRIMARY KEY,
    linkedin_id VARCHAR(255) UNIQUE,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    current_title VARCHAR(255),
    current_company_id UUID REFERENCES companies(id),
    bio TEXT,
    profile_url TEXT,
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Relationships
```sql
CREATE TABLE relationships (
    id UUID PRIMARY KEY,
    from_person_id UUID REFERENCES people(id) NOT NULL,
    to_person_id UUID REFERENCES people(id) NOT NULL,
    relationship_type VARCHAR(50) NOT NULL, -- colleague, classmate, etc.
    from_date DATE,
    to_date DATE,
    current BOOLEAN DEFAULT TRUE,
    source VARCHAR(50), -- linkedin, manual, etc.
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(from_person_id, to_person_id, relationship_type)
);
```

#### Signals
```sql
CREATE TABLE signals (
    id UUID PRIMARY KEY,
    signal_type VARCHAR(50) NOT NULL, -- hiring, funding, partnership, etc.
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    source_url TEXT,
    source_type VARCHAR(50), -- news, linkedin, manual
    company_id UUID REFERENCES companies(id),
    person_id UUID REFERENCES people(id),
    confidence FLOAT DEFAULT 0.8,
    sentiment VARCHAR(20), -- positive, negative, neutral
    published_at TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

#### Company People (Many-to-Many)
```sql
CREATE TABLE company_people (
    id UUID PRIMARY KEY,
    company_id UUID REFERENCES companies(id) NOT NULL,
    person_id UUID REFERENCES people(id) NOT NULL,
    role VARCHAR(255) NOT NULL,
    is_current BOOLEAN DEFAULT TRUE,
    started_at DATE,
    ended_at DATE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    UNIQUE(company_id, person_id, role, started_at)
);
```

---

## 🛠️ Development

### Code Style
- **Frontend**: Prettier + ESLint
- **Backend**: Black + isort + flake8
- **Python**: PEP 8 compliant

### Testing
```bash
# Frontend tests
cd frontend
npm test

# Backend tests
cd backend
pytest tests/

# All tests
cd /workspace/yojedesign__Bazov
docker-compose -f docker/docker-compose.yml run backend pytest tests/
```

### Linting
```bash
# Frontend
cd frontend
npm run lint

# Backend
cd backend
black .
isort .
flake8 .
```

---

## 📜 License

MIT License - See [LICENSE](LICENSE) for details.

---

## 🙏 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📞 Contact

- **GitHub**: [yojedesign](https://github.com/yojedesign)
- **Project**: [Bazov](https://github.com/yojedesign/Bazov)
