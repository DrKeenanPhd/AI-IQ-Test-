# Strategy and Design Notes

This file is for capturing all functional design decisions, technical strategies, and rationale for the AI IQ Test project. It is intended to guide future development and provide context for any new team members or sessions.

---

## 1. Subscription Management
- **Requirements:**
  - Support for trial, upgrade, downgrade, and cancellation flows.
  - Integration with GoHighLevel (GHL) and Stripe for user management and payments.
  - Ability to handle multiple subscription tiers (e.g., Basic, Premiere, Ecosystem).
  - Store subscription status and history per user.
- **Open Questions:**
  - Should GHL or Stripe be the source of truth for subscription status?
  - How should failed payments or cancellations be handled?
  - What user roles or permissions are needed?

## 2. Authentication & Access Control
- **Requirements:**
  - Secure, token-based SmartLink access for test results.
  - Support for multiple sessions/reports per user.
  - Optional SSO or integration with GHL login.
  - Role-based access for users, admins, and agents.
- **Open Questions:**
  - How long should SmartLinks be valid?
  - Should users be able to set/reset passwords, or is access always via SmartLink?
  - How to handle expired or invalid tokens?

## 3. Technical Stack & Architecture
- **Current:**
  - Backend: FastAPI (Python)
  - Frontend: React/TypeScript (Vite, Tailwind)
  - Integrations: GHL, Vapi, Stripe
  - Deployment: Vercel
- **Considerations:**
  - Migrate from in-memory to persistent database (PostgreSQL, MySQL, etc.)
  - Add monitoring, error tracking, and logging for production
  - Document all environment variables and deployment steps

## 4. Functional Design Prompts
- What is the ideal user journey from test start to subscription upgrade?
- How should agent follow-ups and recommendations be displayed and stored?
- What analytics or reporting is needed for business insights?

---

**Instructions for Next Session:**
- Review this file and `PROJECT_AUDIT_PROGRESS.md` for full project context.
- Use this file to document all new design decisions and technical strategies.
- Update as features are implemented or requirements change.
