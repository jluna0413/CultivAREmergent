# Epic: Genetics Marketplace with Fractional G-NFTs - Brownfield Enhancement

**Epic ID:** EPIC-GNFT-001
**Status:** In Progress
**Priority:** High  
**Target Release:** Q1 2025

---

## Epic Goal

Extend the existing CultivAR platform with a comprehensive genetics marketplace enabling breeders to sell seed genetics as fractional NFTs (G-NFTs), implement hybrid minting strategy, state-by-state cannabis compliance, escrow payment system, and breeder gamification leaderboards.

---

## Epic Description

### Existing System Context

**Current CultivAR Functionality:**
- Plant lifecycle tracking (seed → harvest)
- Sensor integration (AC Infinity, Ecowitt)
- Nutrient calculator
- User genetics library
- Grow journaling

**Technology Stack:**
- Backend: FastAPI (Python), SQLAlchemy
- Frontend: Flutter
- Database: SQLite (development), PostgreSQL (production)
- Blockchain: None (greenfield blockchain integration)

**Integration Points:**
- Extend `user_genetics` table with marketplace metadata
- Add blockchain wallet integration to user accounts
- Integrate marketplace UI into existing Flutter app navigation
- Connect escrow payments to existing order system

### Enhancement Details

**What's Being Added:**

1. **Fractional G-NFT System**
   - Master G-NFTs (entire harvest, breeder mints upfront for $2)
   - Pack G-NFTs (3/5/6/10/12 seeds, lazy-minted on purchase)
   - Blockchain integration via Algorand (ASA creation)
   - IPFS metadata storage for NFT provenance
   - 70/20/10 royalty split (breeder/platform/first minter)

2. **Hybrid Minting Strategy (All Listings)**
   - Breeder commits with 10% lot value escrow (e.g., $1,350 on $13,500 lot)
   - Milestone-based escrow releases (25%, 50%, 75%, 90%, 100%)
   - Pack NFTs lazy-minted when user purchases (user pays ~$2 fee)

3. **Cannabis Compliance System**
   - AI agent scrapes state-by-state seed shipping laws
   - Privacy-preserving (agent only sees state code, not addresses)
   - Physical crypto coin fulfillment for restricted states
   - Encrypted address storage
   - Dual-signature redemption (breeder + user sign on-chain)

4. **Fraud Prevention & Appeals**
   - 10% escrow prevents double-selling
   - Auto-burn unfulfilled NFTs if breeder banned
   - Redirect future royalties to platform  
   - Multi-tier appeals process (auto-filter → jury → admin → arbitration)

5. **Multi-Stage Reputation System**
   - Delivery rating (QR scan, 20% weight)
   - Germination reporting (7-21 days, 30% weight)
   - Harvest review (90-150 days, 50% weight)
   - Composite 0-100 score displayed on profile

6. **Breeder Gam

ification**
   - 15-category leaderboards (sales, quality, pack types, NFTs, coins)
   - Achievement badges (milestones, quality, speed)
   - Loyalty points: Sprouts (users), Coin Points (breeders)
   - Merch marketplace (redeem points, user pays shipping)

7. **Dynamic QR Code Verification**
   - Printed on packing slips
   - Auto-adds genetics to user collection
   - Captures device analytics (iOS/Android, screen size, geo)
   - Triggers upsells, social sharing, quality feedback

**How It Integrates:**
- Uses existing `models_async` SQLAlchemy structure  
- Extends `User` model with wallet relationships
- Adds new Flutter feature modules (`marketplace`, `nft`, `wallet`)
- Integrates with existing navigation and authentication
- Reuses `Sensor`, `Grow`, `Plant` for lineage tracking

**Success Criteria:**
- [ ] 100+ breeders onboarded within 3 months
- [ ] 90%+ germination rate across all listed genetics
- [ ] Zero fraudulent listings or double-selling incidents
- [ ] 95%+ user satisfaction with QR verification flow
- [ ] Leaderboards drive 30%+ increase in breeder engagement

---

## Stories

This epic breaks into **10 phased story groups** due to complexity:

### Phase 1: Core Infrastructure (Stories 1-5)

**Story 1**: Database Schema Implementation
- Create 25+ new tables (`breeders`, `gnft_masters`, `gnft_packs`, `gnft_listings`, `wallet_transactions`, `loyalty_points`, etc.)
- Register models in `models_async/__init__.py`
- Create Alembic migration
- ✅ **Status**: Complete

**Story 2**: Hypergraph Knowledge Base Integration
- Define strain, breeder, terpene node types
- Create `DESCENDED_FROM`, `BRED_BY` edges
- Build lineage query service
- Privacy-preserving state restriction nodes

**Story 3**: Algorand Blockchain Setup
- Local testnet node configuration
- ASA creation utilities (Master & Pack NFTs)
- ARC-69 royalty metadata implementation
- Escrow smart contract (PyTeal)
- IPFS integration (Kubo + Pinata backup)

---

### Phase 2: Compliance & Legal (Stories 6-10)

**Story 4**: Cannabis Compliance AI Agent
- `CannabisComplianceAgent` with web scraping
- LLM-based legal text interpretation
- Daily update scheduler
- Admin alert system for law changes
- RBAC permissions (state code only)

**Story 5**: Physical Crypto Coin System
- 4-tier coin specifications (Bronze/Silver/Gold/Platinum)
- Manufacturer API integration
- QR code generation with verification URLs
- Shipping state extraction utility
- Compliance warning modals

---

### Phase 3: Marketplace Backend (Stories 11-18)

**Story 6**: Listing Management API
- CRUD endpoints for G-NFT listings
- Breeder pricing configuration
- Pack availability tracking
- 15% commission calculation
- Payout scheduling service

**Story 7**: Hybrid Minting Service
- Master G-NFT upfront minting flow
- 10% lot value escrow creation
- Pack lazy-minting on purchase
- Royalty configuration (70/20/10)
- Burn mechanism integration

**Story 8**: Escrow & Payment System
- Algorand escrow smart contract deployment
- Dual-signature release API
- 90-day timeout refund logic
- Milestone-based releases (25%, 50%, 75%, 90%, 100%)
- Stripe/Pera Wallet integration

---

### Phase 4: Frontend - Genetics Library (Stories 19-24)

**Story 9**: Enhanced Genetics Onboarding
- Breeder autocomplete
- Seed/clone count inputs
- Metadata form (THC, CBD, flower time)
- Indica/Sativa percentage widgets (3 variants)
- AI scraping button (premium)
- Lineage input field

**Story 10**: Genetics Library Dashboard
- Grid/list view toggle
- Search and filter (breeder, type, scarcity)
- Product cards with thumbnails
- Detail screen with full profile
- Edit/delete actions
- Scarcity tracker widget

**Story 11**: Intelligent Recommendation Modules
- "Suggested to Grow Next" widget
- "Genetics Wish List" with stock alerts
- "Breeders I Follow" feed
- "Marketplace Recommendations" (based on terpenes)
- Collection insights (pie charts, diversity score)

---

### Phase 5: Frontend - Marketplace (Stories 25-30)

**Story 12**: Marketplace Listing Browse
- Featured breeders carousel
- Trending genetics cards
- Filters (breeder, strain type, price, scarcity)
- Sort options (price, scarcity, new arrivals)
- Breeder profile pages
- Search with autocomplete

**Story 13**: Checkout & Compliance Flow
- Address forms (billing & shipping separate)
- Shipping state compliance check
- Seed vs coin fulfillment warnings
- Transparent fee breakdown
- Legal disclaimer modal (first-time users)
- Persistent footer with policy links
- Payment method selection (Stripe/Pera)

**Story 14**: Dual-Signature Redemption UI
- QR code scanner for coins
- User signature confirmation dialog
- Breeder fulfillment dashboard
- Escrow release UI flow
- On-chain transaction proof display
- Redemption history view

---

### Phase 6: Breeder Tools (Stories 31-35)

**Story 15**: Breeder Dashboard
- Master G-NFT minting form
- Pack creation wizard (set sizes & prices)
- Listing management screen
- Sales analytics dashboard
- Payout history view
- Escrow tracking widget

**Story 16**: Fulfillment & Redemption
- Pending orders list (legal states)
- Shipping label generation
- Order status updates
- Pending coin redemptions view
- QR scanner for verification
- Dual-signature confirmation UI

---

### Phase 7: Secondary Market (Stories 36-39)

**Story 17**: NFT Resale Marketplace
- List Pack NFTs for resale (set price)
- Offer/bidding system
- Atomic swap transactions
- Automated royalty distribution (70/20/10)
- Trading history view
- Floor price tracking

**Story 18**: Burn Mechanics
- Burn trigger integration with grow creation
- Confirmation dialog with warnings
- Algorand asset burn transaction
- Scarcity score auto-update
- Burn history and impact display
- Rarest packs leaderboard

---

### Phase 8: Advanced Features (Stories 40-44)

**Story 19**: Lineage Visualization
- Genealogy tree widget (CustomPainter)
- Interactive zoom/pan
- Ancestor/descendant navigation
- Common ancestor finder
- Similar lineage recommendations
- Integration with hypergraph queries

**Story 20**: AI Genetics Scraper Enhancement
- Lineage extraction from breeder websites
- Hypergraph auto-population
- Terpene/effect parsing
- Confidence scoring
- Manual review queue for low-confidence data

---

### Phase 9: Gamification & Reputation (Stories 45-50)

**Story 21**: Multi-Stage Reputation System
- Delivery rating modal (QR scan triggers)
- Germination report form (7-21 day reminder)
- Harvest review screen (quality ratings)
- Composite score calculation (20%/30%/50%)
- Breeder profile score display

**Story 22**: Breeder Leaderboards
- 15-category rankings (sales, quality, pack types, NFTs, coins)
- Real-time position updates
- Top 3 medals (🥇🥈🥉)
- Public/private toggle
- Achievement badges (milestones, speed, quality)

**Story 23**: Loyalty Points & Merch
- Sprouts earning system (10 per $1)
- Coin Points for breeder redemptions
- Merch marketplace UI
- Redemption flow (user pays shipping)
- Loyalty balance tracking
- Reward tier unlocks

---

### Phase 10: Testing, Launch & Docs (Stories 51-56)

**Story 24**: Backend Testing Suite
- Unit tests for all endpoints
- Integration tests for escrow flows
- Compliance agent test suite
- Smart contract audit (external)
- Load testing (1000+ concurrent users)
- Security penetration testing

**Story 25**: Frontend Testing Suite
- Widget tests for all components
- Integration tests for checkout flow
- E2E tests for dual-signature redemption
- Accessibility audits (WCAG 2.1 AA)
- Cross-browser testing
- Mobile responsiveness (iOS & Android)

**Story 26**: Documentation & Launch
- Breeder onboarding guide
- User marketplace tutorial
- Terms of service (genetics sales)
- Legal disclaimers (crypto coins, peer-to-peer trades)
- API documentation
- Smart contract documentation
- State-by-state compliance review
- Beta program launch (50 breeders)

---

## Compatibility Requirements

- [x] Existing plant tracking APIs remain unchanged
- [x] Database schema changes use new tables (no breaking changes to existing)
- [x] UI follows existing Flutter design system (colors, typography, spacing)
- [x] Performance impact minimal (new tables indexed, lazy loading for NFT metadata)
- [x] Blockchain integration isolated (failures don't affect core app)

---

## Risk Mitigation

### Primary Risks

1. **Regulatory Compliance Risk**
   - **Risk**: State laws change, platform liable for illegal shipments
   - **Mitigation**: AI agent monitors daily, admin alerts, encrypted addresses
   - **Rollback**: Disable marketplace in affected states immediately

2. **Blockchain Dependency Risk**
   - **Risk**: Algorand network downtime prevents NFT operations
   - **Mitigation**: Queue transactions, retry logic, fallback to database records
   - **Rollback**: Marketplace continues with database-only mode (NFT minting resumes when network recovers)

3. **Fraud & Double-Selling Risk**
   - **Risk**: Breeder lists same genetics on multiple platforms
   - **Mitigation**: 10% escrow, Master NFT on-chain proof, ban + burn unfulfilled NFTs
   - **Rollback**: Refund users from escrow pool, permanent breeder ban

4. **User Experience Complexity Risk**
   - **Risk**: Blockchain/wallet complexity confuses users
   - **Mitigation**: Optional Pera Wallet (can use Stripe only), in-app tutorial, QR auto-verification
   - **Rollback**: Simplify to fiat-only mode if <10% wallet adoption

### Rollback Plan

**Gradual Rollback Strategy:**
1. **Level 1** (Minor Issue): Disable specific feature (e.g., secondary market)
2. **Level 2** (Moderate Issue): Pause new listings, continue existing orders
3. **Level 3** (Major Issue): Marketplace read-only mode, no new transactions
4. **Level 4** (Critical Issue): Full marketplace shutdown, migrate to maintenance page

**Data Persistence**: All NFT metadata stored in database AND IPFS (redundancy). Blockchain is source of truth for ownership, but app functions without it.

---

## Definition of Done

- [ ] All 56 stories completed with acceptance criteria met
- [ ] Existing CultivAR functionality verified (plant tracking, sensors, nutrients)
- [ ] Blockchain integration working on Algorand testnet
- [ ] Smart contracts audited by external firm
- [ ] Compliance agent monitoring 50 states
- [ ] 100+ breeders onboarded to beta
- [ ] 1000+ users tested marketplace flows
- [ ] Legal counsel reviewed all disclaimers
- [ ] Documentation complete (user guides, API docs, legal policies)
- [ ] Zero high-severity bugs in production
- [ ] Performance benchmarks met (dashboard <1.5s, transaction <3s)

---

## Dependencies

**External:**
- Algorand testnet/mainnet access
- IPFS hosting (Kubo + Pinata)
- Stripe merchant account
- Coin manufacturer partnership
- Legal counsel (state compliance review)
- Smart contract auditor

**Internal:**
- Existing `User`, `UserGenetics`, `Grow`, `Plant` models
- FastAPI authentication system
- Flutter navigation framework
- SQLAlchemy ORM
- Alembic migrations

---

## Success Metrics

**Adoption Metrics:**
- 100+ verified breeders within 3 months
- 500+ G-NFT listings within 6 months
- 10,000+ Pack NFTs minted in first year
- 50+ states mapped for compliance

**Quality Metrics:**
- 90%+ average germination rate (user-reported)
- 95%+ delivery satisfaction (QR feedback)
- <1% fraud rate
- <5% dispute rate

**Engagement Metrics:**
- 30%+ breeder leaderboard participation
- 20%+ user loyalty point redemptions
- 10%+ secondary market trading volume
- 25%+ repeat purchases (same user, different genetics)

**Financial Metrics:**
- $100K+ gross marketplace volume (GMV) in first 6 months
- $15K+ platform commission revenue (15%)
- $50K+ escrow pool (10% of active listings)
- $5K+ royalty distributions (secondary sales)

---

## Timeline Estimate

| Phase | Stories | Estimated Duration | Dependencies |
|-------|---------|-------------------|--------------|
| Phase 1 | 1-5 | 3 weeks | None (foundational) |
| Phase 2 | 6-10 | 2 weeks | Phase 1 complete |
| Phase 3 | 11-18 | 4 weeks | Phase 1 & 2 complete |
| Phase 4 | 19-24 | 3 weeks | Phase 3 backend APIs ready |
| Phase 5 | 25-30 | 4 weeks | Phase 3 complete |
| Phase 6 | 31-35 | 2 weeks | Phase 3 & 5 complete |
| Phase 7 | 36-39 | 2 weeks | Phase 3 & 5 complete |
| Phase 8 | 40-44 | 3 weeks | Hypergraph (Phase 1.2) complete |
| Phase 9 | 45-50 | 3 weeks | Phase 3-7 complete |
| Phase 10 | 51-56 | 4 weeks | All phases complete |

**Total Estimated Duration**: 30 weeks (~7 months)

---

## Notes

- This is a **major brownfield enhancement** requiring full PRD process (not simple epic)
- Blockchain integration is greenfield

 (new tech for platform)
- Compliance system requires ongoing maintenance (AI agent updates)
- Breeder onboarding is critical path (need supply before marketplace launch)
- Legal review mandatory before production launch
- Consider phased rollout (beta → limited states → full US)

---

**Created**: 2025-12-12
**Last Updated**: 2025-12-12
**Owner**: AI Product Manager (BMad Orchestrator)
