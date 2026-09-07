# Smart Civic Grievance Platform — Security Architecture & Practices

> **Document Status:** Active Reference  
> **Extracted from:** [implementation_plan.md](file:///d:/Sem-3_Project/implementation_plan.md)  
> **Design Philosophy:** **Practical, risk-based security.**  
> Implement the controls necessary to safeguard the platform, citizen data, complaint integrity, and administrative functions without unnecessary complexity. Every measure directly mitigates a real, identifiable threat.

---

## Table of Contents

1. [Security Core Philosophy](#1-security-core-philosophy)
2. [Authentication Strategy](#2-authentication-strategy)
3. [JWT Architecture & Lifecycle](#3-jwt-architecture--lifecycle)
4. [Role-Based Access Control (RBAC) — Tiered Security](#4-role-based-access-control-rbac--tiered-security)
5. [Credential Security (Password & PIN)](#5-credential-security)
6. [Domain-Specific Security — Protecting Complaint Integrity](#6-domain-specific-security--protecting-complaint-integrity)
   - [6.1 AI-Generated & Malicious Image Detection (3-Gate Pipeline)](#61-ai-generated--malicious-image-detection-3-gate-pipeline)
   - [6.2 Fake Complaint Prevention Pipeline](#62-fake-complaint-prevention-pipeline)
   - [6.3 Citizen Image Protection (View-Only, Anti-Screenshot & No Download)](#63-citizen-image-protection-view-only-anti-screenshot--no-download)
   - [6.4 Telegram Session Continuity & State Security](#64-telegram-session-continuity--state-security)
   - [6.5 Telegram Bot Security](#65-telegram-bot-security)
7. [API Security — Baseline Protections](#7-api-security--baseline-protections)
8. [Infrastructure, DevOps & Network Security](#8-infrastructure-devops--network-security)
9. [Security Implementation Timeline](#9-security-implementation-timeline)

---

## 1. Security Core Philosophy

- **Built-in from Day 1:** Security is baked into the foundation (data models, middleware, auth layers), not retrofitted at deployment.
- **Risk-Appropriate & Proportional:** Field workers and citizens have frictionless interfaces; the admin panel features tight, strict access controls.
- **No Silent Drops:** Malicious or malformed inputs are either instantly rejected with clear, polite feedback to the citizen or routed to triage with transparency.

---

## 2. Authentication Strategy

The platform serves 3 distinct personas, each authenticated through mechanisms tailored to their trust boundary:

| User Type | Authentication Method | Mechanism & Security Rationale |
|-----------|----------------------|--------------------------------|
| **Citizen** | **Telegram Identity** (Zero login friction) | Telegram passes verified `chat_id` and `username` with every webhook message. The system maps identity on first contact. Citizens never enter credentials; Telegram provides the identity provider layer. |
| **Admin** | **JWT (JSON Web Token)** via Username + Password | Admin logs in via Web PWA with username and password. Password verified against `bcrypt` hash. Issues short-lived access JWT (15-min access, 24-hour refresh). **Stronger security** required because admins manage workers, configure zones, triage complaints, and view sensitive civic records. |
| **Worker** | **JWT (JSON Web Token)** via Phone + 4-digit PIN | Field worker logs in via Mobile PWA with registered phone number + 4-digit PIN. One login per day (issues 24-hour access JWT, no refresh token needed). Token is scoped with `role: worker` and `zone: <zone_id>`. Workers only see their assigned operational area. |

---

## 3. JWT Architecture & Lifecycle

### Authentication & Token Flow

```
  WORKER (Mobile PWA)                    ADMIN (Web PWA)
  ──────────────────                     ────────────────
  
  Phone: 9876543210                      Username: admin_raj
  PIN:   ● ● ● ●                        Password: ••••••••
         │                                      │
         ▼                                      ▼
  POST /auth/worker/login               POST /auth/admin/login
  {phone, pin}                           {username, password}
         │                                      │
         ▼                                      ▼
  Find worker by phone                   Find admin by username
  Verify PIN hash (bcrypt)               Verify password hash (bcrypt)
         │                                      │
         ▼                                      ▼
  JWT {role: worker,                     JWT {role: admin,
       zone: zone_id,                        exp: 15min}
       exp: 24h}                         + Refresh token (24h)
         │                                      │
         ▼                                      ▼
  Works all day ✅                        Re-auth every 15 min
  Logs in again tomorrow                 (auto via refresh token)
```

#### Admin Flow (Username + Password)

```
┌──────────┐         ┌──────────┐         ┌──────────┐
│  Browser │         │ FastAPI  │         │PostgreSQL│
│  (PWA)   │         │ Backend  │         │    DB    │
└────┬─────┘         └────┬─────┘         └────┬─────┘
     │                     │                     │
     │  POST /auth/admin   │                     │
     │  /login             │                     │
     │  {username,password}│                     │
     ├────────────────────►│                     │
     │                     │ Find admin by       │
     │                     │ username            │
     │                     ├────────────────────►│
     │                     │◄────────────────────┤
     │                     │                     │
     │                     │  Verify password    │
     │                     │  (bcrypt compare)   │
     │                     │                     │
     │  200 OK             │                     │
     │  {access_token,     │                     │
     │   refresh_token}    │                     │
     │◄────────────────────┤                     │
     │                     │                     │
     │  GET /api/v1/...    │                     │
     │  Authorization:     │                     │
     │  Bearer <token>     │                     │
     ├────────────────────►│                     │
     │                     │  Decode JWT,        │
     │                     │  check role,        │
     │                     │  check expiry       │
     │                     │                     │
     │  200 OK {data}      │                     │
     │◄────────────────────┤                     │
```

#### Worker Flow (Phone + 4-Digit PIN — Once-Per-Day Login)

```
┌──────────┐         ┌──────────┐         ┌──────────┐
│  Mobile  │         │ FastAPI  │         │PostgreSQL│
│  PWA     │         │ Backend  │         │    DB    │
└────┬─────┘         └────┬─────┘         └────┬─────┘
     │                     │                     │
     │  POST /auth/worker  │                     │
     │  /login             │                     │
     │  {phone, pin}       │                     │
     ├────────────────────►│                     │
     │                     │ Find worker by      │
     │                     │ phone number        │
     │                     ├────────────────────►│
     │                     │◄────────────────────┤
     │                     │                     │
     │                     │  Verify PIN hash    │
     │                     │  (bcrypt compare)   │
     │                     │                     │
     │  200 OK             │                     │
     │  {access_token}     │  ← No refresh token │
     │◄────────────────────┤    (24h is enough)  │
     │                     │                     │
     │  Works all day...   │                     │
     │  GET /api/v1/...    │                     │
     │  Authorization:     │                     │
     │  Bearer <token>     │                     │
     ├────────────────────►│                     │
     │                     │  Decode JWT,        │
     │                     │  check role + zone, │
     │                     │  check expiry       │
     │                     │                     │
     │  200 OK {data}      │                     │
     │◄────────────────────┤                     │
```

### Tiered Token Details

| Property | Admin | Worker | Security Rationale |
|----------|-------|--------|--------------------|
| **Algorithm** | `HS256` | `HS256` | Fast, reliable, suitable for single-server/monolith setup |
| **Login Credential** | **Username + Password** | **Phone + 4-digit PIN** | Workers need frictionless mobile login; admins need stronger credentials for elevated privileges. |
| **Access Token Expiry** | **15 minutes** | **24 hours** (one login per day) | Admin access has elevated privilege, demanding a tight exposure window. Workers log in once per shift; 24h token covers the entire workday. |
| **Refresh Token Expiry** | **24 hours** | **N/A — not needed** | Admins must re-authenticate daily (auto-renewed via refresh token). Field workers need no refresh token — 24h access token is sufficient. |
| **Token Payload** | `{sub: user_id, role: "admin", exp: ...}` | `{sub: user_id, role: "worker", zone: "zone_id", exp: ...}` | Worker JWT carries zone claim to enforce backend server-side authorization filters. |
| **Brute-Force Rate Limit** | **3 attempts/min per IP** | **5 attempts/hour per phone** | Strict per-IP rate limiting on admin login; aggressive per-phone rate limiting on worker PIN login to defeat brute-force of 4-digit PIN space. |
| **Signing Secret** | `JWT_SECRET` in `.env` (Dev) / AWS SSM (Prod) | Same | Never hardcoded in source control; injected at runtime. |

---

## 4. Role-Based Access Control (RBAC) — Tiered Security

The system enforces a tiered RBAC model where privileges correlate directly with administrative responsibility.

### 4.1 Admin-Specific Security (High Privilege)

- **Strict Session Lifetime:** 15-minute access token limit paired with 24-hour refresh token forces daily re-authentication.
- **Worker & Zone Governance:** Only admins have rights to create, assign, or deactivate field worker accounts, and distribute/reset worker 4-digit PINs.
- **Triage & Classification Override:** Only admins can manually review, approve, or alter AI classification predictions.
- **Cross-Zone Visibility:** Admins can view complaints across all zones, while still being constrained by image download restrictions.
- **Aggressive Brute-Force Rate Limiting:** Stricter rate limits on `/api/v1/auth/admin/login` (**3 attempts/min per IP**).

### 4.2 Worker Security (Operational & Zone-Scoped)

- **Server-Side Zone Scoping:** Workers are restricted to complaints in their assigned zone (`zone_id` validated from JWT payload).
- **Task-Only Access:** Restricted strictly to assigned tasks; cannot inspect global dashboards, triage queues, or other worker profiles.
- **Once-Per-Day Shift Lifetime:** 24-hour access token (no refresh token needed); worker logs in once at start of shift and works all day without re-authenticating.
- **Strict Brute-Force Rate Limiting:** Rate-limited on `/api/v1/auth/worker/login` to **5 attempts/hour per phone** (stricter than per-IP because 4-digit PINs have only 10,000 combinations; locks phone for 1 hour after 5 failures).

### 4.3 RBAC Permission Matrix

| Endpoint Group | Citizen (Telegram) | Worker | Admin |
|---------------|:------------------:|:------:|:-----:|
| `POST /complaints` (create complaint) | ✅ (via bot) | ❌ | ❌ |
| `GET /complaints/track/{code}` | ✅ (own complaint) | ✅ (assigned task) | ✅ (all) |
| `GET /workers/me/tasks` | ❌ | ✅ | ❌ |
| `PATCH /complaints/{id}/resolve` | ❌ | ✅ (own task) | ❌ |
| `GET /admin/dashboard/*` | ❌ | ❌ | ✅ |
| `GET /admin/triage` | ❌ | ❌ | ✅ |
| `PATCH /admin/triage/{id}` | ❌ | ❌ | ✅ |
| `POST /admin/workers` (create worker) | ❌ | ❌ | ✅ |
| `PATCH /admin/workers/{id}/zone` | ❌ | ❌ | ✅ |

### 4.4 RBAC Implementation (FastAPI Dependency Injection)

```python
# app/api/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from app.config import settings
from app.services.auth_service import get_user_by_id

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        user_id = payload.get("sub")
        role = payload.get("role")  # "admin" or "worker"
        if user_id is None or role is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired or invalid")
    
    user = await get_user_by_id(user_id, role)
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User inactive or not found")
    return user

def require_role(required_role: str):
    async def role_checker(user = Depends(get_current_user)):
        if user.role != required_role:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user
    return role_checker

# Login schemas
from pydantic import BaseModel, field_validator

class WorkerLoginRequest(BaseModel):
    phone: str       # e.g., "9876543210"
    pin: str         # 4-digit string, e.g., "1234"
    
    @field_validator("pin")
    def validate_pin(cls, v):
        if not v.isdigit() or len(v) != 4:
            raise ValueError("PIN must be exactly 4 digits")
        return v

class AdminLoginRequest(BaseModel):
    username: str
    password: str
```

---

## 5. Credential Security

| Control | Admin | Worker |
|---------|-------|--------|
| **Credential type** | Password (8+ characters) | 4-digit PIN |
| **Hashing** | `bcrypt` via `passlib` | `bcrypt` via `passlib` |
| **Salt** | Auto (built into bcrypt) | Auto (built into bcrypt) |
| **Credential assignment** | Set by admin during account creation | Auto-generated, given to admin to share |
| **Self-service reset** | N/A (single admin assumed) | No — admin resets on request |

### 5.1 Admin Password Security

| Control | Practice | Implementation |
|---------|----------|----------------|
| **Hashing Algorithm** | `bcrypt` via `passlib` | Industry standard, slow hashing function resistant to GPU cracking. Plaintext passwords are never persisted. |
| **Salt Generation** | Automatic per-password salt | Handled internally by `bcrypt` (12 rounds) to prevent rainbow-table attacks. |
| **Password Complexity** | Minimum 8 characters | Enforced at request boundary using Pydantic schema validation. |
| **Response Sanitization** | Omission from schemas | `password_hash` is explicitly excluded from all Pydantic response models. |

### 5.2 Worker PIN Security

> [!IMPORTANT]
> **4-digit PIN security trade-off:** A 4-digit PIN has only 10,000 possible combinations. This is acceptable here because:
> 1. Workers are low-privilege (zone-scoped, task-only access)
> 2. Aggressive rate limiting (5 attempts/hour) makes brute-force impractical
> 3. The phone number itself acts as a "username" — attacker needs both phone + PIN
> 4. Admin can deactivate any worker instantly if compromise is suspected
> 
> This would NOT be acceptable for admin accounts — hence admins keep full passwords.

| Control | Practice | Implementation |
|---------|----------|----------------|
| **Hashing Algorithm** | `bcrypt` via `passlib` | Same bcrypt hashing as admin passwords. Even a 4-digit PIN is never stored in plaintext. |
| **Salt Generation** | Automatic per-PIN salt | Handled internally by `bcrypt` (12 rounds). |
| **PIN Format** | Exactly 4 digits (0000–9999) | Enforced at request boundary using Pydantic `field_validator`. |
| **PIN Assignment** | Admin-generated | Admin creates worker account → system generates random 4-digit PIN → shown once to admin for distribution. Workers do not self-select PINs. |
| **PIN Reset** | Admin-initiated only | Worker requests PIN change via admin. Admin can reset and issue a new PIN at any time. |
| **Brute-Force Protection** | 5 attempts/hour per phone | A 4-digit PIN has only 10,000 possible combinations. After 5 failed attempts, the phone number is locked for 1 hour. This makes brute-force impractical (10,000 ÷ 5 per hour = 2,000 hours to exhaust). |
| **Response Sanitization** | Omission from schemas | `pin_hash` is explicitly excluded from all Pydantic response models. |

---

## 6. Domain-Specific Security — Protecting Complaint Integrity

### 6.1 AI-Generated & Malicious Image Detection (3-Gate Pipeline)

**Threat:** Bad actors submitting AI-generated synthetic imagery (e.g. fabricated potholes, fake waste piles) or uploading abusive/malicious images to exhaust municipal resources.

```
┌─────────────┐     ┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│  Image      │────►│  Gate 1:         │────►│  Gate 2:         │────►│  Gate 3:         │
│  Uploaded   │     │  Unsafe Content  │     │  AI-Generated    │     │  Classification  │
│             │     │  Screen          │     │  Detection       │     │  (MobileNetV2)   │
└─────────────┘     └────────┬─────────┘     └────────┬─────────┘     └────────┬─────────┘
                             │                        │                        │
                    ┌────────▼─────────┐     ┌────────▼─────────┐     ┌────────▼─────────┐
                    │ NSFW / malicious │     │  PASS → continue │     │ Confidence ≥ 50% │
                    │ content detected │     │  SUSPECT → tag   │     │  → Auto-classify │
                    │  → INSTANT       │     │    for triage    │     │ Confidence < 50% │
                    │    REJECT        │     └──────────────────┘     │  → Auto-reject,  │
                    │                  │                              │    ask for better │
                    └──────────────────┘                              │    image          │
                                                                      └──────────────────┘
```

#### Detection Techniques

| Gate & Technique | How It Works | Technology |
|-----------------|--------------|------------|
| **Gate 1: Unsafe content screen (NSFW)** | Screens for inappropriate or unethical images (explicit content, graphic violence). Triggers **instant rejection** — no triage queue pollution. | `opennsfw2` or lightweight CPU classifier |
| **Gate 1: Embedded links / QR codes** | Scans image for embedded QR codes or overlaid URL text to block phishing, malware distribution, or QR exploits. | `pyzbar` (QR decoder) + regex URL pattern check |
| **Gate 2: EXIF metadata analysis** | Genuine camera photos typically retain device metadata (camera model, timestamps, software version, GPS). Synthetic AI images lack standard camera tags or carry synthetic identifiers. | Python `Pillow` library |
| **Gate 2: Error Level Analysis (ELA)** | Resaves the image at a known quality level (e.g., 90%) and calculates pixel error differential. AI images and manipulated splices exhibit uniform or anomalous compression artifacts. | Python `Pillow` + image math |
| **Gate 2: Perceptual hash check** | Hashes image using perceptual difference hashing. Catches duplicates and prevents replay of stock photos. | `imagehash` library |
| **Gate 3: Confidence thresholding** | MobileNetV2 outputs prediction probability. Confidence `< 50%` means the image is unidentifiable, irrelevant, or blurry. | TensorFlow / PyTorch MobileNetV2 |

#### Automated Rejection Rules (Zero Admin Burden)

| Condition | System Action | Citizen Notification |
|-----------|---------------|----------------------|
| `unsafe_content: true` | **Instant Reject** | *"Your image was rejected because it contains inappropriate content. Please submit an appropriate image related to your complaint."* |
| `embedded_links: true` | **Instant Reject** | *"Your image was rejected because it contains embedded links or QR codes. Please submit a clean photo of the issue."* |
| `classification_confidence < 50%` | **Auto-Reject** | *"We couldn't identify the issue in your image (confidence too low). Please submit a clearer photo — make sure the problem (pothole, garbage, etc.) is clearly visible."* |

> [!NOTE]
> **Sub-50% confidence images bypass admin triage entirely.** If the model cannot identify an issue with at least 50% confidence, a human admin is equally likely to find it ambiguous. Automatically asking the citizen for a clearer photo preserves valuable administrator time.

#### Stored Fraud Flags Schema

```json
{
  "unsafe_content": false,
  "embedded_links": false,
  "missing_exif": true,
  "ela_suspicious": false,
  "duplicate_hash": false,
  "classification_confidence": 0.72,
  "fraud_risk": "medium"
}
```

---

### 6.2 Fake Complaint Prevention Pipeline

**Threat:** Automated spam bots, keyboard smashing, duplicate submissions, and misleading complaints draining field operations.

```
┌──────────────────── Complaint Submission Pipeline ────────────────────┐
│                                                                       │
│  Text Submitted          Image Submitted          Both Submitted      │
│       │                       │                       │               │
│       ▼                       ▼                       ▼               │
│  ┌─────────┐            ┌──────────┐           ┌──────────────┐      │
│  │ Text    │            │ Image    │           │ Cross-check  │      │
│  │ Checks  │            │ Checks   │           │ Text vs Image│      │
│  └────┬────┘            └────┬─────┘           └──────┬───────┘      │
│       │                      │                        │               │
│       └──────────┬───────────┘────────────────────────┘               │
│                  ▼                                                     │
│         ┌───────────────┐                                             │
│         │ Fraud Score   │──► Low risk → Auto-classify                 │
│         │ Aggregation   │──► Medium risk → Triage queue (admin)       │
│         │               │──► High risk → Auto-reject + notify citizen │
│         └───────────────┘                                             │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
```

| Check Type | Target Vulnerability | Enforcement Mechanism |
|------------|---------------------|-----------------------|
| **Minimum Text Length** | Prevents empty or meaningless submissions (e.g. "hi", "asdf") | Pydantic schema validation requires ≥ 20 characters in complaint description |
| **Gibberish Detection** | Random characters or automated keyboard smashing | `langdetect` library validates input conforms to recognizable natural language |
| **Duplicate Checking** | Repeated spamming of the same grievance | Cosine similarity check against citizen's submissions within the preceding 24 hours |
| **Rate Limiting** | Bot floods or automated abuse | Enforces max 5 complaints per 24 hours per Telegram `chat_id` |
| **Text-Image Cross Validation** | Intentional mismatch (e.g., text reports "water pipe burst" but image is a domestic pet) | Compares text classifier output against image classifier category; discrepancies flag high fraud risk |

---

### 6.3 Citizen Image Protection (View-Only, Anti-Screenshot & No Download)

**Threat:** Admins or field workers downloading, saving, or taking screenshots of citizen-uploaded images. These photos may capture sensitive personal details in the background (residential interiors, private property, family members, vehicle license plates).

```
┌────────────────────────────────────────────────────────┐
│        Multi-Layer Image & Screenshot Protection       │
├──────────────────────────┬─────────────────────────────┤
│ MinIO / S3 Private Bucket│ No public access permitted  │
│            │             │                             │
│            ▼             │                             │
│ FastAPI Backend          │ Generates 15-min signed URL │
│            │             │                             │
│            ▼             │                             │
│ Frontend Custom Viewer   │ • View-only Canvas (No <img>)│
│                          │ • No download button        │
│                          │ • Right-click & drag OFF    │
│                          │ • Anti-Screenshot Handlers  │
│                          │ • Focus-Loss Blanking       │
│                          │ • Dynamic Watermark Overlay │
│                          │ • Print Blocker (@media)    │
│            │             │                             │
│            ▼             │                             │
│ Mobile PWA (Worker App)  │ Android FLAG_SECURE (OS-ban)│
└──────────────────────────┴─────────────────────────────┘
```

#### Multi-Layer Anti-Download & Anti-Screenshot Controls

| Protection Layer | Mechanism | Implementation Details |
|------------------|-----------|------------------------|
| **1. Time-Limited Signed URLs** | Ephemeral Access | MinIO/S3 buckets are strictly private. Backend issues signed URLs expiring in **15 minutes**. URLs cannot be bookmarked, shared, or fetched after expiry. |
| **2. Canvas Rendering (No `<img>` Tag)** | DOM Protection | Images are rendered directly onto an HTML5 `<canvas>` rather than a standard `<img>` element. Prevents browser "Save Image As", drag-to-desktop, or inspect-element image extraction. |
| **3. Context & Selection Lockout** | Interaction Restrictions | `contextmenu` (right-click) disabled, `pointer-events` controlled, CSS `user-select: none`, and `-webkit-touch-callout: none` (prevents mobile long-press image saving). |
| **4. Anti-Screenshot Key Interception** | Active Key Blocking | JavaScript listens for `PrintScreen` (key code 44), `Meta+Shift+S` (Windows Snipping Tool), and `Ctrl+P`. When detected, the canvas instantly blanks or blurs, and clipboard is cleared to prevent capturing. |
| **5. Focus-Loss / Tab Switch Blanking** | Capture Tool Mitigation | Uses `window.onblur` and the `visibilitychange` API. If the user alt-tabs or activates a third-party screen-snipping tool, the viewer instantly conceals the image with a black security shield until user returns. |
| **6. Print / PDF Export Block** | Media Query Shield | CSS `@media print { .protected-canvas { display: none !important; } }` ensures browser "Print" or "Save as PDF" produces an empty box. |
| **7. Dynamic Forensic Watermarking** | Leaker Traceability & Deterrence | Renders a semi-transparent, diagonal watermark across the canvas displaying: `Admin: <Name> | ID: <ID> | <Client-IP> | <Timestamp>`. If any user captures the screen with an external camera, the image carries undeniable forensic proof of who leaked it. |
| **8. OS-Level Screenshot Block (Mobile PWA)** | Hardware / OS Enforcement | In the Android worker mobile wrapper (TWA / Capacitor), enable `WindowManager.LayoutParams.FLAG_SECURE`. Android OS blocks screenshots completely, rendering a black screen and displaying *"Can't take screenshot due to security policy."* |
| **9. No Images in Export Files** | Administrative Redaction | CSV / Excel export endpoints for complaints contain status, dates, and text notes only — image binaries and image URLs are strictly excluded. |

> [!IMPORTANT]
> **Defense-in-Depth for Screen Captures:** While pure web browsers running on desktop OS cannot physically prevent a user from pointing an external smartphone camera at their monitor, combining **Canvas rendering**, **Active keyboard interception**, **Focus-loss blanking**, and **Dynamic forensic watermarking** makes unauthorized capture technically difficult and forensically traceable.

---

### 6.4 Telegram Session Continuity & State Security

**Threat:** Citizens filing grievances get interrupted by phone calls or app-switching, resulting in lost complaint progress and repeated partial submissions.

```
Citizen starts complaint
        │
        ▼
┌─────────────────────────────────────────────────┐
│  Session stored in Redis                        │
│  Key: telegram:{chat_id}:session                │
│  Value: {step, data_so_far, last_active}        │
│  TTL: 30 minutes (configurable)                 │
└──────────────────────┬──────────────────────────┘
                       │
           ┌───────────┼───────────┐
           │           │           │
     User returns   15 min idle  30 min idle
     within 30 min  (no activity) (TTL expires)
           │           │           │
           ▼           ▼           ▼
     Resume from    Bot sends:   Session deleted.
     where they     "Do you want  Next message
     left off       to continue   starts fresh.
                    filing your
                    complaint?"
                        │
                   ┌────┴────┐
                   │         │
                  Yes       No / No response
                   │        within 15 min
                   │         │
                Resume    Delete session,
                          send "Your session
                          has ended. Start
                          a new complaint
                          anytime with /report"
```

- **Redis Session Storage:** State stored under `telegram:{chat_id}:session` with automatic 30-minute Time-To-Live (TTL).
- **Proactive Inactivity Prompt:** Sent after 15 minutes of idle state asking the citizen if they wish to resume.
- **Graceful Cleanup:** If 30-minute TTL expires, incomplete draft data is cleared from memory, preventing memory leaks and orphaned states.

---

### 6.5 Telegram Bot Security

| Measure | Purpose & Implementation |
|---------|--------------------------|
| **Webhook Secret Token** | Telegram passes a secret token in the `X-Telegram-Bot-Api-Secret-Token` header. The backend validates this token on every incoming request, preventing unauthorized webhook spoofing. |
| **Sender Validation** | Verifies `chat_id` integrity on every message. Unknown, unverified, or anomalous requests are rejected. |
| **PII & Data Anonymization** | Bot messages never expose personal phone numbers, full names, or sensitive worker details. Grievances are referenced solely by unique, anonymized tracking codes (e.g., `#BLR-8421`). |
| **Bot Rate Limiting** | Strict limit of 5 submitted complaints per citizen per 24 hours to eliminate bot-driven spam. |

---

## 7. API Security — Baseline Protections

These protections are enforced across all HTTP endpoints via FastAPI middleware and SQLAlchemy ORM:

| Threat Category | Defense Mechanism | Implementation Strategy |
|-----------------|-------------------|-------------------------|
| **Cross-Origin Attacks (CORS)** | Strict Domain Whitelist | `CORSMiddleware` configured with explicit frontend origins (e.g., `http://localhost:3000`, production domain). Wildcard `*` is prohibited. |
| **Brute-Force Credential Attacks** | Endpoint Rate Limiting | `slowapi` enforces limits: **3 requests/min per IP** for `/auth/admin/login` (username + password) and **5 requests/hour per phone number** for `/auth/worker/login` (phone + 4-digit PIN — stricter because PINs have only 10,000 combinations). |
| **SQL Injection** | Parameterized Queries | 100% database access routed through SQLAlchemy ORM; no raw concatenated SQL strings. |
| **Malformed / Poisoned Payloads** | Strict Input Schema Validation | Pydantic v2 schemas rigorously validate and type-check every incoming JSON payload before route handlers execute. |
| **Resource Exhaustion (Denial of Service)** | File Size Restrictions | Image uploads through `UploadFile` are capped at a **hard limit of 5MB**. |
| **Webhook Forgery** | Secret Header Validation | Compares incoming `X-Telegram-Bot-Api-Secret-Token` with backend environment configuration. |
| **Secrets Exposure** | Environment Variable Isolation | All secrets (`JWT_SECRET`, database passwords, Telegram bot tokens) are managed via `.env` in local development and **AWS Systems Manager (SSM) Parameter Store** in production. Zero secrets in Git. |
| **Man-in-the-Middle (MitM) Attacks** | Transport Layer Security (TLS/HTTPS) | Nginx reverse proxy enforces TLS/SSL via **Let's Encrypt certificates**. Telegram webhooks mandate HTTPS. |

---

## 8. Infrastructure, DevOps & Network Security

### 8.1 Network & Container Isolation

- **Docker Internal Network:** The backend, PostgreSQL database, and Redis cache communicate over an isolated internal Docker bridge network (`backend-network`).
- **Minimal Exposure:** Only Nginx exposes ports `80` and `443` to the host/internet. PostgreSQL (`5432`) and Redis (`6379`) are strictly unreachable from the public internet.
- **Storage Isolation:** MinIO / AWS S3 buckets are configured as private without public read ACLs. All asset access requires backend signed URLs.

### 8.2 Git & CI/CD Security Policies

- **Protected Main Branch:** Direct pushes to `main` and `develop` are disallowed via GitHub branch protection rules.
- **Mandatory Peer Reviews:** Every feature or fix branch requires at least one approving pull request review before merging.
- **CI Security Checks:** Automated linting, test suites, and schema validations run on every pull request before merge eligibility.
- **Credential Hygiene:** `.gitignore` actively blocks `.env`, certificate keys, `.pt` model binaries, and scratch files.

---

## 9. Security Implementation Timeline

Security milestones are mapped into the phased development schedule:

| Phase & Timeline | Milestone | Key Security Deliverables |
|------------------|-----------|---------------------------|
| **Phase 1: Foundation**<br>*(Weeks 1–2)* | Auth & Baseline Security | - Admin password hashing + Worker PIN hashing with `bcrypt`<br>- Admin JWT flow (username + password → 15-min access + 24h refresh)<br>- Worker JWT flow (phone + 4-digit PIN → 24h access token, no refresh)<br>- RBAC dependency injection (`deps.py`)<br>- CORS configuration, Pydantic input schemas (including PIN validator)<br>- Login rate limiting via `slowapi` (3/min per IP for admin, 5/hour per phone for worker) |
| **Phase 2: Core Features**<br>*(Weeks 3–4)* | AI & Complaint Integrity | - Image fraud detection pipeline (Gate 1: NSFW check, Gate 2: EXIF & ELA analysis)<br>- Embedded link / QR code scanning (`pyzbar`)<br>- Classification confidence thresholding (auto-reject `< 50%`)<br>- Text validation (length, gibberish detection) |
| **Phase 3: Integration**<br>*(Weeks 5–6)* | Bot & Asset Protection | - Telegram webhook secret token verification<br>- Citizen rate limiting (5 complaints / 24h)<br>- Redis-backed conversation session continuity with TTL<br>- S3/MinIO private bucket configuration with 15-minute signed URLs<br>- View-only canvas viewer (no download, anti-screenshot key intercept, focus-loss blanking, dynamic forensic watermark, Android `FLAG_SECURE`) |
| **Phase 6: Hardening**<br>*(Weeks 9–10)* | Production Hardening & Audit | - Nginx TLS/SSL setup with Let's Encrypt certificates<br>- AWS SSM Parameter Store secrets integration<br>- Security audit (tighten CORS origins, test token expirations, tune rate limits)<br>- Automated integration tests validating RBAC boundaries |
