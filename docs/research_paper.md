### Title
Farmer's Market: A Digital Platform for Direct Farmer–Merchant Trade

### Authors and Affiliation
Tanvi G. Dongare; Suhani P. Dube; Varsha T. Gandole; Geeta B. Ghegade; Prof. Dr. M. A. Wakchaure  
B.E. Students and Assistant Professor, Amrutvahini College of Engineering, Pune

### Abstract
This paper presents the design and implementation of a lightweight web platform that directly connects farmers and merchants through a transparent, time-bound bidding mechanism. The system reduces reliance on intermediaries, improves price discovery, and shortens time-to-sale. Key capabilities include secure authentication and role-based access, product listing with harvest metadata and grading, searchable catalogs, a bid workflow with full history and audit logs, and an order handoff after bid acceptance. The architecture uses a Python Flask backend, a responsive HTML/CSS/Bootstrap frontend, and SQLite for storage. We discuss requirements, architecture, implementation details, and how the platform advances beyond existing official systems such as e‑NAM and AGMARKNET.

### Keywords
Agricultural marketplace; bidding; price discovery; transparency; Flask; SQLite; farmer; merchant

---

### 1. Introduction
India’s agricultural marketing involves multiple intermediaries that widen the price spread between farm‑gate and retail. Information asymmetry and limited market access especially affect smallholders. This work proposes a direct farmer–merchant platform where farmers publish lot‑level listings and receive competitive bids from verified merchants. Our objectives are to: (1) enable transparent price discovery; (2) provide secure, auditable transactions; and (3) keep the system lightweight enough for low‑resource deployments while remaining extensible to production databases and logistics.

Background and motivation:  
Small and marginal farmers typically sell through local traders or mandis, often without timely knowledge of demand and prevailing prices in nearby urban markets. Official initiatives such as e‑NAM facilitate e‑trading in the APMC ecosystem and AGMARKNET publishes official market prices; however, these systems either operate within market yards or provide information without a direct transaction channel between individual farmers and merchants. As a result, farmers face longer time‑to‑sale, volatile realized prices, and limited negotiation power. Merchants, on the other hand, lack verified, lot‑level information such as harvest date, grade, and available quantity at the moment of procurement.

Quantitative context (motivation for design targets):  
- Price spreads between farm‑gate and retail often include multiple commissions and logistics charges; even single‑digit percentage improvements meaningfully lift farmer margins.  
- Decision latency is high when discovery is manual; reducing listing‑to‑acceptance time by 30–50% can increase freshness and reduce wastage for perishables.  
- Network reliability varies widely, so the platform must remain usable on modest connections and low‑end devices.

Problem definition:  
We target a simple but high‑impact gap—enabling direct, auditable negotiation for individual produce lots outside mandis. The platform must support: (a) farmer‑controlled listings enriched with quality and harvest metadata; (b) a transparent bidding workflow where every offer and decision is recorded; and (c) a clean handoff to order creation immediately after acceptance.

Research questions:  
- RQ1: Can transparent, competitive bidding at the lot level reduce effective price spreads for farmers without adding operational burden?  
- RQ2: Does visibility into bid history and produce metadata (grade, harvest date) improve match quality and time‑to‑sale?  
- RQ3: Can a lightweight stack (Flask + SQLite) deliver acceptable performance and reliability for pilot‑scale deployments, with a clear migration path to production components?

Design goals:  
- Transparency: Every bid has a visible state and timestamp, with a full per‑product history.  
- Fairness: Reserve‑price enforcement and quantity validation prevent predatory or infeasible bids.  
- Trust and security: Role‑based access control, secure sessions, and ownership checks for all sensitive actions.  
- Usability: Mobile‑first, low‑bandwidth pages with clear forms and minimal steps for core tasks.  
- Deployability: A lightweight stack (Flask + SQLite) that runs on modest infrastructure and can later migrate to PostgreSQL and cloud storage.

Novelty and positioning:  
Compared to mandi‑centric e‑trading (e‑NAM), our system is farmer‑owned and lot‑centric, making it suitable for small and ad‑hoc quantities. Compared to information portals (AGMARKNET), it converts market intelligence into live transactions with auditability. Relative to generic e‑commerce, it encodes produce‑specific metadata and a bid lifecycle, balancing transparency with simplicity for field use.

Expected outcomes:  
- Reduced listing‑to‑acceptance time via real‑time, competitive bidding and clear tie‑break rules.  
- Improved realized prices for sellers by surfacing multiple competing offers transparently.  
- Better match quality for buyers through searchable harvest/grade metadata and bid history.  
- Operational traceability thanks to immutable audit logs of offers and decisions.

Scope and contributions:  
The system provides farmer and merchant portals for listing, discovery, bidding, and order handoff. Unlike information‑only portals, it operationalizes price discovery by letting demand compete in real time. Unlike mandi‑centric e‑trading systems, it is farmer‑owned at the lot level and usable for ad‑hoc quantities. We contribute: (i) a practical schema and API that encode produce metadata, bid lifecycle, and auditability; (ii) role‑aware guards that gate every state transition; and (iii) an implementation that can be piloted by FPOs or local communities and later integrated with payment gateways, logistics, and interoperability networks.

Paper organization:  
Section 2 reviews authoritative systems and clarifies how our platform differs. Section 3 states functional and non‑functional requirements derived from field constraints. Section 4 details the architecture, data model, and bidding workflow. Section 5 discusses use cases, benefits, and challenges. Section 6 outlines the stack. Section 7 concludes with future extensions.

---

### 2. Literature Survey (Authoritative sources only)
The following official systems and organizations inform our design. For each, we summarize scope, identify gaps relative to our goals, and state our platform’s added value.

2.1 National Agriculture Market (e‑NAM) — Ministry of Agriculture & Farmers Welfare (GoI)
- Scope: Mandi‑centric electronic trading within the APMC ecosystem; supports assaying, payments, and inter‑mandi trade workflows.  
- Gap: Oriented to market yards and large lots; not a lightweight, farmer‑owned listing app for direct farmer→merchant trades with per‑lot bid history and reserve control.  
- Our addition: Lot‑level listings outside mandis, transparent per‑product bid logs, accept/reject with audit trail, and instant order creation.

2.2 AGMARKNET — Directorate of Marketing & Inspection (GoI)
- Scope: Official daily arrivals and prices from agricultural markets; historical time series.  
- Gap: Information service only; no transaction, authentication, or role‑aware workflows.  
- Our addition: Converts price intelligence into action via searchable listings and real‑time competitive bidding, tied to harvest/grade metadata.

2.3 NABARD — FPO and Digital Marketing Guidance
- Scope: Policy/program guidance on farmer collectives and digital enablement.  
- Gap: Aggregator‑focused; no concrete, open, per‑lot bidding workflow for individual farmers with tamper‑evident logs.  
- Our addition: Lightweight, deployable marketplace at village/FPO level supporting individual or pooled lots with full bid lifecycle.

2.4 FAO — Digital Agriculture and Market Development Guidance
- Scope: Best practices for inclusive digital marketplaces, price transparency, and traceability.  
- Gap: Frameworks, not an implementable role‑aware system with offline‑friendly, low‑bandwidth UI.  
- Our addition: Operationalizes principles with Flask/SQLite, RBAC, and explicit state transitions for bids (pending/accepted/rejected/expired/withdrawn).

2.5 World Bank & NITI Aayog — Market Efficiency and Reform Notes
- Scope: Analyses/policy on reducing spreads and enabling competition through digital tools.  
- Gap: Macro guidance rather than a ready transaction platform that tracks bid history and automates order handoff.  
- Our addition: A concrete application that directly targets spread reduction via competitive bidding and measurable time‑to‑sale improvements.

2.6 ICAR — Grading and Post‑Harvest Practices
- Scope: Produce grading standards and post‑harvest guidance.  
- Gap: Standards are not embedded into listing, search, and bidding flows.  
- Our addition: Encodes grade and harvest metadata in the `products` schema and exposes them as filters and decision signals in bidding.

2.7 ONDC — Agri Domain Specifications
- Scope: Interoperability protocols and early agri pilots.  
- Gap: Network protocol without an out‑of‑the‑box bidding app with history and reserve rules.  
- Our addition: A practical app that can later map to ONDC schemas; currently delivers local, auditable listing→bidding→order flows.

---

### 3. Requirements
3.1 Functional Requirements
- User Management: Registration, secure login, role‑based access (farmer, merchant, admin), profile management.
- Product Management: Create/edit listings with category, grade, unit, quantity, harvest date, minimum acceptable price; upload images.  
- Search & Filtering: Category, grade, min/max price, harvest window, and keyword search.  
- Bidding System: Place bids (price, quantity, message), view per‑product bid history, accept/reject/withdraw, auto‑expiry and notifications.  
- Order Handoff: Create order upon acceptance with totals/fees and payment status placeholder.  
- Auditing & Security: Ownership checks, state validations, and append‑only audit logs.

3.2 Non‑Functional Requirements
- Performance: P95 API < 300 ms; search < 600 ms; P95 page load < 2 s.  
- Scalability: Stateless API; background workers for bid expiry and notifications.  
- Security: Argon2/bcrypt hashing, CSRF, RBAC, rate limiting, encrypted PII.  
- Usability: Responsive UI (Bootstrap), accessible patterns (WAI‑ARIA), mobile‑first forms.  
- Reliability: Idempotent endpoints, retries, structured logging, and monitoring.

---

### 4. Method
4.1 System Architecture
- Client: Responsive web app (HTML/CSS/JS with Bootstrap).  
- Server: Python Flask with blueprints: `auth`, `products`, `bids`, `orders`, `admin`.  
- Database: SQLite in development; migration‑ready for PostgreSQL in production.  
- Authentication: Flask‑Login sessions; CSRF‑protected forms; RBAC middleware.  
- Background Jobs: Bid expiry sweeps, email/SMS notifications, analytics aggregation.  
- Caching/Storage: Optional Redis for sessions and hot queries; object storage for images.  
- Observability: Structured JSON logs, error tracking, request metrics.

4.2 Development Methodology
- Agile iterations with short sprints, early user feedback, and regular reliability checks.  
- CI for testing and database migrations; code reviews for security and access control paths.

4.3 Implementation Details
- Database Design (core tables):  
  `users(id, name, email, phone, password_hash, role, kyc_status, created_at)`  
  `products(id, farmer_id, category, title, description, grade, unit, quantity_available, harvest_date, min_price, status, created_at)`  
  `bids(id, product_id, merchant_id, price, quantity, message, status[pending|accepted|rejected|expired|withdrawn], created_at, expires_at)`  
  `orders(id, product_id, buyer_id, seller_id, agreed_price, quantity, total, payment_status, fulfillment_status, created_at)`  
  `audit_logs(id, actor_id, action, entity_type, entity_id, metadata, created_at)`  
  Indexes: `bids(product_id, price DESC, created_at)`, `products(category, status, harvest_date)`

- API Endpoints (examples):  
  Auth: `POST /auth/register`, `POST /auth/login`, `POST /auth/logout`, `GET /me`  
  Products: `GET /products`, `POST /products`, `GET /products/:id`, `PATCH /products/:id`  
  Bids: `POST /products/:id/bids`, `GET /products/:id/bids`, `POST /bids/:id/accept`, `POST /bids/:id/reject`, `POST /bids/:id/withdraw`  
  Orders: `GET /orders/:id`, `POST /orders/:id/pay` (future payment integration)

- Bidding Logic:  
  Validation: `bid.price ≥ product.min_price`, `bid.quantity ≤ product.quantity_available`.  
  Lifecycle: pending → accepted/rejected/expired/withdrawn; auto‑expiry after configured window.  
  Tie‑breakers: higher price, then earlier timestamp; optional auto‑accept threshold.

- User Interface:  
  Responsive pages, keyboard‑navigable forms, filters and facets, dynamic bid tables, confirmation dialogs, and toasts for status changes.

---

### 5. Discussion
5.1 Use Case Overview (Textual)  
Farmer: create listings → receive/view bids → accept/reject → order created.  
Merchant: search/browse → place bids → track bid status → pay on acceptance (future).  
System: authenticate users, enforce RBAC, validate state transitions, expire stale bids, and log audits.

5.2 Key Features and Benefits  
- Direct interaction without mandatory intermediaries.  
- Transparent, auditable bidding and price discovery.  
- Secure sessions and role‑based access with clear state transitions.  
- Mobile‑friendly UX tuned for low bandwidth and simple forms.

5.3 Challenges Addressed  
- Market access for remote farmers.  
- Price transparency via competitive bids.  
- Supply chain efficiency through digital negotiation and rapid order creation.

---

### 6. Technical Stack
- Frontend: HTML, CSS, JavaScript, Bootstrap.  
- Backend: Python Flask.  
- Database: SQLite (dev), PostgreSQL (prod suggested).  
- Authentication: Flask‑Login, CSRF, bcrypt/Argon2.  
- Deployment: Docker and Nginx (future), HTTPS with Let’s Encrypt (future).

---

### 7. Conclusion and Future Scope
Conclusion: The presented platform operationalizes authoritative guidance while filling gaps left by existing official systems. It enables farmer‑controlled, lot‑level transparent bidding and faster transactions with verifiable histories.  
Future Scope: Native mobile apps; payment gateway/escrow; logistics quotes and tracking; ratings and dispute workflows; ONDC schema mapping; ingestion of AGMARKNET price feeds for decision support.

---

### References (Authorized sources only)
[1] Ministry of Agriculture & Farmers Welfare, Government of India — National Agriculture Market (e‑NAM) — https://www.enam.gov.in  
[2] Directorate of Marketing & Inspection, Government of India — AGMARKNET — https://agmarknet.gov.in  
[3] National Bank for Agriculture and Rural Development (NABARD) — Official publications — https://www.nabard.org  
[4] Food and Agriculture Organization of the United Nations (FAO) — Digital agriculture resources — https://www.fao.org  
[5] World Bank — Agriculture and markets reports — https://www.worldbank.org  
[6] NITI Aayog — Agriculture and market reforms — https://www.niti.gov.in  
[7] Indian Council of Agricultural Research (ICAR) — Post‑harvest and grading — https://icar.org.in  
[8] Open Network for Digital Commerce (ONDC) — Agri domain — https://www.ondc.org  
[9] Ministry of Electronics and Information Technology, Government of India — Digital India initiatives — https://www.meity.gov.in  
[10] Reserve Bank of India — Financial inclusion and digital payments — https://www.rbi.org.in  
[11] Department of Agriculture, Cooperation & Farmers Welfare — Agricultural marketing policies — https://agricoop.nic.in  
[12] Small Farmers' Agribusiness Consortium (SFAC) — Farmer Producer Organizations — https://www.sfacindia.com  
[13] Agricultural and Processed Food Products Export Development Authority (APEDA) — Quality standards — https://www.apeda.gov.in  
[14] National Institute of Agricultural Marketing (NIAM) — Market research and training — https://www.niam.res.in  
[15] International Food Policy Research Institute (IFPRI) — Agricultural market development — https://www.ifpri.org  
[16] United Nations Conference on Trade and Development (UNCTAD) — Digital economy reports — https://unctad.org  
[17] International Telecommunication Union (ITU) — Digital agriculture guidelines — https://www.itu.int  
[18] Asian Development Bank (ADB) — Agricultural technology and markets — https://www.adb.org  
[19] International Fund for Agricultural Development (IFAD) — Rural development and markets — https://www.ifad.org  
[20] World Trade Organization (WTO) — Agricultural trade and digitalization — https://www.wto.org  
[21] United Nations Industrial Development Organization (UNIDO) — Agribusiness development — https://www.unido.org  
[22] International Labour Organization (ILO) — Rural employment and digital platforms — https://www.ilo.org  
[23] World Economic Forum — Digital agriculture transformation — https://www.weforum.org  
[24] McKinsey Global Institute — Digital India and agricultural productivity — https://www.mckinsey.com  
[25] PwC India — Digital agriculture and market access — https://www.pwc.in
