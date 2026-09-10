# Sufiyan — Frontend

> **Role:** Frontend Developer (Admin Dashboard + Field Worker PWA)
> **Primary Workspace:** `frontend/`

---

## 🎯 What You Own

| Area                | Directories / Files                                  |
|---------------------|------------------------------------------------------|
| **Views / Pages**   | `frontend/src/views/`                                |
| **Components**      | `frontend/src/components/`                           |
| **State Management**| `frontend/src/stores/` (Pinia)                       |
| **Routing**         | `frontend/src/router/`                               |
| **API Integration** | `frontend/src/services/` (Axios calls to backend)    |
| **Composables**     | `frontend/src/composables/`                          |
| **Assets & Styling**| `frontend/src/assets/`                               |
| **Build Config**    | `frontend/Dockerfile`, Vite config                   |

---

## 📋 Key Responsibilities

### Phase 1 — Foundation (Weeks 1–2)
- [ ] Set up Vue 3 project with Vite, Pinia, Vue Router
- [ ] Install and configure Bootstrap 5
- [ ] Create app layout shell (sidebar, navbar, responsive container)
- [ ] Build Login / Register pages
- [ ] Set up Axios service layer with JWT auth interceptors

### Phase 2 — Admin Dashboard (Weeks 3–4)
- [ ] **Dashboard Home** — summary cards (total complaints, pending, resolved, SLA breaches)
- [ ] **Complaints Table** — sortable, filterable list with status badges and priority indicators
- [ ] **Complaint Detail** — view full complaint info, photos, timeline, assignment history
- [ ] **Triage Queue** — manually assign/reassign complaints to field workers
- [ ] **Analytics Page** — charts with Chart.js (complaints over time, by category, by ward)

### Phase 3 — Maps & Field Worker (Weeks 5–6)
- [ ] **Hotspot Map** — Leaflet.js map showing complaint clusters with PostGIS data
- [ ] **Field Worker PWA** — mobile-optimized task list view
  - [ ] Daily task queue with priority scoring
  - [ ] Navigate-to-location (link to Google Maps)
  - [ ] Submit resolution proof (photo upload + notes)
- [ ] **Worker Performance** — table/chart of resolution times, completed tasks
- [ ] Make the app a PWA (manifest, service worker, offline support)

### Phase 4 — Polish (Weeks 7–8)
- [ ] Responsive design across all pages (mobile, tablet, desktop)
- [ ] Loading states, error handling, empty states
- [ ] Dark mode toggle (optional but impressive)
- [ ] Accessibility review (keyboard nav, ARIA labels)
- [ ] Dockerize frontend for production build

---

## 🔗 Coordination Points

| With       | What                                                                 |
|------------|----------------------------------------------------------------------|
| **Sairaj** | Align on API contracts — agree on endpoints, request/response shapes, error formats before building pages |
| **Tushar** | Display ML classification results on complaint detail page (category badge, confidence score) |

---

## 📚 Learning Resources

- [Vue 3 Docs (Composition API)](https://vuejs.org/guide/introduction.html)
- [Pinia State Management](https://pinia.vuejs.org/)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.3/)
- [Chart.js with Vue](https://vue-chartjs.org/)
- [Leaflet.js Quick Start](https://leafletjs.com/examples/quick-start/)

---

## 📝 Personal Notes

> Use this space for your own notes, blockers, questions, or ideas.
> This file is gitignored — it's your private scratchpad.

- 

